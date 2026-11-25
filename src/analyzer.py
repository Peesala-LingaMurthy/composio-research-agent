
import re
from urllib.parse import urlparse


def find_matches(text, indicators):
    return [phrase for phrase in indicators if phrase in text]


def classify_access_type(access_results):
    combined_text = " ".join(
        (
            str(item.get("title", "")) + " " +
            str(item.get("content", ""))
        ).lower()
        for item in access_results
    )

    self_serve_indicators = [
        "self-service", "self service", "self-serve", "self serve",
        "register an oauth app", "creating an oauth app",
        "registering a github app", "create an app",
        "register an app", "developer portal",
        "developer dashboard", "developer account",
        "generate an api key", "create an api key",
        "get an api key", "sign up for an account"
    ]

    gated_indicators = [
        "contact sales", "approval required",
        "requires approval", "must be approved",
        "subject to approval", "manual approval",
        "manual review", "invite only", "invitation only",
        "waitlist", "enterprise customers only",
        "enterprise plan required"
    ]

    self_matches = find_matches(combined_text, self_serve_indicators)
    gated_matches = find_matches(combined_text, gated_indicators)

    negative_phrases = [
        "no approval required", "without approval",
        "does not require approval",
        "doesn't require approval"
    ]

    if any(p in combined_text for p in negative_phrases):
        gated_matches = [
            p for p in gated_matches if "approval" not in p
        ]

    if self_matches and gated_matches:
        result = "Mixed"
    elif self_matches:
        result = "Self-serve"
    elif gated_matches:
        result = "Gated"
    else:
        result = "Unknown"

    evidence = list(dict.fromkeys(self_matches + gated_matches))

    reason = ", ".join(evidence) if evidence else "No strong access evidence found"

    return result + " - " + reason


def classify_mcp(app_name, mcp_results):
    if not mcp_results:
        return "Needs manual verification - no MCP evidence found"

    app_terms = [
        term for term in re.findall(r"[a-z0-9]+", app_name.lower())
        if len(term) > 2
    ]

    official_domains = {
        "slack": ["slack.dev"],
        "gmail": ["developers.google.com"],
        "google calendar": ["developers.google.com"],
        "google drive": ["developers.google.com"],
        "github": ["github.com"],
        "notion": ["notion.com"],
        "jira": ["atlassian.com"],
        "salesforce": ["salesforce.com"],
        "hubspot": ["hubspot.com"],
        "dropbox": ["dropbox.com", "dropbox.dev"]
    }

    allowed_domains = official_domains.get(app_name.lower(), [])

    provider_results = []

    for item in mcp_results:
        title = str(item.get("title", "")).lower()
        url = str(item.get("url", ""))
        content = str(item.get("content", "")).lower()

        host = (urlparse(url).hostname or "").lower()

        has_app_name = any(term in title + " " + url.lower() + " " + content
                           for term in app_terms)

        has_mcp = (
            "mcp" in title
            or "model context protocol" in title
            or "mcp server" in content
        )

        official = any(
            host == domain or host.endswith("." + domain)
            for domain in allowed_domains
        )

        if has_app_name and has_mcp:
            provider_results.append((official, title))

    if any(official for official, title in provider_results):
        return (
            "Provider MCP documentation found - "
            "verify server setup and functionality"
        )

    if provider_results:
        return (
            "Provider-related MCP documentation found - "
            "manual verification required"
        )

    return "Needs manual verification - no provider-specific MCP evidence found"


def analyze_app(app_name, category, search_results):

    evidence = {
        "api": [],
        "authentication": [],
        "mcp": [],
        "access requirements": []
    }

    for item in search_results:
        search_type = str(item.get("search_type", "")).lower()

        if search_type in evidence:
            evidence[search_type].append(item)

    api_text = " ".join(
        (
            str(item.get("title", "")) + " " +
            str(item.get("url", "")) + " " +
            str(item.get("content", ""))
        ).lower()
        for item in evidence["api"]
    )

    auth_text = " ".join(
        (
            str(item.get("title", "")) + " " +
            str(item.get("url", "")) + " " +
            str(item.get("content", ""))
        ).lower()
        for item in evidence["authentication"]
    )

    app = app_name.lower()
    auth_methods = []

    if app == "slack":
        if "oauth" in auth_text:
            auth_methods.append("OAuth 2.0")

    elif app == "github":
        if "oauth" in auth_text:
            auth_methods.append("OAuth Apps")
        if "github app" in auth_text:
            auth_methods.append("GitHub Apps")
        if "personal access token" in auth_text:
            auth_methods.append("Personal Access Tokens")

    elif app == "notion":
        if "oauth" in auth_text:
            auth_methods.append("OAuth 2.0")
        if "personal access token" in auth_text:
            auth_methods.append("Personal Access Tokens")
        if "internal connection" in auth_text:
            auth_methods.append("Internal Connection Tokens")
        if "basic authentication" in auth_text:
            auth_methods.append("Basic Auth for OAuth token exchange only")

    elif app == "jira":
        if "oauth 2.0" in auth_text or "3lo" in auth_text:
            auth_methods.append("OAuth 2.0 (3LO)")
        if "api token" in auth_text:
            auth_methods.append("API Token with Basic Authentication")

    else:
        if re.search(r"\boauth\b", auth_text):
            auth_methods.append("OAuth 2.0 - verify exact flow")

        # Do not classify Google API keys or HubSpot private
        # app access tokens as generic API Key authentication.
        if (
            app not in ["google calendar", "gmail", "google drive", "hubspot"]
            and re.search(r"\bapi keys?\b|\bsecret api key\b", auth_text)
        ):
            auth_methods.append("API Key")

        if app == "hubspot" and "private app" in auth_text:
            auth_methods.append("Private App Access Tokens")

        if re.search(r"\bpersonal access tokens?\b", auth_text):
            auth_methods.append("Personal Access Token")

    authentication = (
        ", ".join(dict.fromkeys(auth_methods))
        if auth_methods else "Needs manual verification"
    )

    api_indicators = [
        "api reference", "rest api", "graphql api",
        "api endpoint", "api documentation", "api overview",
        "rest resource", "service endpoint", "http request"
    ]

    api_available = (
        "API documentation evidence found"
        if any(term in api_text for term in api_indicators)
        else "API not confirmed"
    )

    mcp_available = classify_mcp(
        app_name, evidence["mcp"]
    )

    access_type = classify_access_type(
        evidence["access requirements"]
    )

    if (
        api_available.startswith("API documentation")
        and authentication != "Needs manual verification"
    ):
        buildability = "Potentially buildable - access testing required"
        reason = (
            "API and authentication documentation evidence was found. "
            "Credentials, permissions, plan restrictions and live API "
            "testing are still required."
        )
    else:
        buildability = "Needs further investigation"
        reason = (
            "API or authentication evidence is incomplete. "
            "Review official documentation and access requirements."
        )

    evidence_urls = list(dict.fromkeys(
        item.get("url", "")
        for item in search_results
        if item.get("url", "")
    ))

    return {
        "app_name": app_name,
        "category": category,
        "authentication": authentication,
        "api_available": api_available,
        "mcp_available": mcp_available,
        "access_type": access_type,
        "buildability": buildability,
        "buildability_reason": reason,
        "evidence_urls": "; ".join(evidence_urls)
    }
