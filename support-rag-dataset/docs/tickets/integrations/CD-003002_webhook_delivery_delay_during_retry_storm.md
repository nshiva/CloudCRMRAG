---
doc_id: CD-003002
doc_type: support_ticket
ticket_id: CD-003002
product: CloudDesk CRM
module: Integrations
title: "Webhook delivery delay during retry storm - customer case 2"
customer: "Pioneer Legal"
customer_tier: growth
region: APAC
status: resolved
severity: medium
created_at: 2025-02-14
resolved_at: 2025-02-14
tags: ["integrations", "resolved", "ki-003"]
related_ids: ["KI-003", "TG-INT-WEBHOOK-003"]
---

# Ticket CD-003002: Webhook delivery delay during retry storm

## Customer
Pioneer Legal

## Customer Message
This started today and appears related to webhook delivery delay during retry storm.

Additional customer context:
- Customer tier: growth
- Region: APAC
- Reported module: Integrations

## Symptoms Observed
- Customer reports missing webhook callbacks
- Third-party integration receives duplicate retries
- Webhook events arrive late

## Investigation
- Support confirmed the issue belongs to the Integrations module.
- The reported behavior matched known issue KI-003.
- The customer was running an affected version range: 5.0.0-5.0.3.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
A retry storm occurred after third-party endpoint timeouts caused repeated retries without per-customer backoff.

## Resolution Applied
Increase retry backoff and drain the webhook queue for the affected workspace.

## Workaround Shared
Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.

## Final Customer Response
We reviewed the issue and confirmed it matches a known integrations behavior. 
The recommended resolution has been applied: Increase retry backoff and drain the webhook queue for the affected workspace.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 5.0.4.
