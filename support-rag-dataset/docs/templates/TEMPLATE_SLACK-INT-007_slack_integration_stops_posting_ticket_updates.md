---
doc_id: TEMPLATE-SLACK-INT-007
doc_type: response_template
product: CloudDesk CRM
module: Integrations
title: "Customer response template: Slack integration stops posting ticket updates"
last_updated: 2025-04-12
tags: ["integrations", "template", "ki-007"]
related_ids: ["KI-007"]
---

# Customer Response Template: Slack integration stops posting ticket updates

Hi {customer_name},

Thank you for reporting this. We reviewed the behavior and confirmed that it matches a known integrations issue.

## What we found
Slack OAuth tokens were revoked after workspace permission changes, but CloudDesk did not prompt reauthorization.

## What we have done
Ask the customer admin to reconnect Slack integration and reselect the target channels.

## Temporary workaround
Use email notifications until Slack integration is reauthorized.

## Next steps
Please monitor the workspace and let us know if the issue appears again. If the issue continues after applying the recommended resolution, we will escalate the case according to our support process.

Regards,  
CloudDesk Support
