---
name: useful-comments-reviewer
description: Use when reviewing code comments — a review request, a diff that adds or edits comments, or tricky logic where it is unclear whether comments are helping. Judges whether comments are useful, redundant, stale, missing, or hiding code that should be refactored instead.
---

# Useful Comments Reviewer

Use this skill when:
- the user asks for a review of comments
- a diff adds or edits comments
- a file contains tricky logic and it is unclear whether comments are helping
- you need to decide whether to comment, remove a comment, or refactor instead

Do not use this skill for generic code review unless comments are a central part of the request.

## Review Standard

Apply the "Useful comments" rule from `AGENTS.md` at the repository root.

Comments are useful when they explain:
- intent
- context
- tradeoffs
- invariants
- warnings
- non-obvious constraints

Comments are weak when they:
- restate obvious code
- describe control flow line by line
- duplicate names already clear from code
- drift from the current implementation
- replace refactoring with narration

## Reviewer Checklist

For each relevant comment, classify it as one of:
- good
- redundant
- stale
- missing
- refactor-instead

Use this test:
1. If the comment were removed, would a future reader lose important intent or context?
2. If yes, keep or improve it.
3. If no, remove it unless it serves as a concrete TODO/FIXME with actionable detail.

## Output Style

When reviewing, prefer findings first.

Use short findings such as:
- `redundant`: repeats the code without adding intent
- `stale`: no longer matches the implementation
- `missing`: logic needs a brief why/tradeoff/invariant note
- `refactor-instead`: comment is compensating for confusing structure

When no findings exist, say so explicitly.

## Authoring Guidance

When proposing a replacement comment:
- keep it short
- explain why, not only what
- prefer one precise sentence
- avoid essay-style comments

Example:

Bad:
```js
// Incrementa i en 1
i++;
```

Good:
```js
// Retry budget is capped here to avoid duplicate provider sends after reconnect.
attempts += 1;
```
