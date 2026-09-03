# Development Workflow

**Purpose:** define how this project goes from an observed experience or need to software used in real life.

*Template from the governance-kit. Adapt the phases to the project's domain; keep the principles: each phase resolves one uncertainty, do not skip uncertainties, explicit gates.*

---

## 1. Core principle

The project is developed through an **agent-agnostic** process.

```text
                 ┌── opencode
                 │
 REPOSITORY ─────┼── Claude Code
 CANONICAL       │
                 ├── Codex
                 │
                 └── future agents
```

Codex, Claude Code, opencode, Gemini, and other agents are replaceable tools. Canonical knowledge lives in the repository, not in any agent's private memory.

---

## 2. What we are optimizing

We are not optimizing for producing code as fast as possible. We reduce uncertainties in the right order:

```text
Is there a real problem/need?
            ↓
What does the user actually need?
            ↓
How should the experience work?
            ↓
How should it look and feel?
            ↓
Does the experience work when simulated?
            ↓
What exact behavior will we build?
            ↓
How should it be implemented?
            ↓
Does the implementation meet the specification?
            ↓
Does it really work in daily life?
            ↓
What did we learn?
```

Each phase answers a different question. An idea may die, be parked, or return to Discovery.

---

## 3. Fundamental rule: do not skip uncertainties

- If we don't know whether a feature would help the user: **do not optimize its architecture.**
- If we don't know how it should behave: **do not write implementation tests.**
- If we know exactly what it must do but not how: **technical design is appropriate.**

---

## 4. Phases (base template)

```text
F0  Foundation           — how do we work without depending on a specific agent or conversation?
F1  Discovery            — which real situations need support?
F2  Product Definition   — what should the product be able to do?
F3  UX                   — how should the interaction unfold?
F4  UI / Design System   — how is that experience presented?
F5  Experience Prototype — is this how we want it to feel?
F6  Validation           — what helps, bothers, confuses, or is missing?
F7  Specification / SDD  — what exact behavior do we build?
F8  Technical Design     — how should we implement it?
F9  Implementation       — can we build the capability?
F10 Verification/Release — can it be used reliably?
F11 Real-World Learning  — does this actually help?
```

Each phase defines in `PROJECT_MAP.md`: question, artifacts, gate, and what must NOT be done yet.

---

## 5. F0 — Project Foundation (mandatory in every project)

**Question:** how will we work without depending on a specific agent or conversation?

**Artifacts:**

```text
README.md
AGENTS.md

docs/process/
├── DEVELOPMENT_WORKFLOW.md
├── PROJECT_MAP.md
└── CURRENT_STAGE.md
```

**Gate F0:** any new agent can enter the repository and understand, without
prior context, what the project is, how the process works, where the project is,
and which work is allowed next.

---

## 6. Session rule

Each conversation should try to resolve **one main frontier**. Do not try to advance five phases in a single conversation.

A frontier is actionable only when it declares:

```text
Action: one imperative action
Target: one exact file, decision ID, or gate
Done when: one observable completion condition
```

An undefined collection (for example, "remaining findings") is not a frontier.
A warning or historical inconsistency does not become phase work unless the
current gate explicitly depends on it. If a gate's evidence is satisfied and no
real blocker remains, the next frontier is the gate decision itself, not
another review.

A cross-reference to `PROJECT_MAP.md`, `CURRENT_STAGE.md`, or another process
document is context, not a frontier. Do not use a document reference to defer
choosing the action, target, or closure evidence. If the next work requires a
human choice, make that decision the explicit frontier.

After a meaningful session:

```text
1. update artifacts
2. update PROJECT_MAP if a phase changed
3. update CURRENT_STAGE
4. record open decisions
5. define the next frontier
```

---

## 7. Protocol between conversations

The initial message for a new chat can be:

> I am working on `<project>`.
> Read `AGENTS.md` and follow its canonical re-entry order under **Start here**.
> We are in the phase indicated by `CURRENT_STAGE.md`.
> Work only on the current objective and do not advance phases without checking the gate.

That should be enough to rebuild operational state without retelling the whole story.

---

## 8. Over-architecture protection

Before creating any new document, agent, role, workflow, or process, ask:

> What concrete project problem does it solve?

If the answer is mainly "serious projects usually have one": **do not create it yet.**

The methodology itself also evolves:

```text
OBSERVATION → HYPOTHESIS → EXPERIMENT → RESULT
```

---

## 9. Roles as lenses

Roles (Product, UX, UI, Backend, QA, Security, SRE, DBA, Marketing) are neither people nor permanent agents: they are lenses activated when appropriate. The question is not "do we have all the roles?" but "which lens do we need to resolve the current uncertainty?"

---

## 10. ADR

Use an ADR only for decisions that are relevant, persistent, expensive to reverse, and affecting several parts of the system. Do not use an ADR for every minor choice.

---

## 11. Agent-agnostic rule

Canonical documents must be neutral (`PRODUCT_REQUIREMENTS.md`, `spec.md`), never `CLAUDE_PRODUCT_SPEC.md` or `CODEX_ARCHITECTURE.md`. Agent-specific adapters (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) may exist, but they must point to the canonical sources. Never duplicate the project's truth in incompatible formats.
