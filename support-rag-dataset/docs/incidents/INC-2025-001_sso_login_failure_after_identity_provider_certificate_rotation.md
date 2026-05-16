---
doc_id: INC-2025-001
doc_type: incident_report
incident_id: INC-2025-001
product: CloudDesk CRM
module: Authentication
title: "Incident: SSO login failure after identity provider certificate rotation"
severity: sev2
started_at: 2025-03-08T09:20:00Z
resolved_at: 2025-03-08T12:05:00Z
tags: ["authentication", "incident", "ki-001"]
related_ids: ["KI-001"]
---

# Incident INC-2025-001: SSO login failure after identity provider certificate rotation

## Summary
Multiple customers reported symptoms related to sso login failure after identity provider certificate rotation.

## Impact
- Affected module: Authentication
- Affected versions: 3.1.0-3.1.4
- Customer impact varied by tier and region
- No permanent data loss was confirmed

## Root Cause
The identity provider signing certificate was rotated, but CloudDesk still had the previous certificate cached.

## Mitigation
Temporarily enable password login for affected users if allowed by the customer's security policy.

## Resolution
Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.

## Follow-up Actions
- Improve monitoring for this issue pattern.
- Add an internal alert when repeated symptoms are detected.
- Update support training material for this module.
- Confirm all affected customers upgrade to version 3.1.5.

## Related Known Issue
- KI-001
