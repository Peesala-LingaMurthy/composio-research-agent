
import csv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

from researcher import research_app
from analyzer import analyze_app


# Input and output files
input_file = "data/test_apps.csv"
output_file = "output/research_results.csv"
structured_output = "output/app_assessments.csv"

all_results = []
structured_results = []


# Read application list
with open(input_file, "r", encoding="utf-8-sig") as file:

    apps = csv.DictReader(file)

    for app in apps:

        app_name = app["app_name"].strip()
        category = app["category"].strip()

        print(f"\nResearching {app_name}...")

        try:

            result = research_app(app_name, category)

            search_results = result.get("search_results", [])

            analysis = analyze_app(
                app_name,
                category,
                search_results
            )

            structured_results.append(analysis)

            # Save individual documentation results
            for item in search_results:

                all_results.append({
                    "app_name": app_name,
                    "category": category,
                    "search_type": item.get("search_type", ""),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", "")
                })

            print(
                f"Completed {app_name}: "
                f"{len(search_results)} results"
            )

        except Exception as error:

            print(f"Error researching {app_name}: {error}")

            structured_results.append({
                "app_name": app_name,
                "category": category,
                "authentication": "Research failed",
                "api_available": "Not researched",
                "mcp_available": "Not researched",
                "access_type": "Not researched",
                "buildability": "Not assessed",
                "buildability_reason": str(error),
                "evidence_urls": ""
            })


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
        "search_type",
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


# Save structured application assessments
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
print("================================")

print("Applications processed:", len(structured_results))
print("Total documentation results:", len(all_results))

print("Raw results saved to:", output_file)
print("Assessments saved to:", structured_output)

print("================================")
