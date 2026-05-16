---
doc_id: CD-007001
doc_type: support_ticket
ticket_id: CD-007001
product: CloudDesk CRM
module: Integrations
title: "Slack integration stops posting ticket updates - customer case 1"
customer: "NovaCloud Services"
customer_tier: enterprise
region: APAC
status: resolved
severity: medium
created_at: 2024-12-10
resolved_at: 2024-12-10
tags: ["integrations", "resolved", "ki-007"]
related_ids: ["KI-007", "TG-SLACK-INT-007"]
---

# Ticket CD-007001: Slack integration stops posting ticket updates

## Customer
NovaCloud Services

## Customer Message
Can you check why slack notifications are not posted for our workspace?

Additional customer context:
- Customer tier: enterprise
- Region: APAC
- Reported module: Integrations

## Symptoms Observed
- Slack notifications are not posted
- Customer receives authorization revoked error
- Ticket updates no longer appear in channel

## Investigation
- Support confirmed the issue belongs to the Integrations module.
- The reported behavior matched known issue KI-007.
- The customer was running an affected version range: 5.2.0-5.2.5.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
Slack OAuth tokens were revoked after workspace permission changes, but CloudDesk did not prompt reauthorization.

## Resolution Applied
Ask the customer admin to reconnect Slack integration and reselect the target channels.

## Workaround Shared
Use email notifications until Slack integration is reauthorized.

## Final Customer Response
We reviewed the issue and confirmed it matches a known integrations behavior. 
The recommended resolution has been applied: Ask the customer admin to reconnect Slack integration and reselect the target channels.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 5.2.6.
