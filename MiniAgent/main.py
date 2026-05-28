import os

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console
from rich.panel import Panel


console = Console()


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


def ask_llm(client: OpenAI, model: str, user_input: str) -> str:
    """Send one user message to the LLM and return the assistant response."""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "你是一个耐心、清晰的中文 AI Agent 学习助手。",
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        temperature=0.2,
        stream=False,
    )

    return response.choices[0].message.content


def main() -> None:
    config = load_config()
    client = create_client(config)

    console.print(
        Panel.fit(
            f"MiniAgent v0.1\n"
            f"Provider: {config['provider']}\n"
            f"Model: {config['model']}",
            title="Started",
        )
    )

    user_input = input("\nYou: ")

    answer = ask_llm(
        client=client,
        model=config["model"],
        user_input=user_input,
    )

    console.print("\n[bold green]Assistant:[/bold green]")
    console.print(answer)


if __name__ == "__main__":
    main()