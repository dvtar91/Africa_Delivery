# C4 Context — Africa Delivery

**Уровень:** C4 System Context; Mermaid C4Context; внешние системы не подразумевают подписанные договоры. Country/data границы требуют Task4 legal gate. Потоки оплат не проходят через собственный лицензированный процессинг: PSP — system of record.

```mermaid
C4Context
title Africa Delivery — MVP system context
Person(buyer, "Покупатель", "Каталог, заказ, оплата, статус")
Person(seller, "Продавец", "KYB, карточки товара, выплаты")
Person(operator, "Оператор", "Возвраты, споры, сверка")
Person(exec, "CEO/CFO", "KPI, контроль стоимости")
System(ad, "Africa Delivery", "Marketplace MVP: catalog, checkout, order, returns")
System_Ext(mpesa, "M-Pesa", "Лицензированный мобильный платёжный провайдер")
System_Ext(flutter, "Flutterwave", "Платёжный провайдер")
System_Ext(paystack, "Paystack", "Альтернативный PSP, subject to contract")
System_Ext(sendbox, "Sendbox", "Доставка / статусы")
System_Ext(sendy, "Sendy", "Доставка / статусы, availability to verify")
System_Ext(wa, "WhatsApp Business API", "Только разрешённые уведомления")
System_Ext(sms, "SMS/USSD gateway", "SMS, USSD только после scope+operator gate")
Rel(buyer, ad, "Ищет товары, создаёт заказ, смотрит статус", "HTTPS")
Rel(seller, ad, "Публикует товары, KYB, смотрит выплаты", "HTTPS")
Rel(operator, ad, "Решает споры и обрабатывает возвраты", "HTTPS")
Rel(exec, ad, "Просматривает отчёты и KPI", "HTTPS")
Rel(ad, mpesa, "Создаёт платёж, принимает webhook/сверку", "TLS API")
Rel(ad, flutter, "Создаёт платёж, принимает webhook/сверку", "TLS API")
Rel(ad, paystack, "Резервный/региональный checkout после договора", "TLS API")
Rel(ad, sendbox, "Создаёт заявку, получает статусы", "TLS API")
Rel(ad, sendy, "Создаёт заявку, получает статусы при доступности", "TLS API")
Rel(ad, wa, "Отправляет opt-in сообщения", "API")
Rel(ad, sms, "Отправляет разрешённые SMS; USSD только при реализации", "API")
```

**Системные границы:** M-Pesa/Flutterwave/Paystack, Sendbox/Sendy, WhatsApp Business API и SMS/USSD — **внешние интеграции, не микросервисы MVP**; включение провайдера зависит от country-method-cost-legal gate. Source: [ADR-001](adr-001-architecture-style.md); [Task1](../Task1/contradictions.md).
