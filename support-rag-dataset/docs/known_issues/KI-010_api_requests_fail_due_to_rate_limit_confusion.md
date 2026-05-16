---
doc_id: KI-010
doc_type: known_issue
product: CloudDesk CRM
module: Performance
title: "API requests fail due to rate limit confusion"
status: fixed
affected_versions: "8.0.0-8.0.1"
fixed_version: "8.0.2"
last_updated: 2025-02-24
tags: ["performance", "known-issue", "api-rate-010"]
related_ids: []
---

# Known Issue KI-010: API requests fail due to rate limit confusion

## Summary
API requests fail due to rate limit confusion affects CloudDesk CRM customers running versions 8.0.0-8.0.1.

## Affected Versions
- 8.0.0-8.0.1

## Fixed Version
- 8.0.2

## Common Symptoms
- API returns 429 errors
- Customer says API is down
- Bulk import fails midway
- Retry logic causes additional throttling

## Root Cause
Customers exceeded the per-minute workspace API limit, and retry logic did not respect Retry-After headers.

## Workaround
Temporarily lower request concurrency and schedule bulk imports during off-peak hours.

## Permanent Resolution
Update integration retry logic to honor Retry-After headers and reduce batch size.

## Escalation Guidance
Escalate to API Platform only if 429 errors occur below documented rate limits.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
