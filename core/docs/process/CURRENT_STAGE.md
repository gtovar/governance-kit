# Current Stage

**Location:** `docs/process/CURRENT_STAGE.md`
**Updated:** <DATE>

This is the project's operational checkpoint. It must stay deliberately small.

When switching conversations, agents, or machines: read this file first.

---

## Where are we?

```text
Current phase:
F0 — Project Foundation

Current objective:
<ONE SENTENCE — which uncertainty we are resolving>
```

## Completed

```text
- <verified fact, not intention>
```

## Working on

```text
- <the active artifact or frontier>
```

## Next

```text
Action: <imperative action>
Target: <exact file, decision ID, or gate>
Done when: <observable completion condition>
```

## Do NOT do yet

```text
- <work explicitly out of scope in this phase>
```

## Open decisions

```text
- <pending decision + who takes it + what evidence would unblock it>
```

---

## Update rule

This file has one frontier owner: `## Next`. A valid frontier names an action,
an exact target, and observable completion evidence. It must not point to an
undefined collection such as "remaining findings" or "pending issues".
It must not use a cross-reference to another process document as a substitute
for a frontier. When the next step is a human decision, name that decision as
the target and state the evidence that closes it.

Update this file only when a verified fact, phase, scope, decision, or frontier
changes. A read-only re-entry that discovers no state change does not trigger an
update.

A new agent must be able to read this document and know exactly what to do and what not to do, without prior conversation.
