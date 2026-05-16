---
doc_id: INC-2025-010
doc_type: incident_report
incident_id: INC-2025-010
product: CloudDesk CRM
module: Performance
title: "Incident: API requests fail due to rate limit confusion"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["performance", "incident", "ki-010"]
related_ids: ["KI-010"]
---

# Incident INC-2025-010: API requests fail due to rate limit confusion

## Summary
Multiple customers reported symptoms related to api requests fail due to rate limit confusion.

## Impact
- Affected module: Performance
- Affected versions: 8.0.0-8.0.1
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
Customers exceeded the per-minute workspace API limit, and retry logic did not respect Retry-After headers.

## Mitigation
Temporarily lower request concurrency and schedule bulk imports during off-peak hours.

## Resolution
Update integration retry logic to honor Retry-After headers and reduce batch size.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 8.0.2.

## Related Known Issue
- KI-010
