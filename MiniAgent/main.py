import ast
import json
import operator
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel


# 创建 Rich 控制台对象，用于美化终端输出
console = Console()

# history.json 用来保存完整对话历史
# 注意：它是本地文件，不建议提交到 GitHub
HISTORY_FILE = Path("history.json")

# 系统提示词：用于规定模型的基本身份和回答风格
SYSTEM_PROMPT = "你是一个耐心、清晰的中文 AI Agent 学习助手。"

# 每次请求模型时，最多携带最近多少条历史消息
# 注意：一轮对话通常包含 2 条 message：user + assistant
# 这里设置为 10，表示最多携带最近 5 轮左右的对话
# history.json 仍然完整保存全部历史，但真正发给模型的只取最近部分
MAX_CONTEXT_MESSAGES = 10

# 允许 calculator 使用的二元运算符
# 这里不用 eval，而是手动限制可以执行的运算类型，避免执行危险代码
ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,       # +
    ast.Sub: operator.sub,       # -
    ast.Mult: operator.mul,      # *
    ast.Div: operator.truediv,   # /
    ast.Mod: operator.mod,       # %
    ast.Pow: operator.pow,       # **
}

# 允许 calculator 使用的一元运算符
ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,      # +x
    ast.USub: operator.neg,      # -x
}

def safe_calculate(expression: str) -> int | float:
    """安全地计算一个基础数学表达式。"""

    def evaluate_node(node: ast.AST) -> int | float:
        """递归计算 AST 节点。"""

        # 表达式根节点
        if isinstance(node, ast.Expression):
            return evaluate_node(node.body)

        # 数字节点，例如 1、3.14
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value

        # 二元运算节点，例如 1 + 2、3 * 4
        if isinstance(node, ast.BinOp):
            operator_type = type(node.op)

            if operator_type not in ALLOWED_BINARY_OPERATORS:
                raise ValueError("不支持的二元运算符。")

            left_value = evaluate_node(node.left)
            right_value = evaluate_node(node.right)

            return ALLOWED_BINARY_OPERATORS[operator_type](left_value, right_value)

        # 一元运算节点，例如 -3、+5
        if isinstance(node, ast.UnaryOp):
            operator_type = type(node.op)

            if operator_type not in ALLOWED_UNARY_OPERATORS:
                raise ValueError("不支持的一元运算符。")

            value = evaluate_node(node.operand)

            return ALLOWED_UNARY_OPERATORS[operator_type](value)

        # 其他所有语法都不允许
        raise ValueError("表达式中包含不允许的内容。")

    # 把字符串表达式解析为 AST
    parsed_expression = ast.parse(expression, mode="eval")

    # 递归计算 AST
    return evaluate_node(parsed_expression)

def calculator_tool(expression: str) -> str:
    """calculator 工具：计算数学表达式，并返回字符串结果。"""

    result = safe_calculate(expression)

    return str(result)

def load_config() -> dict:
    """从 .env 文件中读取 LLM 配置。"""

    # load_dotenv() 会自动读取当前目录下的 .env 文件
    # 例如：LLM_API_KEY、LLM_BASE_URL、LLM_MODEL 等
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "unknown")
    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")

    # 如果关键配置缺失，就直接报错
    # 这样可以避免程序运行到一半才发现配置不完整
    if not base_url:
        raise ValueError("Missing LLM_BASE_URL in .env")

    if not api_key:
        raise ValueError("Missing LLM_API_KEY in .env")

    if not model:
        raise ValueError("Missing LLM_MODEL in .env")

    return {
        "provider": provider,
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
    }


def create_client(config: dict) -> OpenAI:
    """创建一个 OpenAI-compatible 客户端。"""

    # 虽然这里使用的是 OpenAI SDK，
    # 但因为 base_url 指向 DeepSeek，所以实际请求会发给 DeepSeek API
    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )


def load_history() -> list[dict]:
    """从 history.json 中读取完整对话历史。"""

    # 如果 history.json 不存在，说明还没有历史记录
    if not HISTORY_FILE.exists():
        return []

    # 读取 JSON 文件，并转换成 Python 列表
    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history: list[dict]) -> None:
    """把完整对话历史保存到 history.json。"""

    # ensure_ascii=False 是为了让中文正常保存
    # indent=2 是为了让 JSON 文件更容易阅读
    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def build_messages(history: list[dict], user_input: str) -> list[dict]:
    """构造本次要发送给模型的 messages。"""

    # messages 是真正发送给大模型的上下文
    # 它不是 history.json 的全部内容
    # 而是：系统提示词 + 最近历史 + 当前问题
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # 只取最近 MAX_CONTEXT_MESSAGES 条历史消息
    # 这样 history.json 可以继续完整保存，
    # 但不会每次都把全部历史发给模型
    recent_history = history[-MAX_CONTEXT_MESSAGES:]

    # 把最近历史加入本次请求上下文
    messages.extend(recent_history)

    # 把用户当前这一轮输入加入上下文
    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    return messages


def ask_llm_stream(client: OpenAI, model: str, messages: list[dict]) -> str:
    """向模型发送 messages，并以 streaming 方式输出回答。"""

    # stream=True 表示开启流式输出
    # 模型不会等完整回答生成完才返回，而是边生成边返回 chunk
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        stream=True,
    )

    # answer_parts 用来收集每一个流式片段
    # 最后拼接成完整回答，保存进 history.json
    answer_parts = []

    console.print("\n[bold green]Assistant:[/bold green]")

    for chunk in stream:
        # 有些 chunk 可能不包含 choices，需要跳过
        if not chunk.choices:
            continue

        # delta.content 是当前新生成的一小段文本
        delta = chunk.choices[0].delta.content

        if delta:
            # 边生成边打印
            # markup=False 避免模型输出中的 [] 被 Rich 当作样式标记
            console.print(delta, end="", markup=False, highlight=False)

            # 同时把片段保存起来
            answer_parts.append(delta)

    console.print()

    # 把所有片段拼成完整回答
    return "".join(answer_parts)


def ask_llm_json(client: OpenAI, model: str, user_input: str) -> dict[str, Any]:
    """让模型把用户输入整理成结构化 JSON。"""

    # 这里单独构造一组 messages
    # 注意：/json 是工具命令，不使用聊天历史
    # 这样可以避免历史内容干扰结构化输出
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个结构化信息提取助手。"
                "你必须只输出合法 JSON，不要输出 Markdown，不要输出解释。"
                "JSON 必须包含以下字段：intent、summary、keywords、next_action。"
            ),
        },
        {
            "role": "user",
            "content": (
                "请把下面这段用户输入整理为 JSON：\n\n"
                f"{user_input}\n\n"
                "输出 JSON 格式示例：\n"
                "{\n"
                '  "intent": "用户意图",\n'
                '  "summary": "一句话总结",\n'
                '  "keywords": ["关键词1", "关键词2"],\n'
                '  "next_action": "建议下一步动作"\n'
                "}"
            ),
        },
    ]

    # response_format={"type": "json_object"} 表示要求模型输出 JSON 对象
    # temperature 设置低一点，是为了让结构化输出更稳定
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,
        stream=False,
        response_format={"type": "json_object"},
    )

    # 模型返回的 content 本质上还是字符串
    content = response.choices[0].message.content

    if not content:
        raise ValueError("模型返回了空的 JSON 内容。")

    # 把 JSON 字符串解析成 Python 字典
    return json.loads(content)

def ask_tool_decision(
    client: OpenAI,
    model: str,
    history: list[dict],
    user_input: str,
) -> dict[str, Any]:
    """让模型判断当前用户输入是否需要调用工具。"""

    # 只带最近历史，避免完整 history 干扰工具判断
    recent_history = history[-MAX_CONTEXT_MESSAGES:]

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个工具调用决策器。"
                "你的任务是判断用户问题是否需要调用工具。"
                "当前可用工具只有一个：calculator。"
                "calculator 用于计算基础数学表达式，例如 23 * 45、(12 + 8) / 4。"
                "你必须只输出合法 JSON，不要输出 Markdown，不要输出解释。"
                "JSON 必须包含字段：need_tool、tool_name、arguments、reason。"
            ),
        }
    ]

    # 加入最近历史，让模型在必要时知道前文
    messages.extend(recent_history)

    messages.append(
        {
            "role": "user",
            "content": (
                "请判断下面这个用户输入是否需要调用工具。\n\n"
                f"用户输入：{user_input}\n\n"
                "如果需要计算，请输出：\n"
                "{\n"
                '  "need_tool": true,\n'
                '  "tool_name": "calculator",\n'
                '  "arguments": {"expression": "数学表达式"},\n'
                '  "reason": "为什么需要调用工具"\n'
                "}\n\n"
                "如果不需要工具，请输出：\n"
                "{\n"
                '  "need_tool": false,\n'
                '  "tool_name": null,\n'
                '  "arguments": {},\n'
                '  "reason": "为什么不需要调用工具"\n'
                "}"
            ),
        }
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.1,
        stream=False,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("模型没有返回工具决策 JSON。")

    return json.loads(content)

def execute_tool_call(tool_decision: dict[str, Any]) -> dict[str, Any]:
    """根据模型输出的 tool_call JSON 执行对应工具。"""

    need_tool = tool_decision.get("need_tool", False)

    if not need_tool:
        return {
            "used_tool": False,
            "tool_name": None,
            "arguments": {},
            "result": None,
            "error": None,
        }

    tool_name = tool_decision.get("tool_name")
    arguments = tool_decision.get("arguments", {})

    if tool_name != "calculator":
        return {
            "used_tool": False,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": f"未知工具：{tool_name}",
        }

    expression = arguments.get("expression")

    if not expression:
        return {
            "used_tool": False,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": "calculator 缺少 expression 参数。",
        }

    try:
        result = calculator_tool(expression)

        return {
            "used_tool": True,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": result,
            "error": None,
        }

    except Exception as error:
        return {
            "used_tool": False,
            "tool_name": tool_name,
            "arguments": arguments,
            "result": None,
            "error": str(error),
        }

def build_tool_answer_messages(
    history: list[dict],
    user_input: str,
    tool_decision: dict[str, Any],
    tool_result: dict[str, Any],
) -> list[dict]:
    """把工具执行结果重新组织成 messages，让模型生成最终回答。"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    # 最终回答时也只带最近历史
    recent_history = history[-MAX_CONTEXT_MESSAGES:]
    messages.extend(recent_history)

    # 用户原始问题
    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # 把工具决策和工具执行结果作为上下文交给模型
    messages.append(
        {
            "role": "user",
            "content": (
                "下面是程序已经执行完成的工具调用结果。\n"
                "请你基于工具结果回答用户，不要编造额外计算结果。\n\n"
                f"工具决策 JSON：\n{json.dumps(tool_decision, ensure_ascii=False, indent=2)}\n\n"
                f"工具执行结果 JSON：\n{json.dumps(tool_result, ensure_ascii=False, indent=2)}"
            ),
        }
    )

    return messages

def show_json_result(result: dict[str, Any]) -> None:
    """在终端中格式化显示 JSON 结果。"""

    console.print("\n[bold green]JSON Output:[/bold green]")

    # console.print_json 可以把 JSON 高亮显示出来
    # json.dumps(..., ensure_ascii=False) 是为了正常显示中文
    console.print_json(json.dumps(result, ensure_ascii=False))


def show_history(history: list[dict]) -> None:
    """在终端中显示当前完整对话历史。"""

    if not history:
        console.print("[yellow]History is empty.[/yellow]")
        return

    console.print(Panel.fit(f"Total messages: {len(history)}", title="History"))

    for index, message in enumerate(history, start=1):
        role = message.get("role", "unknown")
        content = message.get("content", "")

        console.print(f"\n[bold cyan]{index}. {role}[/bold cyan]")
        console.print(content)


def clear_history() -> list[dict]:
    """清空完整对话历史，并同步写入 history.json。"""

    history = []

    # 保存空列表到 history.json
    # 这样本地历史文件也会被清空
    save_history(history)

    console.print("[bold yellow]History cleared.[/bold yellow]")

    return history


def show_help() -> None:
    """显示当前 CLI 支持的命令。"""

    console.print(
        Panel.fit(
            "/history              查看当前完整对话历史\n"
            "/clear                清空当前对话历史\n"
            "/json <text>          将文本转换为结构化 JSON\n"
            "/tools                查看当前可用工具\n"
            "/help                 查看命令说明\n"
            "exit                  退出程序\n"
            "quit                  退出程序",
            title="Commands",
        )
    )

def show_tools() -> None:
    """显示当前 MiniAgent 可用的工具。"""

    console.print(
        Panel.fit(
            "calculator: 计算基础数学表达式，例如 23 * 45、(12 + 8) / 4",
            title="Available Tools",
        )
    )

def main() -> None:
    """MiniAgent 主程序入口。"""

    # 1. 读取配置
    config = load_config()

    # 2. 创建 LLM API 客户端
    client = create_client(config)

    # 3. 读取本地完整历史
    history = load_history()

    # 4. 打印启动信息
    console.print(
        Panel.fit(
            f"MiniAgent v0.5\n"
            f"Provider: {config['provider']}\n"
            f"Model: {config['model']}\n"
            f"History messages: {len(history)}\n"
            f"Max context messages: {MAX_CONTEXT_MESSAGES}",
            title="Started",
        )
    )

    console.print("输入 [bold red]exit[/bold red] 或 [bold red]quit[/bold red] 退出。")
    console.print("输入 [bold cyan]/help[/bold cyan] 查看可用命令。")

    # 5. 进入命令行循环
    # 这个 while True 让程序可以持续对话，而不是问一次就结束
    while True:
        user_input = input("\nYou: ").strip()

        # exit / quit 用于退出程序
        if user_input.lower() in ["exit", "quit"]:
            console.print("\n[bold yellow]Bye.[/bold yellow]")
            break

        # 如果用户什么都没输入，就重新进入下一轮
        if not user_input:
            continue

        # /help 是程序命令，不发送给模型
        if user_input == "/help":
            show_help()
            continue
        
        if user_input == "/tools":
            show_tools()
            continue

        # /history 是程序命令，用于查看完整本地历史
        # 注意：它不会调用模型
        if user_input == "/history":
            show_history(history)
            continue

        # /clear 是程序命令，用于清空本地历史
        # 注意：它不会调用模型
        if user_input == "/clear":
            history = clear_history()
            continue

        # /json 是结构化输出命令
        # 它会调用模型，但不会写入普通对话历史
        if user_input.startswith("/json "):
            # 取出 /json 后面的真实文本
            json_input = user_input.removeprefix("/json ").strip()

            if not json_input:
                console.print("[yellow]请在 /json 后面输入要整理的文本。[/yellow]")
                continue

            try:
                result = ask_llm_json(
                    client=client,
                    model=config["model"],
                    user_input=json_input,
                )
                show_json_result(result)
            except Exception as error:
                console.print(f"[bold red]JSON 输出失败:[/bold red] {error}")

            # /json 是工具命令，不进入普通聊天流程
            continue

        if user_input.startswith("/calc "):
            expression = user_input.removeprefix("/calc ").strip()

            if not expression:
                console.print("[yellow]请在 /calc 后面输入数学表达式。[/yellow]")
                continue

            try:
                result = calculator_tool(expression)
                console.print(f"[bold green]Calculator Result:[/bold green] {result}")
            except Exception as error:
                console.print(f"[bold red]Calculator failed:[/bold red] {error}")

            continue

        # 普通聊天流程：
        # 1. 构造本次 messages
        # 2. 调用模型并流式输出
        # 3. 把 user 和 assistant 保存到 history.json
        
        try:
            # 第一步：让模型判断是否需要调用工具
            tool_decision = ask_tool_decision(
                client=client,
                model=config["model"],
                history=history,
                user_input=user_input,
            )

            # 第二步：如果模型认为需要工具，就由 Python 执行工具
            tool_result = execute_tool_call(tool_decision)

            # 第三步：如果工具成功执行，把工具结果交回模型生成最终回答
            if tool_result["used_tool"]:
                console.print(
                    f"\n[bold blue]Tool Call:[/bold blue] "
                    f"{tool_result['tool_name']}({tool_result['arguments']})"
                )
                console.print(f"[bold blue]Tool Result:[/bold blue] {tool_result['result']}")

                messages = build_tool_answer_messages(
                    history=history,
                    user_input=user_input,
                    tool_decision=tool_decision,
                    tool_result=tool_result,
                )

                answer = ask_llm_stream(
                    client=client,
                    model=config["model"],
                    messages=messages,
                )

            # 第四步：如果不需要工具，就走普通聊天流程
            else:
                if tool_result["error"]:
                    console.print(f"[yellow]Tool skipped:[/yellow] {tool_result['error']}")

                messages = build_messages(history, user_input)

                answer = ask_llm_stream(
                    client=client,
                    model=config["model"],
                    messages=messages,
                )

        except Exception as error:
            console.print(f"[bold red]Tool calling failed:[/bold red] {error}")

            # 如果工具判断流程失败，就退回普通聊天
            messages = build_messages(history, user_input)

            answer = ask_llm_stream(
                client=client,
                model=config["model"],
                messages=messages,
            )

        # 保存用户这一轮输入
        history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # 保存模型这一轮回答
        history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # 把更新后的完整历史写入 history.json
        save_history(history)


if __name__ == "__main__":
    main()