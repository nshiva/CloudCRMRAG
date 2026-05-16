---
doc_id: CD-008002
doc_type: support_ticket
ticket_id: CD-008002
product: CloudDesk CRM
module: Permissions
title: "User role mismatch after team migration - customer case 2"
customer: "BrightPath Health"
customer_tier: startup
region: US
status: resolved
severity: medium
created_at: 2025-03-16
resolved_at: 2025-03-16
tags: ["permissions", "resolved", "ki-008"]
related_ids: ["KI-008", "TG-PERM-MISMATCH-008"]
---

# Ticket CD-008002: User role mismatch after team migration

## Customer
BrightPath Health

## Customer Message
Can you check why user cannot access expected team records for our workspace?

Additional customer context:
- Customer tier: startup
- Region: US
- Reported module: Permissions

## Symptoms Observed
- User sees access denied for shared dashboards
- Permissions differ after team migration
- User cannot access expected team records

## Investigation
- Support confirmed the issue belongs to the Permissions module.
- The reported behavior matched known issue KI-008.
- The customer was running an affected version range: 3.5.0-3.5.3.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
Team migration copied workspace membership but did not recalculate inherited role grants.

## Resolution Applied
Recalculate inherited permissions for the affected team and confirm role mapping.

## Workaround Shared
Manually assign the affected user to the required role until recalculation completes.

## Final Customer Response
We reviewed the issue and confirmed it matches a known permissions behavior. 
The recommended resolution has been applied: Recalculate inherited permissions for the affected team and confirm role mapping.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 3.5.4.
