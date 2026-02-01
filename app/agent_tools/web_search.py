from pydantic_ai import Tool
from ddgs import DDGS


def duckduckgo_search(query: str) -> str:
    with DDGS() as ddgs:
        print(f"Searching for {query}")
        results = ddgs.text(query, max_results=2)
        print(f"Results: {results}")
        return "\n".join(r["body"] for r in results if "body" in r)


duckduckgo_tool = Tool(
    duckduckgo_search,
    name="duckduckgo_search",
    description="Search the web using DuckDuckGo",
)
