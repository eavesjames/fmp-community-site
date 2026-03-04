---
title: "AWS Designs In-Rack Micro UPS Units For a More Efficient Cloud"
date: 2020-12-11
lastmod: 2026-03-03
description: "AWS deploys rack-level micro UPS units, eliminating centralized UPS to reduce energy conversion loss by 35% and enable seconds-long battery swaps without downtime."
summary: "Amazon Web Services announced custom rack-level micro UPS units that eliminate centralized UPS systems in their data centers. The distributed architecture reduces energy conversion loss by 35% by simplifying the power path and removing AC/DC conversions. Battery packs can be swapped in seconds without system shutdown, reducing maintenance risk."

type: "pulse"
artifact_type: "press"

source_url: "https://www.datacenterfrontier.com/cloud/article/11428519/aws-designs-in-rack-micro-ups-units-for-a-more-efficient-cloud"
source_name: "Data Center Frontier"
source_date: 2020-12-11
vertical: "data-centers"
persona: "facilities"
so_what: "Distributed UPS architecture eliminates centralized failure domains, reduces maintenance risk, and cuts conversion losses by simplifying AC/DC/voltage steps."

players: ["other"]
topics: ["ups-resilience", "power-quality-surge", "reliability-uptime", "commissioning", "monitoring-telemetry"]
value_levers: []

canonical_source: "https://www.datacenterfrontier.com/cloud/article/11428519/aws-designs-in-rack-micro-ups-units-for-a-more-efficient-cloud"
sources:
  - "https://www.datacenterfrontier.com/cloud/article/11428519/aws-designs-in-rack-micro-ups-units-for-a-more-efficient-cloud"

confidence: "high"
---
## What it is

Amazon Web Services announced custom rack-level micro UPS units that eliminate centralized UPS systems in their data centers. The distributed architecture reduces energy conversion loss by 35% by simplifying the power path and removing AC/DC conversions. Battery packs can be swapped in seconds without system shutdown, reducing maintenance risk.

## Why it matters

Shifting UPS from facility-level to rack-level changes the failure domain from entire data halls to single racks, while eliminating voltage conversion steps that waste power. Facilities managers and data center operators must reconsider maintenance procedures, as battery replacement moves from hours-long facility events to seconds-long hot-swaps. This architecture trade-off impacts design decisions around redundancy topology, power chain efficiency, and risk mitigation for third-party software dependencies.

**Evidence from source:**

- Distributed UPS reduces energy conversion loss by 35 percent by eliminating centralized UPS and simplifying AC/DC conversions and voltage step-downs
- Batteries can be removed and replaced in seconds rather than hours without turning off the system, drastically reducing maintenance risk
- Single UPS failure impacts only servers in a single rack rather than an entire data hall or building

## Links

- **Canonical source**: [https://www.datacenterfrontier.com/cloud/article/11428519/aws-designs-in-rack-micro-ups-units-for-a-more-efficient-cloud](https://www.datacenterfrontier.com/cloud/article/11428519/aws-designs-in-rack-micro-ups-units-for-a-more-efficient-cloud)
- **Player**: /players/other/
- **Topic**: /topics/ups-resilience/
- **Topic**: /topics/power-quality-surge/

## Open questions

- What are the upfront cost and complexity trade-offs of distributed vs. centralized UPS for smaller operators without AWS's custom design capabilities?
- How does rack-level UPS impact commissioning and monitoring protocols compared to centralized battery management systems?
