# Database Seeder Guide (Template)

> Generalizada a partir de la guía Sequelize original.
> Regla del kit: si un proyecto crea una base de datos, debe tener una guía de seeders con este formato.
> Adaptar los comandos a la herramienta del proyecto (Sequelize CLI, Alembic, Prisma, Flyway, raw SQL).

## Purpose

- Load reproducible reference data (roles, states, templates, etc.).
- Simplify local development with realistic datasets.
- Eliminate manual SQL scripts and reduce human error.

## 1) Tools

| Tool | Version | Purpose |
| --- | --- | --- |
| <migration/seeder tool> | ^X | Generate and execute seeders |

Install as a dev dependency:

```bash
<install command>
```

## 2) Directory structure

```text
<project>/
├── seeders/            (o migrations/ si la herramienta unifica)
│   └── YYYYMMDDHHmmss-description.js
└── migrations/
```

## 3) Naming convention

```text
YYYYMMDDHHmmss-description
```

Example: `20250718143000-create-default-roles.js`

## 4) Core commands

| Action | Command |
| --- | --- |
| Generate seeder | `<comando> --name <description>` |
| Run all seeders | `<comando>` |
| Undo last seeder | `<comando>` |
| Undo all seeders | `<comando>` |

Add convenient scripts to `package.json` (or Makefile).

## 5) Best practices

1. Use only for **reference data**, not user data.
2. Prefer idempotent upserts (`findOrCreate`/`ON CONFLICT`) over plain inserts.
3. Separate seeders by environment.
4. Always implement rollback (`down()`/downgrade).
5. Document purpose and context in each PR.

## 6) FAQ (adaptar)

| Question | Answer |
| --- | --- |
| Can I edit an applied seeder? | No — create a new one. |
| How are seeders executed? | Sorted by timestamp ascending. |
| Can I run only one seeder? | Use the tool's single-target option. |
