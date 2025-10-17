import os
import yaml
import json
from dotenv import load_dotenv

# --- Custom utility imports ---
from utils.apollo_api import fetch_apollo_data
from utils.builtwith_api import fetch_builtwith_data
from utils.serpapi_api import fetch_serpapi_jobs
from utils.merge_utils import merge_results
from utils.scoring_utils import add_confidence_score

# ==============================
# STEP 0: Load environment variables
# ==============================
load_dotenv()

# ==============================
# STEP 1: Load ICP + Signals Input
# ==============================
def load_icp_input(file_path="icp_input.yaml"):
    """Read ICP input and signals from YAML."""
    if not os.path.exists(file_path):
        print(f"⚠️ ICP input file not found: {file_path}")
        return {}, {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            icp = data.get("ICP", {})
            signals = data.get("Signals", {})
            print("✅ ICP and Signals loaded successfully!")
            return icp, signals
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return {}, {}

# ==============================
# STEP 2: Run APIs (Apollo, BuiltWith, SerpAPI)
# ==============================
def run_prospect_pipeline(icp, signals):
    """Main prospecting workflow integrating all APIs."""

    # --- Extract ICP filters ---
    industry = icp.get("industry", ["B2B Software"])[0]
    keywords = icp.get("keywords", ["AI"])
    geography = icp.get("geography", ["USA"])[0]

    print(f"\n🔍 Running ProspectSearchAgent for:")
    print(f"   🏢 Industry: {industry}")
    print(f"   🌍 Geography: {geography}")
    print(f"   🧠 Keywords: {keywords}")

    # --- Apollo API: company & contact discovery ---
    apollo_data = fetch_apollo_data(industry, keywords, geography)
    print(f"\n📊 Apollo API fetched {len(apollo_data.get('companies', []))} companies.")

    # --- BuiltWith API: tech stack enrichment ---
    builtwith_summary = {}
    for company in apollo_data.get("companies", []):
        domain = company.get("website_url") or company.get("domain")
        if domain:
            tech_stack_data = fetch_builtwith_data(domain)
            builtwith_summary[domain] = tech_stack_data.get("tech_stack", [])
            print(f"💻 BuiltWith found {len(builtwith_summary[domain])} technologies for {domain}.")
        else:
            print("⚠️ No domain found for BuiltWith lookup.")

    # --- SerpAPI: hiring signal detection ---
    serp_signal = fetch_serpapi_jobs(f"{industry} companies hiring in {geography}")
    print(f"\n🧠 Hiring Signal: {'Active Hiring' if serp_signal else 'No Hiring Signal Detected'}")

    # --- Merge & score results ---
    merged = merge_results(apollo_data, builtwith_summary, serp_signal)
    scored = add_confidence_score(merged)

    return scored

# ==============================
# STEP 3: Save Output to JSON
# ==============================
def save_results(data, output_path="output/results.json"):
    """Save final output as JSON."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Results saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")

# ==============================
# MAIN ENTRY POINT
# ==============================
def main():
    print("🚀 Starting ProspectSearchAgent (Full Version)...\n")

    icp, signals = load_icp_input("icp_input.yaml")

    if not icp:
        print("⚠️ No ICP data found. Exiting.")
        return

    final_results = run_prospect_pipeline(icp, signals)
    save_results(final_results)

    print(f"\n💾 Total prospects processed: {len(final_results)}")
    print("✅ ProspectSearchAgent completed successfully!\n")


if __name__ == "__main__":
    main()
