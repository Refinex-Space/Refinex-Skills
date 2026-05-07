# Security Standards

> **Scope**: Spring Security configuration, authentication/authorization patterns, input validation, OWASP Top 10 in Java context, secrets management, CORS, CSRF, SQL injection prevention, XSS prevention.

## Table of Contents

1. Spring Security Configuration
2. Authentication and Authorization Patterns
3. Input Validation
4. OWASP Top 10 in Java Context
5. Secrets Management
6. CORS and CSRF

---

## 1. Spring Security Configuration

Use Spring Security's `SecurityFilterChain` bean configuration (not the deprecated `WebSecurityConfigurerAdapter`).

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Disable for stateless APIs with JWT
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .build();
    }
}
```

Rules: Follow the principle of least privilege — deny by default, permit explicitly. List specific public endpoints first, then restrict everything else with `.anyRequest().authenticated()`. Never use `.permitAll()` on `.anyRequest()`. Use `@EnableMethodSecurity` for fine-grained method-level authorization when URL patterns are insufficient.

---

## 2. Authentication and Authorization Patterns

**JWT-based stateless authentication** is the standard for REST APIs. The server issues a token on login; the client sends it in the `Authorization: Bearer <token>` header on subsequent requests. The server validates the token without maintaining session state.

**Token standards**: Use short-lived access tokens (15-30 minutes) and long-lived refresh tokens (7-30 days). Store the refresh token in an HTTP-only, Secure cookie — not in localStorage (vulnerable to XSS). Rotate refresh tokens on use (one-time use tokens).

**Method-level authorization**: Use `@PreAuthorize` for declarative authorization on service methods. Prefer expressions over role-based checks for complex rules.

```java
@PreAuthorize("hasRole('ADMIN') or @orderSecurityService.isOwner(#orderId, authentication)")
public OrderDto getOrder(Long orderId) { ... }
```

**Password storage**: Use BCrypt (`BCryptPasswordEncoder`) with a work factor of at least 10. Never store passwords in plain text or with reversible encryption. Never implement custom hashing — use the framework's password encoder.

---

## 3. Input Validation

All external input must be validated before processing. "External" means anything from the client, another service, a file upload, or a database query result when the database is shared.

**Bean Validation (JSR 380)**: Use Jakarta Validation annotations on DTOs. Apply `@Valid` on controller method parameters.

```java
public record OrderCreateRequest(
    @NotNull(message = "Customer ID is required")
    Long customerId,

    @NotEmpty(message = "Order must contain at least one item")
    @Size(max = 100, message = "Order cannot exceed 100 items")
    List<@Valid OrderItemRequest> items,

    @Size(max = 500, message = "Note cannot exceed 500 characters")
    String note
) {}
```

**Custom validators**: For business rules that go beyond standard annotations, implement `ConstraintValidator<AnnotationType, FieldType>`.

**Validation groups**: Use groups to apply different validation rules for different operations (create vs. update). Define marker interfaces (`OnCreate.class`, `OnUpdate.class`) and use `@Validated(OnCreate.class)` on controller methods.

**Critical rule**: Never trust client input even after validation. Server-side validation is mandatory — client-side validation is a UX convenience, not a security measure.

---

## 4. OWASP Top 10 in Java Context

**A01 — Broken Access Control**: Enforce authorization on every endpoint. Test that users cannot access other users' resources by manipulating IDs in URLs. Use object-level authorization checks: verify the authenticated user owns or has permission to access the requested resource.

**A02 — Cryptographic Failures**: Use TLS 1.2+ for all communications. Use AES-256-GCM for encryption at rest. Never implement custom cryptography. Use `java.security` and `javax.crypto` APIs. Store keys in a key management service, not in code.

**A03 — Injection**: SQL injection: use parameterized queries exclusively (JPA named parameters, MyBatis `#{}`, JdbcTemplate `?` placeholders). Never concatenate user input into SQL strings. LDAP injection, OS command injection, XPath injection: sanitize input before passing to interpreters.

**A04 — Insecure Design**: Implement rate limiting on authentication endpoints to prevent brute force. Implement account lockout after N failed attempts. Use CAPTCHAs for public-facing forms. Design with the assumption that every input is malicious.

**A05 — Security Misconfiguration**: Disable debug endpoints in production. Remove default credentials. Disable unnecessary HTTP methods (OPTIONS, TRACE). Set security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`.

**A07 — XSS (Cross-Site Scripting)**: Encode all user-supplied content in responses. Spring's Thymeleaf auto-escapes by default. For REST APIs returning JSON, Jackson's default serialization is safe. Do not construct HTML or JavaScript from user input on the server.

---

## 5. Secrets Management

Never hardcode secrets (passwords, API keys, tokens, certificates) in source code, configuration files committed to version control, or Docker images.

**Acceptable approaches (from most to least preferred)**: Cloud provider secrets manager (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault). HashiCorp Vault with Spring Vault integration. Kubernetes Secrets (mounted as volumes, not environment variables). Environment variables (acceptable for simple deployments, but less auditable).

**Unacceptable approaches**: `application.yml` with embedded passwords committed to Git. `.env` files committed to Git (even in .gitignore — accidents happen). Encrypted properties files where the decryption key is also in the repository.

When secrets must appear in configuration, use Spring Cloud Config Server with encryption or externalized environment variables: `spring.datasource.password=${DB_PASSWORD}`.

---

## 6. CORS and CSRF

**CORS (Cross-Origin Resource Sharing)**: Configure explicitly. Never use `allowedOrigins("*")` with `allowCredentials(true)` — this is a security vulnerability. Specify exact allowed origins for production.

```java
@Bean
public WebMvcConfigurer corsConfigurer() {
    return new WebMvcConfigurer() {
        @Override
        public void addCorsMappings(CorsRegistry registry) {
            registry.addMapping("/api/**")
                .allowedOrigins("https://app.company.com")
                .allowedMethods("GET", "POST", "PUT", "DELETE")
                .allowedHeaders("Authorization", "Content-Type")
                .maxAge(3600);
        }
    };
}
```

**CSRF (Cross-Site Request Forgery)**: CSRF protection is essential for session-based (cookie-based) authentication. For stateless JWT APIs where the token is sent in the Authorization header (not a cookie), CSRF protection can be disabled because the token is not automatically attached by the browser. If using cookies for JWT storage, CSRF must remain enabled.