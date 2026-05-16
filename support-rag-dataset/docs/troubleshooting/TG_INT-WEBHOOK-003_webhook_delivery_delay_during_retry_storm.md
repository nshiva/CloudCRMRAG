---
doc_id: TG-INT-WEBHOOK-003
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Integrations
title: "Troubleshooting: Webhook delivery delay during retry storm"
version: 1.0
last_updated: 2025-04-21
severity_default: medium
tags: ["integrations", "troubleshooting", "int-webhook-003"]
related_ids: ["KI-003"]
---

# Troubleshooting: Webhook delivery delay during retry storm

## When to Use This Guide
Use this guide when a customer reports symptoms related to webhook delivery delay during retry storm.

## Symptoms
- Webhook events arrive late
- Customer reports missing webhook callbacks
- Webhook retry queue grows rapidly
- Third-party integration receives duplicate retries

## Initial Checks
1. Confirm the customer is using an affected version: 5.0.0-5.0.3.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 5.0.4.

## Recommended Resolution
Increase retry backoff and drain the webhook queue for the affected workspace.

## Workaround
Ask the customer to temporarily reduce webhook subscription volume or disable non-critical endpoints.

## When to Escalate
Escalate to Integrations Engineering if queue depth exceeds 50,000 events.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
