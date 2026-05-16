---
doc_id: PROD-API-RATE-010
doc_type: product_article
product: CloudDesk CRM
module: Performance
title: "Performance module behavior overview"
last_updated: 2025-02-05
tags: ["performance", "product-doc"]
related_ids: []
---

# Performance Module Behavior Overview

The Performance module in CloudDesk CRM supports customer workflows related to performance.

## Expected Behavior
CloudDesk attempts to provide reliable and auditable behavior for all performance operations.

## Common Support Areas
Support teams commonly review:
- API returns 429 errors
- Customer says API is down
- Bulk import fails midway
- Retry logic causes additional throttling

## Operational Notes
Customers on enterprise plans may require faster escalation when the issue blocks production workflows.

## Support Guidance
Before escalating, support should collect:
- Workspace ID
- Customer tier
- Region
- Affected version
- First observed timestamp
- Screenshots or error messages when available
