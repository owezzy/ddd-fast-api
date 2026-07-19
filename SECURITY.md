# Security Policy

## Supported versions

The project is still pre-release. Security fixes will be applied to the latest
state on `main` until tagged releases begin.

## Reporting a vulnerability

Please do not open public GitHub issues for suspected vulnerabilities.

Instead:

1. Contact the maintainer privately through the repository owner profile or a
   private disclosure channel when one is published.
2. Include a clear description of the issue, affected area, reproduction steps,
   and impact.
3. If possible, include a minimal proof of concept and suggested remediation.

## Scope

Security-sensitive areas for this template include:

- authentication and authorization wiring;
- secret and environment handling;
- dependency and container supply chain;
- HTTP input validation and error handling;
- deployment manifests and network exposure.

## Expectations for contributors

- Never commit real credentials, signing keys, or private tokens.
- Use `.env.example` for configuration examples only.
- Prefer safe defaults and fail-fast startup checks for security-sensitive
  settings.
