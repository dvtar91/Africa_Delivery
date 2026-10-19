# Реестр нефункциональных требований — Africa Delivery

**Дата:** 19.10.2026. **Статус:** проектные, проверяемые SLO/NFR для MVP, ожидают подтверждения CTO/CFO/CEO, проверки PSP и юридической допустимости размещения. Исторический срок 15.10.2026 не является подтверждением запуска. Базовая архитектура — **модульный монолит**, managed PostgreSQL после country legal gate, stateless HTTP API и transactional outbox ([ADR-001](../Task2/adr-001-architecture-style.md)). Слово «сервис» в SLO означает **наблюдаемый пользовательский путь/модуль**, а не отдельный микросервис.

| ID | Категория | Проверяемое требование | SLI/метрика | Цель (предложение) | Проверка/доказательство | Источник |
|---|---|---|---|---|---|---|
| NFR-01 | Доступность каталога | Выдавать непустой корректный каталог | good / eligible HTTP + synthetic | 99,9% / скользящие 30 суток | RUM + Prometheus + synthetic probe | [Vision](../Task2/architecture-vision.md), [Catalog SLO](slo/catalog.md) |
| NFR-02 | Доступность оплаты | Сохранить заказ/безопасно инициировать платёж, не терять подтверждения PSP | good checkout/eligible attempts | 99,9% / 30 суток; PSP измеряется отдельно | бизнес-события + сверка + synthetic sandbox | [Vision](../Task2/architecture-vision.md), [Payments SLO](slo/payments.md) |
| NFR-03 | Надёжность уведомлений | Принятые в outbox согласованные сообщения своевременно передаются шлюзу | delivered-to-gateway <=5 мин / valid outbox | 99,0% / 30 суток | outbox lag, retry/DLQ | [Notifications SLO](slo/notifications.md), [Marketing](../input_data/marketing-brief.md) |
| NFR-04 | Задержка каталог API | При нормальной нагрузке обработать GET catalog | p95 и p99 backend server latency | p95 ≤500 мс, p99 ≤1 000 мс | histogram + k6, 30 суток; отдельно клиентский UX | [Vision](../Task2/architecture-vision.md) |
| NFR-05 | Задержка checkout | Сохранить intent/возвратить статус, без времени внешнего PSP | p95 и p99 internal checkout latency | p95 ≤1 500 мс, p99 ≤3 000 мс | histogram + нагрузочный replay | [ADR-001](../Task2/adr-001-architecture-style.md) |
| NFR-06 | 3G доступность UX | Первый товар доступен при дешёвом Android и ограниченном 3G | p75 time-to-first-product | ≤2 с как **экспериментальная цель**, не SLA | throttled real-device lab | [Marketing](../input_data/marketing-brief.md), [Task1 R-22](../input_data/requirements-traceability.md) |
| NFR-07 | Пропускная способность | Обработать базовые пиковые запросы с сохранением NFR-01,04,05 | sustained RPS, error rate, queue lag | **100 catalog RPS + 10 checkout RPS** в течение 30 мин (нагрузочная гипотеза) | k6 staging 30 мин, 2× burst на 5 мин | [Task1 R-03](../input_data/requirements-traceability.md) |
| NFR-08 | Целостность денег | Повтор callback не создаёт второго списания/заказа | duplicate financial effects | 0 в 100k replay тестов; все события audit+reconcile | PSP mock/webhook chaos, ledger reconciliation | [ADR-001](../Task2/adr-001-architecture-style.md) |
| NFR-09 | Recovery | Документированный recovery для приложения | измеренный RTO | **≤60 мин** для app-tier; зависит от backend + БД | quarterly game day с таймером | [Task1 R-09](../input_data/requirements-traceability.md) |
| NFR-10 | Data loss | Возможность восстановить committed DB writes | измеренный RPO | **≤15 мин** DB при PITR/backup, только после restore drill | restore в изолированном окружении, сравнение WAL | [Task1 R-09](../input_data/requirements-traceability.md) |
| NFR-11 | Ошибки/деградация | Безопасный отказ PSP: no false success | % незасчитанных финансовых операций | 0 false-positive payment-success; pending + reconciliation | автоматизированные fault tests | [Vision](../Task2/architecture-vision.md) |
| NFR-12 | Защита PII | Не передавать чувствительные данные между странами до legal sign-off | unapproved cross-border transfers | 0 | DLP/config audit/egress tests | [Task1 R-10](../input_data/requirements-traceability.md) |
| NFR-13 | Consent | Не отправлять маркетинговые SMS без законного основания | unauthorized campaigns | 0 | review consent ledger + suppression list | [Task1 C-05](../Task1/contradictions.md) |
| NFR-14 | Cloud Native / portability | Сборка из контейнера и декларативный deploy без зависимости от K8s | rebuild+redeploy time | clean rebuild + staging deploy ≤30 мин | CI drill, OCI image signature, IaC diff | [CTO](../input_data/letter-cto.md), [ADR-001](../Task2/adr-001-architecture-style.md) |
| NFR-15 | CN managed by default | Зафиксировать managed/self-hosted exception | documented exception / total | 100% исключений с TCO, риском и owner | ADR review | [Task1 R-07](../input_data/requirements-traceability.md) |
| NFR-16 | CN API interoperability | Строго версионированные контракты HTTP/webhook/async | compatibility contract test | 100% критичных партнерских endpoints, idempotency; sync разрешён | CI consumer/provider tests | [Task1 R-08](../input_data/requirements-traceability.md) |
| NFR-17 | Observability | Четыре золотых сигнала + trace/span correlation по 3 путям | coverage of key paths | 100% catalog/checkout/outbox; **не** 100% sampling | telemetry acceptance test | [Observability](observability.md) |
| NFR-18 | Бюджет | Все run-cost infra+technical SaaS ограничены CFO | USD per month | ≤$5 000 первые 6 месяцев, затраты >$500/item предодобрены | billing export+monthly approval | [CFO](../input_data/letter-cfo.md) |
| NFR-19 | Security | Исключить платёжные PAN, защитить callbacks | raw PAN records; unsigned accepted hooks | 0; authenticated signature+replay protection | security test + webhook fixtures | [Vision](../Task2/architecture-vision.md) |
| NFR-20 | Резервирование | Зависимости на PSP и SMS не распространяют каскадную ошибку | worker exhaustion, CB trips | 0 exhausted shared request pool в chaos tests | FMEA failure injection | [FMEA](fmea.md) |

**Cloud Native пояснение.** CN-чек-лист CTO — набор критериев для тестирования, **не подтверждение сертификации CNCF**. Размещение «у любого провайдера» означает переносимость кода/деплоя с документированным RTO миграции и cost review, а не одинаковую managed-инфраструктуру во всех странах.

## Экономика девяток и решение

Период 365 дней = 525 600 минут. Сценарная, **не подтверждённая финансовыми данными** ставка инвестора $12 000 за минуту (это может быть оборот, а не потерянная прибыль). Ниже показаны **потолки бюджета ошибки**, если всю минуту недоступности считать одинаково дорогой; реальные сервисные потери неаддитивны.

| Цель uptime | Допустимый простой в год | Условный эффект при $12k/мин | Δ к предыдущему уровню | Примерная дополнительная infra/ops цена, в год* |
|---|---:|---:|---:|---:|
| 99,0% | 5 256 мин | $63 072 000 | — | базовый |
| **99,9%** | **525,6 мин** | **$6 307 200** | экономия 4 730,4 мин | базовый стек ADR-001 ($31 200/год infra+SaaS в TCO) |
| 99,95% | 262,8 мин | $3 153 600 | экономия 262,8 мин | **+$12 000/год** (гипотеза standby/ops) |
| 99,99% | 52,56 мин | $630 720 | экономия 210,24 мин | **+$48 000/год** к 99,9% (гипотеза multi-region/ops) |
| 99,999% | 5,256 мин | $63 072 | экономия 47,304 мин | **+$180 000/год** к 99,9% (гипотеза active-active/24×7) |

\* Цена резервирования иллюстративная, **не коммерческий оффер**; значения при 99,95/99,99/99,999 не суммируются. Стартовый пример: $2 600/мес. базовый run-rate, резерв $2 400 до потолка $5 000 без согласования отдельных статей >$500. Требуемое 99,99% с предполагаемым дополнительным $4 000/мес. дало бы $6 600/мес. и нарушило лимит. Расчёт бизнес-выгоды 99,99% по $12k/мин *не обосновывает* её, пока CFO не подтвердит валовую маржу, реальную стоимость отказа конкретного пути, вероятность и возможность 99,99% у PSP. Инвестиционное решение: **начать с 99,9% для каталога/платёжного intent; 99,0% доставки уведомлений**, затем пересмотреть при подтверждённых метриках и ценах. Условная «цена дополнительной девятки» — не универсальная константа; проверка через реальные тарифы и практические failure drills обязательна.

**Пересмотр:** после 30 суток чистой телеметрии, отдельного PSP SLA, первых подтверждённых заказов и CFO cost approval. Предлагаемые значения **не означают действующий договорный SLA**.
