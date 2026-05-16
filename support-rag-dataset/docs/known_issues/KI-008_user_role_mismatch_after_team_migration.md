---
doc_id: KI-008
doc_type: known_issue
product: CloudDesk CRM
module: Permissions
title: "User role mismatch after team migration"
status: fixed
affected_versions: "3.5.0-3.5.3"
fixed_version: "3.5.4"
last_updated: 2025-03-06
tags: ["permissions", "known-issue", "perm-mismatch-008"]
related_ids: []
---

# Known Issue KI-008: User role mismatch after team migration

## Summary
User role mismatch after team migration affects CloudDesk CRM customers running versions 3.5.0-3.5.3.

## Affected Versions
- 3.5.0-3.5.3

## Fixed Version
- 3.5.4

## Common Symptoms
- User cannot access expected team records
- Admin role appears as agent role
- Permissions differ after team migration
- User sees access denied for shared dashboards

## Root Cause
Team migration copied workspace membership but did not recalculate inherited role grants.

## Workaround
Manually assign the affected user to the required role until recalculation completes.

## Permanent Resolution
Recalculate inherited permissions for the affected team and confirm role mapping.

## Escalation Guidance
Escalate to Identity Platform if permission recalculation fails.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
