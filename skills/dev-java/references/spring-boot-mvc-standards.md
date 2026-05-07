# Spring Boot MVC Standards

> **Scope**: Spring Boot monolith project structure (layer-based and feature-based), Controller/Service/Repository conventions, configuration management, profile strategy, auto-configuration, starter dependencies, actuator, graceful shutdown.

## Table of Contents

1. Project Structure
2. Layer Responsibilities and Conventions
3. DTO / VO / PO Conventions
4. Configuration Management
5. Dependency and Starter Conventions
6. Actuator, Health Checks, and Graceful Shutdown

---

## 1. Project Structure

### Layer-Based Structure (recommended for small-to-medium projects)

The application root class (`@SpringBootApplication`) sits in the root package. All other packages are immediate children. Spring's component scan discovers everything below the root.

```
com.company.project
├── Application.java                 # @SpringBootApplication entry point
├── config/                          # @Configuration classes, WebMvcConfigurer, SecurityConfig
├── controller/                      # @RestController classes, one per aggregate/resource
│   └── advice/                      # @ControllerAdvice for global exception handling
├── service/                         # @Service classes (interfaces + implementations)
│   └── impl/                        # Implementation classes if separating interface from impl
├── repository/                      # Spring Data repositories, MyBatis mappers
├── model/                           # Domain model
│   ├── entity/                      # JPA entities / MyBatis POJOs
│   ├── dto/                         # Data Transfer Objects (request/response)
│   ├── vo/                          # View Objects (read-only presentation data)
│   └── enums/                       # Business enumerations
├── common/                          # Cross-cutting utilities
│   ├── constant/                    # Constants classes
│   ├── exception/                   # Custom exception classes
│   ├── util/                        # Utility classes (static methods, private constructor)
│   └── result/                      # Unified response wrapper (Result<T>)
├── interceptor/                     # HandlerInterceptor implementations
├── filter/                          # Servlet Filter implementations
├── aspect/                          # AOP @Aspect classes
└── task/                            # @Scheduled tasks
```

### Feature-Based Structure (recommended for larger projects)

Group all classes related to a feature/module together. Each feature package contains its own controller, service, repository, and model. Shared code lives in a `common` or `shared` package.

```
com.company.project
├── Application.java
├── common/                          # Shared across all features
│   ├── config/
│   ├── exception/
│   ├── result/
│   └── util/
├── order/                           # Order feature module
│   ├── OrderController.java
│   ├── OrderService.java
│   ├── OrderRepository.java
│   ├── Order.java                   # Entity
│   ├── OrderDto.java                # DTO
│   └── OrderStatus.java             # Enum
├── product/                         # Product feature module
│   ├── ProductController.java
│   ├── ProductService.java
│   ├── ...
└── user/                            # User feature module
    ├── ...
```

**Selection guide**: Use layer-based for projects with fewer than 15 entities where one team owns the entire codebase. Use feature-based when the project exceeds 15 entities, has multiple development teams, or is a candidate for future microservices decomposition (each feature package maps naturally to a microservice).

---

## 2. Layer Responsibilities and Conventions

### Controller Layer

Controllers handle HTTP concerns only: request parsing, response formatting, validation triggering, status codes. They contain zero business logic. A controller method should be 5-15 lines — if it exceeds 20 lines, business logic has leaked in.

```java
@RestController
@RequestMapping("/api/v1/orders")
@RequiredArgsConstructor
@Tag(name = "Order Management")
public class OrderController {

    private final OrderService orderService;

    @PostMapping
    @Operation(summary = "Create a new order")
    public ResponseEntity<Result<OrderDto>> createOrder(
            @Valid @RequestBody OrderCreateRequest request) {
        OrderDto order = orderService.createOrder(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(Result.success(order));
    }
}
```

Rules: Never inject a `Repository` into a `Controller` — always go through `Service`. Never catch exceptions in controllers — let `@ControllerAdvice` handle them. Use `@Valid` or `@Validated` on request bodies for bean validation. Return `ResponseEntity<T>` for explicit HTTP status control.

### Service Layer

Services contain business logic, orchestrate repositories and other services, and define transaction boundaries. Service interfaces are required for all services — this enables AOP proxying and testability.

```java
public interface OrderService {
    OrderDto createOrder(OrderCreateRequest request);
    OrderDto getOrder(Long orderId);
    Page<OrderDto> listOrders(OrderQueryRequest query, Pageable pageable);
}

@Service
@RequiredArgsConstructor
@Slf4j
public class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;
    private final InventoryService inventoryService;
    private final OrderMapper orderMapper;

    @Override
    @Transactional
    public OrderDto createOrder(OrderCreateRequest request) {
        // 1. Validate business rules
        // 2. Reserve inventory
        // 3. Create order entity
        // 4. Publish domain event
        // 5. Map to DTO and return
    }
}
```

Rules: Place `@Transactional` on service methods, never on controllers or repositories. Use `@Transactional(readOnly = true)` on query methods — it enables Hibernate flush-mode optimization. Service methods should operate on DTOs at the boundary and entities internally. Never expose entities outside the service layer.

### Repository Layer

Repositories handle data access only. No business logic, no DTO mapping, no validation.

For Spring Data JPA: Extend `JpaRepository<Entity, IdType>`. Use method name derivation for simple queries, `@Query` for custom JPQL/SQL, and `Specification` or `QueryDSL` for dynamic queries.

For MyBatis: Annotate mapper interfaces with `@Mapper`. Prefer XML mapper files over annotation-based SQL for complex queries. Keep SQL readable — one clause per line.

---

## 3. DTO / VO / PO Conventions

**PO (Persistent Object) / Entity**: Mirrors the database table. Annotated with JPA annotations or MyBatis mapping. Contains domain behavior if following rich domain model. Never returned directly from a controller.

**DTO (Data Transfer Object)**: Carries data across boundaries. Separate DTOs for request and response: `OrderCreateRequest`, `OrderUpdateRequest`, `OrderDto` (response). DTOs are flat — do not nest entity relationships deeply. Use records (Java 16+) for DTOs when possible.

**VO (Value Object)**: Read-only objects for presentation. Often combines data from multiple entities. Immutable. Example: `OrderSummaryVo` containing order details + customer name + delivery status.

**Mapping between layers**: Use MapStruct (compile-time, zero-reflection) over BeanUtils (runtime reflection, error-prone) or manual mapping. Define mapper interfaces annotated with `@Mapper(componentModel = "spring")` for Spring integration.

```java
@Mapper(componentModel = "spring")
public interface OrderMapper {
    OrderDto toDto(Order entity);
    Order toEntity(OrderCreateRequest request);
}
```

---

## 4. Configuration Management

**application.yml as the primary config file.** Use YAML over properties for hierarchical configuration — it is more readable.

**Profile strategy**: `application.yml` (shared defaults), `application-dev.yml` (local development), `application-test.yml` (test/CI), `application-staging.yml`, `application-prod.yml`. Activate via `spring.profiles.active`. Never put production secrets in config files — use environment variables, Vault, or cloud secrets manager.

**Custom configuration properties**: Use `@ConfigurationProperties` with a prefix, not `@Value`. It provides type safety, validation, and IDE auto-completion.

```java
@ConfigurationProperties(prefix = "app.order")
@Validated
public record OrderProperties(
    @NotNull @Min(1) Integer maxItemsPerOrder,
    @NotNull Duration paymentTimeout,
    @NotNull String notificationEndpoint
) {}
```

Register with `@EnableConfigurationProperties(OrderProperties.class)` or `@ConfigurationPropertiesScan`.

---

## 5. Dependency and Starter Conventions

Use Spring Boot starters as the primary way to add functionality: `spring-boot-starter-web`, `spring-boot-starter-data-jpa`, `spring-boot-starter-security`, etc. Starters bring in transitive dependencies with tested, compatible versions.

Pin the Spring Boot parent POM version. Never mix Spring Boot versions within a project. Use the Spring Boot BOM (`spring-boot-dependencies`) for version management.

For third-party dependencies not managed by Spring Boot, declare versions in a `<properties>` block or a separate BOM. Never hardcode version numbers in individual `<dependency>` declarations.

Exclude unnecessary transitive dependencies to reduce attack surface and startup time. Common exclusions: `spring-boot-starter-logging` (when switching to Log4j2), `tomcat-embed-*` (when using Undertow or Netty).

---

## 6. Actuator, Health Checks, and Graceful Shutdown

Enable Actuator for production monitoring: `spring-boot-starter-actuator`. Expose only necessary endpoints (health, info, metrics) via configuration. Never expose all actuator endpoints in production.

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus
  endpoint:
    health:
      show-details: when_authorized
```

Implement custom health indicators for critical dependencies (database, cache, external APIs) via `HealthIndicator`.

Enable graceful shutdown to allow in-flight requests to complete: `server.shutdown=graceful` with `spring.lifecycle.timeout-per-shutdown-phase=30s`. This is critical for zero-downtime deployments.

Configure liveness and readiness probes for Kubernetes: `/actuator/health/liveness` and `/actuator/health/readiness`. Liveness tells the orchestrator "I'm alive, don't restart me." Readiness tells the load balancer "I'm ready to accept traffic."