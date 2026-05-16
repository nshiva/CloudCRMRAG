---
doc_id: TG-PERM-MISMATCH-008
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Permissions
title: "Troubleshooting: User role mismatch after team migration"
version: 1.0
last_updated: 2025-04-22
severity_default: medium
tags: ["permissions", "troubleshooting", "perm-mismatch-008"]
related_ids: ["KI-008"]
---

# Troubleshooting: User role mismatch after team migration

## When to Use This Guide
Use this guide when a customer reports symptoms related to user role mismatch after team migration.

## Symptoms
- User cannot access expected team records
- Admin role appears as agent role
- Permissions differ after team migration
- User sees access denied for shared dashboards

## Initial Checks
1. Confirm the customer is using an affected version: 3.5.0-3.5.3.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 3.5.4.

## Recommended Resolution
Recalculate inherited permissions for the affected team and confirm role mapping.

## Workaround
Manually assign the affected user to the required role until recalculation completes.

## When to Escalate
Escalate to Identity Platform if permission recalculation fails.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
