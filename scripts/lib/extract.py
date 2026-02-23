"""Extract and enrich metadata from raw intake using Claude"""
import os
import json
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

def extract_metadata_from_url(url, title, snippet, client):
    """Use Claude to extract metadata from a URL"""
    
    prompt = f"""Visit this URL and extract metadata for a Fault Managed Power (FMP) knowledge base:

URL: {url}
Title: {title}
Snippet: {snippet}

Extract the following information:

1. **artifact_type**: Choose ONE from: press, product, event, case-study, standard, doc, video, other
2. **publish_date**: Publication date if available (YYYY-MM-DD format), or null
3. **description**: 150-170 character meta description
4. **players**: Array of relevant organizations from: voltserver, panduit, cisco, fmp-alliance, other
5. **topics**: Array from: class-4, safety-model, estimating, schedule-value, space-value, digital-connectivity, smart-buildings, data-centers, retrofits, code-standards, commissioning
6. **value_levers**: Array from: labor, schedule, space, digital-connectivity, risk, feasibility, operations
7. **confidence**: high, medium, or low (how relevant is this to FMP?)
8. **summary**: 2-3 sentence summary of what this is and why it matters for FMP

Respond ONLY with valid JSON:
{{
  "artifact_type": "...",
  "publish_date": "...",
  "description": "...",
  "players": [...],
  "topics": [...],
  "value_levers": [...],
  "confidence": "...",
  "summary": "..."
}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response
        response_text = message.content[0].text
        
        # Extract JSON from response (might have markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        metadata = json.loads(response_text)
        return metadata
    except Exception as e:
        print(f"    Error extracting metadata: {e}")
        return None

def run_extract():
    """Extract metadata from raw intake files"""
    print("Running extract...")
    
    # Get API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Load raw intake files
    raw_dir = PROJECT_ROOT / "data" / "pulse" / "raw"
    if not raw_dir.exists():
        print("No raw intake files found")
        return
    
    # Get most recent intake file
    intake_files = sorted(raw_dir.glob("intake_*.json"))
    if not intake_files:
        print("No intake files to process")
        return
    
    latest_intake = intake_files[-1]
    print(f"Processing: {latest_intake.name}")
    
    with open(latest_intake) as f:
        raw_items = json.load(f)
    
    print(f"Found {len(raw_items)} items to extract")
    
    extracted_items = []
    
    for i, item in enumerate(raw_items):
        print(f"  [{i+1}/{len(raw_items)}] Extracting: {item['title'][:50]}...")
        
        metadata = extract_metadata_from_url(
            url=item["link"],
            title=item["title"],
            snippet=item.get("snippet", ""),
            client=client
        )
        
        if metadata:
            # Combine raw item with extracted metadata
            extracted_item = {
                **item,
                **metadata,
                "extracted_at": datetime.now().isoformat()
            }
            extracted_items.append(extracted_item)
            print(f"    ✓ Confidence: {metadata.get('confidence')}, Type: {metadata.get('artifact_type')}")
        else:
            print(f"    ✗ Failed to extract")
    
    # Save extracted items
    if extracted_items:
        extracted_dir = PROJECT_ROOT / "data" / "pulse" / "extracted"
        extracted_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = extracted_dir / f"extracted_{timestamp}.json"
        
        with open(output_file, "w") as f:
            json.dump(extracted_items, f, indent=2)
        
        print(f"\nSaved {len(extracted_items)} extracted items to {output_file}")
    else:
        print("\nNo items extracted")

if __name__ == "__main__":
    run_extract()
