import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel


console = Console()

HISTORY_FILE = Path("history.json")

SYSTEM_PROMPT = "你是一个耐心、清晰的中文 AI Agent 学习助手。"


def load_config() -> dict:
    """Load LLM configuration from .env file."""
    load_dotenv()

    provider = os.getenv("LLM_PROVIDER", "unknown")
    base_url = os.getenv("LLM_BASE_URL")
    api_key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")

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
    """Create an OpenAI-compatible client."""
    return OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"],
    )


def load_history() -> list[dict]:
    """Load conversation history from history.json."""
    if not HISTORY_FILE.exists():
        return []

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history: list[dict]) -> None:
    """Save conversation history to history.json."""
    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def build_messages(history: list[dict], user_input: str) -> list[dict]:
    """Build messages for Chat Completions API."""
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    return messages


def ask_llm(client: OpenAI, model: str, messages: list[dict]) -> str:
    """Send messages to the LLM and return the assistant response."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        stream=False,
    )

    return response.choices[0].message.content


def show_history(history: list[dict]) -> None:
    """Print conversation history in the terminal."""
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
    """Clear conversation history and save an empty history file."""
    history = []
    save_history(history)
    console.print("[bold yellow]History cleared.[/bold yellow]")
    return history


def show_help() -> None:
    """Show available commands."""
    console.print(
        Panel.fit(
            "/history  查看当前对话历史\n"
            "/clear    清空当前对话历史\n"
            "/help     查看命令说明\n"
            "exit      退出程序\n"
            "quit      退出程序",
            title="Commands",
        )
    )


def main() -> None:
    config = load_config()
    client = create_client(config)
    history = load_history()

    console.print(
        Panel.fit(
            f"MiniAgent v0.2.1\n"
            f"Provider: {config['provider']}\n"
            f"Model: {config['model']}\n"
            f"History messages: {len(history)}",
            title="Started",
        )
    )

    console.print("输入 [bold red]exit[/bold red] 或 [bold red]quit[/bold red] 退出。")
    console.print("输入 [bold cyan]/help[/bold cyan] 查看可用命令。")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() in ["exit", "quit"]:
            console.print("\n[bold yellow]Bye.[/bold yellow]")
            break

        if not user_input:
            continue

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/history":
            show_history(history)
            continue

        if user_input == "/clear":
            history = clear_history()
            continue

        messages = build_messages(history, user_input)

        answer = ask_llm(
            client=client,
            model=config["model"],
            messages=messages,
        )

        console.print("\n[bold green]Assistant:[/bold green]")
        console.print(answer)

        history.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        save_history(history)


if __name__ == "__main__":
    main()