---
doc_id: CD-006005
doc_type: support_ticket
ticket_id: CD-006005
product: CloudDesk CRM
module: Reporting
title: "CSV export fails for large reports - customer case 5"
customer: "UrbanCart"
customer_tier: enterprise
region: US
status: resolved
severity: low
created_at: 2024-12-22
resolved_at: 2024-12-22
tags: ["reporting", "resolved", "ki-006"]
related_ids: ["KI-006", "TG-EXP-CSV-006"]
---

# Ticket CD-006005: CSV export fails for large reports

## Customer
UrbanCart

## Customer Message
Can you check why large report download fails for our workspace?

Additional customer context:
- Customer tier: enterprise
- Region: US
- Reported module: Reporting

## Symptoms Observed
- Large report download fails
- Customer cannot download records above 100,000 rows
- CSV export times out

## Investigation
- Support confirmed the issue belongs to the Reporting module.
- The reported behavior matched known issue KI-006.
- The customer was running an affected version range: 6.1.0-6.1.8.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
The export worker exceeded memory limits when generating large CSV files synchronously.

## Resolution Applied
Retry export using the asynchronous export pipeline.

## Workaround Shared
Ask the customer to reduce the date range or split the export by region.

## Final Customer Response
We reviewed the issue and confirmed it matches a known reporting behavior. 
The recommended resolution has been applied: Retry export using the asynchronous export pipeline.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 6.1.9.
