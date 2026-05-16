---
doc_id: KI-007
doc_type: known_issue
product: CloudDesk CRM
module: Integrations
title: "Slack integration stops posting ticket updates"
status: fixed
affected_versions: "5.2.0-5.2.5"
fixed_version: "5.2.6"
last_updated: 2025-03-30
tags: ["integrations", "known-issue", "slack-int-007"]
related_ids: []
---

# Known Issue KI-007: Slack integration stops posting ticket updates

## Summary
Slack integration stops posting ticket updates affects CloudDesk CRM customers running versions 5.2.0-5.2.5.

## Affected Versions
- 5.2.0-5.2.5

## Fixed Version
- 5.2.6

## Common Symptoms
- Slack notifications are not posted
- Ticket updates no longer appear in channel
- Slack integration shows connected but inactive
- Customer receives authorization revoked error

## Root Cause
Slack OAuth tokens were revoked after workspace permission changes, but CloudDesk did not prompt reauthorization.

## Workaround
Use email notifications until Slack integration is reauthorized.

## Permanent Resolution
Ask the customer admin to reconnect Slack integration and reselect the target channels.

## Escalation Guidance
Escalate to Integrations Support if reconnect flow fails.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
