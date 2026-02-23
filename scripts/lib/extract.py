"""Extract and enrich metadata from raw intake using Claude"""
import os
import json
from pathlib import Path
from datetime import datetime
import anthropic
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

PROJECT_ROOT = Path(__file__).parent.parent.parent

# Load environment variables from .env file
load_dotenv(PROJECT_ROOT / ".env")

def fetch_page_content(url, timeout=10):
    """Fetch and extract text content from a URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # Get text content
        text = soup.get_text(separator='\n', strip=True)

        # Clean up whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        content = '\n'.join(lines)

        # Limit to first 3000 characters for API efficiency
        return content[:3000]
    except Exception as e:
        print(f"    Warning: Could not fetch content ({str(e)}), using snippet only")
        return None

def is_linkedin_post(url):
    """Check if URL is a LinkedIn post"""
    parsed = urlparse(url)
    return 'linkedin.com' in parsed.netloc and '/posts/' in parsed.path

def extract_metadata_from_url(url, title, snippet, client):
    """Use Claude to extract metadata from a URL"""

    # Fetch actual page content
    page_content = fetch_page_content(url)
    is_linkedin = is_linkedin_post(url)

    # Build context for Claude
    context = f"""URL: {url}
Original Title: {title}
Snippet: {snippet}"""

    if page_content:
        context += f"\n\nPage Content:\n{page_content}"

    prompt = f"""{context}

Extract metadata for a Fault Managed Power (FMP) knowledge base.

IMPORTANT TITLE GUIDELINES:
- For LinkedIn posts: Generate a descriptive title like "LinkedIn post by [Author] discussing [main topic]"
- For other content: Use a clear, descriptive title (improve the original if needed)
- Keep titles under 100 characters
- Remove hashtags and social media artifacts

Extract the following information:

1. **title**: A clear, descriptive title (see guidelines above)
2. **artifact_type**: Choose ONE from: press, product, event, case-study, standard, doc, video, linkedin-post, other
3. **publish_date**: Publication date if available (YYYY-MM-DD format), or null
4. **description**: 150-170 character meta description
5. **players**: Array of relevant organizations from: voltserver, panduit, cisco, fmp-alliance, other
6. **topics**: Array from: class-4, safety-model, estimating, schedule-value, space-value, digital-connectivity, smart-buildings, data-centers, retrofits, code-standards, commissioning
7. **value_levers**: Array from: labor, schedule, space, digital-connectivity, risk, feasibility, operations
8. **confidence**: high, medium, or low (how relevant is this to FMP?)
9. **summary**: 2-3 sentence summary explaining what this content is about and its key points

Respond ONLY with valid JSON:
{{
  "title": "...",
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
            # Use Claude's generated title if available, otherwise use original
            extracted_item = {
                **item,
                **metadata,
                "title": metadata.get("title", item["title"]),  # Prefer Claude's title
                "extracted_at": datetime.now().isoformat()
            }
            extracted_items.append(extracted_item)
            print(f"    ✓ Confidence: {metadata.get('confidence')}, Type: {metadata.get('artifact_type')}")
            if metadata.get("title") != item["title"]:
                print(f"    → Improved title: {metadata.get('title')[:60]}...")
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
