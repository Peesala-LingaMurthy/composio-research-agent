
import csv
import sys
from pathlib import Path
from collections import defaultdict, Counter

sys.path.append(str(Path(__file__).parent / "src"))

from analyzer import analyze_app

INPUT_FILE = Path("output/research_results.csv")
OUTPUT_FILE = Path("output/app_assessments.csv")


def identify_types(row):
    title = row.get("title", "").lower()
    url = row.get("url", "").lower()
    content = row.get("content", "").lower()

    text = title + " " + url + " " + content
    types = []

    if (
        "mcp" in title
        or "model context protocol" in title
        or "/mcp" in url
        or "mcp server" in title
    ):
        types.append("mcp")

    auth_terms = [
        "oauth", "authentication", "authorization",
        "access token", "api key", "personal access token",
        "credentials", "auth flow"
    ]

    if any(term in text for term in auth_terms):
        types.append("authentication")

    access_terms = [
        "contact sales", "approval required",
        "requires approval", "request access",
        "developer account", "developer portal",
        "register an app", "create an app",
        "self-service", "self serve", "waitlist",
        "allowlist", "enterprise plan"
    ]

    if any(term in text for term in access_terms):
        types.append("access requirements")

    api_terms = [
        "api", "rest", "graphql", "endpoint",
        "api reference", "api overview"
    ]

    if any(term in text for term in api_terms):
        types.append("api")

    return types


grouped = defaultdict(list)
categories = {}
counts = Counter()

with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        app_name = row["app_name"].strip()
        category = row["category"].strip()

        categories[app_name] = category

        for search_type in identify_types(row):
            grouped[app_name].append({
                "search_type": search_type,
                "title": row["title"],
                "url": row["url"],
                "content": row["content"]
            })
            counts[search_type] += 1


assessments = []

for app_name, category in categories.items():
    print("Analyzing:", app_name)

    result = analyze_app(
        app_name,
        category,
        grouped[app_name]
    )

    assessments.append(result)


fields = [
    "app_name",
    "category",
    "authentication",
    "api_available",
    "mcp_available",
    "access_type",
    "buildability",
    "buildability_reason",
    "evidence_urls"
]

with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(assessments)


print("\nRE-ANALYSIS COMPLETED")
print("Applications:", len(assessments))
print("Reconstructed evidence categories:")

for name, count in sorted(counts.items()):
    print(name, ":", count)

print("Saved to:", OUTPUT_FILE)
print("Tavily API calls: 0")
