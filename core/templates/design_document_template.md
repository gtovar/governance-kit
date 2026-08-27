# Design Document Template

> System design document. Maximum cognitive offloading: tables, diagrams, mapping to real code.

## 1. System Overview and Context

- What the system is and which problem it solves, in one sentence.
- Main components and their relationships.

## 2. Key Technology Decisions and Justification

Comparison table:

| Decision | Options considered | Chosen | Why |
| -------- | ------------------ | ------ | --- |
| <...>    | <2-4>              | <...>  | <accepted trade-off> |

- Architectural decisions with a real commit go to ADRs; here only the summary.

## 3. Critical Data Flow

- In 5 steps maximum, with a diagram (Mermaid or similar) when it helps.

## 4. Code Structure

- Mapping architectural pattern → real folders/files.
- Do not describe the future: only what exists in the repo.

## Rules

- Language: English. Factual tone.
- Every claim with coordinates (file/endpoint/test/commit).
- If it contradicts the code, the code wins and this document is corrected.
