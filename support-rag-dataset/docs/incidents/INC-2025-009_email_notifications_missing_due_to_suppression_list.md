---
doc_id: INC-2025-009
doc_type: incident_report
incident_id: INC-2025-009
product: CloudDesk CRM
module: Notifications
title: "Incident: Email notifications missing due to suppression list"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["notifications", "incident", "ki-009"]
related_ids: ["KI-009"]
---

# Incident INC-2025-009: Email notifications missing due to suppression list

## Summary
Multiple customers reported symptoms related to email notifications missing due to suppression list.

## Impact
- Affected module: Notifications
- Affected versions: 7.0.0-7.0.2
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
Recipients were added to the suppression list after repeated soft bounces from their mail server.

## Mitigation
Ask customer IT to allowlist CloudDesk notification domains.

## Resolution
Remove the verified recipient from suppression list and send a test notification.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 7.0.3.

## Related Known Issue
- KI-009
