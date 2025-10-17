def add_confidence_score(merged_results):
    """Add confidence scores based on tech stack + hiring signals."""
    for result in merged_results:
        score = 0
        if result.get("tech_stack"):
            score += 50
        if result.get("hiring_signal"):
            score += 30
        result["confidence_score"] = score
    return merged_results
