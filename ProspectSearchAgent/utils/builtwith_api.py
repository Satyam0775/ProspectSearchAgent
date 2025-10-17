import os
import requests
from dotenv import load_dotenv
import time

# Load environment variables from .env
load_dotenv()

def fetch_builtwith_data(domain):
    """Fetch tech stack details from BuiltWith Free API."""
    
    api_key = os.getenv("BUILTWITH_API_KEY")
    url = "https://api.builtwith.com/free1/api.json"  # ✅ Correct endpoint for Free API

    # Clean domain (remove http/https/www)
    clean_domain = domain.replace("http://", "").replace("https://", "").replace("www.", "").split("/")[0]

    params = {"KEY": api_key, "LOOKUP": clean_domain}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # ✅ Parse the simplified Free API response structure
        domain_info = data.get("domain", clean_domain)
        groups = data.get("groups", [])

        tech_stack = []
        for group in groups:
            for category in group.get("categories", []):
                if category.get("live", 0) > 0:
                    tech_stack.append(category.get("name"))

        # ✅ Add small delay to respect 1 request/sec rate limit
        time.sleep(1)

        print(f"✅ Successfully fetched data for: {clean_domain}")
        return {"domain": domain_info, "tech_stack": tech_stack}

    except requests.exceptions.RequestException as e:
        print(f"❌ BuiltWith API request error for {clean_domain}: {e}")
        return {"domain": clean_domain, "tech_stack": []}

    except Exception as e:
        print(f"⚠️ Unexpected error for {clean_domain}: {e}")
        return {"domain": clean_domain, "tech_stack": []}


# Example usage (for testing)
if __name__ == "__main__":
    result = fetch_builtwith_data("builtwith.com")
    print(result)
