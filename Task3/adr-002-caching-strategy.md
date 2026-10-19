# ADR-002 — стратегия кеширования

- **Дата:** 2026-10-19
- **Статус:** **Proposed**, требует согласования CTO/Product/Security; не подтверждён эксплуатационными испытаниями.
- **Связь:** [ADR-001 — modular monolith](../Task2/adr-001-architecture-style.md), [SLO Catalog](slo/catalog.md), [FMEA](fmea.md); ограничения Task1 R-22 (3G/изображения), R-09 (SLO), R-10 (data residency).

## Контекст
Дешёвые Android/3G, быстрый каталог и рекламные всплески повышают ценность кеширования. Но кеш некорректных цен или складских остатков на checkout может привести к потере денег. Универсальная Redis-инфраструктура увеличивает регулярные затраты и операционные риски при лимите CFO $5k/month.

## Решение
CDN/edge кешируют **только публичные** статические активы и анонимные ответы; backend реализует Cache-Aside для read-heavy каталога с in-process LRU bounded cache как первичным вариантом, без обязательного Redis. Изменения каталога инвалидируют теги/ключи после commit через outbox; при потере invalidation TTL остаётся верхней границей устаревания. Payment/Order/PII/cache-user-content **не кешировать** на общих промежуточных узлах.

| Объект | Место | TTL / директива | Инвалидация и защита |
|---|---|---|---|
| Изображения SKU (версионный URL) | CDN + browser | 7 суток, immutable при хэше | новый asset URL по изменению, purge при legal take-down |
| JS/CSS с content hash | CDN + browser | 30 суток immutable | новый build hash |
| Публичная карточка/категория | Edge/private service LRU | 60 с, jitter ±20%; stale-while-revalidate максимум 60 с **только для browsing** | после commit event `ProductChanged` purge SKU/tag; TTL fallback |
| Категорийная навигация/справочники | Backend LRU | 10 мин | version increment + manual invalidation |
| Поиск/листинг (анонимные и легальные) | Edge/server | 30 с | tag/publish event, capped cache keys |
| Availability/price на странице | Backend read cache | **≤5 с** (предварительный максимум) | после изменения stock/price drop-key; checkout **всегда повторно читает транзакционный source of truth** |
| Персональные корзины/checkout/auth token | **не общий кеш** | `Cache-Control: no-store` | durable DB, encrypted session if needed; no cached payment success |
| KYB/consent/PII/settlement/ledger | **не общий кеш** | no-store | database+audit, no public CDN |
| Provider PSP status | **не кешировать как факт оплаты** | no-store | signed webhook + reconciliation |

**Cache key:** `country:locale:catalog-version:sku/filter-hash`, теги стране/языку; never mix NG and KE personalized datasets. CDN cache cookies stripped for public GET only; Vary correctly; prohibit cache poisoning by normalized query/key length. Use negative cache 404 ≤10s for public SKUs only. Singleflight request coalescing, bounded size and per-country quotas protect origin against stampede.

## Отвергнутые альтернативы
1. No cache: проще в операциях, но риск p99/3G и избыточной нагрузки на DB.
2. Redis для всего: не нужен без измеренных hit ratio/latency, дороже и создаёт отдельный failure domain; Redis может быть выбран позже только после экспериментального сравнения.
3. Long-TTL stock/payment cache: неприемлем для корректного платёжного пути.

## Последствия
**Плюсы:** дешевле, меньше обязательных сервисов, отзывчивее чтения, простой rollback и CDN bandwidth control. **Минусы:** ограниченная когерентность после изменения каталога; версионность и outbox events обязательны; in-process LRU живёт отдельно на каждом instance; purge CDN может быть eventually consistent.

## Критерии проверки и пересмотра
Нагрузочный тест 100 RPS baseline и 2× burst, p99 каталога ≤1s, cache hit ratio ≥70% на **репрезентативном browse** (только trial target), отсутствие stale price/stock в 100k checkout replay cases. Пересмотреть Redis/выделенный caching tier при устойчивом miss pressure, экономически обоснованной цене, одобренном CFO run-cost и подтверждённом legal region. При изменении policy страны запрещать CDN edge caching регионально до legal approval.
