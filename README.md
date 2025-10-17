# 🧠 ProspectSearchAgent — AI-Powered B2B Prospect Finder

This project is part of the **Analytos.ai Data Science Intern Task**, where I designed an **autonomous agent workflow** that automatically discovers and enriches B2B companies matching a given **Ideal Customer Profile (ICP)** using free and public APIs.  
The workflow was built and orchestrated entirely inside **n8n (no-code + AI-assisted automation)**.

---

## 🚀 Objective

The **ProspectSearchAgent** automatically:
- Takes ICP input (industry, keywords, geography, etc.)
- Queries multiple APIs to discover companies
- Fetches firmographic and hiring data
- Enriches results with technology stack
- Scores and returns structured JSON output

---

## 🧩 Workflow Overview

**n8n Cloud Workflow:**  
🔗 [View Live Workflow](https://satyam-prospectagent.app.n8n.cloud/workflow/gkPSHND9H9vfIDZd)

**Flow:**

Webhook → Apollo API → SerpAPI Jobs → Merge Results (Code) → Respond to Webhook

markdown
Copy code

**Description:**
1. **Webhook** — Receives ICP JSON input from Postman.  
2. **Apollo API** — Fetches firmographic details (revenue, industry, employees, etc.) using free developer API.  
3. **SerpAPI** — Queries Google Jobs to identify recent hiring signals.  
4. **Merge Results (Code Node)** — Combines Apollo + SerpAPI data, extracts tech stack, calculates confidence score, and formats clean JSON output.  
5. **Respond to Webhook** — Sends the final JSON response back to Postman.

---

## 🧠 APIs Used

| Function | API | Description |
|-----------|-----|-------------|
| Company & Contact Search | [Apollo.io API](https://apollo.io/) | Provides company firmographics, revenue, keywords, and tech stack. |
| Hiring Signals | [SerpAPI](https://serpapi.com/) | Extracts live job postings from Google Jobs results. |
| Orchestration | [n8n Cloud](https://n8n.io/) | Used to automate and connect all APIs with custom logic. |

---

## 🧮 Confidence Scoring Logic

Implemented in **Merge Results** node (JavaScript):

```javascript
score = 0.4 (base firmographic match)
      + 0.3 (tech stack found)
      + 0.3 (hiring signal detected)
Resulting in a confidence score (0.0–1.0) for each company.

🧱 Example ICP Input (Postman)
json
Copy code
{
  "ICP": {
    "industry": ["B2B Software"],
    "keywords": ["AI", "automation"],
    "geography": ["USA"]
  }
}
📊 Example JSON Output
json
Copy code
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
  "source": ["Apollo", "SerpAPI"],
  "confidence": "1.00"
}
⚙️ How to Run the Demo
🧪 Option 1 — Test via Postman
Copy your webhook test URL from n8n (e.g., https://satyam-prospectagent.app.n8n.cloud/webhook-test/...)

In Postman, create a new POST request.

Paste the webhook URL.

Add the sample ICP JSON as the body.

Click Send — you’ll receive the enriched company JSON as a response.

🧪 Option 2 — Inside n8n
Click Execute Workflow.

Watch nodes turn green in real-time.

See merged and scored output in the Merge Results node.

📂 Repository Structure
bash
Copy code
ProspectSearchAgent/
│
├── README.md                # Project documentation
├── n8n_workflow.json        # Exported n8n workflow
├── example_output.json      # Sample run output
└── screenshots/             # Optional demo screenshots
💡 Design Choices
Used n8n for orchestration to mimic agent-like automation.

Used Apollo.io Free API for rich company data.

Used SerpAPI to extract job listings as a real-time hiring signal.

Merge Results node acts as the “intelligent agent brain” — merging, scoring, and formatting all API data.

Final JSON output is clean and standardized for easy downstream usage.

