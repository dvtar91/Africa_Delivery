# Диаграмма C4 Container — страновые контуры Africa Delivery

**Статус:** проектная структура, а не утверждённые/развёрнутые кластеры. Mermaid C4Container; каждый контейнер подписан по стране. NG и KE используют одну кодовую базу модульного монолита, но **отдельные хранилища и ключи**. Будущий ZA-контур показан как неактивный. Конкретные местные поставщики NG/KE не выбраны.

```mermaid
C4Container
title Africa Delivery — регионально изолированные контейнеры (предлагаемая схема)
Person(buyer, "Покупатель", "Покупки в своей стране")
Person(seller, "Продавец", "Публикация товаров / KYB")
Person(ops, "Оператор", "Поддержка и сверка")
System_Ext(psp, "Лицензированный PSP", "M-Pesa / Flutterwave / Paystack, договоры не подтверждены")
System_Ext(delivery, "Партнёрская доставка", "Sendbox / Sendy, договоры не подтверждены")
System_Ext(notify, "Шлюз уведомлений", "SMS / WhatsApp, только правомерные сообщения")
Container(router, "Страновой маршрутизатор", "HTTPS", "Определяет страну по явному маршруту без обмена PII")

Boundary(ng, "НИГЕРИЯ — NG-LOCAL, местный ЦОД не выбран") {
 Container(ngApp, "NG: приложение", "OCI / HTTP", "Модульный монолит: каталог, заказ, оплата")
 ContainerDb(ngDb, "NG: PostgreSQL", "PostgreSQL", "Профили, заказы, согласия NG")
 Container(ngWorker, "NG: обработчик событий", "Рабочий процесс", "Outbox, уведомления, сверка")
 ContainerDb(ngBackup, "NG: резерв и журналы", "Защищённое хранилище", "Бэкапы и ключи только в NG")
}
Boundary(ke, "КЕНИЯ — KE-LOCAL, местный ЦОД не выбран") {
 Container(keApp, "KE: приложение", "OCI / HTTP", "Модульный монолит: каталог, заказ, оплата")
 ContainerDb(keDb, "KE: PostgreSQL", "PostgreSQL", "Профили, заказы, согласия KE")
 Container(keWorker, "KE: обработчик событий", "Рабочий процесс", "Outbox, уведомления, сверка")
 ContainerDb(keBackup, "KE: резерв и журналы", "Защищённое хранилище", "Бэкапы и ключи только в KE")
}
Boundary(za, "ЮАР — только после отдельного согласования") {
 Container(zaApp, "ZA: предполагаемое приложение", "OCI", "Не развёрнуто")
 ContainerDb(zaDb, "ZA: предполагаемая БД", "PostgreSQL", "Не развёрнуто")
}
Rel(buyer, router, "Открывает местный рынок", "HTTPS")
Rel(seller, router, "Входит в кабинет продавца", "HTTPS")
Rel(ops, router, "Работает с допуском по стране", "HTTPS")
Rel(router, ngApp, "Запросы NG, без передачи PII в KE", "HTTPS")
Rel(router, keApp, "Запросы KE, без передачи PII в NG", "HTTPS")
Rel(ngApp, ngDb, "Читает и пишет NG-данные", "SQL/TLS")
Rel(keApp, keDb, "Читает и пишет KE-данные", "SQL/TLS")
Rel(ngApp, ngWorker, "События NG после фиксации транзакции", "Внутренний канал")
Rel(keApp, keWorker, "События KE после фиксации транзакции", "Внутренний канал")
Rel(ngDb, ngBackup, "Резервное копирование и журналы в NG", "Шифрованный канал")
Rel(keDb, keBackup, "Резервное копирование и журналы в KE", "Шифрованный канал")
Rel(ngApp, psp, "NG: платёж после договора и legal gate", "TLS API")
Rel(keApp, psp, "KE: платёж после договора и legal gate", "TLS API")
Rel(ngWorker, delivery, "NG: доставка после договора", "TLS API")
Rel(keWorker, delivery, "KE: доставка после договора", "TLS API")
Rel(ngWorker, notify, "NG: уведомления при наличии основания", "TLS API")
Rel(keWorker, notify, "KE: уведомления при наличии основания", "TLS API")
```

**Пояснения:** C4 Container — логические исполняемые части; «страна» — граница развёртывания, а не доказательство независимых центров обработки данных. Маршрутизатор не должен хранить запросы/PII в третьей стране. Статический каталог может публиковаться в CDN после проверки данных; персональные объекты не кешируются общим CDN (ADR-002). Подписи связей обязательны. См. [ADR-003](adr-003-data-residency.md), [схему развёртывания](deployment-diagram.md).
