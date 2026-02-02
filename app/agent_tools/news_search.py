"""Yahoo Finance News Search Tool"""

from pydantic_ai import Tool
import feedparser
from datetime import datetime, timedelta
from typing import Optional


def search_financial_news(
    ticker: Optional[str] = None,
    query: Optional[str] = None,
    days_back: int = 7,
    max_results: int = 5,
) -> str:
    """Search for financial news from Yahoo Finance."""

    if ticker:
        url = f"https://finance.yahoo.com/rss/headline?s={ticker.upper()}"
        print(f"Fetching news for {ticker.upper()}")
    else:
        url = "https://finance.yahoo.com/news/rssindex"
        print(f"Fetching general market news")

    feed = feedparser.parse(url)
    cutoff_date = datetime.now() - timedelta(days=days_back)

    articles = []
    for entry in feed.entries[: max_results * 2]:
        try:
            pub_date = (
                datetime(*entry.published_parsed[:6])
                if hasattr(entry, "published_parsed")
                else datetime.now()
            )
        except:
            pub_date = datetime.now()

        if pub_date < cutoff_date:
            continue
        if (
            query
            and query.lower() not in entry.get("title", "").lower()
            and query.lower() not in entry.get("summary", "").lower()
        ):
            continue

        articles.append(
            {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", "") or entry.get("description", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
            }
        )

        if len(articles) >= max_results:
            break

    if not articles:
        return f"No news found for {ticker.upper() if ticker else 'your search'}"

    lines = [
        f"Found {len(articles)} news articles{' for ' + ticker.upper() if ticker else ''}:\n"
    ]
    for idx, art in enumerate(articles, 1):
        lines.extend(
            [
                f"Article {idx}:\n",
                f"Title: {art['title']}\n",
                f"Published: {art['published']}\n",
                f"Summary: {art['summary'][:300]}{'...' if len(art['summary']) > 300 else ''}\n",
                f"Link: {art['link']}\n",
            ]
        )

    return "\n".join(lines)


financial_news_tool = Tool(
    search_financial_news,
    name="financial_news_search",
    description="""Search for financial news from Yahoo Finance.
    
    Supports ticker searches (AAPL, MSFT, TSLA, etc.) and keyword filtering.
    
    Parameters:
    - ticker: stock symbol like 'AAPL', 'MSFT' (optional)
    - query: keywords to filter (optional)
    - days_back: how many days back (default: 30)
    - max_results: max articles (default: 5)
    """,
)
