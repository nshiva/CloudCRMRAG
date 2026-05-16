---
doc_id: CD-001003
doc_type: support_ticket
ticket_id: CD-001003
product: CloudDesk CRM
module: Authentication
title: "SSO login failure after identity provider certificate rotation - customer case 3"
customer: "UrbanCart"
customer_tier: growth
region: US
status: resolved
severity: low
created_at: 2025-02-02
resolved_at: 2025-02-02
tags: ["authentication", "resolved", "ki-001"]
related_ids: ["KI-001", "TG-AUTH-SSO-001"]
---

# Ticket CD-001003: SSO login failure after identity provider certificate rotation

## Customer
UrbanCart

## Customer Message
Can you check why only users from one identity provider are affected for our workspace?

Additional customer context:
- Customer tier: growth
- Region: US
- Reported module: Authentication

## Symptoms Observed
- Users redirected back to login page
- Invalid SAML response error
- Only users from one identity provider are affected

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
