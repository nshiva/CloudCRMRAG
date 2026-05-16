---
doc_id: TG-API-RATE-010
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Performance
title: "Troubleshooting: API requests fail due to rate limit confusion"
version: 1.0
last_updated: 2025-03-31
severity_default: medium
tags: ["performance", "troubleshooting", "api-rate-010"]
related_ids: ["KI-010"]
---

# Troubleshooting: API requests fail due to rate limit confusion

## When to Use This Guide
Use this guide when a customer reports symptoms related to api requests fail due to rate limit confusion.

## Symptoms
- API returns 429 errors
- Customer says API is down
- Bulk import fails midway
- Retry logic causes additional throttling

## Initial Checks
1. Confirm the customer is using an affected version: 8.0.0-8.0.1.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 8.0.2.

## Recommended Resolution
Update integration retry logic to honor Retry-After headers and reduce batch size.

## Workaround
Temporarily lower request concurrency and schedule bulk imports during off-peak hours.

## When to Escalate
Escalate to API Platform only if 429 errors occur below documented rate limits.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
