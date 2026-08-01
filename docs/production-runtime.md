# Production Runtime Capabilities

The runtime phase adds replaceable platform seams without importing framework
concerns into the domain or application layers.

## Authentication and authorization

`HMACBearerAuthenticator` validates standard three-segment HS256 bearer tokens
and returns an `AuthenticatedPrincipal`. It is intentionally a local adapter:
production deployments should replace it with an OIDC/JWKS adapter while
keeping the HTTP dependencies unchanged.

For local testing, request a token from `POST /auth/dev-token`:

```json
{
  "subject": "user-1",
  "roles": ["admin"],
  "permissions": ["catalog:read"]
}
```

Use the returned `access_token` as `Authorization: Bearer <token>`. The helper
returns `404` when `DDD_FAST_API_APP_ENV=production`.

- `GET /identity/me` demonstrates authenticated principal wiring.
- `GET /catalog/management-preview` demonstrates a permission dependency.
- The `admin` role grants all permissions in this example policy.

## Health semantics

- `GET /health/live` only checks that the process can answer.
- `GET /health/ready` reports whether shared resources are ready for traffic.
- `GET /health/startup` reports whether lifespan startup completed.
- `GET /health` remains the backwards-compatible scaffold response.

Readiness and startup return `503` until the corresponding lifespan state is
set. This makes the endpoints suitable for container probes without making
the liveness probe depend on PostgreSQL.

## Telemetry

The HTTP middleware preserves or creates `X-Request-ID` and `X-Trace-ID`
headers, returns both headers to callers, and records response counters. The
`GET /metrics` endpoint emits Prometheus text format. The `Telemetry` object is
an injectable seam for replacing these counters with an OpenTelemetry or
Prometheus implementation later.

## Resilient outbound HTTP

`ResilientHttpClient` owns an async `httpx` client and supports configurable
timeouts, bounded retries, and exponential backoff for connection/read errors
and `429`, `500`, `502`, `503`, and `504` responses. Only explicitly idempotent
requests are retried; `GET` is idempotent by default and non-idempotent calls
must opt in deliberately.

Configure the adapter with:

- `DDD_FAST_API_OUTBOUND_TIMEOUT_SECONDS`
- `DDD_FAST_API_OUTBOUND_MAX_RETRIES`

The application lifespan creates and closes the shared client.
