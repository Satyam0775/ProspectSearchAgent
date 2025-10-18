# 🧠 ProspectSearchAgent — AI-Powered B2B Prospect Finder

This project is part of the **Analytos.ai Data Science Intern Task**, where I designed an **AI-powered ProspectSearchAgent** that automatically discovers and enriches B2B companies matching a given **Ideal Customer Profile (ICP)** using multiple free and public APIs.  

The agent’s orchestration logic was developed using **LangChain (Python)**, while the **end-to-end workflow automation and API integration** were implemented using **n8n Cloud** for visualization and execution.

---

## 🚀 Objective

The **ProspectSearchAgent** autonomously:
- Takes ICP input (industry, keywords, geography, etc.)
- Queries multiple APIs (Apollo, BuiltWith, SerpAPI)
- Fetches firmographic, hiring, and tech stack data
- Merges and enriches the results
- Assigns a confidence score based on matching criteria
- Returns structured JSON output ready for analysis

---

## 🧩 System Architecture

### **Local Orchestration: LangChain**
- Used to define the logical flow and data dependencies.
- Each API integration is treated as a LangChain “Tool.”
- Handles merging, deduplication, and scoring logic programmatically.

### **End-to-End Automation: n8n Workflow**
- The visual workflow in n8n executes API calls and data enrichment steps automatically.
- Used for testing and validating the full pipeline with real-time API calls.

**Workflow Structure:**

Webhook → Apollo API → BuiltWith API → SerpAPI Jobs → Merge Results (Code Node) → Respond to Webhook

yaml

---

## ⚙️ Workflow Description

| Step | Node | Function |
|------|------|-----------|
| 1️⃣ | **Webhook** | Receives ICP input JSON from Postman or LangChain call. |
| 2️⃣ | **Apollo API** | Fetches firmographics like name, revenue, industry, and employees. |
| 3️⃣ | **BuiltWith API** | Extracts the company’s technology stack and hosting information. |
| 4️⃣ | **SerpAPI (Jobs)** | Retrieves hiring data and job listings for hiring signal detection. |
| 5️⃣ | **Merge Results (LangChain Logic / n8n Code Node)** | Merges and enriches all API responses into one structured output. |
| 6️⃣ | **Respond to Webhook** | Returns the final JSON to the client or Postman. |

---

## 🧠 APIs Used

| Function | API | Description |
|-----------|-----|-------------|
| **Company Data** | [Apollo.io API](https://apollo.io/) | Provides company firmographics, keywords, and contact data. |
| **Tech Stack Data** | [BuiltWith API](https://builtwith.com/) | Detects technology stack and platform usage for domains. |
| **Hiring Signals** | [SerpAPI](https://serpapi.com/) | Extracts real-time job listings from Google Jobs. |
| **Workflow Orchestration** | [LangChain](https://www.langchain.com/) | Manages logical flow and tool execution locally. |
| **Automation Platform** | [n8n Cloud](https://n8n.io/) | Used for executing and visualizing the workflow end-to-end. |

---

## 🧮 Confidence Scoring Logic

Implemented using **LangChain Tool Logic** and replicated inside the **Merge Results** node:

```javascript
score = 0.4 * firmographic_match
      + 0.3 * tech_stack_match
      + 0.3 * hiring_signal_detected
This results in a confidence score (0.0 – 1.0) representing how strongly a company matches the target ICP.

🧱 Example ICP Input (Postman)
json
{
  "ICP": {
    "industry": ["B2B Software"],
    "keywords": ["AI", "automation"],
    "geography": ["USA"]
  }
}
📊 Example JSON Output
json
{
  "company_name": "Snowflake",
  "domain": "snowflake.com",
  "industry": "Information Technology & Services",
  "revenue": "3.8B",
  "employee_count": 7900,
  "location": "Menlo Park, CA 94563, US",
  "keywords": [
    "data warehousing",
    "cloud",
    "analytics",
    "data lake",
    "data applications",
    "data science",
    "machine learning"
  ],
  "tech_stack": [
    "AI",
    "Android",
    "CloudFlare CDN",
    "Gmail",
    "Salesforce Service Cloud",
    "VueJS",
    "Snowflake",
    "WP Engine",
    "Wistia"
  ],
  "signals": {
    "recent_hiring": true
  },
  "source": ["Apollo", "BuiltWith", "SerpAPI"],
  "confidence": "1.00"
}
🧪 How to Run the Demo
Option 1 — Test via Postman
Copy your n8n webhook test URL (e.g., https://satyam-prospectagent.app.n8n.cloud/webhook-test/...)

In Postman, create a POST request with the above URL.

Paste the sample ICP JSON in the request body.

Click Send.

View the enriched JSON response in Postman.

Option 2 — Execute Inside n8n
Click Execute Workflow.

Watch each node turn green as data flows through.

View the merged and scored JSON inside the Merge Results node.

📂 Repository Structure
bash
ProspectSearchAgent/
│
├── README.md                # Project documentation
├── langchain_pipeline.py    # Local orchestration using LangChain
├── n8n_workflow.json        # Exported n8n workflow
├── example_output.json      # Sample run output
└── screenshots/             # Workflow images
💡 Design Choices
Used LangChain for modular orchestration and logic management.

Used n8n Cloud for visual end-to-end workflow execution.

Used Apollo, BuiltWith, and SerpAPI as the data sources.

The Merge Results node acts as the intelligent “agent brain,” merging all sources and scoring matches.

The output format is clean, standardized JSON, ideal for integration into dashboards or CRMs.

