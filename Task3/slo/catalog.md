# OpenSLO-style contract: Catalog (SLI/SLO/SLA)

**Status:** proposed, 19.10.2026; owner: CTO + Product. **System:** `Africa Delivery`, logical module `Catalog` of ADR-001 monolith. **Window:** rolling 30×24 hours UTC, evaluated hourly; country tags NG/KE with separate dashboards. Do not assume actual launches.

## SLI: what is measured
Eligible: legitimate GET `/v1/catalog/**` and `/v1/products/**` requests reaching the edge, including synthetic probes; exclude **only** documented health checks, malformed client requests (4xx excluding 429), robots blocked by policy, and *pre-announced* synthetic load. 429 for legitimate consumers **is bad**. Good: non-5xx HTTP response with an expected body/schema (200/304 or valid 404 for a genuinely missing SKU), finished ≤1,000 ms measured at edge origin; gateway 502/503/504 **bad**, including when origin unavailable. Do not count empty successful payloads for known SKUs as good. Denominator from edge request counter plus synthetic availability probes, not only healthy app pods. Separately record request availability (correct response, regardless of latency) and latency p95/p99 for origin (do not conflate business SLI with synthetic RUM).

\[
SLI_{catalog}=\frac{\#\text{ eligible correct responses in }\le 1000\text{ms}}{\#\text{ eligible requests}}
\]

## SLO
- **99,9% good requests** per rolling 30 days. At 100k eligible requests, ≤100 bad request-equivalents; this is request-weighted, **not** a promise of 43,2 min real-world downtime.
- Latency objective origin p95 ≤500ms, p99 ≤1,000ms for defined 100 catalog RPS baseline; no untested promise at 10M users.
- Error budget = 0,1% × eligible requests; alert when burn rate >14.4× over 1h+5m (fast) or >6× over 6h+30m (slow), plus synthetic complete failure 5min.

## SLA (proposed only, subject to agreement)
No legally binding external uptime guarantee exists. Proposed internal business commitment: Product receives monthly compliance report, incidents P1 if >5 consecutive minutes browse unavailable in one launch country; P2 if error budget consumption >50% in first 15 days. Repeated violations → pause risky deployments, incident review ≤2 business days, corrective plan ≤5 business days. Customer remedy/service credit **not committed** and must be approved by Legal/CFO.

## Dependencies and exclusions
CDN stale-while-revalidate may keep public catalog readable when origin is down; stale price/stock must not be used for chargeable checkout without live verification. Regional network and PSP failures separately tracked, not silently excluded from end-to-end telemetry. Source [NFR](../nfr-registry.md), [ADR-002](../adr-002-caching-strategy.md).
