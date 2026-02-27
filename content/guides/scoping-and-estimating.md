---
title: "Scoping and Estimating an FMP Project"
description: "Key cost and schedule drivers for FMP installations: endpoint count, transmitter capacity, riser access, and AHJ familiarity."
summary: "FMP project cost is driven by endpoint count and riser access — not by conduit or service upgrades. Here's how to scope and estimate."
slug: scoping-and-estimating
type: guides
weight: 50
---

## Primary cost drivers

| Driver | Why it matters |
|---|---|
| Endpoint count | Each load (heat pump unit, rack, cabinet) needs a receiver — this is the primary material cost line |
| Transmitter model | One transmitter serves one or multiple zones; capacity determines the model and its cost |
| Cable routing distance | Longer runs affect transmitter sizing; standard runs under 300 ft are routine |
| Riser access | Abandoned risers reduce labor significantly; no risers means surface-mount or new pathway cost |
| AHJ familiarity | First-time Class 4 permit in a jurisdiction adds 2–4 weeks; repeat installs move faster |

## What FMP eliminates from the cost model

Traditional electrical retrofits include line items that FMP projects do not:

- **Panel upgrade**: $5,000–$15,000 per building or tier
- **Service upgrade**: $10,000–$30,000 (utility coordination + switchgear)
- **Conduit material and labor**: significant in pre-1973 buildings with no available pathways
- **Permit delays from utility queue**: 6–18 months in many markets

FMP eliminates the service upgrade — typically the largest cost and longest schedule item in a retrofit.

## Transmitter sizing (rough rules)

- 1 residential heat pump unit ≈ 5–12 kW load at nameplate
- 1 data center rack at AI density ≈ 27 kW average (AFCOM 2025)
- A single transmitter serves multiple endpoints depending on model capacity and total load
- Check the OEM datasheet for max load and max cable run per transmitter

## Pre-bid checklist

Before pricing an FMP scope:

1. **Riser survey**: which pathways are available and clear? Any with fire-stop penetrations that need rework?
2. **Panel location**: transmitter connects to an existing panel; distance matters for labor
3. **Load schedule**: connected devices and nameplate kW for each endpoint
4. **AHJ research**: has this jurisdiction permitted a Class 4 install before? Which NEC edition?
5. **Code edition**: are they on 2020, 2023, or 2026 NEC? Affects permit document language — see [Article 726 guide](/guides/nec-class-4-article-726/)

## More detail

- [How FMP Is Installed](/guides/how-fmp-is-installed/) — installation steps and commissioning
- [Where FMP Fits](/guides/where-fmp-fits/) — verticals and use case context
