# OpenSLO-style contract: Payments / checkout

**Status:** proposed 19.10.2026; owner: CTO + CFO + PSP integration lead. A logical `Payment/Order` journey within the monolith, NOT proprietary licensed payment processing. Requires country×method×PSP contract validation (Task1 C-07).

## SLI
**Checkout intent availability**: denominator all eligible authenticated buyer checkout POST attempts received at the edge with valid items, including duplicate retry attempts as separately tracked HTTP attempts; good if **within 3 seconds** the backend durably persists an order/intent, returns valid `pending`/redirect/payment-provider request or a correctly identified *business* decline; 5xx, timeout, missing persist or false `paid` are bad. Real PSP unavailability counted in **end-to-end completion SLI**, not hidden by a backend pending response.

**PSP journey completion** (secondary dependency SLI): eligible paid-intent journeys reach a reconciled terminal state within 15 minutes, excluding *only verified user cancellation*, measured from intent creation; `pending` >15m and unmatched callback are bad. Track reason breakdown: PSP down, fraud hold, bank/settlement, timeout. Instrument approved PSP per country and partner SLA separately.

\[
SLI_{intent}=goodIntentResponses/eligibleCheckoutRequests;\quad
SLI_{settlement}=reconciledTerminalIntents_{15m}/eligiblePaidIntents
\]

## SLO
- **Intent good response ≥99,9%** over rolling 30 UTC days (fast burn alerts as in catalog). Origin p95 ≤1.5s and p99 ≤3s excluding PSP network delay, but PSP E2E separately measured.
- **Terminal PSP journey ≥99,0%** in 15 min, **provisional, partner-dependent**, not promised to customers until PSP commercial SLA and sandbox/production verification.
- Duplicate confirmed charges caused by platform = **0** (safety invariant, immediate Sev1 on detection); audit, idempotency key, signed hooks, outbox and daily reconciliation mandatory.
- Recovery objective proposed **RTO ≤60min / RPO ≤15min** for local database tier, validated by drill. For *financial ledger*, data-loss safety requirement is reconciliation-to-zero unmatched after recovery; **not** a claim that RPO=0.

## SLA (proposed internal)
No executed contractual end-to-end SLA or same-day seller settlement guarantee. Internal handling: checkout intents completely unavailable >2min country-wide = Sev1; false payment success/duplicate charge = Sev1 immediately; paid-intent unmatched >15min enters queue with on-call alert; cases unresolved >60min escalate to CFO/ops. Within 1 business day produce incident timeline; dispute/refund follows legal/PSP terms, not fabricated instant-refund SLA. Legal and CFO must approve user-facing promises/remedies.

## Failure handling
Do not infinitely retry non-idempotent create-charge; persist idempotency key. On PSP timeout, show pending; query status/reconcile before retry; exponential backoff with jitter, bounded attempts, circuit breaker, partner bulkhead. No secret or PAN in traces. Sources [ADR-001](../../Task2/adr-001-architecture-style.md), [FMEA](../fmea.md).
