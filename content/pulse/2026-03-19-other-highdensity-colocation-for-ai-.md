---
title: "High-Density Colocation for AI & GPU Infrastructure: Power & Cooling"
date: 2026-03-19
lastmod: 2026-03-28
description: "Analysis of power density evolution from 5-10 kW traditional racks to 40-132 kW AI/GPU racks, thermal challenges, and implications for colocation facility design."
summary: "Netrality examines infrastructure requirements for AI/GPU colocation, documenting the progression from 5-10 kW traditional racks to current 40-80 kW AI deployments and NVIDIA's 132 kW Blackwell systems. Projects 250-600 kW per rack by 2027 with roadmap showing 576 GPUs per enclosure, while industry average remains 5-9 kW."

type: "pulse"
artifact_type: "other"

source_url: "https://netrality.com/blog/high-density-colocation-for-ai-and-gpu-infrastructure-what-it-takes-to-support-the-next-generation-of-computing/"
source_name: "Netrality"
source_date: 2026-03-19
vertical: "data-centers"
persona: "owner-operator"
so_what: "AI rack densities reaching 132 kW today and projected 250-600 kW by 2027 force fundamental data center power distribution redesign beyond traditional models."

players: ["other"]
topics: ["ai-infrastructure", "reliability-uptime", "power-quality-surge", "pathways-install"]
value_levers: []

canonical_source: "https://netrality.com/blog/high-density-colocation-for-ai-and-gpu-infrastructure-what-it-takes-to-support-the-next-generation-of-computing/"
sources:
  - "https://netrality.com/blog/high-density-colocation-for-ai-and-gpu-infrastructure-what-it-takes-to-support-the-next-generation-of-computing/"

confidence: "high"
---
## What it is

Netrality examines infrastructure requirements for AI/GPU colocation, documenting the progression from 5-10 kW traditional racks to current 40-80 kW AI deployments and NVIDIA's 132 kW Blackwell systems. Projects 250-600 kW per rack by 2027 with roadmap showing 576 GPUs per enclosure, while industry average remains 5-9 kW.

## Why it matters

Data center owner-operators face a power density gap where most facilities designed for 5-9 kW racks cannot support AI workloads now demanding 40-132 kW per rack, with projections to 600 kW by 2027. This drives fundamental redesign of electrical distribution, thermal management, and capacity planning for any facility pursuing AI tenants or workloads.

**Evidence from source:**

- NVIDIA Blackwell GB200NVL72 rack requires ~132 kW; roadmap shows 250-600 kW per rack by 2027 with up to 576 GPUs per enclosure
- Traditional racks: 5-10 kW. AI racks: 40-80 kW routine, approaching 100 kW. Uptime Institute survey shows industry average remains 5-9 kW over past 5 years
- Single AI server with eight 1,200W+ accelerators consumes ~10 kW just for GPUs before CPUs, memory, storage; ten servers = ~100 kW per rack

## Links

- **Canonical source**: [https://netrality.com/blog/high-density-colocation-for-ai-and-gpu-infrastructure-what-it-takes-to-support-the-next-generation-of-computing/](https://netrality.com/blog/high-density-colocation-for-ai-and-gpu-infrastructure-what-it-takes-to-support-the-next-generation-of-computing/)
- **Player**: /players/other/
- **Topic**: /topics/ai-infrastructure/
- **Topic**: /topics/reliability-uptime/

## Open questions

- What electrical distribution architectures (busway, PDU topology, breaker sizing) are capable facilities deploying to support 100+ kW racks today and scale to 600 kW?
- How do hyperscalers at 36 kW average rack density manage the mix of traditional and high-density loads on shared infrastructure?
