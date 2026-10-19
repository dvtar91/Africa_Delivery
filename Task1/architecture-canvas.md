# Architecture Canvas — Africa Delivery

**Горизонт:** MVP к **15.10.2026** (плановое обязательство из исходных писем); пилот **Нигерия + Кения**, затем ЮАР. **Статус:** рабочее видение, не утверждённое инвестором.

| Область | Содержание | Источники |
|---|---|---|
| **Проблема и ценность** | Недорогой мультикатегорийный маркетплейс для покупателей и продавцов в Африке; доверие, доступная доставка и локальные способы оплаты. Конкуренты Jumia/Takealot присутствуют, «рынка нет» нельзя считать фактом. | [description.md](../description.md); [input_data/marketing-brief.md](../input_data/marketing-brief.md) |
| **Успех MVP** | Покупатель видит товар → оформляет заказ → платит → получает подтверждение; продавец может разместить товар и получить выплату. Ориентиры **5 000 SKU, 100 продавцов**, 2 страны; базовая аналитика CEO. Приёмка выплат и доставки требует отдельного gate. | [description.md](../description.md); [input_data/letter-investor.md](../input_data/letter-investor.md) |
| **Сроки** | Рекламная кампания/запуск **15.10**, страницы в app stores **к 01.10**; медиа уже выкуплены на **$180 000**. Даты из исходного кейса, не фактически подтверждённые поставки. | [input_data/meeting-investor.md](../input_data/meeting-investor.md); [input_data/marketing-brief.md](../input_data/marketing-brief.md) |
| **Финансовые и кадровые рамки** | **≤$5 000/мес.** на всю регулярную техническую инфраструктуру/SaaS первые 6 месяцев; согласование >$500/мес.; **6 контракторов до декабря**, runway 9 мес.; без годовой предоплаты. | [input_data/letter-cfo.md](../input_data/letter-cfo.md) |
| **Внешние зависимости** | Лицензированные PSP (M-Pesa, Flutterwave, Paystack по странам), Sendbox/Sendy, SMS/USSD и WhatsApp; локальные data/consent требования. | [description.md](../description.md); [input_data/lawyer-letter.md](../input_data/lawyer-letter.md); [input_data/system-scheme.md](../input_data/system-scheme.md) |
| **Драйверы качества** | 99,99% — запрос инвестора/CTO, а **не подтверждённый SLO**; устойчивость к плохой 3G/4G связи, легковесный клиент, безопасные платежи, региональные границы данных, восстановление после отказов. | [input_data/meeting-investor.md](../input_data/meeting-investor.md); [input_data/letter-cto.md](../input_data/letter-cto.md); [input_data/marketing-brief.md](../input_data/marketing-brief.md) |
| **Архитектурное направление (гипотеза)** | Простой эволюционный backend с модульными границами, API-адаптерами PSP/логистики, очередью для асинхронных побочных действий; отказ от 40–50 сервисов **до** количественного сравнения альтернатив в ADR-001. | [input_data/letter-cto.md](../input_data/letter-cto.md); [input_data/letter-cfo.md](../input_data/letter-cfo.md) |
| **Неподвижные ограничения** | Нельзя обойти законы через решение инвестора; нельзя обещать все 29 P0 при фиксированной ёмкости команды; нельзя считать $9 000 инфраструктурным лимитом; лицензирование платежей через партнёра. | [input_data/lawyer-letter.md](../input_data/lawyer-letter.md); [input_data/list-of-functions-product-manager.md](../input_data/list-of-functions-product-manager.md); [input_data/letter-cfo.md](../input_data/letter-cfo.md) |
| **Главные риски** | Разрыв между рекламой и продуктом (доставка/возвраты/языки/live); покупная SMS-база без подтверждённых согласий; размещение PII; 10 млн пользователей без load-модели; отсутствие местной продуктовой команды. | [input_data/marketing-brief.md](../input_data/marketing-brief.md); [input_data/lawyer-letter.md](../input_data/lawyer-letter.md); [input_data/letter-cto.md](../input_data/letter-cto.md); [input_data/company-structure.md](../input_data/company-structure.md) |
| **Границы MVP (предложение)** | Включить: каталог, минимальный onboarding продавцов с проверкой, заказ, оплату через согласованного PSP, статус и уведомление, оперируемый процесс поддержки/возврата. Отложить: токены, кредитный скоринг, ML, развитые кабинеты, собственный логистический движок, полноценные live-streams; **требуется решение об изменении рекламных обязательств**. | [input_data/list-of-functions-product-manager.md](../input_data/list-of-functions-product-manager.md); [input_data/marketing-brief.md](../input_data/marketing-brief.md) |

## Допущения

1. **A-01:** на MVP достаточно одной операционной конфигурации на страну и партнёрских PSP/доставки при наличии договоров и допустимых комиссий; подтверждение — Task5.
2. **A-02:** временно действует консервативная сегрегация персональных данных по юрисдикциям; конкретные трансграничные потоки **не разрешены** до заключения местных юристов; подтверждение — Task4.
3. **A-03:** разделяем **ёмкость будущего масштабирования** и **реально оплачиваемую стартовую мощность**; нагрузочные сценарии и сравнение решений выполняются в Task2/3.
4. **A-04:** инвариант первого релиза — оплачиваемый и подтверждённый заказ, а не все рекламные возможности; любые расхождения с рекламой выносятся CEO/инвестору **до запуска**.
5. **A-05:** CTO выбирает технологический вариант после расчёта TCO и принятия ограничений CFO; окончательный архитектурный стиль здесь не утверждается.

**Критические решения:** [Task1/contradictions.md](contradictions.md) · **Вопросы:** [Task1/open-questions.md](open-questions.md) · **Матрица:** [input_data/requirements-traceability.md](../input_data/requirements-traceability.md).

## Контроль полноты входных ограничений

## Полная трассировка 28 записей исходного аудита

**Источник:** [requirements-traceability.md](../input_data/requirements-traceability.md). Эта таблица — **классификация Task1**, а не изменение исходных данных. «Конфликт» означает несовместимые обязательства в одном релизе; «риск/напряжение» требует проверки; «пробел» означает отсутствующий сценарий; «ошибка документации» исправляется без бизнес-арбитража.

| ID | Класс в Task1 | Предмет | Владелец | Обработка и решение |
|---|---|---|---|---|
| [R-01](../input_data/requirements-traceability.md) | Ошибка документации | Ошибка TCO-лимита | CFO; архитектор | Исправить TCO; $5 000/мес. включает тех-SaaS |
| [R-02](../input_data/requirements-traceability.md) | Конфликт требований | Ресурсный конфликт CTO/CFO | CFO; CTO; CEO | C-01: TCO и штатный лимит до ADR |
| [R-03](../input_data/requirements-traceability.md) | Неопределённость | Разные прогнозы и единицы нагрузки | CTO; маркетинг; CEO | Q-05: MAU, покупатели, RPS, стресс-сценарии |
| [R-04](../input_data/requirements-traceability.md) | Неопределённость | Два последовательных срока, не логический конфликт | CEO; маркетинг | Q-01: gate публикации 01.10 и запуска 15.10 |
| [R-05](../input_data/requirements-traceability.md) | Конфликт требований | Полный список P0 против ограниченного MVP | CEO; инвестор | C-02: подписанный MVP scope |
| [R-06](../input_data/requirements-traceability.md) | Конфликт требований | Микросервисный подход против ресурсов | CTO; CFO | C-01: количественное сравнение архитектур |
| [R-07](../input_data/requirements-traceability.md) | Конфликт требований | Self-hosted по умолчанию против CN.MSV.01 | CTO | C-08: исключения для managed-сервисов |
| [R-08](../input_data/requirements-traceability.md) | Неопределённость | Запрет синхронности строже CN.LCP.05; не взаимоисключение | CTO | ADR-001: выбрать стиль API, уточнить CNCF-цель |
| [R-09](../input_data/requirements-traceability.md) | Напряжение / риск | SLO/стоимость не доказаны, не логически несовместимы | CTO; CFO | Q-05: оценить error budget и TCO |
| [R-10](../input_data/requirements-traceability.md) | Неопределённость | Предварительная правовая трактовка | Юрист | Q-04: legal gate и консервативная локализация |
| [R-11](../input_data/requirements-traceability.md) | Напряжение / риск | Маркетинговая рассылка без подтверждённого правового основания | Юрист; маркетинг | C-05: приостановить до legal sign-off |
| [R-12](../input_data/requirements-traceability.md) | Конфликт требований | Публичные методы оплаты шире MVP | CEO; CFO; юрист | C-07: PSP матрица и публичные обещания |
| [R-13](../input_data/requirements-traceability.md) | Пробел требований | Нет settlement в MVP при требовании same-day | CFO; Product | C-07: проверить выплату по договорам PSP |
| [R-14](../input_data/requirements-traceability.md) | Конфликт требований | Собственный движок 6 мес. против MVP 8 недель | CEO; CTO | C-06: partner-first для MVP |
| [R-15](../input_data/requirements-traceability.md) | Конфликт требований | Возвраты к запуску против плана на год | CEO; маркетинг | C-03: возвраты или пересмотр обещания |
| [R-16](../input_data/requirements-traceability.md) | Конфликт требований | Пять языков к запуску против года | CEO; маркетинг | C-04: согласовать языковой scope |
| [R-17](../input_data/requirements-traceability.md) | Ошибка документации | 60%/100% мобильного трафика без разграничения | Product; архитектор | Уточнить статистику рынка и проектный канал |
| [R-18](../input_data/requirements-traceability.md) | Пробел требований | USSD/SMS охват без MVP-флоу заказа | CEO; Product | C-09: scope USSD и договор оператора |
| [R-19](../input_data/requirements-traceability.md) | Напряжение / риск | Простая регистрация совместима с KYC, но бейдж требует доказательств | Product; Compliance | C-10: gate верификации до бейджа |
| [R-20](../input_data/requirements-traceability.md) | Ошибка документации | 12–15 всего vs +15 в схеме | Maintainer | Исправить формулировку в схеме |
| [R-21](../input_data/requirements-traceability.md) | Ошибка документации | Отсутствие конкурентов vs Jumia/Takealot | CEO; маркетинг | Исправить вводное позиционирование |
| [R-22](../input_data/requirements-traceability.md) | Напряжение / риск | Высокое качество изображений vs 3G/<2 сек., требует измерения | CTO; Product | Performance budget и тесты |
| [R-23](../input_data/requirements-traceability.md) | Пробел требований | Live-stream 17.10 без описанной реализации | CEO; маркетинг | Go/no-go партнёрского стриминга |
| [R-24](../input_data/requirements-traceability.md) | Ошибка документации | Некорректные пути и имена файлов | Maintainer | Исправить ссылки/названия |
| [R-25](../input_data/requirements-traceability.md) | Статус исполнения | Статус артефактов на момент первичного аудита | Maintainer | Task1 создан; Task2–5 проверить отдельно |
| [R-26](../input_data/requirements-traceability.md) | Пробел требований | Cloud Native без матрицы тестов | CTO; DevOps | Task3: контроль CN.* → проверка |
| [R-27](../input_data/requirements-traceability.md) | Ошибка документации | OpenSLO и этапы перехода неоднозначны | Maintainer | Уточнить формат и шестимесячный этап |
| [R-28](../input_data/requirements-traceability.md) | Неопределённость | $12k/мин — гипотеза инвестора, не P&L | CFO; инвестор | TCO чувствительность; не смешивать GMV и прибыль |

**Сводка:** конфликты — 8; риски/напряжения — 4; неопределённости — 5; пробелы — 4; ошибки документации — 6; статус — 1. Все 28 ID представлены ровно по одному разу.



**Дополнение к Canvas:** R-18 (USSD-заказ) и R-23 (live-stream) — не реализованные по умолчанию функции; требуют go/no-go и партнёрских соглашений. R-19 — риск доверия: self-onboarding не равен автоматическому статусу «проверен». R-22 — бюджет изображения/времени загрузки должен проверяться на дешёвых Android и 3G. R-28 — $12 000/мин не подтверждены финансовой отчётностью, применять как сценарий чувствительности. R-25 — снимок первоначального аудита: после подготовки Task1 его состояние изменилось, а Task2–Task5 не следует считать автоматически выполненными.

