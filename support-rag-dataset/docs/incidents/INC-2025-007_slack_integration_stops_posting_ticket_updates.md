---
doc_id: INC-2025-007
doc_type: incident_report
incident_id: INC-2025-007
product: CloudDesk CRM
module: Integrations
title: "Incident: Slack integration stops posting ticket updates"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["integrations", "incident", "ki-007"]
related_ids: ["KI-007"]
---

# Incident INC-2025-007: Slack integration stops posting ticket updates

## Summary
Multiple customers reported symptoms related to slack integration stops posting ticket updates.

## Impact
- Affected module: Integrations
- Affected versions: 5.2.0-5.2.5
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
Slack OAuth tokens were revoked after workspace permission changes, but CloudDesk did not prompt reauthorization.

## Mitigation
Use email notifications until Slack integration is reauthorized.

## Resolution
Ask the customer admin to reconnect Slack integration and reselect the target channels.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 5.2.6.

## Related Known Issue
- KI-007
