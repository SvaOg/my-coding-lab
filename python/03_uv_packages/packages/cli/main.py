import typer
from rich.console import Console
from core.news import fetch_headlines
from summarizer import summarize_text
from dotenv import load_dotenv
import os

load_dotenv()

app = typer.Typer()
console = Console()


@app.command()
def headlines(limit: int = 5):
    headlines = fetch_headlines(limit)
    for i, title in enumerate(headlines, 1):
        console.print(f"[green]{i}[/green] {title}")

    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        summary = summarize_text("\n".join(headlines), api_key)
        console.print("\n[bold magenta]Summary[/bold magenta]")
        console.print(summary)


if __name__ == "__main__":
    app()
