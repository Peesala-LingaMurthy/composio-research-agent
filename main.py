
import csv
import sys
from pathlib import Path

# Add src folder to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from researcher import research_app
from analyzer import analyze_app

# File paths
input_file = "data/apps.csv"
output_file = "output/research_results.csv"
structured_output = "output/app_assessments.csv"

# Store research results
all_results = []
structured_results = []

# Read application list
with open(input_file, "r", encoding="utf-8") as file:

    apps = csv.DictReader(file)

    for app in apps:

        app_name = app["app_name"]
        category = app["category"]

        print(f"\nResearching {app_name}...")

        try:

            # Research application documentation
            result = research_app(app_name, category)

            search_results = result.get("search_results", [])

            # Analyze collected documentation
            analysis = analyze_app(
                app_name,
                category,
                search_results
            )

            structured_results.append(analysis)

            # Store raw research results
            for item in search_results:

                all_results.append({
                    "app_name": app_name,
                    "category": category,
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", "")
                })

        except Exception as error:

            print(f"Error researching {app_name}: {error}")


# Save raw research results
with open(
    output_file,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "app_name",
        "category",
        "title",
        "url",
        "content"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(all_results)


# Save structured assessments
with open(
    structured_output,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
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

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(structured_results)


# Final summary
print("\n================================")
print("RESEARCH COMPLETED")
print("Total search results:", len(all_results))
print("Structured assessments:", len(structured_results))
print("Saved to:", output_file)
print("Saved to:", structured_output)
print("================================")


