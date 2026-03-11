---
title: "UPS for Industrial Automation - Xtreme Power Conversion"
date: 2026-03-10
lastmod: 2026-03-10
description: "Product page detailing UPS deployment in industrial control cabinets, PLC systems, and automation racks with specific form factors for edge control infrastructure."
summary: "Xtreme Power Conversion markets online double-conversion UPS systems for industrial automation environments, specifically targeting deployment in control cabinets, shallow racks, and edge control infrastructure. The page details power disturbances common in industrial settings (voltage sags from equipment startup, electrical noise from drives/motors) and maps specific UPS models (J60, J60C, J90, Li90) to deployment environments based on form factor constraints."

type: "pulse"
artifact_type: "product"

source_url: "https://xpcc.com/ups-for-industrial-automation/"
source_name: "Xtreme Power Conversion"
vertical: "edge-power-ups"
persona: "ot-controls"
so_what: "Addresses UPS deployment constraints in industrial control cabinets and shallow racks where PLC reboot time and space limitations drive backup power design."

players: ["other"]
topics: ["ups-resilience", "ot-controls-plc", "power-quality-surge", "pathways-install"]
value_levers: []

canonical_source: "https://xpcc.com/ups-for-industrial-automation/"
sources:
  - "https://xpcc.com/ups-for-industrial-automation/"

confidence: "medium"
---
## What it is

Xtreme Power Conversion markets online double-conversion UPS systems for industrial automation environments, specifically targeting deployment in control cabinets, shallow racks, and edge control infrastructure. The page details power disturbances common in industrial settings (voltage sags from equipment startup, electrical noise from drives/motors) and maps specific UPS models (J60, J60C, J90, Li90) to deployment environments based on form factor constraints.

## Why it matters

OT controls engineers face space and form factor constraints when protecting PLC systems, SCADA infrastructure, and industrial networks inside control cabinets and shallow racks. The excerpt identifies that PLC systems require several minutes to reboot after power loss, creating a resilience requirement that drives UPS sizing and placement decisions in automation cabinets versus larger network racks.

**Evidence from source:**

- Specific deployment mapping: 'PLC control cabinet: J60/J60i; Shallow industrial rack: J60C/J60Ci; Industrial network rack: J90/J90i'
- PLC systems require 'several minutes to reboot after power loss,' creating operational constraint for backup power runtime
- UPS deployed 'directly inside the control cabinet' for automation equipment including PLCs, industrial power supplies, and network switches

## Links

- **Canonical source**: [https://xpcc.com/ups-for-industrial-automation/](https://xpcc.com/ups-for-industrial-automation/)
- **Player**: /players/other/
- **Topic**: /topics/ups-resilience/
- **Topic**: /topics/ot-controls-plc/

## Open questions

- What runtime specifications differentiate the J60/J90/Li90 models for typical PLC cabinet vs. network rack deployments?
- How do industrial electrical noise characteristics (drives, motors) affect UPS filtering requirements versus commercial edge deployments?
