---
doc_id: POLICY-ESCALATION-001
doc_type: escalation_policy
product: CloudDesk CRM
title: "Support escalation rules"
last_updated: 2025-04-10
tags: ["policy", "escalation", "support"]
related_ids: []
---

# Support Escalation Rules

## Escalate to Engineering
Escalate when:
- A customer-facing error affects more than 10 workspaces.
- A valid API request fails repeatedly with 5xx errors.
- A documented workaround does not resolve the issue.
- Data loss, duplication, or corruption is suspected.

## Escalate to Billing Operations
Escalate when:
- Refunds exceed $5,000.
- Duplicate invoices cannot be voided by support.
- Tax calculation errors affect finalized invoices.

## Escalate to Security
Escalate when:
- Unauthorized access is suspected.
- SSO or MFA failure affects all admin users.
- Audit logs show unexpected login activity.

## Escalate to Messaging Operations
Escalate when:
- Suppression list removal does not restore email delivery.
- Notification delivery is delayed for multiple enterprise customers.

## Escalate to API Platform
Escalate when:
- 429 errors occur below documented rate limits.
- Valid authenticated API requests repeatedly fail with server errors.
