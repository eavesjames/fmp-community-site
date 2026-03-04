---
title: "Liquid Cooling for High-Density Data Center Racks: Power and Thermal Constraints"
date: 2025-01-13
lastmod: 2026-03-03
description: "EdgeConneX CMO explains liquid cooling necessity as rack densities grow from 8.4kW to 40+kW, exceeding air cooling limits and driving infrastructure redesign."
summary: "Phillip Marangella of EdgeConneX discusses the shift from air to liquid cooling driven by rapid rack density increases. The article cites Uptime Institute data showing average densities rose from 2.4kW (2011) to 8.4kW (2020), with current GPU racks exceeding 40kW and air cooling maxing out at 25-40kW with containment solutions."

type: "pulse"
artifact_type: "other"

source_url: "https://www.datacenterfrontier.com/sponsored/article/55252826/breaking-barriers-in-rack-density-why-liquid-cooling-is-the-key-to-tomorrows-data-centers"
source_name: "Data Center Frontier"
source_date: 2025-01-13
vertical: "data-centers"
persona: "facilities"
so_what: "Rack densities jumping from 8.4kW avg to 40+kW for GPU workloads force cooling infrastructure changes that directly impact power distribution design."

players: ["other"]
topics: ["power-quality-surge", "reliability-uptime", "ai-infrastructure"]
value_levers: []

canonical_source: "https://www.datacenterfrontier.com/sponsored/article/55252826/breaking-barriers-in-rack-density-why-liquid-cooling-is-the-key-to-tomorrows-data-centers"
sources:
  - "https://www.datacenterfrontier.com/sponsored/article/55252826/breaking-barriers-in-rack-density-why-liquid-cooling-is-the-key-to-tomorrows-data-centers"

confidence: "medium"
---
## What it is

Phillip Marangella of EdgeConneX discusses the shift from air to liquid cooling driven by rapid rack density increases. The article cites Uptime Institute data showing average densities rose from 2.4kW (2011) to 8.4kW (2020), with current GPU racks exceeding 40kW and air cooling maxing out at 25-40kW with containment solutions.

## Why it matters

Facilities managers and owner-operators face a step-change in power distribution constraints as GPU-driven AI workloads push rack densities beyond air cooling's 25-40kW ceiling. This forces simultaneous redesign of cooling infrastructure, electrical distribution, and UPS/backup systems to handle 40+kW per rack densities that were rare (5% of sites) just five years ago.

**Evidence from source:**

- Average rack density increased from 2.4kW (2011) to 8.4kW (2020), a 3.5x increase; in 2020, 17% reported >20kW/rack and 5% reported >40kW/rack
- Air cooling with hot/cold aisle containment can reach 25-40kW, but current GPU racks require >40kW and need rear-door heat exchangers even for air-cooled variants
- Article explicitly states GPU rack power requirements are 'not just a step forward—they're a massive leap' beyond what air cooling infrastructure can handle

## Links

- **Canonical source**: [https://www.datacenterfrontier.com/sponsored/article/55252826/breaking-barriers-in-rack-density-why-liquid-cooling-is-the-key-to-tomorrows-data-centers](https://www.datacenterfrontier.com/sponsored/article/55252826/breaking-barriers-in-rack-density-why-liquid-cooling-is-the-key-to-tomorrows-data-centers)
- **Player**: /players/other/
- **Topic**: /topics/power-quality-surge/
- **Topic**: /topics/reliability-uptime/

## Open questions

- How do liquid cooling infrastructure requirements alter feeder sizing, panel placement, and hot-aisle containment strategies compared to 25kW air-cooled designs?
- What are the UPS runtime and redundancy implications when rack densities double from typical air-cooled levels to 40+kW GPU configurations?
