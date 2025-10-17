import os
import requests
from dotenv import load_dotenv

load_dotenv()

def fetch_apollo_data(industry, keyword, geography):
    """
    Fetch limited company details using Apollo's free /organizations/enrich endpoint.
    Works on the free plan. Pulls sample companies by domain for enrichment.
    """
    api_key = os.getenv("APOLLO_API_KEY")
    url = "https://api.apollo.io/v1/organizations/enrich"

    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": api_key  # ✅ Required in header for new security policy
    }

    # ✅ You can modify or add more domains for demo purposes
    test_domains = [
        "snowflake.com",
        "databricks.com",
        "zapier.com",
        "hubspot.com",
        "dataiq.com"
    ]

    results = {"companies": []}

    for domain in test_domains:
        payload = {"domain": domain}
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if "organization" in data:
                    org = data["organization"]
                    # Add contact info placeholder for schema consistency
                    org["contacts"] = [{
                        "name": "Not Available (Free Tier)",
                        "title": "N/A",
                        "email": "N/A",
                        "linkedin": "N/A"
                    }]
                    results["companies"].append(org)
                    print(f"✅ Fetched data for: {domain}")
                else:
                    print(f"⚠️ No organization data for {domain}")
            else:
                print(f"⚠️ Apollo skipped {domain}: {response.status_code}")
        except Exception as e:
            print(f"❌ Error fetching {domain}: {str(e)}")

    print(f"\n✅ Apollo returned {len(results['companies'])} companies total.")
    return results
