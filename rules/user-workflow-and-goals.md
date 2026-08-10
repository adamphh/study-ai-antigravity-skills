# User Workflow, Environment & Personal Goals Rules

## 1. Environment & Execution Setup
- **Frontend (WebPOS Client)**: Run directly using `npm` (`npm run upgrade`, `npm run test`...).
- **Backend (Magento 2 PHP)**: PHP is NOT installed on the host machine. All PHP/Magento CLI and PHP unit test commands MUST be run via Docker container (e.g. `docker exec ...`).

## 2. Mandatory 4-Step Hybrid Workflow
Whenever handling a user task or feature request, AI MUST strictly follow this 4-step workflow:
- **Step 1: Analysis & Plan Creation**:
  - Trace codebase, understand requirements, and ask proactive clarifying questions if anything is ambiguous or unclear. Never guess intent.
  - Create plan file: `Plans/{ma_du_an}-{ma_issue}-{noi_dung_task_tom_tat}.md` and the implementation plan artifact.
- **Step 2: Self-Review Plan & Report**:
  - AI acts as Code Reviewer to audit its own plan: check allowed scope (`app/code/Magestore/` with FixBug/Custom, `client/pos/src/extension/`), check for potential plugin conflicts, XML tags integrity, maximum line length (120 chars), copyright headers.
  - Present the plan and the self-review findings to the user for approval.
- **Step 3: User Approval**:
  - Wait for the user to review, approve the plan, and explicitly command execution.
- **Step 4: Execution, Automated Testing & Walkthrough**:
  - Write complete extension/plugin code.
  - Run automated tests (`npm` for JS, `docker exec` for PHP).
  - Write detailed execution & test report into `walkthrough.md`.

## 3. Communication & Clarification Mandate
- **Strict Clarification Rule**: Always ask the user directly for clarification whenever a requirement, design detail, error log, or task description is ambiguous, missing, or unclear. Never make blind assumptions or patch symptoms silently.

## 4. Automation & Code Optimization Objectives
- **Phase 1 (Time & Workflow Optimization)**: Maximize automation in daily tasks (auto-tracing, proactive subagents, docker/npm testing, self-review, handover notes).
- **Phase 2 (WebPOS Codebase Audit & Performance Optimization)**: Proactively observe and audit WebPOS client/backend code during tasks to identify bottlenecks, race conditions, offline IndexedDB sync issues, or anti-patterns, and propose refactoring/optimization recommendations.
