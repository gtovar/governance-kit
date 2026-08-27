# ADR Policy

> **Vehículo**: enrutada desde la constitución ante decisiones arquitectónicas + skill `documentation-governance` (clasificación ADR vs DDR vs ninguno).
> **Autoridad**: normativa.

> This file is part of the active governance system. It defines when an ADR is valid, when a DDR is enough, and what evidence is required before an ADR can exist.

## Purpose

This policy prevents architectural drift, shallow ADRs, and false positives where a structural signal is treated as a finished architectural decision.

An ADR is not a generic note about a technical change.
An ADR is a durable record of an architectural decision with explicit trade-offs.

## Definition

An ADR is valid only when the decision:

- affects system structure, responsibility boundaries, contracts, data flow, or long-term maintainability
- is non-trivial
- is not purely stylistic
- is not cheap to reverse
- has already been decided, not merely explored
- is backed by a real implementation commit

If any of those conditions is missing, the record is not yet a valid ADR.

## ADR vs DDR vs No Record

### Use an ADR when all of these are true

- the change is architectural
- trade-offs were considered
- alternatives were evaluated
- the final direction has already been chosen
- the decision is stable enough to be worth preserving
- a real commit hash exists that reflects the decision in code

### Use a DDR when any of these are true

- the change is structural but too small or too local for a full ADR
- the reasoning should be preserved, but the decision is not broad enough to deserve a standalone architectural record
- the repo has no ADR area yet, but a durable decision note is still needed

### Use no ADR yet when any of these are true

- the change is still under evaluation
- the direction is tentative
- there is no real commit yet
- the change is cosmetic, stylistic, or operationally trivial

If the decision is still being explored, record it as an open question or a DDR note. Do not create an ADR yet.

## Mandatory ADR Questions

A valid ADR must answer all of these questions:

1. What problem or constraint forced the decision?
2. Why is this decision architectural rather than incidental?
3. Which options were considered?
4. Why was the chosen option selected over the others?
5. What trade-offs are accepted?
6. What are the positive consequences?
7. What are the negative consequences, risks, and mitigations?
8. Which exact commit reflects the decision in code?

If the record cannot answer these questions, it is incomplete.

## Required ADR Structure

Every ADR must include:

1. `Title`
2. `Status`
3. `Date`
4. `Context`
5. `Options considered`
6. `Decision`
7. `Consequences`
8. `Commit hash`

Status values:

- `proposed`
- `accepted`
- `superseded`

Rules:

- do not use `proposed` as a placeholder for uncertainty
- if the decision is still tentative, it is not ready for an ADR
- once code lands and the decision is active, the expected state is usually `accepted`

## Prohibitions

Do not use an ADR for:

- minor implementation details
- style choices
- formatting preferences
- low-cost local refactors
- decisions that have not been made yet
- decisions with no real code commit behind them

Do not write an ADR that lacks:

- alternatives
- trade-offs
- consequences
- commit hash

## Detection Rule

A structural signal only means:

- architectural evaluation may be needed

It does not mean:

- an ADR is automatically required

Correct sequence:

1. detect structural signal
2. evaluate ADR questions
3. decide `ADR`, `DDR`, or `none`
4. write the correct record in the correct place

## Canonical Location

- `docs/adr/*.md` in this repository.
- A sub-repo without its own ADR area uses a DDR in its state/log until a local ADR area exists.

## Relationship with Other Governance Docs

- `AGENTS.md` decides when ADR/DDR evaluation must be considered
- `docs/documentation_rules.md` defines owner-doc routing and documentation gates
- The DDR decision-record template lives in `docs/documentation_rules.md`
- This policy defines validity; ADR templates define the exact write shape
