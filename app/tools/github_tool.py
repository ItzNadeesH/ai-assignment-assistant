import requests

def search_github_code(query: str) -> list:
    """
    Fetch top 5 GitHub repositories for a query.

    Args:
        query (str): search keyword

    Returns:
        list: list of repo name + URL
    """
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5"
        res = requests.get(url, timeout=5)
        data = res.json()

        results = []

        if "items" in data:
            for repo in data["items"][:5]:
                results.append(f"{repo['name']} - {repo['html_url']}")

        return results if results else ["No repo found"]

    except Exception as e:
        return [f"Error: {str(e)}"]