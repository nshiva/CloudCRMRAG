---
doc_id: TEMPLATE-AUTH-SSO-001
doc_type: response_template
product: CloudDesk CRM
module: Authentication
title: "Customer response template: SSO login failure after identity provider certificate rotation"
last_updated: 2025-04-29
tags: ["authentication", "template", "ki-001"]
related_ids: ["KI-001"]
---

# Customer Response Template: SSO login failure after identity provider certificate rotation

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known authentication issue.

## What we found
The identity provider signing certificate was rotated, but CloudDesk still had the previous certificate cached.

## What we have done
Ask the customer admin to upload the renewed IdP certificate and clear the SSO metadata cache.

## Temporary workaround
Temporarily enable password login for affected users if allowed by the customer's security policy.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
