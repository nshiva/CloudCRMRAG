---
doc_id: CD-005004
doc_type: support_ticket
ticket_id: CD-005004
product: CloudDesk CRM
module: Reporting
title: "Dashboard revenue numbers mismatch exported report - customer case 4"
customer: "BrightPath Health"
customer_tier: growth
region: US
status: resolved
severity: low
created_at: 2025-04-30
resolved_at: 2025-04-30
tags: ["reporting", "resolved", "ki-005"]
related_ids: ["KI-005", "TG-REP-MISMATCH-005"]
---

# Ticket CD-005004: Dashboard revenue numbers mismatch exported report

## Customer
BrightPath Health

## Customer Message
This started today and appears related to dashboard revenue numbers mismatch exported report.

Additional customer context:
- Customer tier: growth
- Region: US
- Reported module: Reporting

## Symptoms Observed
- Report filters appear to be ignored
- Customer reports incorrect monthly revenue
- Saved dashboard and exported report show different totals

## Investigation
- Support confirmed the issue belongs to the Reporting module.
- The reported behavior matched known issue KI-005.
- The customer was running an affected version range: 6.3.0-6.3.1.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
Dashboard cache used UTC date boundaries while CSV export used workspace-local timezone boundaries.

## Resolution Applied
Refresh dashboard cache after applying workspace-local timezone calculation.

## Workaround Shared
Use CSV export as the source of truth until dashboard cache refresh completes.

## Final Customer Response
We reviewed the issue and confirmed it matches a known reporting behavior. 
The recommended resolution has been applied: Refresh dashboard cache after applying workspace-local timezone calculation.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 6.3.2.
