
import os
import time
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import Client

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")

official_domains = {
    "Slack": "docs.slack.dev",
    "Gmail": "developers.google.com",
    "Google Calendar": "developers.google.com",
    "Notion": "developers.notion.com",
    "GitHub": "docs.github.com",
    "Jira": "developer.atlassian.com",
    "Salesforce": "developer.salesforce.com",
    "HubSpot": "developers.hubspot.com",
    "Dropbox": "developers.dropbox.com",
    "Google Drive": "developers.google.com"
}


def search_documentation(client, query, domain, app_name):

    for attempt in range(1, 4):

        try:
            print(f"Attempt {attempt} for {app_name}...")

            response = client.search(
                query=query,
                max_results=3
            )

            results = response.get("results", [])

            official_results = [
                item for item in results
                if urlparse(
                    item.get("url", "")
                ).hostname == domain
            ]

            return official_results

        except Exception as error:

            print(f"Attempt {attempt} failed: {error}")

            if attempt < 3:
                time.sleep(3)

    return []


def research_app(app_name, category):

    if not api_key:
        raise ValueError(
            "TAVILY_API_KEY is missing. Check your .env file."
        )

    client = Client(api_key=api_key)

    domain = official_domains.get(app_name)

    if not domain:
        raise ValueError(
            f"No official documentation domain configured for {app_name}"
        )

    # --------------------------------
    # 1. API documentation search
    # --------------------------------

    api_query = (
        f"site:{domain} {app_name} official API reference "
        "REST API endpoints developer documentation"
    )

    # --------------------------------
    # 2. Authentication search
    # --------------------------------

    auth_query = (
        f"site:{domain} {app_name} official API authentication "
        "OAuth API token developer documentation"
    )

    # --------------------------------
    # 3. MCP documentation search
    # --------------------------------

    mcp_query = (
        f"site:{domain} {app_name} official "
        "Model Context Protocol MCP server documentation"
    )

    # --------------------------------
    # 4. API access requirements search
    # --------------------------------

    access_query = (
        f"site:{domain} {app_name} API access requirements "
        "developer account self service approval registration "
        "free tier paid plan enterprise restrictions"
    )

    # HubSpot-specific searches
    if app_name == "HubSpot":

        api_query = (
            "site:developers.hubspot.com/docs/api-reference "
            "HubSpot CRM REST API endpoints"
        )

        auth_query = (
            "site:developers.hubspot.com/docs/apps "
            "HubSpot OAuth private app access token authentication"
        )

        mcp_query = (
            "site:developers.hubspot.com/docs/apps/developer-platform/build-apps "
            "remote HubSpot MCP server Model Context Protocol"
        )

        access_query = (
            "site:developers.hubspot.com "
            "HubSpot developer account app creation OAuth "
            "private app access requirements approval"
        )

    # --------------------------------
    # Run all four searches
    # --------------------------------

    queries = [
        ("API", api_query),
        ("authentication", auth_query),
        ("MCP", mcp_query),
        ("access requirements", access_query)
    ]

    combined_results = []
    seen_urls = set()

    for search_type, query in queries:

        print(
            f"\nSearching {search_type} documentation for {app_name}..."
        )

        results = search_documentation(
            client,
            query,
            domain,
            app_name
        )

        for item in results:

            url = item.get("url", "")

            if url and url not in seen_urls:
                combined_results.append(item)
                seen_urls.add(url)

    return {
        "app_name": app_name,
        "category": category,
        "search_results": combined_results
    }


if __name__ == "__main__":

    sample = research_app("HubSpot", "CRM")

    print("\nRESEARCH RESULTS")
    print("================")

    for item in sample["search_results"]:

        print("\nTitle:", item.get("title"))
        print("URL:", item.get("url"))
        print("Content:", item.get("content", "")[:300])

    print("\nTotal official results:", len(sample["search_results"]))
