# Frontend Specification (Intent)

## Purpose
Provide human operators visibility and control over Chimera agent activity.

## Core Screens
1. Dashboard
   - Agent status (idle / running / blocked)
   - Recent executions
   - Error counts

2. Content Review
   - Draft text
   - Confidence score
   - Policy decision
   - Approve / Reject actions

3. Audit & Logs
   - Execution history
   - Human approvals
   - Policy escalations

## User Flows
- Review content → approve → publish
- Low-confidence draft → human escalation
- View agent health and failures

## API Mapping
- GET /v1/drafts
- POST /v1/reviews
- POST /v1/publish
