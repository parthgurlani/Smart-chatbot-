from tools.search_tool import search_web


def needs_realtime_data(query):

    query = query.lower()

    realtime_keywords = [
        "today",
        "current",
        "latest",
        "recent",
        "live",
        "weather",
        "news",
        "score",
        "stock",
        "price",
        "who is",
        "president",
        "prime minister",
        "pm of",
        "election",
        "2026",
        "2025",
        "now",
        "right now",
        "breaking",
        "update"
    ]

    return any(
        keyword in query
        for keyword in realtime_keywords
    )


def route_tool(user_query):

    # Doesn't need internet
    if not needs_realtime_data(user_query):
        return None

    try:

        results = search_web(user_query)

        # No search results found
        if not results:

            return {
                "tool_used": "DuckDuckGo",
                "context": f"""
No search results were found for:

{user_query}

Answer using your existing knowledge if possible.
"""
            }

        context_parts = []

        for r in results:

            title = r.get("title", "")
            body = r.get("body", "")
            href = r.get("href", "")

            context_parts.append(
                f"""
Title: {title}

Content: {body}

Source: {href}
"""
            )

        context = "\n\n".join(
            context_parts
        )

        return {
            "tool_used": "DuckDuckGo",
            "context": context
        }

    except Exception as e:

        print(
            f"Tool Router Error: {e}"
        )

        return {
            "tool_used": "DuckDuckGo",
            "context": f"""
Search failed.

Error:
{str(e)}

Answer using your existing knowledge.
"""
        }