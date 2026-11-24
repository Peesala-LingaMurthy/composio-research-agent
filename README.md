\# Composio App Research Agent



\## Project Overview



The Composio App Research Agent is a Python-based research prototype that collects official developer documentation and evaluates application integration capabilities.



It investigates four important areas:



\- API availability

\- Authentication methods

\- Model Context Protocol (MCP) documentation

\- API access requirements and potential integration buildability



The project currently demonstrates the workflow using 10 sample applications across different categories.



\## Applications Researched



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



\## Technology Stack



\- Python

\- Tavily Search API

\- OpenAI Python package

\- BeautifulSoup

\- Requests

\- CSV for storing research results

\- Git and GitHub



\## Project Structure



```text

composio-research-agent/

│

├── data/

│   ├── apps.csv

│   └── manual\_verification.csv

│

├── src/

│   ├── researcher.py

│   ├── analyzer.py

│   └── compare.py

│

├── output/

│   ├── research\_results.csv

│   ├── research\_results\_improved.csv

│   ├── app\_assessments.csv

│   ├── app\_assessments\_improved.csv

│   ├── comparison\_results.csv

│   └── comparison\_first\_pass.csv

│

├── main.py

├── .gitignore

└── README.md

```



\## How It Works



1\. Reads application names and categories from `data/apps.csv`.

2\. Searches for official developer documentation.

3\. Collects information about APIs, authentication, MCP, and access requirements.

4\. Analyzes the collected search results using Python rules.

5\. Generates structured application assessments.

6\. Saves raw research data and assessments as CSV files.

7\. Compares selected automated results with reference labels.



\## Setup and Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Peesala-LingaMurthy/composio-research-agent.git

cd composio-research-agent

```



\### 2. Create a virtual environment



```bash

python -m venv venv

```



\### 3. Activate the environment



Windows PowerShell:



```powershell

.\\venv\\Scripts\\Activate.ps1

```



\### 4. Install dependencies



```bash

pip install openai==1.39.0 tavily-python==0.1.9 pydantic==1.10.27 python-dotenv==1.2.4 requests==2.34.2 beautifulsoup4==4.15.0

```



\### 5. Configure the API key



Create a `.env` file in the project root:



```text

TAVILY\_API\_KEY=your\_tavily\_api\_key

```



Use your own API key. Never commit the `.env` file to GitHub.



\### 6. Run the project



```bash

python main.py

```



\### 7. Compare research results



```bash

python src/compare.py

```



\## Output Files



| File | Purpose |

|---|---|

| `research\_results.csv` | Collected documentation and search evidence |

| `app\_assessments.csv` | Structured application assessments |

| `comparison\_results.csv` | Comparison of selected automated predictions with reference labels |



\## Current Results



The current prototype has been tested on 10 applications.



\- 10 application assessments generated.

\- 110 official-domain search results collected in the latest run.

\- Separate searches performed for API, authentication, MCP, and access requirements.



\## Limitations and Future Improvements



This is an initial research prototype, not a production-ready integration verification system.



\- Search-result classification uses keyword-based rules and requires manual review.

\- Documentation evidence does not prove that an API integration works with live credentials.

\- Access requirements need further verification against current official documentation.

\- MCP documentation detection requires more precise validation.

\- The current dataset contains 10 applications; the target is to expand it to 100 applications.

\- The current prototype uses Tavily for research and does not yet implement a complete Composio SDK or MCP integration workflow.



Future improvements include expanding the dataset, improving classification accuracy, validating results manually, testing API access, and integrating Composio SDK capabilities.



\## Repository



GitHub: https://github.com/Peesala-LingaMurthy/composio-research-agent

