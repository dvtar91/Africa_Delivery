# Схема
```mermaid
flowchart LR
    Sellers["Sellers"]

    subgraph Core["Core"]
        direction TB
        Catalog["Catalog"]
        Inventories["Inventories"]
        Ordering["Ordering"]
        Reports["Reports"]
        Notifications["Notifications"]
        Payments["Payments"]
        Fulfillment["Fulfillment"]
    end

    DeliveryApp["Delivery App"]

    PaymentProviders(["Payment providers<br/>(M-PESA)"])
    LogisticProviders(["Logistic providers"])

    Sellers -->|"API"| Catalog
    Payments -->|"API"| Sellers

    Catalog --> DeliveryApp
    DeliveryApp --> Ordering
    Notifications --> DeliveryApp

    Payments --> PaymentProviders
    Fulfillment --> LogisticProviders

    Platforms["Apple / Google<br/>iPhone / Android"]
    Features["Features from PM"]
    Couriers["Couriers"]

    DeliveryApp -.-> Platforms
    Features -.-> DeliveryApp
    LogisticProviders -.-> Couriers

    classDef external fill:#e8eef8,stroke:#57759b,color:#172b4d
    classDef core fill:#e8f2ec,stroke:#56836a,color:#183c29
    classDef provider fill:#f8dada,stroke:#b66b6b,color:#532525

    class Sellers,DeliveryApp,Platforms,Features external
    class Catalog,Inventories,Ordering,Reports,Notifications,Payments,Fulfillment core
    class PaymentProviders,LogisticProviders,Couriers provider
```
# Дополнительные параметры из схемы
| Параметр | Значение |
|----------|----------|
| География	| Nigeria, Kenya, South Africa, +15 стран | 
| Целевая доля рынка |	40% |
| Архитектура |	Cloud Native |
| Платформы | iOS, Android |
| Защита данных | GDPR |
| TCO |	Не определён |
| Функциональность | Features from PM |
