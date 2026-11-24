
def analyze_app(app_name, category, search_results):

    combined_text = " ".join(
        (
            item.get("title", "") + " " +
            item.get("url", "") + " " +
            item.get("content", "")
        )
        for item in search_results
    ).lower()

    # 1. Authentication detection
    auth_methods = []

    if "oauth" in combined_text:
        auth_methods.append("OAuth 2.0")

    if "personal access token" in combined_text:
        auth_methods.append("Personal Access Token")

    if (
        "private app" in combined_text
        and "access token" in combined_text
    ):
        auth_methods.append("Private App Access Token")

    if "bearer token" in combined_text:
        auth_methods.append("Bearer Token")

    auth_methods = list(dict.fromkeys(auth_methods))

    if not auth_methods:
        auth_methods = ["Needs manual verification"]

    # 2. API evidence
    api_indicators = [
        "/api/",
        "rest api",
        "api reference",
        "api endpoint",
        "api documentation"
    ]

    api_available = "Not confirmed"

    if any(word in combined_text for word in api_indicators):
        api_available = "Documentation evidence found - verify manually"

    # 3. MCP evidence
    mcp_indicators = [
        "model context protocol",
        "mcp server",
        "mcp integration"
    ]

    mcp_available = "No MCP evidence found in collected results"

    if any(word in combined_text for word in mcp_indicators):
        mcp_available = "MCP documentation evidence found - verify manually"

    # 4. Access requirements
    access_details = {
        "Gmail": (
            "Self-serve OAuth setup; sensitive scopes require verification"
        ),
        "Slack": (
            "Developer sandbox available; verify feature restrictions"
        ),
        "HubSpot": (
            "Access and distribution limits vary by app type"
        ),
        "Notion": (
            "Workspace and plan restrictions may apply"
        ),
        "GitHub": (
            "Public API; endpoint permissions and token scopes apply"
        ),
        "Dropbox": (
            "Self-serve app registration; team permissions may apply"
        ),
        "Google Calendar": (
            "OAuth setup; quota increase approval may be required"
        ),
        "Google Drive": (
            "OAuth scopes and user-data policies apply"
        ),
        "Jira": (
            "Atlassian permissions and plan requirements need review"
        ),
        "Salesforce": (
            "Administrator configuration and API permissions may apply"
        )
    }

    access_type = access_details.get(
        app_name,
        "Needs manual verification"
    )

    # 5. Buildability assessment
    if (
        api_available.startswith("Documentation evidence")
        and auth_methods != ["Needs manual verification"]
    ):

        buildability = "Potentially buildable - access testing required"

        buildability_reason = (
            "API and authentication documentation evidence was found. "
            "Credentials, permissions, plan restrictions and live API "
            "testing must be checked before confirming buildability."
        )

    else:

        buildability = "Needs further investigation"

        buildability_reason = (
            "API or authentication evidence is incomplete. "
            "Review official documentation and access requirements."
        )

    # 6. Return results
    return {
        "app_name": app_name,
        "category": category,
        "authentication": ", ".join(auth_methods),
        "api_available": api_available,
        "mcp_available": mcp_available,
        "access_type": access_type,
        "buildability": buildability,
        "buildability_reason": buildability_reason,
        "evidence_urls": "; ".join(
            item.get("url", "")
            for item in search_results
        )
    }
