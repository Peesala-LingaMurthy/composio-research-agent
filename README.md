# Composio App Research Agent

## Project Overview

The Composio App Research Agent is a Python-based research prototype that evaluates application integration capabilities using developer documentation and structured analysis.

It examines four areas:

- API availability
- Authentication methods
- Model Context Protocol (MCP) documentation
- API access requirements and potential integration buildability

**Current scope:** A 10-application prototype.

## Applications

| Application | Category |
|---|---|
| Slack | Communication |
| Gmail | Communication |
| Google Calendar | Productivity |
| Notion | Productivity |
| GitHub | Developer Tools |
| Jira | Project Management |
| Salesforce | CRM |
| HubSpot | CRM |
| Dropbox | Storage |
| Google Drive | Storage |

## Technology Stack

- Python
- Tavily Search API
- OpenAI Python package
- Requests
- BeautifulSoup
- Python CSV module
- Git and GitHub

## Project Structure

```text
composio-research-agent/
├── data/
│   ├── apps.csv
│   ├── test_apps.csv
│   └── manual_verification.csv
├── src/
│   ├── researcher.py
│   ├── analyzer.py
│   └── compare.py
├── output/
│   ├── research_results.csv
│   ├── app_assessments.csv
│   └── comparison_results.csv
├── main.py
├── reanalyze.py
├── requirements.txt
├── .gitignore
└── README.md
```

## How It Works

1. Reads the 10 sample applications from `data/test_apps.csv`.
2. Searches for developer documentation using the research module.
3. Collects evidence related to APIs, authentication, MCP and access requirements.
4. Analyzes available evidence using Python-based classification rules.
5. Generates structured application assessments.
6. Saves research evidence and assessments as CSV files.
7. Compares selected automated assessments with manually reviewed reference records.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Peesala-LingaMurthy/composio-research-agent.git
cd composio-research-agent
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Tavily

Create a `.env` file in the project root:

```text
TAVILY_API_KEY=your_tavily_api_key
```

Never commit `.env` or expose API keys publicly.

### 5. Run the research pipeline

```powershell
python main.py
```

This requires an active Tavily API plan with available usage.

### 6. Reanalyze saved research results

```powershell
python reanalyze.py
```

This step analyzes previously saved research records without making new Tavily API calls. It reconstructs evidence categories using keyword-based rules.

### 7. Compare assessments

```powershell
python src/compare.py
```

## Output Files

| File | Description |
|---|---|
| `output/research_results.csv` | Collected documentation records |
| `output/app_assessments.csv` | Structured application assessments |
| `output/comparison_results.csv` | Comparison against manually reviewed reference records |

## Results and Verification

- 10 application assessments are included.
- The saved research dataset contains 110 documentation records.
- The analysis reconstructs evidence categories from saved records.
- Manual verification data is available for comparison.
- The revised comparison reports 24 matching comparable field records out of 24, giving 100% agreement under its normalization rules.

**Important:** The 100% figure is limited to those 24 comparable field records. It is not a general accuracy measurement of the research system. Access-type classifications and some MCP findings still require further verification.

The reconstructed evidence categories are heuristic assignments, not independently verified research-query counts.

## Limitations

- The prototype currently covers 10 applications rather than the original 100-app target.
- Search-result classification uses keyword-based rules and requires human review.
- Documentation evidence does not prove that a live API integration works.
- MCP documentation detection does not confirm that an MCP server is operational.
- Access requirements need additional manual verification.
- The saved dataset is used for reanalysis because the current Tavily account encountered a usage-limit response.
- The project does not yet implement a complete Composio SDK integration or live MCP workflow.
- Deployment and live integration testing are not included in the current prototype.

## Future Improvements

- Expand coverage to 100 applications.
- Improve evidence classification.
- Perform broader manual verification.
- Test API authentication and access with authorized credentials.
- Validate MCP server functionality.
- Integrate Composio SDK capabilities.
- Deploy an interactive research dashboard.

## Repository

GitHub: https://github.com/Peesala-LingaMurthy/composio-research-agent
