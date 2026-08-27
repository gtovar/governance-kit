# Project Map

**Location:** `docs/process/PROJECT_MAP.md`
**Version:** 0.1
**Current phase:** F0 — Project Foundation

This is the project's navigation map. A person or agent must be able to answer:

- what phases does the project have?
- which phase are we in?
- what is already done?
- what are we doing now?
- what comes next?
- which artifacts belong to each phase?
- which condition allows advancing?
- what must NOT be done yet?

It does not replace `DEVELOPMENT_WORKFLOW.md`: the workflow explains **how the process works**; this map shows **where we are inside that process**.

---

## Big Picture

```text
F0  PROJECT FOUNDATION
        ↓
F1  PRODUCT DISCOVERY
        ↓
F2  PRODUCT DEFINITION
        ↓
F3  UX
        ↓
F4  UI / DESIGN SYSTEM
        ↓
F5  EXPERIENCE PROTOTYPE
        ↓
F6  VALIDATION
        ↓
F7  SPECIFICATION / SDD
        ↓
F8  TECHNICAL DESIGN
        ↓
F9  IMPLEMENTATION
        ↓
F10 VERIFICATION / RELEASE
        ↓
F11 REAL-WORLD LEARNING
        │
        └──────────────→ F1 DISCOVERY
```

*For non-product projects, replace the phases with those defined by the project's own `DEVELOPMENT_WORKFLOW.md`. The principle does not change: each phase resolves one uncertainty; do not skip uncertainties.*

---

## General status

| Phase | Name | Status |
| ----- | ---- | ------ |
| F0    | Project Foundation    | **IN_PROGRESS ← WE ARE HERE** |
| F1    | Product Discovery     | NOT_STARTED |
| F2    | Product Definition    | NOT_STARTED |
| F3    | UX                    | NOT_STARTED |
| F4    | UI / Design System    | NOT_STARTED |
| F5    | Experience Prototype  | NOT_STARTED |
| F6    | Validation            | NOT_STARTED |
| F7    | Specification / SDD   | NOT_STARTED |
| F8    | Technical Design      | NOT_STARTED |
| F9    | Implementation        | NOT_STARTED |
| F10   | Verification / Release| NOT_STARTED |
| F11   | Real-World Learning   | NOT_STARTED |

Allowed states: `NOT_STARTED` · `IN_PROGRESS` · `BLOCKED` · `READY_FOR_GATE` · `COMPLETE` · `REVISIT`

---

## F0 — Project Foundation

**Question it resolves:** how can this project be developed without depending on a specific chat, agent, or one person's memory?

**Artifacts:**

```text
README.md
AGENTS.md

docs/process/
├── DEVELOPMENT_WORKFLOW.md
├── PROJECT_MAP.md
└── CURRENT_STAGE.md
```

**Gate F0:** any new agent can enter the repository, read the entry documents,
and determine without prior context what the project is, which rules to respect,
how the workflow works, the current phase, and the next allowed piece of work.

---

## Document creation rule

A file appearing in this map does NOT mean it must be created immediately. Create a document only when:

1. real information needs to live there;
2. its separation reduces ambiguity;
3. it has a responsibility different from existing documents;
4. a human or agent will use it.

Avoid ceremonial documentation.

---

## Rule for switching chats or agents

Before closing a meaningful session:

1. save the artifacts produced;
2. update this map if a phase changed;
3. update `CURRENT_STAGE.md`;
4. record open decisions;
5. leave the next frontier explicit.
