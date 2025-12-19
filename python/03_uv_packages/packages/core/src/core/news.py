from bs4 import BeautifulSoup
import httpx

NEWS_URL = "https://news.ycombinator.com"
AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"


def fetch_headlines(limit: int = 5) -> list[str]:
    headers = {"User-Agent": AGENT}  # Use a user agent to avoid potential issues
    response = httpx.get(NEWS_URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    soup.prettify()
    titles = [a.get_text() for a in soup.select(".titleline a")]
    return titles[:limit]
