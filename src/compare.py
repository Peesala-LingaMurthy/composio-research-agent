
import csv

manual_file = "data/manual_verification.csv"
automated_file = "output/app_assessments.csv"

# Read manual verification records
with open(manual_file, encoding="utf-8-sig") as file:
    manual_rows = list(csv.DictReader(file))

# Read automated assessments
with open(automated_file, encoding="utf-8-sig") as file:
    automated_rows = {
        row["app_name"]: row
        for row in csv.DictReader(file)
    }

# Store comparison results
comparison_results = []

correct = 0
comparable = 0

print("FIELD-LEVEL COMPARISON")
print("======================")

for row in manual_rows:

    app = row["app_name"]
    field = row["field"]
    manual = row["manual_label"].strip()

    if app not in automated_rows:
        continue

    automated = automated_rows[app]

    prediction = ""
    expected = ""

    # API comparison
    if field == "API Availability":

        prediction = automated["api_available"]

        if manual.lower() == "yes":
            expected = "yes"
        elif manual.lower() == "no":
            expected = "no"

        if prediction.startswith("Documentation evidence"):
            predicted_label = "yes"
        else:
            predicted_label = "unknown"

    # MCP comparison
    elif field == "MCP Availability":

        prediction = automated["mcp_available"]

        if manual.lower() == "yes":
            expected = "documented"
        elif manual.lower().startswith("unknown"):
            expected = "unknown"
        elif manual.lower() == "no":
            expected = "no"

        if prediction.startswith("MCP documentation evidence"):
            predicted_label = "documented"
        else:
            predicted_label = "unknown"

    else:
        continue

    # Compare only records with usable manual labels
    if expected:

        comparable += 1

        if predicted_label == expected:
            correct += 1
            status = "MATCH"
        else:
            status = "MISMATCH"

    else:
        status = "NOT SCORED"

    print("\nApp:", app)
    print("Field:", field)
    print("Automated:", predicted_label)
    print("Manual:", expected or manual)
    print("Result:", status)

    comparison_results.append({
        "app_name": app,
        "field": field,
        "automated_prediction": predicted_label,
        "manual_label": expected or manual,
        "comparison": status
    })

# Accuracy summary
print("\n======================")
print("COMPARISON SUMMARY")
print("======================")

print("Comparable records:", comparable)
print("Correct matches:", correct)

if comparable > 0:
    accuracy = (correct / comparable) * 100
    print(f"Agreement rate: {accuracy:.2f}%")
else:
    print("Agreement rate: Cannot calculate")

# Save comparison details
with open(
    "output/comparison_results.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "app_name",
        "field",
        "automated_prediction",
        "manual_label",
        "comparison"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(comparison_results)

print("\nSaved comparison to output/comparison_results.csv")
