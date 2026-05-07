# API Design Standards

> **Scope**: RESTful URL naming, HTTP method semantics, status code selection, request/response DTO design, pagination/sorting/filtering, API versioning, idempotency, rate limiting, OpenAPI/Swagger documentation.

## Table of Contents

1. RESTful URL Naming
2. HTTP Method and Status Code Semantics
3. Request/Response Design
4. Pagination, Sorting, and Filtering
5. API Versioning
6. Idempotency and Rate Limiting
7. API Documentation

---

## 1. RESTful URL Naming

URLs represent resources (nouns), not actions (verbs). Use plural nouns for collection resources.

**Correct**: `GET /api/v1/orders`, `POST /api/v1/orders`, `GET /api/v1/orders/{id}`, `PUT /api/v1/orders/{id}`, `DELETE /api/v1/orders/{id}`.

**Wrong**: `GET /api/v1/getOrders`, `POST /api/v1/createOrder`, `POST /api/v1/deleteOrder`.

Nested resources express ownership: `GET /api/v1/orders/{orderId}/items` — items belonging to a specific order. Limit nesting to two levels. If deeper nesting is needed, flatten by promoting the nested resource: `GET /api/v1/order-items?orderId=123`.

Use lowercase with hyphens for multi-word resources: `/api/v1/order-items`, not `/api/v1/orderItems` or `/api/v1/order_items`. URLs are case-sensitive in the HTTP spec.

For actions that don't map naturally to CRUD, use a verb sub-resource: `POST /api/v1/orders/{id}/cancel`, `POST /api/v1/orders/{id}/ship`. These should be POST (they cause side effects) even though they don't create a new resource.

---

## 2. HTTP Method and Status Code Semantics

**GET**: Retrieve a resource. Must be safe (no side effects) and idempotent. Never use GET for operations that modify state.

**POST**: Create a new resource or trigger an action. Not idempotent by default — implement idempotency explicitly when needed (see section 6).

**PUT**: Full replacement of a resource. The request body must contain the complete representation. Idempotent.

**PATCH**: Partial update. The request body contains only the fields to update. Prefer PATCH over PUT when clients typically update a subset of fields.

**DELETE**: Remove a resource. Idempotent — deleting an already-deleted resource should return 204 or 404, not an error.

**Status codes that matter most**: `200 OK` for successful GET/PUT/PATCH. `201 Created` for successful POST that creates a resource (include `Location` header). `204 No Content` for successful DELETE or PUT with no response body. `400 Bad Request` for validation errors (malformed input). `401 Unauthorized` for missing or invalid authentication. `403 Forbidden` for valid authentication but insufficient permissions. `404 Not Found` for nonexistent resources. `409 Conflict` for state conflicts (e.g., duplicate creation). `422 Unprocessable Entity` for business rule violations. `429 Too Many Requests` for rate limiting. `500 Internal Server Error` for unexpected server failures only.

Never return 200 with an error body. If the operation failed, the HTTP status code must reflect the failure.

---

## 3. Request/Response Design

**Unified response wrapper** for all successful responses:

```java
public record Result<T>(int code, String message, T data) {
    public static <T> Result<T> success(T data) {
        return new Result<>(200, "success", data);
    }

    public static <T> Result<T> success() {
        return new Result<>(200, "success", null);
    }
}
```

**Request DTOs**: Separate DTOs for create, update, and query operations. `OrderCreateRequest`, `OrderUpdateRequest`, `OrderQueryRequest`. Use Jakarta Bean Validation annotations (`@NotNull`, `@Size`, `@Pattern`, `@Min`, `@Max`, `@Email`) on request fields. Use `@Valid` or `@Validated` on controller method parameters.

**Response DTOs**: Never expose internal entity structure directly. Strip internal IDs, sensitive fields, and implementation details. Use flat structures — avoid deep nesting. Include HATEOAS links for discoverability when appropriate.

**Naming conventions**: Request DTOs end with `Request` or `Cmd` (command). Response DTOs end with `Dto`, `Vo`, or `Response`. Query parameters use `Query` or `Criteria` suffix.

---

## 4. Pagination, Sorting, and Filtering

**Pagination**: Use `page` (0-based) and `size` (items per page) query parameters. Return pagination metadata in the response.

```java
public record PageResult<T>(
    List<T> content,
    int page,
    int size,
    long totalElements,
    int totalPages,
    boolean hasNext
) {}
```

Set a maximum page size (e.g., 100) and enforce it server-side. Default to a sensible page size (e.g., 20) when not specified.

For large datasets or infinite scroll, prefer cursor-based (keyset) pagination over offset-based. Offset pagination degrades on deep pages (`OFFSET 100000` is slow). Cursor pagination uses the last seen record's key: `GET /api/v1/orders?after=order_123&size=20`.

**Sorting**: Use a `sort` parameter with field name and direction: `?sort=createdAt,desc`. Support multiple sort fields: `?sort=status,asc&sort=createdAt,desc`. Spring Data's `Pageable` and `Sort` handle this automatically.

**Filtering**: Use query parameters for simple filters: `?status=ACTIVE&customerId=123`. For complex filters, accept a structured query object in a POST to a search endpoint: `POST /api/v1/orders/search`.

---

## 5. API Versioning

Use URL path versioning: `/api/v1/orders`. This is the most common, most visible, and simplest to implement and route. Other approaches (header versioning, content negotiation) add complexity without proportional benefit in most projects.

Version only when breaking changes are unavoidable. Adding new fields to a response is not a breaking change. Removing fields, renaming fields, or changing field types are breaking changes.

When introducing v2, maintain v1 until all clients have migrated. Set a deprecation timeline and communicate it. Use `@Deprecated` on v1 controller methods and return a deprecation warning header.

---

## 6. Idempotency and Rate Limiting

**Idempotency**: POST operations that create resources should accept an idempotency key (client-generated UUID) in a request header (`Idempotency-Key`). If the server receives a duplicate key, it returns the original response without re-executing the operation. Store idempotency keys in Redis or a database table with a TTL.

**Rate limiting**: Apply rate limits at the API gateway or with a filter. Return `429 Too Many Requests` with a `Retry-After` header. Common patterns: per-user rate limits (authenticated endpoints), per-IP rate limits (public endpoints), per-endpoint limits (expensive operations). Use token bucket or sliding window algorithms. Spring Cloud Gateway provides built-in rate limiting with Redis.

---

## 7. API Documentation

Use OpenAPI 3.0 (Swagger) for API documentation. Annotate controllers and DTOs with OpenAPI annotations (`@Tag`, `@Operation`, `@Schema`, `@Parameter`).

Generate documentation automatically from code — never maintain a separate API document that can drift. Use `springdoc-openapi` (the active replacement for `springfox-swagger`).

Every endpoint must document its purpose (`@Operation(summary=...)`), expected request format, possible response codes, and error scenarios. Every DTO field must have a `@Schema(description=...)` annotation.

Expose the Swagger UI at `/swagger-ui.html` in development and staging environments. Disable or protect it in production.