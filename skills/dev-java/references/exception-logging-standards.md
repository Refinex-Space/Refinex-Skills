# Exception and Logging Standards

> **Scope**: Exception hierarchy design, global exception handling (`@ControllerAdvice`), error response format, SLF4J + Logback configuration, log level semantics, structured logging, MDC for distributed tracing, log rotation and retention.

## Table of Contents

1. Exception Hierarchy Design
2. Global Exception Handling
3. Unified Error Response Format
4. Logging Standards
5. MDC and Distributed Tracing
6. Log Configuration

---

## 1. Exception Hierarchy Design

Design a project-wide exception hierarchy rooted in a single base exception. This enables uniform handling in `@ControllerAdvice` and consistent error codes.

```java
/**
 * Base exception for all business exceptions in this project.
 * Carries an error code and a user-facing message.
 */
public abstract class BusinessException extends RuntimeException {
    private final String errorCode;
    private final int httpStatus;

    protected BusinessException(String errorCode, int httpStatus, String message) {
        super(message);
        this.errorCode = errorCode;
        this.httpStatus = httpStatus;
    }

    protected BusinessException(String errorCode, int httpStatus, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
        this.httpStatus = httpStatus;
    }

    public String getErrorCode() { return errorCode; }
    public int getHttpStatus() { return httpStatus; }
}

// Concrete exceptions
public class ResourceNotFoundException extends BusinessException {
    public ResourceNotFoundException(String resource, Object id) {
        super("NOT_FOUND", 404,
              String.format("%s with id %s not found", resource, id));
    }
}

public class BusinessRuleViolationException extends BusinessException {
    public BusinessRuleViolationException(String message) {
        super("BUSINESS_RULE_VIOLATION", 422, message);
    }
}
```

**Rules**: Use unchecked exceptions (`RuntimeException` subtypes) for business exceptions — they propagate cleanly through Spring's transaction and AOP infrastructure. Use checked exceptions only when the caller is genuinely expected to handle the exception as part of normal program flow (rare in web applications). Never throw `Exception`, `RuntimeException`, or `Throwable` directly — always use a specific subclass.

**Exception message standards**: Messages should be developer-readable (for logs) and may optionally include a separate user-facing message. Never expose stack traces, internal class names, or SQL in API responses. Log the full exception server-side; return a sanitized error to the client.

---

## 2. Global Exception Handling

Use a single `@RestControllerAdvice` class to handle all exceptions uniformly.

```java
@RestControllerAdvice
@Slf4j
@Order(Ordered.HIGHEST_PRECEDENCE)
public class GlobalExceptionHandler {

    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ErrorResponse> handleBusiness(BusinessException ex) {
        log.warn("Business exception: code={}, message={}", ex.getErrorCode(), ex.getMessage());
        return ResponseEntity.status(ex.getHttpStatus())
            .body(ErrorResponse.of(ex.getErrorCode(), ex.getMessage()));
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(MethodArgumentNotValidException ex) {
        String details = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> e.getField() + ": " + e.getDefaultMessage())
            .collect(Collectors.joining("; "));
        log.warn("Validation failed: {}", details);
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of("VALIDATION_ERROR", details));
    }

    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception ex) {
        // Log the FULL exception for debugging — include the exception object
        log.error("Unexpected error", ex);
        // Return a generic message to the client — never expose internals
        return ResponseEntity.internalServerError()
            .body(ErrorResponse.of("INTERNAL_ERROR",
                  "An unexpected error occurred. Please contact support."));
    }
}
```

**Critical rule**: The catch-all handler (`Exception.class`) must log the full exception including stack trace by passing `ex` as the second argument to the logger: `log.error("message", ex)`. Writing `log.error("error: " + ex.getMessage())` loses the stack trace and makes debugging nearly impossible.

---

## 3. Unified Error Response Format

Every error response from the API must follow a consistent structure.

```java
public record ErrorResponse(
    String code,
    String message,
    String traceId,
    Instant timestamp
) {
    public static ErrorResponse of(String code, String message) {
        return new ErrorResponse(code, message, MDC.get("traceId"), Instant.now());
    }
}
```

The `traceId` field connects the client error to the server-side log entry, enabling quick debugging. The `timestamp` field helps with time-based log correlation.

---

## 4. Logging Standards

### Logger Declaration

Use SLF4J as the logging facade. The implementation (Logback, Log4j2) is configured via the classpath. With Lombok, use `@Slf4j`. Without Lombok:

```java
private static final Logger log = LoggerFactory.getLogger(OrderService.class);
```

Never use `System.out.println()` or `System.err.println()` — they are not configurable, not level-aware, and not machine-parseable.

Never use `e.printStackTrace()` — it writes to `System.err`, which may be swallowed or interleaved with other output. Use `log.error("message", e)`.

### Log Level Semantics

**ERROR**: Something broken that needs human attention now. The operation failed and cannot be retried automatically. Examples: database connection failure, external service returning 500 after all retries, data corruption detected. ERROR logs should trigger alerts.

**WARN**: Something unexpected happened but the operation can continue or recover. Examples: retry attempt succeeded after initial failure, deprecated API called, resource pool nearing capacity, slow query detected (>1s). WARN logs should be monitored for trends.

**INFO**: Normal business events that are meaningful for operational visibility. Examples: application started, user logged in, order placed, scheduled job completed, configuration loaded. INFO is the default production log level. Every INFO message should answer "what happened" without being noisy.

**DEBUG**: Detailed information useful for debugging specific issues. Examples: method entry/exit with parameters, intermediate calculation results, cache hit/miss. Never include sensitive data (passwords, tokens, PII) in DEBUG logs — they may be enabled in production during troubleshooting.

**TRACE**: Extremely detailed logging, typically framework-level. Rarely used in application code.

### Parameterized Logging

Always use SLF4J parameterized messages. Never use string concatenation.

```java
// Good — string is only built if the level is enabled
log.debug("Processing order: id={}, items={}", orderId, itemCount);

// Bad — string concatenation happens regardless of log level
log.debug("Processing order: id=" + orderId + ", items=" + itemCount);
```

### What to log (and what not to)

Log at method boundaries for critical business operations: who did what, when, with what parameters, and what was the outcome. Never log passwords, credit card numbers, tokens, or PII (personally identifiable information) at any level. If you must log a request body, sanitize sensitive fields first.

---

## 5. MDC and Distributed Tracing

Use MDC (Mapped Diagnostic Context) to attach trace context to every log line. In Spring Boot, configure a filter to populate MDC at the start of each request.

```java
@Component
public class TraceFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request,
            HttpServletResponse response, FilterChain chain) throws ... {
        String traceId = Optional.ofNullable(request.getHeader("X-Trace-Id"))
            .orElse(UUID.randomUUID().toString().replace("-", ""));
        MDC.put("traceId", traceId);
        response.setHeader("X-Trace-Id", traceId);
        try {
            chain.doFilter(request, response);
        } finally {
            MDC.clear();  // Critical — prevents leaking context to the next request
        }
    }
}
```

Configure Logback to include the traceId in every log line: `%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] [%X{traceId}] %-5level %logger{36} - %msg%n`.

For microservices, use Micrometer Tracing (successor to Spring Cloud Sleuth) to propagate trace IDs across service boundaries automatically.

---

## 6. Log Configuration

Use `logback-spring.xml` (not `logback.xml`) to leverage Spring Boot's profile-aware configuration. Separate log files by concern: `application.log` for business logs, `error.log` for ERROR-level logs, `access.log` for HTTP access logs.

Rotate logs by size (100MB per file) and time (daily). Retain logs for 30 days in production. Compress rotated logs with gzip.

In production, log to stdout/stderr when running in containers (Docker/Kubernetes) — the container runtime handles log collection. When running on VMs, log to files with rotation.

Async logging (`AsyncAppender` in Logback) improves throughput by offloading log I/O to a background thread. Configure with a queue size of 1024-8192 and a discard threshold for DEBUG/TRACE when the queue is 80%+ full.