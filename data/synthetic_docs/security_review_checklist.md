---
document_id: security-review-checklist
title: Security Review Checklist
document_type: security
business_domain: application-security
sensitivity_level: synthetic-demo
created_at: 2026-02-05T00:00:00Z
---
# Security Review Checklist

Security review covers authentication, authorization, input validation, dependency scanning,
network exposure, secret handling, logging controls, and abuse-case testing. AI services add
prompt-injection tests, source-citation checks, refusal tests, and trace metadata review.

The service should avoid hardcoded secrets, validate request payloads, and keep demo data separate
from generated indexes.

