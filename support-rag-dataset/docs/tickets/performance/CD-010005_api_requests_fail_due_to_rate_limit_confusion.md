---
doc_id: CD-010005
doc_type: support_ticket
ticket_id: CD-010005
product: CloudDesk CRM
module: Performance
title: "API requests fail due to rate limit confusion - customer case 5"
customer: "NovaCloud Services"
customer_tier: enterprise
region: APAC
status: resolved
severity: high
created_at: 2024-12-11
resolved_at: 2024-12-11
tags: ["performance", "resolved", "ki-010"]
related_ids: ["KI-010", "TG-API-RATE-010"]
---

# Ticket CD-010005: API requests fail due to rate limit confusion

## Customer
NovaCloud Services

## Customer Message
This started today and appears related to api requests fail due to rate limit confusion.

Additional customer context:
- Customer tier: enterprise
- Region: APAC
- Reported module: Performance

## Symptoms Observed
- Customer says API is down
- Bulk import fails midway
- Retry logic causes additional throttling

## Investigation
- Support confirmed the issue belongs to the Performance module.
- The reported behavior matched known issue KI-010.
- The customer was running an affected version range: 8.0.0-8.0.1.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
Customers exceeded the per-minute workspace API limit, and retry logic did not respect Retry-After headers.

## Resolution Applied
Update integration retry logic to honor Retry-After headers and reduce batch size.

## Workaround Shared
Temporarily lower request concurrency and schedule bulk imports during off-peak hours.

## Final Customer Response
We reviewed the issue and confirmed it matches a known performance behavior. 
The recommended resolution has been applied: Update integration retry logic to honor Retry-After headers and reduce batch size.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 8.0.2.
