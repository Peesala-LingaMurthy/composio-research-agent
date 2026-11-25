import os
import time
from urllib.parse import urlparse

from dotenv import load_dotenv
from tavily import Client

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")


# Official documentation domains for 100 applications
official_domains = {
    # Communication
    "Slack": "docs.slack.dev",
    "Microsoft Teams": "learn.microsoft.com",
    "Discord": "discord.com",
    "Zoom": "developers.zoom.us",
    "Telegram": "core.telegram.org",
    "Twilio": "www.twilio.com",
    "SendGrid": "docs.sendgrid.com",
    "Intercom": "developers.intercom.com",
    "WhatsApp Business": "developers.facebook.com",
    "Google Chat": "developers.google.com",

    # Productivity
    "Notion": "developers.notion.com",
    "Google Calendar": "developers.google.com",
    "Google Sheets": "developers.google.com",
    "Google Docs": "developers.google.com",
    "Airtable": "airtable.com",
    "Todoist": "developer.todoist.com",
    "Asana": "developers.asana.com",
    "Trello": "developer.atlassian.com",
    "Monday.com": "developer.monday.com",
    "ClickUp": "developer.clickup.com",

    # Developer Tools
    "GitHub": "docs.github.com",
    "GitLab": "docs.gitlab.com",
    "Bitbucket": "developer.atlassian.com",
    "Jenkins": "www.jenkins.io",
    "Docker Hub": "docs.docker.com",
    "Sentry": "docs.sentry.io",
    "Datadog": "docs.datadoghq.com",
    "Postman": "learning.postman.com",
    "Vercel": "vercel.com",
    "Cloudflare": "developers.cloudflare.com",

    # Project Management
    "Jira": "developer.atlassian.com",
    "Linear": "developers.linear.app",
    "Wrike": "developers.wrike.com",
    "Basecamp": "github.com",
    "Smartsheet": "developers.smartsheet.com",
    "Teamwork": "apidocs.teamwork.com",
    "Shortcut": "developer.shortcut.com",
    "YouTrack": "www.jetbrains.com",
    "Miro": "developers.miro.com",
    "Aha!": "www.aha.io",

    # CRM
    "Salesforce": "developer.salesforce.com",
    "HubSpot": "developers.hubspot.com",
    "Zoho CRM": "www.zoho.com",
    "Pipedrive": "developers.pipedrive.com",
    "Freshsales": "developers.freshworks.com",
    "Microsoft Dynamics 365": "learn.microsoft.com",
    "Copper": "developer.copper.com",
    "Close": "developer.close.com",
    "Insightly": "api.insightly.com",
    "Nimble": "nimble.com",

    # Storage
    "Google Drive": "developers.google.com",
    "Dropbox": "developers.dropbox.com",
    "Box": "developer.box.com",
    "OneDrive": "learn.microsoft.com",
    "Amazon S3": "docs.aws.amazon.com",
    "Cloudinary": "cloudinary.com",
    "Egnyte": "developers.egnyte.com",
    "Backblaze B2": "www.backblaze.com",
    "Wasabi": "docs.wasabi.com",
    "pCloud": "docs.pcloud.com",

    # Finance
    "Stripe": "docs.stripe.com",
    "PayPal": "developer.paypal.com",
    "Square": "developer.squareup.com",
    "Razorpay": "razorpay.com",
    "Plaid": "plaid.com",
    "QuickBooks": "developer.intuit.com",
    "Xero": "developer.xero.com",
    "FreshBooks": "www.freshbooks.com",
    "Chargebee": "apidocs.chargebee.com",
    "Wise": "docs.wise.com",

    # Marketing
    "Mailchimp": "mailchimp.com",
    "Brevo": "developers.brevo.com",
    "Klaviyo": "developers.klaviyo.com",
    "ActiveCampaign": "developers.activecampaign.com",
    "Marketo": "experienceleague.adobe.com",
    "Campaign Monitor": "www.campaignmonitor.com",
    "ConvertKit": "developers.kit.com",
    "Hootsuite": "developer.hootsuite.com",
    "Buffer": "buffer.com",
    "Typeform": "www.typeform.com",

    # Customer Support
    "Zendesk": "developer.zendesk.com",
    "Freshdesk": "developers.freshworks.com",
    "Help Scout": "developer.helpscout.com",
    "Gorgias": "developers.gorgias.com",
    "Crisp": "docs.crisp.chat",
    "Tawk.to": "developer.tawk.to",
    "Front": "dev.frontapp.com",
    "Gladly": "developer.gladly.com",
    "Kustomer": "developer.kustomer.com",
    "Zoho Desk": "www.zoho.com",

    # E-commerce
    "Shopify": "shopify.dev",
    "WooCommerce": "developer.woocommerce.com",
    "BigCommerce": "developer.bigcommerce.com",
    "Magento": "developer.adobe.com",
    "Wix": "dev.wix.com",
    "Squarespace": "developers.squarespace.com",
    "Etsy": "developers.etsy.com",
    "eBay": "developer.ebay.com",
    "Amazon Selling Partner API": "developer-docs.amazon.com",
    "ShipStation": "docs.shipstation.com"
}


def search_documentation(client, query, domain, app_name):

    for attempt in range(1, 4):

        try:
            print(f"Attempt {attempt} for {app_name}...")

            response = client.search(
                query=query,
                max_results=5
            )

            results = response.get("results", [])
            official_results = []

            for item in results:

                hostname = urlparse(
                    item.get("url", "")
                ).hostname or ""

                hostname = hostname.lower()

                if not (
                    hostname == domain
                    or hostname.endswith("." + domain)
                ):
                    continue

                title = item.get("title", "").lower()
                content = item.get("content", "").lower()
                url = item.get("url", "").lower()

                combined_text = title + " " + content + " " + url

                # Product-specific filtering for Google products
                if app_name == "Google Docs":

                    if "/workspace/docs/" not in url:
                        continue

                elif app_name == "Google Sheets":

                    if "/workspace/sheets/" not in url:
                        continue

                else:

                    app_words = (
                        app_name.lower()
                        .replace("-", " ")
                        .split()
                    )

                    if not any(
                        word in combined_text
                        for word in app_words
                    ):
                        continue

                official_results.append(item)

            return official_results

        except Exception as error:

            print(f"Attempt {attempt} failed: {error}")

            if attempt < 3:
                time.sleep(3)

    return []


def get_queries(app_name, domain):

    queries = [

        (
            "API",
            f"site:{domain} {app_name} official API reference "
            "REST API endpoints developer documentation"
        ),

        (
            "authentication",
            f"site:{domain} {app_name} API authentication "
            "OAuth 2.0 API key personal access token "
            "access token bearer token developer documentation"
        ),

        (
            "MCP",
            f"site:{domain} {app_name} official "
            "Model Context Protocol MCP server documentation"
        ),

        (
            "access requirements",
            f"site:{domain} {app_name} developer portal "
            "sign up create developer account register application "
            "self service API access"
        ),

        (
            "access requirements",
            f"site:{domain} {app_name} API access "
            "approval required request access allowlist restricted scopes "
            "enterprise plan contact sales"
        )
    ]

    if app_name == "GitHub":

        queries[0] = (
            "API",
            "site:docs.github.com/en/rest GitHub REST API endpoints"
        )

        queries[1] = (
            "authentication",
            "site:docs.github.com GitHub authentication OAuth Apps "
            "GitHub Apps personal access tokens fine-grained tokens"
        )

        queries[2] = (
            "MCP",
            "site:docs.github.com GitHub official MCP server "
            "Model Context Protocol"
        )

        queries[3] = (
            "access requirements",
            "site:docs.github.com GitHub developer account "
            "create application register OAuth App"
        )

        queries[4] = (
            "access requirements",
            "site:docs.github.com GitHub API approval restrictions "
            "rate limits organization approval permissions"
        )

    elif app_name == "HubSpot":

        queries[0] = (
            "API",
            "site:developers.hubspot.com/docs/api-reference "
            "HubSpot CRM REST API endpoints"
        )

        queries[1] = (
            "authentication",
            "site:developers.hubspot.com/docs/apps "
            "HubSpot OAuth private app access token authentication"
        )

        queries[2] = (
            "MCP",
            "site:developers.hubspot.com HubSpot MCP server "
            "Model Context Protocol"
        )

        queries[3] = (
            "access requirements",
            "site:developers.hubspot.com HubSpot developer account "
            "create app register developer account"
        )

        queries[4] = (
            "access requirements",
            "site:developers.hubspot.com HubSpot API approval "
            "restricted scopes request access"
        )

    return queries


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

    queries = get_queries(app_name, domain)

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

            # Preserve the search type for each result.
            # The same URL can be relevant to different research fields.
            key = (url, search_type)

            if url and key not in seen_urls:

                result_item = dict(item)
                result_item["search_type"] = search_type

                combined_results.append(result_item)
                seen_urls.add(key)

    return {
        "app_name": app_name,
        "category": category,
        "search_results": combined_results
    }


if __name__ == "__main__":

    sample = research_app(
        "GitHub",
        "Developer Tools"
    )

    print("\nRESEARCH RESULTS")
    print("================")

    for item in sample["search_results"]:

        print("\nSearch type:", item.get("search_type"))
        print("Title:", item.get("title"))
        print("URL:", item.get("url"))
        print("Content:", item.get("content", "")[:300])

    print(
        "\nTotal official results:",
        len(sample["search_results"])
    )
