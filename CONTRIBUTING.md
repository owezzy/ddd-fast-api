# Contributing to ddd-fast-api

Thanks for helping improve the template.

## Workflow

1. Start from a clean `main` branch.
2. Use `bd ready` to find unblocked work or create a new issue before coding.
3. Claim the issue with `bd update <id> --claim`.
4. Keep changes small, testable, and aligned with the layer rules in `README.md`.
5. Run the local quality gates before committing.
6. Commit with a conventional message.
7. Push code and beads state together.

## Local setup

```bash
uv sync --group dev
make hooks
```

Optional hook tooling requires Node.js and npm. The Python workflow remains the
primary runtime and development path.

## Quality gates

Run these before opening a pull request:

```bash
make format
make lint
make type-check
make test
```

## Commit workflow

- `make hooks` installs Husky hooks locally.
- `make commit` opens an interactive Commitizen prompt.
- Direct commits are also allowed, but the `commit-msg` hook will reject
  messages that do not follow the configured conventional commit rules.

## Architecture expectations

- Domain code must not depend on FastAPI, Pydantic, SQLAlchemy, or outer layers.
- Application code orchestrates use cases and should not import entrypoints or
  infrastructure directly.
- Foundation code should stay reusable and avoid project business-layer imports.
- Transport, domain, and persistence models should remain explicitly mapped.

## Documentation expectations

Update documentation alongside behavior changes when you:

- add or change HTTP behavior;
- change settings or local developer workflow;
- introduce a new architectural seam or dependency rule;
- add deployment, CI, or operational behavior.

Use ADRs for decisions that are expensive to reverse or hard to infer from code.

## Pull requests

Pull requests should include:

- the bead or issue ID being addressed;
- a short summary of the change;
- the validation commands you ran;
- any follow-up work that should become a new bead.
