# Data Access Standards

> **Scope**: MyBatis XML mapper standards, MyBatis-Plus conventions, JPA entity mapping and query optimization, JdbcTemplate patterns, transaction management (`@Transactional` semantics, propagation, isolation), N+1 prevention, connection pool configuration.

## Table of Contents

1. Technology Selection Guide
2. MyBatis Standards
3. MyBatis-Plus Standards
4. JPA / Spring Data JPA Standards
5. JdbcTemplate Standards
6. Transaction Management
7. Connection Pool Configuration

---

## 1. Technology Selection Guide

Choose the data access technology based on the project's characteristics. Do not mix multiple ORM frameworks within a single service unless there is a compelling reason (e.g., using JPA for CRUD and MyBatis for complex reporting queries).

**JPA / Spring Data JPA**: Best for domain-driven projects with a rich object model. Provides automatic dirty checking, lazy loading, and cache. Ideal when the database schema closely follows the domain model.

**MyBatis**: Best for SQL-centric projects where the team wants full control over SQL. Ideal for complex queries, stored procedure calls, and projects where the database schema was designed independently of the application.

**MyBatis-Plus**: Extension of MyBatis that provides CRUD automation, code generation, and pagination out of the box. Good for rapid development when most operations are standard CRUD with occasional custom SQL.

**JdbcTemplate**: Best for simple data access without ORM overhead, microservices with minimal persistence needs, or when you need absolute control over SQL with no magic. Also suitable for batch operations where ORM per-row overhead is unacceptable.

---

## 2. MyBatis Standards

### Mapper XML Standards

Organize mapper XML files under `src/main/resources/mapper/` mirroring the Java package structure. One mapper XML per table/entity.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
    "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!-- Namespace must match the fully qualified mapper interface name -->
<mapper namespace="com.company.project.repository.OrderMapper">

    <!-- Base column list — reuse across queries to avoid duplication -->
    <sql id="baseColumns">
        id, customer_id, status, total_amount, created_at, updated_at
    </sql>

    <!-- ResultMap for complex mappings; use resultType for simple ones -->
    <resultMap id="orderResultMap" type="com.company.project.model.entity.Order">
        <id column="id" property="id" />
        <result column="customer_id" property="customerId" />
        <result column="status" property="status"
                typeHandler="org.apache.ibatis.type.EnumTypeHandler" />
        <result column="total_amount" property="totalAmount" />
        <result column="created_at" property="createdAt" />
        <result column="updated_at" property="updatedAt" />
    </resultMap>

    <select id="findById" resultMap="orderResultMap">
        SELECT <include refid="baseColumns" />
        FROM orders
        WHERE id = #{id}
    </select>
</mapper>
```

**Rules**: Use `#{}` (parameterized) for all user-supplied values — never use `${}` except for dynamic column/table names that are validated and controlled by the application (never from user input). Use `<sql>` fragments for reusable column lists and conditions. Use `<where>`, `<set>`, `<foreach>` dynamic SQL elements instead of manual string concatenation. Keep SQL readable: one clause per line, uppercase keywords.

### Mapper Interface Standards

```java
@Mapper
public interface OrderMapper {
    Order findById(@Param("id") Long id);
    List<Order> findByCustomerId(@Param("customerId") Long customerId);
    int insert(Order order);
    int updateStatus(@Param("id") Long id, @Param("status") OrderStatus status);
}
```

Always use `@Param` for multi-parameter methods. For single-parameter methods with simple types, `@Param` is optional but recommended for clarity.

---

## 3. MyBatis-Plus Standards

Use MyBatis-Plus's `BaseMapper<T>` for standard CRUD operations. Only write custom SQL for complex queries that cannot be expressed with the wrapper API.

```java
public interface OrderMapper extends BaseMapper<Order> {
    // Custom queries only — CRUD inherited from BaseMapper
    @Select("SELECT o.*, c.name as customer_name FROM orders o " +
            "JOIN customers c ON o.customer_id = c.id WHERE o.id = #{id}")
    OrderDetailDto findDetailById(@Param("id") Long id);
}
```

**Wrapper usage rules**: Use `LambdaQueryWrapper` instead of `QueryWrapper` — lambda wrappers are refactoring-safe (column references are method references, not strings).

```java
// Good — refactoring-safe
LambdaQueryWrapper<Order> wrapper = new LambdaQueryWrapper<Order>()
    .eq(Order::getCustomerId, customerId)
    .ge(Order::getCreatedAt, startDate)
    .orderByDesc(Order::getCreatedAt);

// Bad — string-based, breaks silently on column rename
QueryWrapper<Order> wrapper = new QueryWrapper<Order>()
    .eq("customer_id", customerId);
```

**Entity annotation standards**: Use `@TableName` for table mapping, `@TableId` for primary key, `@TableField` for column mapping, `@TableLogic` for logical delete, `@Version` for optimistic locking.

**Pagination**: Use MyBatis-Plus's `Page<T>` with the `PaginationInnerInterceptor`. Configure the interceptor in a `@Configuration` class. Never use `LIMIT` with large offsets for deep pagination — use keyset pagination (cursor-based) instead.

---

## 4. JPA / Spring Data JPA Standards

### Entity Mapping

```java
@Entity
@Table(name = "orders", indexes = {
    @Index(name = "idx_customer_id", columnList = "customer_id"),
    @Index(name = "idx_created_at", columnList = "created_at")
})
public class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "customer_id", nullable = false)
    private Long customerId;

    @Enumerated(EnumType.STRING)  // Never EnumType.ORDINAL — ordinal breaks on reorder
    @Column(nullable = false, length = 20)
    private OrderStatus status;

    @Column(precision = 12, scale = 2)
    private BigDecimal totalAmount;

    @CreationTimestamp
    @Column(updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    private LocalDateTime updatedAt;
}
```

Rules: Always use `EnumType.STRING` for enum mapping — `ORDINAL` breaks silently when enum constants are reordered. Define database indexes in `@Table` for frequently queried columns. Use `@CreationTimestamp` and `@UpdateTimestamp` for audit fields.

### N+1 Prevention

The N+1 query problem is the most common JPA performance issue. It occurs when Hibernate lazily loads a collection for each entity in a result set, producing 1 query for the list + N queries for each entity's associations.

**Solution 1 — JOIN FETCH**: `@Query("SELECT o FROM Order o JOIN FETCH o.items WHERE o.customerId = :customerId")`. This eagerly loads the association in a single query.

**Solution 2 — Entity Graph**: `@EntityGraph(attributePaths = {"items"})` on the repository method. Declaratively specifies which associations to fetch eagerly for this query.

**Solution 3 — Batch fetching**: `@BatchSize(size = 50)` on the collection mapping. When Hibernate loads the first association, it pre-fetches the next 50 in a single IN query. Less precise but requires no query changes.

**Solution 4 — DTO projection**: For read-only queries, project directly into a DTO to avoid loading entities at all. Use `@Query` with constructor expressions or interface-based projections.

### Repository conventions

Prefer method name derivation for simple queries: `findByStatusAndCreatedAtAfter(OrderStatus status, LocalDateTime date)`. For queries with more than 3 conditions, use `@Query` with JPQL — long method names become unreadable. For truly dynamic queries (optional filter criteria), use `Specification<T>` or QueryDSL.

---

## 5. JdbcTemplate Standards

Use named parameters (`NamedParameterJdbcTemplate`) instead of positional `?` placeholders. Named parameters are self-documenting and less error-prone when modifying queries.

```java
@Repository
@RequiredArgsConstructor
public class OrderJdbcRepository {
    private final NamedParameterJdbcTemplate jdbc;

    public Optional<Order> findById(Long id) {
        String sql = "SELECT id, customer_id, status, total_amount, created_at " +
                     "FROM orders WHERE id = :id";
        MapSqlParameterSource params = new MapSqlParameterSource("id", id);
        List<Order> results = jdbc.query(sql, params, orderRowMapper());
        return results.stream().findFirst();
    }

    private RowMapper<Order> orderRowMapper() {
        return (rs, rowNum) -> new Order(
            rs.getLong("id"),
            rs.getLong("customer_id"),
            OrderStatus.valueOf(rs.getString("status")),
            rs.getBigDecimal("total_amount"),
            rs.getTimestamp("created_at").toLocalDateTime()
        );
    }
}
```

For batch inserts, use `jdbc.batchUpdate()` with a batch size of 500-1000 rows. This is significantly faster than individual inserts.

---

## 6. Transaction Management

### @Transactional semantics

`@Transactional` is managed by Spring AOP proxies. Understanding proxy behavior is essential to avoid silent failures.

**Rule 1**: `@Transactional` only works on public methods. On private, protected, or package-private methods, the annotation is silently ignored because the proxy cannot intercept the call.

**Rule 2**: Self-invocation bypasses the proxy. If method A in the same class calls method B annotated with `@Transactional`, the transaction on B does not apply. The call goes through `this`, not through the proxy.

```java
// Bug — createOrder calls self.validate(), bypassing the proxy
@Transactional
public void createOrder(OrderRequest request) {
    validate(request);  // this.validate() — NOT proxied
    // ...
}

@Transactional(propagation = Propagation.REQUIRES_NEW)
public void validate(OrderRequest request) { ... }
```

**Fix**: Extract the validated method into a separate `@Service` bean, or use `@EnableAspectJAutoProxy(exposeProxy = true)` + `AopContext.currentProxy()` (less clean).

**Rule 3**: Default propagation is `REQUIRED` — join the existing transaction or create a new one. Use `REQUIRES_NEW` when you need a completely independent transaction (e.g., audit logging that must persist even if the outer transaction rolls back). Use `SUPPORTS` for read-only methods that should participate in a transaction if one exists but do not need their own.

**Rule 4**: Default isolation level is the database default (usually `READ_COMMITTED`). Override only when necessary. `SERIALIZABLE` prevents phantom reads but severely limits concurrency — use it only for financial calculations. `REPEATABLE_READ` prevents non-repeatable reads — use for reports that must see a consistent snapshot.

**Rule 5**: Default rollback is on unchecked exceptions (`RuntimeException` and its subclasses). Checked exceptions do NOT trigger rollback by default. If you need rollback on a checked exception: `@Transactional(rollbackFor = BusinessException.class)`. Many teams use `@Transactional(rollbackFor = Exception.class)` as a project-wide standard to avoid subtle rollback failures.

**Rule 6**: Mark read-only queries with `@Transactional(readOnly = true)`. This tells the JPA provider to skip dirty checking and tells the database driver to optimize for reads (some databases route to read replicas).

---

## 7. Connection Pool Configuration

Use HikariCP (Spring Boot default). Key parameters to tune:

`maximum-pool-size`: Formula: `2 * CPU_cores + effective_spindle_count`. For a typical 4-core cloud VM with SSD: `2 * 4 + 1 = 9`, rounded to 10. For most applications, 10-20 is optimal. Never set to 100+ "just to be safe" — this causes connection contention and degrades performance.

`minimum-idle`: Set equal to `maximum-pool-size` for steady-state applications. Set lower for bursty workloads. Setting `minimum-idle` < `maximum-pool-size` causes connection churn — Hikari will repeatedly create and destroy connections.

`connection-timeout`: Time to wait for a connection from the pool. Default 30s is usually fine. Increase for environments with slow network (VPN, cross-region).

`max-lifetime`: Must be several seconds less than the database's `wait_timeout` to avoid using connections that the database has already closed. For MySQL with default `wait_timeout=28800` (8 hours), set `max-lifetime=1800000` (30 minutes).

`idle-timeout`: How long a connection can sit idle before being removed. Only applies when `minimum-idle` < `maximum-pool-size`. Default 600000ms (10 minutes) is usually fine.