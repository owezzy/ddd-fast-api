# Architecture Decision Records

This directory stores Architecture Decision Records (ADRs) for decisions that
are important, non-obvious, and costly to reverse.

## When to write an ADR

Create an ADR when a change:

- affects layering or dependency direction;
- introduces or removes a significant dependency;
- changes the persistence, deployment, or security model;
- establishes a long-lived contributor workflow or release policy.

## Suggested format

Use a numbered file such as `0001-short-title.md` with sections like:

1. Status
2. Context
3. Decision
4. Consequences
5. Alternatives considered

Keep ADRs short and focused. Link related issues or beads where useful.
