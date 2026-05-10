# Markup, Configuration, and Other Languages Commenting Standards

This reference covers commenting standards for XML, HTML, YAML, SQL (including stored procedures/functions), CSS/SCSS, Shell scripts, Go, C/C++, Kotlin, and Swift.

---

## Table of Contents

1. [XML](#xml)
2. [HTML](#html)
3. [YAML](#yaml)
4. [SQL](#sql)
5. [CSS and SCSS](#css-and-scss)
6. [Shell Scripts (Bash/Zsh)](#shell-scripts)
7. [Go](#go)
8. [C and C++](#c-and-c)
9. [Kotlin](#kotlin)
10. [Swift](#swift)

---

## XML

XML uses `<!-- comment -->` syntax. Comments cannot be nested and cannot contain `--`.

### Configuration Files (Spring, Maven, MyBatis, web.xml, etc.)

Every logical section and non-obvious element must be commented. This is critical for framework configuration where element names are often opaque.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- Application context configuration for the authentication module.
     Defines security filters, authentication providers, and session management. -->
<beans xmlns="http://www.springframework.org/schema/beans">

    <!-- ==================== Security Filters ==================== -->

    <!-- JWT authentication filter: intercepts all /api/** requests,
         extracts the Bearer token from the Authorization header,
         and validates it against the signing key. -->
    <bean id="jwtFilter" class="com.example.security.JwtAuthFilter">
        <property name="signingKey" value="${jwt.signing-key}" />
        <!-- Token expiration in seconds. Default: 3600 (1 hour) -->
        <property name="expirationSeconds" value="${jwt.expiration:3600}" />
    </bean>

    <!-- ==================== Data Source ==================== -->

    <!-- Primary database connection pool. Uses HikariCP for connection pooling.
         Pool size is configured for the expected 50 concurrent users. -->
    <bean id="dataSource" class="com.zaxxer.hikari.HikariDataSource">
        <!-- Maximum pool size: 10 connections per server instance.
             With 5 instances, this gives 50 total database connections. -->
        <property name="maximumPoolSize" value="10" />
        <!-- Connection idle timeout in milliseconds (10 minutes) -->
        <property name="idleTimeout" value="600000" />
    </bean>
</beans>
```

### Maven pom.xml

```xml
<project>
    <!-- ==================== Project Identity ==================== -->
    <groupId>com.example</groupId>
    <artifactId>user-service</artifactId>
    <!-- SemVer: major.minor.patch-qualifier -->
    <version>2.3.1-SNAPSHOT</version>

    <dependencies>
        <!-- Spring Boot web starter: includes embedded Tomcat, Spring MVC,
             and Jackson JSON serialization -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- MapStruct: compile-time DTO <-> Entity mapper code generation.
             Requires the annotation processor in the build plugins section. -->
        <dependency>
            <groupId>org.mapstruct</groupId>
            <artifactId>mapstruct</artifactId>
            <version>${mapstruct.version}</version>
        </dependency>
    </dependencies>
</project>
```

### MyBatis Mapper XML

```xml
<!-- User data access mapper. Maps to UserMapper.java interface. -->
<mapper namespace="com.example.mapper.UserMapper">

    <!-- Result map for the User entity. Maps snake_case columns
         to camelCase Java fields. -->
    <resultMap id="UserResultMap" type="com.example.entity.User">
        <id column="user_id" property="id" />
        <result column="display_name" property="displayName" />
        <!-- JSON column: stored as TEXT, deserialized by the JSON type handler -->
        <result column="preferences" property="preferences"
                typeHandler="com.example.handler.JsonTypeHandler" />
    </resultMap>

    <!-- Finds users matching the search criteria with pagination.
         Uses dynamic SQL to conditionally apply filters. -->
    <select id="search" resultMap="UserResultMap">
        SELECT user_id, display_name, email, preferences
        FROM users
        WHERE deleted_at IS NULL
        <!-- Name filter: case-insensitive partial match -->
        <if test="name != null and name != ''">
            AND LOWER(display_name) LIKE CONCAT('%', LOWER(#{name}), '%')
        </if>
        ORDER BY created_at DESC
        LIMIT #{pageSize} OFFSET #{offset}
    </select>
</mapper>
```

---

## HTML

HTML uses `<!-- comment -->` syntax. In HTML, comments serve as section markers and explain non-obvious structure or accessibility decisions.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <!-- Viewport meta: ensures responsive layout on mobile devices -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Preconnect to API server to reduce connection latency for first API call -->
    <link rel="preconnect" href="https://api.example.com">
    <title>Dashboard</title>
</head>
<body>
    <!-- ==================== Navigation ==================== -->
    <!-- Main navigation: uses aria-label to distinguish from footer nav -->
    <nav aria-label="Main navigation">
        <!-- Skip link: allows keyboard users to bypass navigation -->
        <a href="#main-content" class="skip-link">Skip to main content</a>
    </nav>

    <!-- ==================== Main Content ==================== -->
    <main id="main-content">
        <!-- Dashboard grid: 3 columns on desktop, stacks vertically on mobile.
             See dashboard.css .grid-container for breakpoint details. -->
        <div class="grid-container">
            <!-- Revenue card: data fetched from /api/metrics/revenue -->
            <section class="card" aria-labelledby="revenue-heading">
                <h2 id="revenue-heading">Revenue</h2>
            </section>
        </div>
    </main>

    <!-- ==================== Footer ==================== -->
    <footer>
        <!-- Legal links required by compliance team (GDPR, CCPA) -->
        <nav aria-label="Legal">
            <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a>
        </nav>
    </footer>
</body>
</html>
```

---

## YAML

YAML uses `#` for comments. Because YAML is whitespace-sensitive, comments are the primary way to explain structure. Every logical section and every non-obvious key must be commented.

### Application Configuration (Spring Boot application.yml, Docker Compose, K8s, etc.)

```yaml
# ============================================================
# Application Server Configuration
# ============================================================
server:
  # Listen port. Override with SERVER_PORT env var in production.
  port: 8080
  # Graceful shutdown: wait up to 30s for in-flight requests to complete
  shutdown: graceful
  servlet:
    # Context path: all endpoints are prefixed with /api/v1
    context-path: /api/v1

# ============================================================
# Database Configuration
# ============================================================
spring:
  datasource:
    # JDBC URL. Uses HikariCP connection pool by default.
    # Production URL is injected via SPRING_DATASOURCE_URL env var.
    url: jdbc:postgresql://localhost:5432/myapp
    username: ${DB_USERNAME:myapp}
    password: ${DB_PASSWORD:secret}
    hikari:
      # Max pool size: tuned for 50 concurrent users across 5 instances
      maximum-pool-size: 10
      # Connection timeout in ms: fail fast if pool is exhausted
      connection-timeout: 5000
      # Idle timeout in ms: close connections idle for more than 10 minutes
      idle-timeout: 600000

  jpa:
    # DDL auto: validate in production, update in development
    hibernate:
      ddl-auto: validate
    # Show SQL in logs (disable in production for performance)
    show-sql: false
    properties:
      hibernate:
        # Batch size for bulk inserts: reduces round-trips to the database
        jdbc.batch_size: 50

# ============================================================
# Logging Configuration
# ============================================================
logging:
  level:
    # Application packages: DEBUG in dev, INFO in production
    com.example: ${LOG_LEVEL:INFO}
    # Suppress noisy Hibernate SQL parameter logging
    org.hibernate.type.descriptor.sql: WARN
```

### Docker Compose

```yaml
# Docker Compose configuration for local development environment.
# Start with: docker compose up -d

services:
  # ---- Application Service ----
  app:
    build:
      context: .
      # Multi-stage build: uses the 'development' target for hot-reload
      target: development
    ports:
      # Host port 3000 → container port 8080
      - "3000:8080"
    environment:
      # Database connection (uses the 'db' service below)
      - SPRING_DATASOURCE_URL=jdbc:postgresql://db:5432/myapp
      - DB_USERNAME=postgres
      - DB_PASSWORD=postgres
    depends_on:
      db:
        # Wait for the database to be ready before starting the app
        condition: service_healthy

  # ---- Database Service ----
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      # Persist data across container restarts
      - postgres_data:/var/lib/postgresql/data
      # Initialization scripts: run once when the volume is first created
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      # Check that PostgreSQL is accepting connections
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  # Named volume for PostgreSQL data persistence
  postgres_data:
```

---

## SQL

SQL uses `--` for single-line comments and `/* ... */` for block comments.

### DDL (Tables, Indexes, Constraints)

```sql
-- ============================================================
-- User account table
-- Stores core identity and authentication data for all registered users.
-- Soft-delete via deleted_at column (NULL = active).
-- ============================================================
CREATE TABLE users (
    -- Auto-incrementing primary key
    id          BIGSERIAL PRIMARY KEY,
    -- Unique login identifier (email format, max 255 chars)
    email       VARCHAR(255) NOT NULL UNIQUE,
    -- BCrypt-hashed password (60 chars for BCrypt)
    password    CHAR(60) NOT NULL,
    -- User's display name, shown in the UI and emails
    full_name   VARCHAR(100) NOT NULL,
    -- Account status: ACTIVE, SUSPENDED, PENDING_VERIFICATION
    status      VARCHAR(20) NOT NULL DEFAULT 'PENDING_VERIFICATION',
    -- Record timestamps (UTC, managed by application layer)
    created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Soft-delete timestamp. NULL means the account is active.
    deleted_at  TIMESTAMP
);

-- Index for email lookup during authentication (most frequent query path)
CREATE INDEX idx_users_email ON users (email) WHERE deleted_at IS NULL;

-- Index for listing active users sorted by registration date
CREATE INDEX idx_users_created ON users (created_at DESC) WHERE deleted_at IS NULL;
```

### Stored Procedures and Functions

```sql
-- ============================================================
-- Procedure: transfer_funds
-- Purpose:   Transfers money between two accounts within a single
--            transaction. Validates sufficient balance before transfer.
--
-- Parameters:
--   p_from_account_id  BIGINT   - Source account ID
--   p_to_account_id    BIGINT   - Destination account ID
--   p_amount           NUMERIC  - Transfer amount (must be positive)
--   p_currency         CHAR(3)  - ISO 4217 currency code (e.g., 'USD')
--
-- Returns: void
--
-- Raises:
--   INSUFFICIENT_FUNDS  - Source account balance is less than p_amount
--   ACCOUNT_NOT_FOUND   - Either account ID does not exist
--   CURRENCY_MISMATCH   - Accounts are in different currencies
--
-- Side effects:
--   - Creates two entries in the transactions table (debit + credit)
--   - Updates the balance column on both accounts
--   - Acquires row-level locks on both accounts (ordered by ID to prevent deadlocks)
-- ============================================================
CREATE OR REPLACE PROCEDURE transfer_funds(
    p_from_account_id BIGINT,
    p_to_account_id   BIGINT,
    p_amount          NUMERIC(15, 2),
    p_currency        CHAR(3)
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_from_balance NUMERIC(15, 2);
    v_from_currency CHAR(3);
    v_to_currency CHAR(3);
BEGIN
    -- Lock both accounts in a consistent order (lower ID first) to prevent deadlocks
    -- when concurrent transfers occur between the same pair of accounts
    IF p_from_account_id < p_to_account_id THEN
        SELECT balance, currency INTO v_from_balance, v_from_currency
        FROM accounts WHERE id = p_from_account_id FOR UPDATE;

        SELECT currency INTO v_to_currency
        FROM accounts WHERE id = p_to_account_id FOR UPDATE;
    ELSE
        SELECT currency INTO v_to_currency
        FROM accounts WHERE id = p_to_account_id FOR UPDATE;

        SELECT balance, currency INTO v_from_balance, v_from_currency
        FROM accounts WHERE id = p_from_account_id FOR UPDATE;
    END IF;

    -- Validate: both accounts must exist
    IF v_from_balance IS NULL THEN
        RAISE EXCEPTION 'ACCOUNT_NOT_FOUND: source account % does not exist', p_from_account_id;
    END IF;

    -- Validate: sufficient balance
    IF v_from_balance < p_amount THEN
        RAISE EXCEPTION 'INSUFFICIENT_FUNDS: balance % < requested %', v_from_balance, p_amount;
    END IF;

    -- Validate: currency match
    IF v_from_currency != p_currency OR v_to_currency != p_currency THEN
        RAISE EXCEPTION 'CURRENCY_MISMATCH: accounts use different currencies';
    END IF;

    -- Execute the transfer: debit source, credit destination
    UPDATE accounts SET balance = balance - p_amount, updated_at = NOW()
    WHERE id = p_from_account_id;

    UPDATE accounts SET balance = balance + p_amount, updated_at = NOW()
    WHERE id = p_to_account_id;

    -- Record the transaction entries for audit trail
    INSERT INTO transactions (account_id, type, amount, currency, counterparty_account_id, created_at)
    VALUES
        (p_from_account_id, 'DEBIT',  p_amount, p_currency, p_to_account_id,   NOW()),
        (p_to_account_id,   'CREDIT', p_amount, p_currency, p_from_account_id, NOW());
END;
$$;
```

### Complex Queries

```sql
-- Monthly revenue report: calculates total revenue, order count, and
-- average order value grouped by product category for the specified month.
-- Uses LEFT JOIN to include categories with zero orders.
SELECT
    c.name AS category_name,
    -- COALESCE handles categories with no orders (NULL from LEFT JOIN)
    COALESCE(SUM(oi.quantity * oi.unit_price), 0) AS total_revenue,
    COUNT(DISTINCT o.id) AS order_count,
    -- Avoid division by zero for categories with no orders
    CASE
        WHEN COUNT(DISTINCT o.id) > 0
        THEN SUM(oi.quantity * oi.unit_price) / COUNT(DISTINCT o.id)
        ELSE 0
    END AS avg_order_value
FROM categories c
LEFT JOIN products p ON p.category_id = c.id
LEFT JOIN order_items oi ON oi.product_id = p.id
-- Only include completed orders from the target month
LEFT JOIN orders o ON o.id = oi.order_id
    AND o.status = 'COMPLETED'
    AND o.completed_at >= DATE_TRUNC('month', :target_date)
    AND o.completed_at < DATE_TRUNC('month', :target_date) + INTERVAL '1 month'
GROUP BY c.id, c.name
ORDER BY total_revenue DESC;
```

---

## CSS and SCSS

CSS uses `/* ... */` comments. SCSS also supports `//` single-line comments.

```css
/* ============================================================
   Typography System
   Base font sizes, line heights, and font family definitions.
   All sizes use rem units relative to the 16px html root.
   ============================================================ */

/* Primary body text: optimized for readability at 16px/1.6 */
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
}

/* Heading scale: uses a 1.25 modular scale (Major Third) */
h1 { font-size: 2.441rem; }  /* 39.06px */
h2 { font-size: 1.953rem; }  /* 31.25px */

/* ============================================================
   Layout Utilities
   ============================================================ */

/* Constrains content width and centers horizontally.
   Max width matches the 12-column grid at 1200px. */
.container {
  max-width: 75rem; /* 1200px */
  margin-inline: auto;
  padding-inline: 1rem;
}
```

---

## Shell Scripts

Shell scripts use `#` for comments. Every script must start with a header comment block.

```bash
#!/usr/bin/env bash
# ============================================================
# deploy.sh — Deploy the application to the target environment
#
# Usage: ./deploy.sh <environment> [--dry-run]
#   environment: dev | staging | prod
#   --dry-run:   Show what would be deployed without executing
#
# Prerequisites:
#   - AWS CLI configured with appropriate credentials
#   - Docker logged in to the ECR registry
#   - kubectl context set to the target cluster
#
# Exit codes:
#   0 - Deployment successful
#   1 - Invalid arguments
#   2 - Build failure
#   3 - Deployment failure
# ============================================================

set -euo pipefail  # Exit on error, undefined vars, and pipe failures

# ---- Configuration ----
readonly REGISTRY="123456789.dkr.ecr.us-east-1.amazonaws.com"
readonly APP_NAME="user-service"
# Image tag: git short SHA for traceability
readonly IMAGE_TAG="$(git rev-parse --short HEAD)"

# ---- Argument Parsing ----
# Validate that at least one argument (environment) is provided
if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <environment> [--dry-run]" >&2
    exit 1
fi
```

---

## Go

Go uses `//` for comments. The `godoc` tool extracts comments that immediately precede top-level declarations. The first sentence is used as the summary.

```go
// Package auth provides JWT-based authentication and authorization.
//
// It supports token generation, validation, and refresh operations.
// All tokens use RS256 signing with keys loaded from the configured
// key store.
package auth

// TokenService manages JWT token lifecycle operations.
//
// It is safe for concurrent use by multiple goroutines.
type TokenService struct {
	// signingKey is the RSA private key used to sign new tokens.
	signingKey *rsa.PrivateKey

	// tokenTTL is the duration for which newly issued tokens are valid.
	tokenTTL time.Duration
}

// GenerateToken creates a new signed JWT for the given user.
//
// The token includes the user's ID, email, and roles as claims.
// It expires after the configured TTL.
//
// Returns an error if the signing operation fails.
func (s *TokenService) GenerateToken(user *User) (string, error) {
```

---

## C and C++

C uses `/* ... */` block comments and `//` line comments (C99+). C++ uses `//` and Doxygen-style `/** ... */` or `///` for documentation.

```c
/**
 * @file ring_buffer.h
 * @brief Lock-free single-producer single-consumer ring buffer.
 *
 * Provides a fixed-capacity FIFO queue suitable for inter-thread
 * communication without locks. Uses memory barriers for correct
 * ordering on weakly-ordered architectures (ARM, RISC-V).
 *
 * @note Capacity must be a power of 2 for the masking optimization.
 */

/**
 * @brief Pushes an element onto the ring buffer.
 *
 * @param rb   Pointer to the ring buffer instance.
 * @param data Pointer to the data to copy into the buffer.
 * @param size Size of the data in bytes. Must not exceed element_size.
 * @return 0 on success, -1 if the buffer is full (EAGAIN).
 */
int ring_buffer_push(ring_buffer_t *rb, const void *data, size_t size);
```

---

## Kotlin

Kotlin uses KDoc (`/** ... */`) which follows the same conventions as Javadoc with Kotlin-specific tags like `@receiver`.

```kotlin
/**
 * Retries the given [block] with exponential backoff.
 *
 * @param maxAttempts Maximum number of attempts (must be ≥ 1).
 * @param initialDelay Initial delay between retries in milliseconds.
 * @param maxDelay Maximum delay cap in milliseconds.
 * @param block The suspending function to retry.
 * @return The successful result of [block].
 * @throws Exception The exception from the last failed attempt if
 *   all retries are exhausted.
 */
suspend fun <T> retry(
    maxAttempts: Int = 3,
    initialDelay: Long = 100L,
    maxDelay: Long = 10_000L,
    block: suspend () -> T,
): T {
```

---

## Swift

Swift uses `///` for documentation comments with Markdown support, processed by DocC.

```swift
/// A thread-safe, bounded cache with LRU eviction policy.
///
/// Use `Cache` to store frequently accessed values that are expensive
/// to compute. When the cache reaches its capacity, the least recently
/// accessed entry is evicted.
///
/// - Note: All operations are O(1) amortized.
/// - Important: The cache does not persist across app launches.
public final class Cache<Key: Hashable, Value> {

    /// Creates a new cache with the specified capacity.
    ///
    /// - Parameter capacity: Maximum number of entries. Must be positive.
    /// - Precondition: `capacity > 0`
    public init(capacity: Int) {

    /// Retrieves the value for the given key, if present.
    ///
    /// Accessing a value promotes it to the most recently used position,
    /// protecting it from eviction.
    ///
    /// - Parameter key: The key to look up.
    /// - Returns: The cached value, or `nil` if the key is not in the cache.
    public func get(_ key: Key) -> Value? {
```