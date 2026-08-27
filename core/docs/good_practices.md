# Good Practices Guide (Canonical)

> **Vehículo**: referencia enrutada desde la constitución (matriz "si toco X") + auditoría del subagente `reviewer` (check #10). Los determinizables (formato, lint, secretos, commits) se bajan a hooks/configs por perfil de fase (roadmap S4); SOLID y juicio de diseño viven aquí y en el reviewer — no son linteables. La filosofía (fundamentos DRY/SOLID) es referencia pura.
> **Autoridad**: semi-normativa. Manda como baseline de ingeniería; el proyecto puede definir excepciones documentadas.

> Engineering baseline for this repository. Agents must apply these by default;
> they are not optional "nice to have" conventions to skip for speed.
> Project-specific overrides belong in the project's own docs, not here.

## Part 1 — Naming and format

**Naming**
- Variables: descriptive names, `camelCase` for locals/params, plural for collections, no abbreviations.
- Functions: verb phrases, `camelCase`, never generic names like `doSomething`.
- Classes: `PascalCase`, noun names that describe responsibility.
- Constants: `UPPER_CASE_SNAKE_CASE`.
- Interfaces: `PascalCase`.
- Modules/packages: lowercase.

**Format**
- Line width: 80–120 chars.
- Indentation: 2 or 4 spaces, never tabs.
- Spaces after commas and around operators; none inside parens/brackets/braces.
- Opening brace on the same line as the declaration; closing brace on its own line.
- Blank lines separate logical blocks; one blank line at end of file.
- Methods short and focused; prefer methods that do one thing.

## Part 2 — Structure and organization

- One class per file; filename matches class name.
- Declaration order in a class: static fields → instance fields → constructors → public → protected → private.
- Declaration order in a file: stdlib imports → third-party imports → internal imports → globals → functions → executable code.
- Small functions, single responsibility.
- Classes with single responsibility; no god classes.
- Modularity: logical modules with clear responsibility.
- Encapsulation: hide implementation details, use proper access modifiers.
- Separation of concerns: business logic separated from presentation; data access separated from business logic.

## Part 3 — Code style and principles

- **DRY** — no duplication; refactor repeated code into shared functions/classes.
- **KISS** — keep it simple; avoid needless complexity.
- **YAGNI** — don't build what is not needed now; focus on current requirements.
- **SOLID** — SRP, OCP, LSP, ISP, DIP.
- High cohesion within modules; low coupling between modules.
- Errors: handle consistently, clear messages, specific exception types, centralized logging strategy.
- Comments: meaningful and current (see "Useful comments" rule in `AGENTS.md`); TODO/FIXME in a consistent format.

## Part 4 — Testing

- Unit tests for critical functions/methods; independent and repeatable.
- Integration tests where modules must work together; cover the most important use cases.
- Functional tests validate requirements (Selenium/Cypress/Playwright class).
- Performance tests for bottlenecks (JMeter/Gatling class) when the project requires them.
- Aim for high coverage without sacrificing quality for quantity.
- TDD is a technique, not a mandate: use it for logic, contracts, transformations, deterministic behavior.
- Update tests when requirements change; remove obsolete tests.

## Part 5 — Version control and process

- Branch model: pick one consistent model (Git Flow, GitHub Flow, trunk-based); main/master stable and production-ready; feature branches; hotfix branches.
- Commits: small and focused on one change; clear messages; Conventional Commits prefixes (`feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`).
- Code review for all significant changes, with context in the request.
- CI: automated build/test pipeline; all tests green before merge.
- CD: automated deploys; staging environments to validate before production.
- Post-mortems after critical incidents: what went well, what went wrong, what improves; lessons documented.

## Part 6 — Security and maintenance

- Validate and sanitize all user input.
- Robust authn/authz; standard protocols (OAuth2, OpenID Connect).
- Never expose error details to users; log errors safely.
- Keep dependencies updated (Dependabot/Snyk); regular security reviews; static and dynamic analysis.
- Secrets never in the repo (`.env` only as `.env.example`); PII hygiene (no real emails in logs/screenshots).
- Maintain technical docs; monitoring and alerts (Prometheus/Datadog class); incident management process; recovery plan; regular patches.

## Part 7 — Repo hardening checklist (apply when a repo has real code and CI)

- [ ] CodeQL or equivalent static security scanning in CI
- [ ] Dependabot (or equivalent) for dependency ecosystems in use
- [ ] Branch protection on main + required status checks
- [ ] Conventional Commits enforced (commitlint or hook)
- [ ] PR template with checklist (tests, docs, security)
- [ ] Pre-commit: formatting + lint + secret scan
- [ ] `.nvmrc`/tool-version pinning to align local and CI
- [ ] `SECURITY.md` (reporting + response window)
- [ ] `CODEOWNERS`
- [ ] Secret scanning + push protection enabled
- [ ] License
- [ ] Versioned artifacts declared (why versioned, how regenerated)
