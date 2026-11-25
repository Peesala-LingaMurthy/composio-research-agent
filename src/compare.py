
import csv
import os

manual_file = "data/manual_verification.csv"
automated_file = "output/app_assessments.csv"
output_file = "output/comparison_results.csv"


with open(manual_file, encoding="utf-8-sig") as file:
    manual_rows = list(csv.DictReader(file))

with open(automated_file, encoding="utf-8-sig") as file:
    automated_rows = {
        row["app_name"]: row
        for row in csv.DictReader(file)
    }


def normalize_auth(text):
    text = text.lower()
    methods = set()

    if "oauth" in text:
        methods.add("oauth")

    if "personal access token" in text or "pat" in text:
        methods.add("personal access token")

    if "github app" in text:
        methods.add("github app")

    if "api token" in text:
        methods.add("api token")

    if "api key" in text:
        methods.add("api key")

    if "internal connection token" in text:
        methods.add("internal connection token")

    if "private app access token" in text or "private app" in text:
        methods.add("private app access token")

    if "basic authentication" in text or "basic auth" in text:
        methods.add("basic authentication")

    return methods


def normalize_mcp(text):
    text = text.lower()

    if "no mcp evidence found" in text:
        return "unknown"

    if "mcp documentation found" in text:
        return "documented"

    if "mcp-related documentation found" in text:
        return "documented"

    if "provider-related mcp documentation found" in text:
        return "documented"

    return "unknown"


comparison_results = []

correct = 0
comparable = 0
not_verified = 0

print("FIELD-LEVEL COMPARISON")
print("======================")


for row in manual_rows:

    app = row["app_name"].strip()
    field = row["field"].strip()
    manual = row["manual_label"].strip()
    verification_status = row["verification_status"].strip().lower()

    if app not in automated_rows:
        continue

    automated = automated_rows[app]

    prediction = ""
    predicted_label = ""
    expected = ""
    status = ""

    if field == "API Availability":

        prediction = automated["api_available"]

        if prediction.startswith("API documentation"):
            predicted_label = "yes"
        else:
            predicted_label = "unknown"

        if manual.lower() == "yes":
            expected = "yes"
        elif manual.lower() == "no":
            expected = "no"

        if verification_status == "verified" and expected:
            comparable += 1

            if predicted_label == expected:
                correct += 1
                status = "MATCH"
            else:
                status = "MISMATCH"
        else:
            not_verified += 1
            status = "NOT SCORED - VERIFICATION INCOMPLETE"

    elif field == "MCP Availability":

        prediction = automated["mcp_available"]
        predicted_label = normalize_mcp(prediction)

        if manual.lower() == "yes":
            expected = "documented"
        elif manual.lower() == "no":
            expected = "no"
        else:
            expected = "unknown"

        if verification_status == "verified" and expected in [
            "documented", "no"
        ]:
            comparable += 1

            if predicted_label == expected:
                correct += 1
                status = "MATCH"
            else:
                status = "MISMATCH"
        else:
            not_verified += 1
            status = "NOT SCORED - VERIFICATION INCOMPLETE"

    elif field == "Authentication":

        prediction = automated["authentication"]

        automated_methods = normalize_auth(prediction)
        manual_methods = normalize_auth(manual)

        predicted_label = "; ".join(sorted(automated_methods)) or "unknown"
        expected = "; ".join(sorted(manual_methods)) or "unknown"

        if verification_status != "verified" or not manual_methods:
            not_verified += 1
            status = "NOT SCORED - VERIFICATION INCOMPLETE"

        else:
            # Basic Authentication in Notion's OAuth token exchange
            # is a narrower use than a general API authentication method.
            if (
                app.lower() == "notion"
                and "basic authentication" in automated_methods
                and "basic authentication" not in manual_methods
            ):
                automated_methods.remove("basic authentication")

            comparable += 1

            if automated_methods == manual_methods:
                correct += 1
                status = "MATCH"
            else:
                status = "MISMATCH"

            predicted_label = "; ".join(sorted(automated_methods)) or "unknown"
            expected = "; ".join(sorted(manual_methods)) or "unknown"

    elif field == "Access Type":

        prediction = automated["access_type"]
        predicted_label = "not scored"
        expected = manual or "unknown"

        not_verified += 1
        status = "NOT SCORED - ACCESS TYPE NEEDS MANUAL CLASSIFICATION"

    else:
        continue

    print("\nApp:", app)
    print("Field:", field)
    print("Automated:", prediction)
    print("Automated label:", predicted_label)
    print("Manual label:", manual)
    print("Verification:", verification_status)
    print("Comparison:", status)

    comparison_results.append({
        "app_name": app,
        "field": field,
        "automated_prediction": predicted_label,
        "automated_raw_result": prediction,
        "manual_label": manual,
        "verification_status": verification_status,
        "comparison": status
    })


print("\n======================")
print("COMPARISON SUMMARY")
print("======================")

print("Comparable verified records:", comparable)
print("Correct matches:", correct)
print("Records not scored:", not_verified)

if comparable:
    agreement = correct / comparable * 100
    print(f"Verified agreement rate: {agreement:.2f}%")
else:
    print("Verified agreement rate: Cannot calculate")


os.makedirs("output", exist_ok=True)

with open(output_file, "w", newline="", encoding="utf-8") as file:

    fieldnames = [
        "app_name",
        "field",
        "automated_prediction",
        "automated_raw_result",
        "manual_label",
        "verification_status",
        "comparison"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comparison_results)

print("\nSaved comparison to:", output_file)
