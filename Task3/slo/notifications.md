# OpenSLO-style contract: Notifications

**Status:** proposed, 19.10.2026; owner: Product + Operations. Notification is a logical outbox worker in the ADR-001 monolith, NOT an externally guaranteed SMS/WhatsApp delivery service.

## SLI
Denominator: lawful, correctly addressed, consent-eligible **transactional** messages committed to outbox (channel, country, event timestamp); exclude messages suppressed **before enqueue** according to consent rules, test events and verified invalid recipient IDs. Good if accepted (provider ACK/id) by SMS/WhatsApp gateway within **5 minutes** after outbox commit. Delivery to handset is a different downstream SLI and is **not** measurable solely from gateway acceptance. No messages are sent to purchased 410k-list until separate legal permission.

\[
SLI_{notify}=gatewayAcceptedWithin5m/validEnqueued
\]

## SLO
- ≥**99,0%** good valid enqueued events in rolling 30d UTC; separately track DLQ rate, backlog age, provider rejects and channel country distribution.
- p99 enqueue-to-gateway-ack ≤5 minutes for SLO-compliant paths (a p99 latency can be infeasible exactly at 99% edge; report percentiles and good-event ratio separately).
- Dead-letter queue has zero unexamined items aged >1 hour at end of staffed monitoring interval (operational target).
- During PSP outage, no false `paid` notification, and notification retry must never retry payment itself.

## SLA (proposed internal only)
Product receives daily status, incident Sev2 if queue age >10 min continuously for ≥5 min or SLO error budget exhausted; Sev1 only when critical payment confirmation is falsely sent or legally restricted bulk notification is dispatched. Operations restores queue/partner integration, communicates delayed alerts without promising gateway or handset delivery. No external service credits/remedies until partner contract/Legal approval.

## Resilience and traceability
Outbox polling, bounded exponential retry+full jitter, provider circuit breaker and country/channel-specific bulkheads; DLQ manual replay with idempotent external request IDs and consent revalidation. Dependency on partner outages shown explicitly. Sources [ADR-001](../../Task2/adr-001-architecture-style.md), [Task1](../../Task1/contradictions.md), [Observability](../observability.md).
