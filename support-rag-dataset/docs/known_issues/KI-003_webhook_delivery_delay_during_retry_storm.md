---
doc_id: KI-003
doc_type: known_issue
product: CloudDesk CRM
module: Integrations
title: "Webhook delivery delay during retry storm"
status: fixed
affected_versions: "5.0.0-5.0.3"
fixed_version: "5.0.4"
last_updated: 2025-04-16
tags: ["integrations", "known-issue", "int-webhook-003"]
related_ids: []
---

# Known Issue KI-003: Webhook delivery delay during retry storm

## Summary
Webhook delivery delay during retry storm affects CloudDesk CRM customers running versions 5.0.0-5.0.3.

## Affected Versions
- 5.0.0-5.0.3

## Fixed Version
- 5.0.4

## Common Symptoms
- Webhook events arrive late
- Customer reports missing webhook callbacks
- Webhook retry queue grows rapidly
- Third-party integration receives duplicate retries

## Root Cause
A retry storm occurred after third-party endpoint timeouts caused repeated retries without per-customer backoff.

## Workaround
Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.

## Permanent Resolution
Increase retry backoff and drain the webhook queue for the affected workspace.

## Escalation Guidance
Escalate to Integrations Engineering if queue depth exceeds 50,000 events.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
