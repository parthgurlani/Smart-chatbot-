from ddgs import DDGS


def search_web(query):
    """
    Searches the web using DuckDuckGo and returns the results.
    
    Args:
        query (str): The search query.
        
    Returns:
        tuple: A tuple containing the search results (list) and an error message (str) if any.
    """
    try:
        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )
        return results, None
    except Exception as e:
        error_message = f"Search Error: {e}"
        print(error_message)
        return [], error_message