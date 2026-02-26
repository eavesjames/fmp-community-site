"""Content intake from configured sources"""
import os
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

def load_queries():
    """Load search queries from config"""
    queries_path = PROJECT_ROOT / "config" / "queries.yaml"
    with open(queries_path) as f:
        return yaml.safe_load(f)

def run_intake():
    """Fetch new content using SerpAPI"""
    print("Running intake...")
    
    config = load_queries()
    settings = config.get("settings", {})
    queries = config.get("queries", [])
    
    # Prepare output directory
    raw_dir = PROJECT_ROOT / "data" / "pulse" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Get API key
    serp_api_key = os.getenv("SERP_API_KEY")
    if not serp_api_key:
        print("Warning: SERP_API_KEY not set. Skipping web search.")
        return
    
    results = []
    seen_urls = set()

    for query_config in queries:
        print(f"  Searching: {query_config['name']}")

        params = {
            "q": query_config["query"],
            "api_key": serp_api_key,
            "num": settings.get("max_results_per_query", 10),
        }

        # Add date range — per-query key takes priority; null disables recency for that query
        if "recency_days" in query_config:
            recency_days = query_config["recency_days"]   # None = explicitly disabled
        else:
            recency_days = settings.get("recency_days")
        if recency_days:
            params["tbs"] = f"qdr:d{recency_days}"

        try:
            response = requests.get("https://serpapi.com/search", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            organic_results = data.get("organic_results", [])
            added = 0
            for result in organic_results:
                url = result.get("link", "")
                if url in seen_urls:
                    continue  # Skip duplicates across queries
                seen_urls.add(url)
                results.append({
                    "query_name": query_config["name"],
                    "query_vertical": query_config.get("vertical", ""),
                    "player": query_config.get("player", "other"),
                    "title": result.get("title"),
                    "link": url,
                    "snippet": result.get("snippet"),
                    "discovered_at": datetime.now().isoformat(),
                })
                added += 1

            print(f"    Found {len(organic_results)} results, {added} new after dedup")
        except Exception as e:
            print(f"    Error: {e}")

    # Save raw results
    if results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = raw_dir / f"intake_{timestamp}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved {len(results)} results to {output_file}")
    else:
        print("No results found")

if __name__ == "__main__":
    run_intake()
