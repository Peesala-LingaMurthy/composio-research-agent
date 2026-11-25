
import csv
import html
from pathlib import Path
from collections import Counter

BASE = Path(__file__).parent
OUTPUT = BASE / "output"
ASSESSMENTS = OUTPUT / "app_assessments.csv"
COMPARISONS = OUTPUT / "comparison_results.csv"
REPORT = OUTPUT / "research_report.html"


def read_csv(path):
    with open(path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def safe(value):
    return html.escape(str(value or ""))


apps = read_csv(ASSESSMENTS)
comparisons = read_csv(COMPARISONS)

if not apps:
    raise SystemExit("No application assessment records found.")

total_apps = len(apps)
api_count = sum(
    "evidence found" in row["api_available"].lower()
    for row in apps
)

mcp_count = sum(
    "documentation found" in row["mcp_available"].lower()
    for row in apps
)

buildable_count = sum(
    "potentially buildable" in row["buildability"].lower()
    for row in apps
)

access_counts = Counter(row["access_type"] for row in apps)

scored = [
    row for row in comparisons
    if row["comparison"].upper() in ("MATCH", "MISMATCH")
]

matches = sum(row["comparison"].upper() == "MATCH" for row in scored)
mismatches = sum(row["comparison"].upper() == "MISMATCH" for row in scored)

agreement = (matches / len(scored) * 100) if scored else 0

field_counts = Counter(row["field"] for row in comparisons)
not_scored = len(comparisons) - len(scored)


app_rows = ""

for row in apps:
    app_rows += f"""
    <tr>
        <td><strong>{safe(row['app_name'])}</strong></td>
        <td>{safe(row['category'])}</td>
        <td>{safe(row['authentication'])}</td>
        <td>{safe(row['api_available'])}</td>
        <td>{safe(row['mcp_available'])}</td>
        <td>{safe(row['access_type'])}</td>
        <td>{safe(row['buildability'])}</td>
    </tr>
    """


comparison_rows = ""

for row in comparisons:
    comparison_rows += f"""
    <tr>
        <td>{safe(row['app_name'])}</td>
        <td>{safe(row['field'])}</td>
        <td>{safe(row['automated_prediction'])}</td>
        <td>{safe(row['manual_label'])}</td>
        <td>{safe(row['verification_status'])}</td>
        <td>{safe(row['comparison'])}</td>
    </tr>
    """


access_items = ""

for label, count in access_counts.items():
    access_items += f"""
    <li><strong>{safe(label)}</strong>: {count}</li>
    """


field_items = ""

for field, count in field_counts.items():
    field_items += f"""
    <li><strong>{safe(field)}</strong>: {count} records</li>
    """


report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Composio App Research Report</title>
<style>
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6fa;
    color: #202938;
    line-height: 1.6;
}}
header {{
    background: #172554;
    color: white;
    padding: 38px 7%;
}}
header h1 {{ margin: 0 0 8px; font-size: 30px; }}
header p {{ margin: 0; color: #dbeafe; }}
main {{ max-width: 1250px; margin: 30px auto; padding: 0 20px; }}
section {{
    background: white;
    margin-bottom: 24px;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 9px #0000000c;
}}
h2 {{ color: #172554; margin-top: 0; }}
.metrics {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 15px;
    margin-bottom: 24px;
}}
.metric {{
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 9px #0000000c;
}}
.metric strong {{
    display: block;
    font-size: 29px;
    color: #1d4ed8;
}}
.metric span {{ color: #526071; font-size: 14px; }}
.table-wrap {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; min-width: 850px; }}
th, td {{
    padding: 11px;
    border-bottom: 1px solid #e5e7eb;
    text-align: left;
    vertical-align: top;
    font-size: 13px;
}}
th {{ background: #eff4ff; color: #172554; }}
tr:hover {{ background: #f8fafc; }}
.note {{
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    padding: 14px;
    border-radius: 5px;
}}
ul {{ padding-left: 22px; }}
footer {{
    text-align: center;
    padding: 25px;
    color: #64748b;
}}
@media print {{
    body {{ background: white; }}
    section, .metric {{ box-shadow: none; border: 1px solid #ddd; }}
}}
</style>
</head>

<body>
<header>
    <h1>Composio App Research Agent</h1>
    <p>Application API, Authentication, MCP and Integration Readiness Analysis</p>
    <p>Research prototype | 10 applications | November 2026</p>
</header>

<main>

<section>
<h2>1. Project Overview</h2>
<p>
This Python research prototype evaluates application integration capabilities
using collected developer documentation and rule-based analysis.
It examines API availability, authentication methods, MCP documentation,
access requirements and potential integration buildability.
</p>
<div class="note">
<strong>Scope:</strong> This deliverable is a 10-application prototype,
not the original 100-application target.
</div>
</section>

<div class="metrics">
    <div class="metric"><strong>{total_apps}</strong><span>Applications assessed</span></div>
    <div class="metric"><strong>{api_count}</strong><span>With API documentation evidence</span></div>
    <div class="metric"><strong>{mcp_count}</strong><span>With MCP documentation evidence</span></div>
    <div class="metric"><strong>{buildable_count}</strong><span>Potentially buildable</span></div>
    <div class="metric"><strong>{len(comparisons)}</strong><span>Comparison records</span></div>
</div>

<section>
<h2>2. Application Assessment</h2>
<div class="table-wrap">
<table>
<thead>
<tr>
<th>Application</th><th>Category</th><th>Authentication</th>
<th>API</th><th>MCP</th><th>Access type</th><th>Buildability</th>
</tr>
</thead>
<tbody>{app_rows}</tbody>
</table>
</div>
</section>

<section>
<h2>3. Access Classification Summary</h2>
<ul>{access_items}</ul>
<p>
Unknown access classifications indicate that the collected evidence
was insufficient for a confident self-serve or gated determination.
</p>
</section>

<section>
<h2>4. Manual Verification Comparison</h2>
<div class="metrics">
    <div class="metric"><strong>{len(scored)}</strong><span>Comparable verified records</span></div>
    <div class="metric"><strong>{matches}</strong><span>Matching records</span></div>
    <div class="metric"><strong>{mismatches}</strong><span>Non-matching records</span></div>
    <div class="metric"><strong>{agreement:.1f}%</strong><span>Agreement on scored records</span></div>
    <div class="metric"><strong>{not_scored}</strong><span>Records not scored</span></div>
</div>

<p>
Comparison records by field:
</p>
<ul>{field_items}</ul>

<div class="note">
<strong>How to interpret the agreement:</strong>
The agreement percentage applies only to comparable records scored by
the comparison script under its normalization rules. It is not a general
accuracy estimate of the research system. Unverified and non-comparable
records are excluded. Access-type classifications are not scored.
</div>

<div class="table-wrap">
<table>
<thead>
<tr>
<th>Application</th><th>Field</th><th>Automated result</th>
<th>Manual reference</th><th>Verification</th><th>Comparison</th>
</tr>
</thead>
<tbody>{comparison_rows}</tbody>
</table>
</div>
</section>

<section>
<h2>5. Methodology</h2>
<ol>
<li>Read application names and categories from the input CSV.</li>
<li>Collect developer documentation and search-result evidence.</li>
<li>Classify API, authentication, MCP and access-related information.</li>
<li>Generate structured application assessments.</li>
<li>Compare selected automated findings against manually reviewed records.</li>
</ol>
<p>
Saved research records were reanalyzed using reconstructed evidence categories.
These categories are heuristic assignments and do not represent independently
verified research-query counts.
</p>
</section>

<section>
<h2>6. Limitations and Future Work</h2>
<ul>
<li>The current prototype covers 10 applications, not 100.</li>
<li>Classification relies on keyword-based rules and requires human review.</li>
<li>Documentation evidence does not prove successful live API integration.</li>
<li>MCP documentation does not prove that an MCP server is operational.</li>
<li>Some access requirements and MCP findings need further verification.</li>
<li>The saved dataset was used for reanalysis after a Tavily usage-limit response.</li>
<li>A complete Composio SDK integration and live MCP workflow have not been implemented.</li>
</ul>
<h3>Future improvements</h3>
<ul>
<li>Expand the dataset to 100 applications.</li>
<li>Improve classification and evidence extraction.</li>
<li>Perform more manual verification.</li>
<li>Test authorized API authentication and live access.</li>
<li>Validate MCP server functionality.</li>
<li>Integrate Composio SDK capabilities and deploy a dashboard.</li>
</ul>
</section>

<section>
<h2>7. Technology Stack</h2>
<p>
Python, Tavily Search API, OpenAI Python package, Requests,
BeautifulSoup, CSV, Git and GitHub.
</p>
<p>
GitHub repository:
<a href="https://github.com/Peesala-LingaMurthy/composio-research-agent">
Composio App Research Agent
</a>
</p>
</section>

</main>
<footer>
Composio App Research Agent — Research Prototype
</footer>
</body>
</html>
"""

OUTPUT.mkdir(exist_ok=True)
REPORT.write_text(report, encoding="utf-8")

print("HTML report created successfully.")
print("Report location:", REPORT)
print("Applications:", total_apps)
print("Comparable records:", len(scored))
print("Matches:", matches)
print("Agreement:", f"{agreement:.1f}%")
