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

    excerpt = page_content or "(not available — use SERP title and snippet only)"

    prompt = f"""You are the Stage-2 Evaluation agent for faultmanagedpower.org.

Context: The pipeline fetches ONLY the first ~3,000 characters of a page. Stage 3 will DROP items with confidence="low". Your output must be conservative, grounded, and high-signal.

GOAL
Identify items relevant to the FMP community OR meaningfully adjacent via power distribution constraints in one of three verticals:
1) Edge Infrastructure Power & UPS
2) Data Centers
3) Building Electrification / Decarbonization

INPUTS

SERP:
title: {title}
snippet: {snippet}
url: {url}

PAGE_EXCERPT (first ~3,000 chars):
{excerpt}

TITLE RULES
- LinkedIn posts: "LinkedIn post by [Author] discussing [main topic]"
- All others: clear descriptive title, <=100 chars, no hashtags or social artifacts

FMP RELEVANCE RUBRIC
- HIGH: Clearly concerns power distribution constraints, safety/compliance, monitoring, commissioning, UPS/resilience, pathways/install bottlenecks, or a concrete deployment/case study in one vertical. Standards/code updates qualify as HIGH if clearly relevant.
- MEDIUM: Adjacent but constraint-rich (e.g., data center power density affecting distribution choices; MDU retrofit bottlenecks like risers/panels; edge deployments constrained by UPS/runtime/monitoring). Must contain at least one concrete detail.
- LOW: Generic trend piece, pure marketing, device-only announcement, or insufficient detail in excerpt to justify relevance.

HARD REJECT CONDITIONS — set confidence="low" if ANY apply:
- Excerpt is mostly marketing claims with no constraints, tradeoffs, or details.
- You cannot extract at least ONE concrete detail (named standard, number, constraint, failure mode, timeline, specific project context).
- Not meaningfully about power distribution / reliability / code / install constraints.

EVIDENCE REQUIREMENT
Provide 1–3 short bullets quoting or paraphrasing concrete details from the excerpt. If you have zero evidence bullets, confidence MUST be "low".

SO_WHAT REQUIREMENT (<=160 chars)
One sentence explaining why this matters for FMP via at least one lever:
install/pathways, labor/schedule, safety model, monitoring/telemetry, commissioning/maintenance, UPS/resilience, code/AHJ friction, retrofit disruption, scaling/power density.

WHY_IT_MATTERS (2–3 sentences max, grounded in the excerpt)
State: the constraint or change, who it impacts (persona), and what decision it affects (design/install/ops/approval).

OPEN_QUESTIONS
1–2 short questions a practitioner could pursue after reading.

PLAYERS
Use ONLY if clearly mentioned in the excerpt. Keys: voltserver, panduit, cisco, fmp-alliance, cence-power, sinclair-digital, southwire, belden, commscope, other.

CALIBRATION EXAMPLES

HIGH (standards/code): Excerpt mentions NEC/NFPA/UL/CSA, specific article/standard, and what changed. Evidence includes the named standard and a concrete change.
HIGH (case study): Excerpt includes project context (facility type, scope, numbers, constraints). Evidence includes at least one number or explicit constraint.
MEDIUM (adjacent): "interconnect delays forcing phased builds," "power density increasing," "panel/service upgrades delaying retrofits," "UPS runtime burden." Evidence: at least one explicit constraint or named mechanism.
LOW (reject): Mostly brand promises ("revolutionary," "best-in-class") with no details. Evidence would be empty or generic.

OUTPUT — respond ONLY with valid JSON, no markdown, no extra text:
{{
  "title": "clear descriptive title <=100 chars",
  "artifact_type": "press|product|standard|case-study|event|doc|linkedin-post|other",
  "publish_date": "YYYY-MM-DD or null",
  "description": "150-170 char meta description",
  "source_name": "short publication or outlet name",
  "source_date": "YYYY-MM-DD or null",
  "confidence": "high|medium|low",
  "vertical": "edge-power-ups|data-centers|building-electrification",
  "persona": "owner-operator|facilities|it-network|security-integrator|ot-controls|gc-mep|electrical-contractor",
  "topics": ["1-6 from: safety-model, code-standards, pathways-install, estimating, schedule-value, monitoring-telemetry, ups-resilience, ot-controls-plc, physical-security, power-quality-surge, dc-distribution, commissioning, reliability-uptime, prefab-modular, labor-productivity, ai-infrastructure, incentives-policy, retrofits-mdus"],
  "players": [],
  "so_what": "<=160 chars",
  "summary": "2-3 sentence overview of what the content is",
  "why_it_matters": "2-3 sentences grounded in excerpt: constraint, persona impact, decision affected",
  "open_questions": ["question 1", "question 2"],
  "evidence": ["concrete detail from excerpt", "concrete detail from excerpt"]
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
