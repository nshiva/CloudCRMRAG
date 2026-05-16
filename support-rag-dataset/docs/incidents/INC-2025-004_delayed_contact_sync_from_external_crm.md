---
doc_id: INC-2025-004
doc_type: incident_report
incident_id: INC-2025-004
product: CloudDesk CRM
module: Data Sync
title: "Incident: Delayed contact sync from external CRM"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["data sync", "incident", "ki-004"]
related_ids: ["KI-004"]
---

# Incident INC-2025-004: Delayed contact sync from external CRM

## Summary
Multiple customers reported symptoms related to delayed contact sync from external crm.

## Impact
- Affected module: Data Sync
- Affected versions: 4.2.0-4.2.2
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
The incremental sync cursor stalled when the external CRM returned partial pagination results.

## Mitigation
Run a manual full sync for the affected workspace during off-peak hours.

## Resolution
Reset the workspace sync cursor and restart incremental sync.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 4.2.3.

## Related Known Issue
- KI-004
