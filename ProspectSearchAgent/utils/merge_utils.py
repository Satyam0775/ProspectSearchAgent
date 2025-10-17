def merge_results(apollo_data, builtwith_data, serp_signal):
    """Combine Apollo, BuiltWith, and SerpAPI data."""
    merged = []
    for company in apollo_data.get("companies", []):
        domain = company.get("website_url")
        merged.append({
            "company": company["name"],
            "domain": domain,
            "tech_stack": builtwith_data.get(domain, []),
            "hiring_signal": serp_signal
        })
    return merged
