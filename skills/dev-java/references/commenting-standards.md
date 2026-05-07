# Commenting Standards

> **Scope**: Javadoc for classes, interfaces, methods, fields, POJOs; inline comments; XML/YAML/Properties file comments; TODO/FIXME conventions.

## Table of Contents

1. Javadoc Standards
2. Inline Comment Rules
3. POJO and DTO Comments
4. Configuration File Comments (XML, YAML, Properties)
5. TODO/FIXME/HACK Conventions

---

## 1. Javadoc Standards

Every public class, interface, enum, and annotation must have a Javadoc comment. Every public and protected method must have a Javadoc comment. Private methods may optionally have Javadoc if the logic is non-obvious.

### Class/Interface Javadoc

The class Javadoc must include a one-sentence summary (the first sentence, ending with a period), a longer description if needed, and `@author` and `@since` tags.

```java
/**
 * Manages the lifecycle of customer orders from placement to fulfillment.
 *
 * <p>This service handles order validation, inventory reservation, payment
 * processing, and shipping coordination. It serves as the primary entry
 * point for all order-related business operations.</p>
 *
 * <p>Thread safety: This class is thread-safe. All mutable state is
 * protected by internal synchronization.</p>
 *
 * @author zhangsan
 * @since 1.0.0
 * @see OrderRepository
 * @see PaymentService
 */
public class OrderService { ... }
```

### Method Javadoc

Method Javadoc must include: what the method does (not how), all parameters with `@param`, the return value with `@return` (unless void), and all checked exceptions with `@throws`. Describe parameter constraints (nullable? range? format?).

```java
/**
 * Finds all orders placed by the specified customer within the given date range.
 *
 * <p>Results are sorted by order date descending. Returns an empty list if
 * no orders match — never returns null.</p>
 *
 * @param customerId the unique identifier of the customer, must not be null
 * @param startDate  the inclusive start of the date range, must not be null
 * @param endDate    the inclusive end of the date range, must be after startDate
 * @return an unmodifiable list of matching orders, possibly empty
 * @throws IllegalArgumentException if endDate is before startDate
 * @throws CustomerNotFoundException if no customer exists with the given ID
 */
public List<OrderDto> findOrdersByCustomer(
        Long customerId, LocalDate startDate, LocalDate endDate) { ... }
```

### Field Javadoc

Public and protected fields must have Javadoc. Constants should explain the value's meaning, not just restate the name.

```java
/**
 * Maximum number of retry attempts for payment processing before
 * the order is moved to the manual review queue.
 */
public static final int MAX_PAYMENT_RETRIES = 3;
```

### Javadoc anti-patterns to avoid

Never write Javadoc that restates the method name: `/** Gets the name. */ public String getName()` is worse than no Javadoc at all — it adds noise without information. If the method name already says everything, add value: describe constraints, edge cases, or return value semantics.

Never leave empty Javadoc tags: `@param id` with no description is a violation. Either document the parameter meaningfully or omit the Javadoc entirely.

Never use `@author` on methods — it belongs on classes only. Use version control for method-level authorship tracking.

---

## 2. Inline Comment Rules

Inline comments explain **why**, not **what**. Code should be self-documenting for what it does through clear naming. Comments are for the reasoning behind non-obvious decisions.

```java
// Good — explains WHY
// Use insertion sort for small arrays because it has lower overhead than
// merge sort for n < 47 (benchmarked on JDK 21, see PERF-1234)
if (array.length < INSERTION_SORT_THRESHOLD) {
    insertionSort(array, fromIndex, toIndex);
}

// Bad — explains WHAT (the code already says this)
// Check if array length is less than threshold
if (array.length < INSERTION_SORT_THRESHOLD) {
```

Comment blocks before complex algorithms should explain the approach, not repeat the code line by line. Use `//` for single-line comments, `/* */` for multi-line blocks within methods. Never use `/** */` Javadoc syntax for inline comments.

Delete commented-out code. It belongs in version control history, not in the codebase. Commented-out code creates confusion about whether it is intentional, temporary, or forgotten.

---

## 3. POJO and DTO Comments

For POJOs, DTOs, VOs, and entity classes, every field should have a brief comment explaining its business meaning, especially when the field name alone is insufficient.

```java
public class OrderCreateRequest {
    /** Customer's unique identifier in the CRM system. */
    private Long customerId;

    /** List of product SKUs with quantities. Must contain at least one item. */
    private List<OrderItemRequest> items;

    /**
     * Desired delivery date. If null, the system assigns the earliest
     * available date based on inventory and shipping capacity.
     */
    @DateTimeFormat(pattern = "yyyy-MM-dd")
    private LocalDate preferredDeliveryDate;

    /** Coupon code for discount. Case-insensitive. Validated against promotion service. */
    private String couponCode;
}
```

For enum classes, every constant should be documented:

```java
public enum OrderStatus {
    /** Order created but not yet paid. Can be cancelled by customer. */
    PENDING,
    /** Payment confirmed. Inventory reserved. Cannot be cancelled. */
    CONFIRMED,
    /** Order shipped. Tracking number assigned. */
    SHIPPED,
    /** Order delivered and signed by customer. */
    DELIVERED,
    /** Order cancelled by customer or system. Inventory released. */
    CANCELLED
}
```

---

## 4. Configuration File Comments

### XML (Spring, MyBatis, Maven)

Use XML comments (`<!-- -->`) to explain non-obvious configurations. Group related configurations with section headers.

```xml
<!-- ==================== Data Source Configuration ==================== -->
<!-- Primary data source for read-write operations. Connection pool managed
     by HikariCP with a max pool size of 20 (tuned for 4-core, 8GB instance). -->
<bean id="dataSource" class="com.zaxxer.hikari.HikariDataSource">
    ...
</bean>
```

### YAML (Spring Boot application.yml)

Use `#` comments to document non-default values, explain why a value was chosen, and mark environment-specific overrides.

```yaml
spring:
  datasource:
    hikari:
      # Max pool size = 2 * CPU cores + effective_spindle_count
      # For 4-core cloud VM with SSD: 2 * 4 + 1 = 9, rounded to 10
      maximum-pool-size: 10
      # Connection timeout set higher than default (30s) to accommodate
      # slow VPN connections in staging environment
      connection-timeout: 45000
```

### Properties files

Use `#` comments. Group properties by function with blank line separators and section headers.

```properties
# ===== Server Configuration =====
server.port=8080
# Enable graceful shutdown to finish in-flight requests (max 30s)
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

---

## 5. TODO/FIXME/HACK Conventions

Every `TODO`, `FIXME`, and `HACK` comment must include a responsible person (or team) and a ticket reference. Orphan TODOs are technical debt that never gets addressed.

```java
// TODO(zhangsan, JIRA-1234): Replace with distributed cache when Redis cluster is provisioned
private final Map<String, UserProfile> localCache = new ConcurrentHashMap<>();

// FIXME(lisi, BUG-5678): Race condition when two threads update the same order simultaneously.
// Temporary workaround: synchronized block. Proper fix requires optimistic locking on OrderEntity.
synchronized (this) {
    order.setStatus(newStatus);
    orderRepository.save(order);
}

// HACK(devteam, TECH-9999): MyBatis mapper cannot handle this complex query.
// Raw JDBC used as a stopgap until the mapper is rewritten with dynamic SQL.
```

TODOs in production code should be tracked in the issue tracker. During code review, every new TODO must have a corresponding ticket. TODOs without tickets are not accepted.