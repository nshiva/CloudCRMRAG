---
doc_id: KI-001
doc_type: known_issue
product: CloudDesk CRM
module: Authentication
title: "SSO login failure after identity provider certificate rotation"
status: fixed
affected_versions: "3.1.0-3.1.4"
fixed_version: "3.1.5"
last_updated: 2025-02-08
tags: ["authentication", "known-issue", "auth-sso-001"]
related_ids: []
---

# Known Issue KI-001: SSO login failure after identity provider certificate rotation

## Summary
SSO login failure after identity provider certificate rotation affects CloudDesk CRM customers running versions 3.1.0-3.1.4.

## Affected Versions
- 3.1.0-3.1.4

## Fixed Version
- 3.1.5

## Common Symptoms
- Invalid SAML response error
- Users redirected back to login page
- SSO login fails while password login works
- Only users from one identity provider are affected

## Root Cause
The identity provider signing certificate was rotated, but CloudDesk still had the previous certificate cached.

## Workaround
Temporarily enable password login for affected users if allowed by the customer's security policy.

## Permanent Resolution
Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.

## Escalation Guidance
Escalate to Security Engineering if SAML response validation fails after certificate refresh.

## Support Notes
When responding to customers, explain the symptom in plain language and include the workaround only when it is safe for the customer's tier and region.
