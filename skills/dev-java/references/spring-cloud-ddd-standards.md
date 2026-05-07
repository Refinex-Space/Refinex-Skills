# Spring Cloud DDD Microservices Standards

> **Scope**: DDD tactical patterns (Entity, Value Object, Aggregate, Domain Event, Repository, Domain Service, Application Service), bounded context mapping, hexagonal architecture layout, Spring Cloud component selection, inter-service communication, CQRS/Event Sourcing basics.

## Table of Contents

1. Bounded Context and Service Decomposition
2. DDD Tactical Patterns in Java
3. Hexagonal Architecture Project Structure
4. Spring Cloud Component Selection
5. Inter-Service Communication Patterns
6. CQRS and Event Sourcing Basics

---

## 1. Bounded Context and Service Decomposition

Every microservice owns exactly one bounded context. A bounded context is a semantic boundary within which a particular domain model applies consistently. The same real-world concept (e.g., "Customer") may have different representations in different bounded contexts: the Order context sees a customer ID and shipping address; the CRM context sees a full profile with history and preferences.

**Decomposition rules**: Decompose by business capability, not by technical layer. An "Order Service" is correct; a "Database Service" or "Validation Service" is wrong. Each service owns its data — no shared databases between services. If two services need the same data, they synchronize through events or APIs, never through a shared database.

**Service sizing**: A microservice should be owned and deployable by a single team (2-pizza team). If a service requires multiple teams to coordinate on a release, it is too large. If a service has fewer than 3 entities and no independent business value, it is too small — consider merging it with a related service.

**Context mapping patterns**: Anti-Corruption Layer (ACL) when integrating with legacy systems or external APIs — translate their model into your domain language at the boundary. Shared Kernel when two contexts co-evolve tightly and share a small, explicitly defined subset of the model. Customer-Supplier when one context depends on another's output but cannot influence it.

---

## 2. DDD Tactical Patterns in Java

### Entity

An object with a persistent identity that matters across time. Two entities with the same attributes but different IDs are different entities (e.g., two orders with the same items but different order IDs).

```java
@Entity
@Table(name = "orders")
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderItem> items = new ArrayList<>();

    // Domain behavior — NOT anemic getters/setters
    public void addItem(Product product, int quantity) {
        validateCanModify();
        items.add(new OrderItem(this, product, quantity));
    }

    public void cancel(String reason) {
        if (status != OrderStatus.PENDING) {
            throw new OrderCannotBeCancelledException(id, status);
        }
        this.status = OrderStatus.CANCELLED;
        registerEvent(new OrderCancelledEvent(this.id, reason));
    }

    private void validateCanModify() {
        if (status != OrderStatus.DRAFT) {
            throw new OrderNotModifiableException(id, status);
        }
    }
}
```

Entities have rich behavior. If an entity class has only getters and setters, the model is anemic and the business logic is scattered across service classes — this is a critical design smell.

### Value Object

An object defined by its attributes, not its identity. Two value objects with the same attributes are equal. Value objects are immutable.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        Objects.requireNonNull(amount, "Amount must not be null");
        Objects.requireNonNull(currency, "Currency must not be null");
        if (amount.scale() > currency.getDefaultFractionDigits()) {
            throw new IllegalArgumentException("Scale exceeds currency precision");
        }
    }

    public Money add(Money other) {
        requireSameCurrency(other);
        return new Money(this.amount.add(other.amount), this.currency);
    }
}
```

Use value objects to eliminate primitive obsession: `Money` instead of `BigDecimal`, `EmailAddress` instead of `String`, `OrderId` instead of `Long`.

### Aggregate

A cluster of entities and value objects treated as a single unit for data changes. The aggregate root is the only entry point for external access. All modifications go through the aggregate root, which enforces invariants.

Rules: Aggregates should be small — prefer single-entity aggregates when possible. Reference other aggregates by ID, not by object reference. Transactions should not span multiple aggregates — use eventual consistency via domain events.

### Domain Event

An immutable record of something that happened in the domain. Named in past tense: `OrderPlacedEvent`, `PaymentConfirmedEvent`, `InventoryReservedEvent`.

```java
public record OrderPlacedEvent(
    Long orderId,
    Long customerId,
    List<OrderItemInfo> items,
    Instant occurredAt
) {
    public OrderPlacedEvent {
        Objects.requireNonNull(orderId);
        if (occurredAt == null) occurredAt = Instant.now();
    }
}
```

Within a bounded context, publish events via Spring's `ApplicationEventPublisher`. Across bounded contexts, publish to a message broker (Kafka, RabbitMQ). Use `@TransactionalEventListener(phase = AFTER_COMMIT)` to ensure events fire only after the transaction succeeds.

### Repository

The repository pattern provides collection-like access to aggregates. In DDD, a repository exists per aggregate root, not per entity. The domain layer defines the repository interface; the infrastructure layer provides the implementation.

### Domain Service

Logic that doesn't naturally belong to a single entity or value object. Example: transferring money between two accounts involves two Account entities — neither owns the transfer logic. Domain services are stateless and operate on entities/value objects.

### Application Service

Orchestrates domain objects, coordinates transactions, and maps between DTOs and domain objects. Application services are thin — they delegate to domain objects for business logic. They are the entry point for use cases.

---

## 3. Hexagonal Architecture Project Structure

```
com.company.service.order
├── application/                     # Use case orchestration (Application Services)
│   ├── port/
│   │   ├── in/                      # Inbound ports (interfaces for use cases)
│   │   │   └── CreateOrderUseCase.java
│   │   └── out/                     # Outbound ports (interfaces for infra)
│   │       ├── OrderRepository.java
│   │       ├── PaymentGateway.java
│   │       └── EventPublisher.java
│   └── service/                     # Use case implementations
│       └── OrderApplicationService.java
├── domain/                          # Pure domain model (NO framework dependencies)
│   ├── model/
│   │   ├── Order.java               # Aggregate root
│   │   ├── OrderItem.java           # Entity within aggregate
│   │   ├── Money.java               # Value object
│   │   └── OrderStatus.java         # Enum
│   ├── event/
│   │   └── OrderPlacedEvent.java    # Domain event
│   └── service/
│       └── PricingService.java      # Domain service
├── adapter/                         # Framework integrations
│   ├── in/                          # Inbound adapters (drive the application)
│   │   ├── web/
│   │   │   ├── OrderController.java
│   │   │   └── dto/
│   │   │       ├── CreateOrderRequest.java
│   │   │       └── OrderResponse.java
│   │   └── messaging/
│   │       └── OrderEventListener.java
│   └── out/                         # Outbound adapters (driven by the application)
│       ├── persistence/
│       │   ├── OrderJpaRepository.java
│       │   ├── OrderJpaEntity.java  # JPA-specific entity (separate from domain)
│       │   └── OrderPersistenceAdapter.java
│       ├── payment/
│       │   └── StripePaymentAdapter.java
│       └── messaging/
│           └── KafkaEventPublisher.java
└── config/                          # Spring configuration
    └── OrderModuleConfig.java
```

**The critical rule**: The `domain` package has ZERO dependencies on Spring, JPA, MyBatis, or any framework. It contains only pure Java. The `application` layer depends on the domain. The `adapter` layer depends on both the application and domain layers, plus frameworks. Dependencies flow inward — never outward.

---

## 4. Spring Cloud Component Selection

**Service Discovery**: Spring Cloud Netflix Eureka (self-hosted) or Spring Cloud Kubernetes (K8s-native). Prefer Kubernetes-native service discovery when running on K8s.

**API Gateway**: Spring Cloud Gateway (reactive, non-blocking). Replaces the deprecated Netflix Zuul. Handles routing, rate limiting, circuit breaking, and authentication at the edge.

**Configuration**: Spring Cloud Config Server for centralized configuration. Alternatives: Consul, Nacos. For Kubernetes, consider ConfigMaps + Secrets with Spring Cloud Kubernetes.

**Circuit Breaker**: Resilience4j (replaces deprecated Netflix Hystrix). Annotate with `@CircuitBreaker`, `@Retry`, `@RateLimiter`, `@Bulkhead`. Configure thresholds in application.yml.

**Distributed Tracing**: Micrometer Tracing with OpenTelemetry (replaces Spring Cloud Sleuth). Propagates trace IDs across service calls. Export to Jaeger, Zipkin, or Grafana Tempo.

**Message Broker Integration**: Spring Cloud Stream with Kafka or RabbitMQ binder. Abstracts messaging details behind `Supplier`, `Function`, `Consumer` functional interfaces.

---

## 5. Inter-Service Communication Patterns

**Synchronous (REST/gRPC)**: Use `WebClient` (reactive) or `RestClient` (blocking, Spring 6.1+) with Resilience4j circuit breaker. Never call another service synchronously inside a transaction — if the call fails, the local transaction is wasted. Use the Saga pattern for distributed transactions.

**Asynchronous (Events)**: Prefer event-driven communication for cross-context operations. Publish domain events to Kafka/RabbitMQ. Consumer services react independently. This achieves loose coupling and resilience — if a consumer is down, the event is retained in the broker.

**Saga Pattern**: For distributed transactions that span multiple services, use the Saga pattern (choreography or orchestration). Choreography: each service publishes an event and the next service reacts. Orchestration: a central coordinator directs each step. Prefer choreography for simple flows (2-3 steps), orchestration for complex flows (4+ steps with compensation).

---

## 6. CQRS and Event Sourcing Basics

**CQRS (Command Query Responsibility Segregation)**: Separate the write model (commands) from the read model (queries). The write side enforces invariants and publishes events. The read side builds optimized views from events. This is justified when read and write patterns differ significantly — e.g., complex aggregation queries that would be slow against the normalized write model.

**Event Sourcing**: Instead of storing the current state, store the sequence of events that produced it. The current state is derived by replaying events. Use when audit trail is a hard requirement, when you need temporal queries ("what was the account balance on March 15?"), or when the domain is inherently event-driven (banking, trading).

Do NOT adopt CQRS or Event Sourcing by default. They add significant complexity (eventual consistency, event schema evolution, projection management). Use them only when the complexity is justified by specific requirements. A simple CRUD service does not need CQRS.