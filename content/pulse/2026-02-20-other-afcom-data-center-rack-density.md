---
title: "AFCOM: Data Center Rack Density Climbs to 27 kW, AI Pushing Toward 600 kW"
date: 2026-02-20
lastmod: 2026-02-26
description: "AFCOM State of the Data Center report shows average rack density jumped 69% YoY to 27 kW; AI workloads driving roadmaps toward 600 kW racks, requiring energy backbone redesign."
summary: "AFCOM's 10th anniversary State of the Data Center report documents average rack density reaching 27 kW per rack (69% YoY increase from 16 kW), driven by AI workloads. The article traces density evolution from 1 kW (1988) to today's AI-capable systems, with NVIDIA roadmaps projecting 600 kW per rack for upcoming platforms like Rubin Ultra NVL576."

type: "pulse"
artifact_type: "other"

source_url: "https://afcom.com/news/720658/"
source_name: "AFCOM"
source_date: 2026-02-20
vertical: "data-centers"
persona: "facilities"
so_what: "27 kW average (up from 16 kW) and 600 kW AI racks force complete redesign of power distribution, thermal, and energy infrastructure—not incremental tuning."

players: ["other"]
topics: ["ai-infrastructure", "reliability-uptime", "power-quality-surge", "commissioning"]
value_levers: []

canonical_source: "https://afcom.com/news/720658/"
sources:
  - "https://afcom.com/news/720658/"

confidence: "high"
---
## What it is

AFCOM's 10th anniversary State of the Data Center report documents average rack density reaching 27 kW per rack (69% YoY increase from 16 kW), driven by AI workloads. The article traces density evolution from 1 kW (1988) to today's AI-capable systems, with NVIDIA roadmaps projecting 600 kW per rack for upcoming platforms like Rubin Ultra NVL576.

## Why it matters

Facilities managers face a power distribution constraint shift from incremental scaling to backbone redesign: a single NVIDIA DGX H100 draws 10+ kW, and upcoming rack-scale systems approach 600 kW. This affects power delivery design, cooling capacity, and whether existing infrastructure can support AI deployment without campus-level power producer roles. The 74% planning AI-capable infrastructure must decide now if their distribution gear, thermal systems, and service capacity can handle 10x–20x density jumps.

**Evidence from source:**

- Average rack density reached 27 kW per rack, up 69% YoY from 16 kW and up from 6.1 kW in earliest study edition.
- Single NVIDIA DGX H100 system can draw 10 kW or more at node level; NVIDIA Rubin Ultra NVL576 rack expected to approach 600 kW threshold.
- 74% of respondents plan to deploy AI-capable infrastructure; 72% expect AI workloads to significantly increase capacity requirements.

## Links

- **Canonical source**: [https://afcom.com/news/720658/](https://afcom.com/news/720658/)
- **Player**: /players/other/
- **Topic**: /topics/ai-infrastructure/
- **Topic**: /topics/reliability-uptime/

## Open questions

- What specific power distribution architecture changes (busway, direct feed, modular UPS) are operators selecting for 100+ kW and 600 kW rack targets?
- How are commissioning and monitoring strategies adapting to detect thermal or power faults at these densities before catastrophic failure?
