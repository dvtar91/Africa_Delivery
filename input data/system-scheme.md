# Схема
```mermaid
flowchart LR
    Sellers["Sellers<br/>40% Market Share"]

    subgraph Core["Core - Cloud Native"]
        direction TB
        Catalog["Catalog"]
        Inventories["Inventories"]
        Ordering["Ordering - P0"]
        Notifications["Notifications - P0"]
        Fulfillment["Fulfillment"]
        Payments["Payments"]
    end

    Reports["Reports"]

    App["WP / Delivery App<br/>iPhone / Android"]

    Logistics(["Logistics - P0"])
    Couriers["Couriers"]
    PaymentProviders(["Payment Providers<br/>M-PESA"])

    subgraph Advertising["Advertising - P1"]
        Advertisers["Advertisers"]
        Blockchain["Blockchain"]
    end

    Sellers -->|"SaaS / API / USD"| Catalog
    Payments -->|"Payments / API"| Sellers

    Catalog -->|"API"| App
    App --> Ordering
    Notifications --> App

    Payments --> PaymentProviders
    Fulfillment --> Logistics
    Logistics --> Couriers

    Reports -.- Core

    Advertisers --- Blockchain

    classDef core fill:#e7f2eb,stroke:#438363
    classDef external fill:#e6eefb,stroke:#507bb5
    classDef priority fill:#fff0cd,stroke:#d29a30
    classDef provider fill:#f9dddd,stroke:#b86666

    class Catalog,Inventories,Fulfillment,Payments core
    class Sellers,App,Reports,Couriers external
    class Ordering,Notifications,Logistics,Advertisers,Blockchain priority
    class PaymentProviders provider
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
