---
doc_id: TG-AUTH-SSO-001
doc_type: troubleshooting_guide
product: CloudDesk CRM
module: Authentication
title: "Troubleshooting: SSO login failure after identity provider certificate rotation"
version: 1.0
last_updated: 2025-04-23
severity_default: medium
tags: ["authentication", "troubleshooting", "auth-sso-001"]
related_ids: ["KI-001"]
---

# Troubleshooting: SSO login failure after identity provider certificate rotation

## When to Use This Guide
Use this guide when a customer reports symptoms related to sso login failure after identity provider certificate rotation.

## Symptoms
- Invalid SAML response error
- Users redirected back to login page
- SSO login fails while password login works
- Only users from one identity provider are affected

## Initial Checks
1. Confirm the customer is using an affected version: 3.1.0-3.1.4.
2. Collect the customer workspace ID, region, and time of first occurrence.
3. Check whether the issue affects one user, one workspace, or multiple customers.
4. Search historical tickets for the same symptoms and module.
5. Apply the documented workaround only if it does not create data loss or security risk.
6. Confirm whether the customer can upgrade to fixed version 3.1.5.

## Recommended Resolution
Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.

## Workaround
Temporarily enable password login for affected users if allowed by the customer's security policy.

## When to Escalate
Escalate to Security Engineering if SAML response validation fails after certificate refresh.

## Customer Communication Guidance
Acknowledge the customer impact, describe the current known behavior, avoid overpromising timelines, and provide the next action clearly.
