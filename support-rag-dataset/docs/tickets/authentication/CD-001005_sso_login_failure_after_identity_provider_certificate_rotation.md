---
doc_id: CD-001005
doc_type: support_ticket
ticket_id: CD-001005
product: CloudDesk CRM
module: Authentication
title: "SSO login failure after identity provider certificate rotation - customer case 5"
customer: "Pioneer Legal"
customer_tier: startup
region: EU
status: resolved
severity: low
created_at: 2025-01-28
resolved_at: 2025-01-28
tags: ["authentication", "resolved", "ki-001"]
related_ids: ["KI-001", "TG-AUTH-SSO-001"]
---

# Ticket CD-001005: SSO login failure after identity provider certificate rotation

## Customer
Pioneer Legal

## Customer Message
Our team says sso login fails while password login works and it is blocking daily work.

Additional customer context:
- Customer tier: startup
- Region: EU
- Reported module: Authentication

## Symptoms Observed
- Invalid SAML response error
- Only users from one identity provider are affected
- SSO login fails while password login works

## Investigation
- Support confirmed the issue belongs to the Authentication module.
- The reported behavior matched known issue KI-001.
- The customer was running an affected version range: 3.1.0-3.1.4.
- No evidence of permanent data loss was found.
- Support compared the case with previous resolved tickets in the same cluster.

## Root Cause
The identity provider signing certificate was rotated, but CloudDesk still had the previous certificate cached.

## Resolution Applied
Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.

## Workaround Shared
Temporarily enable password login for affected users if allowed by the customer's security policy.

## Final Customer Response
We reviewed the issue and confirmed it matches a known authentication behavior. 
The recommended resolution has been applied: Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.
Please monitor the workspace and contact CloudDesk Support if the symptoms return.

## Internal Notes
If this issue appears again for the same customer, check whether the customer has upgraded to version 3.1.5.
