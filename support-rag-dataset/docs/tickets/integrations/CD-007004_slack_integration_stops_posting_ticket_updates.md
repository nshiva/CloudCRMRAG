---
doc_id: CD-007004
doc_type: support_ticket
ticket_id: CD-007004
product: CloudDesk CRM
module: Integrations
title: "Slack integration stops posting ticket updates - customer case 4"
customer: "Atlas Learning"
customer_tier: startup
region: US
status: resolved
severity: medium
created_at: 2025-02-22
resolved_at: 2025-02-22
tags: ["integrations", "resolved", "ki-007"]
related_ids: ["KI-007", "TG-SLACK-INT-007"]
---

# Ticket CD-007004: Slack integration stops posting ticket updates

## Customer
Atlas Learning

## Customer Message
Our team says ticket updates no longer appear in channel and it is blocking daily work.

Additional customer context:
- Customer tier: startup
- Region: US
- Reported module: Integrations

## Symptoms Observed
- Customer receives authorization revoked error
- Slack integration shows connected but inactive
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
