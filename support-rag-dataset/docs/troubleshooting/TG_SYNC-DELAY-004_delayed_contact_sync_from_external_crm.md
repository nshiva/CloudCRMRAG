---
doc_id: TG-SYNC-DELAY-004
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Data Sync
title: "Troubleshooting: Delayed contact sync from external CRM"
version: 1.0
last_updated: 2025-03-19
severity_default: medium
tags: ["data sync", "troubleshooting", "sync-delay-004"]
related_ids: ["KI-004"]
---

# Troubleshooting: Delayed contact sync from external CRM

## When to Use This Guide
Use this guide when a customer reports symptoms related to delayed contact sync from external crm.

## Symptoms
- Contacts appear several hours late
- Customer sees stale contact records
- Sync status remains in pending state
- External CRM updates do not immediately appear

## Initial Checks
1. Confirm the customer is using an affected version: 4.2.0-4.2.2.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 4.2.3.

## Recommended Resolution
Reset the workspace sync cursor and restart incremental sync.

## Workaround
Run a manual full sync for the affected workspace during off-peak hours.

## When to Escalate
Escalate to Data Platform if full sync fails or duplicate records are created.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
