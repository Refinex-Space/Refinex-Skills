# Java Commenting Standards Reference

Authoritative sources: Oracle Javadoc Tool Guide, JDK Documentation Comment Specification (JDK 17/21), Google Java Style Guide §7, Oracle Code Conventions §5.

---

## Table of Contents

1. [Two Types of Java Comments](#two-types-of-java-comments)
2. [Class and Interface Comments](#class-and-interface-comments)
3. [Method Comments](#method-comments)
4. [Field Comments](#field-comments)
5. [POJO / DTO / Entity Comments](#pojo--dto--entity-comments)
6. [Enum Comments](#enum-comments)
7. [Package and Module Comments](#package-and-module-comments)
8. [Implementation (Inline) Comments](#implementation-inline-comments)
9. [Tag Reference and Ordering](#tag-reference-and-ordering)
10. [Calibrated Examples](#calibrated-examples)

---

## Two Types of Java Comments

Java distinguishes **documentation comments** (`/** ... */`) from **implementation comments** (`//` or `/* ... */`).

Documentation comments describe the API contract — what a class, method, or field does from the caller's perspective. They are processed by the `javadoc` tool and displayed in IDEs.

Implementation comments explain the internal logic — why a particular algorithm was chosen, what a workaround addresses, or how a tricky piece of code works. They are for the maintainer reading the source.

Both types are required. Documentation comments on every public and protected API surface. Implementation comments on non-obvious internal logic.

---

## Class and Interface Comments

Every class, interface, abstract class, and annotation type requires a Javadoc comment immediately before the declaration.

Required content:
- First sentence: what this class represents or does (standalone summary, ends with period)
- Longer description if needed: design rationale, lifecycle, thread-safety, usage patterns
- `@param` for each type parameter on generic classes
- `@author` if project convention requires it (many modern projects omit this)
- `@since` for the version when this class was introduced
- `@see` for related classes
- `@deprecated` with replacement guidance if applicable

```java
/**
 * Manages user authentication and session lifecycle.
 *
 * <p>This service handles credential validation, JWT token generation,
 * and session tracking. It is thread-safe and intended to be used as
 * a singleton managed by the Spring container.
 *
 * <p>Authentication failures are logged but never throw exceptions to
 * the caller — instead, an {@link AuthResult#failure(String)} is returned
 * with the reason.
 *
 * @param <C> the credential type accepted by this authenticator
 * @since 2.1.0
 * @see AuthResult
 * @see SessionStore
 */
public class AuthenticationService<C extends Credential> {
```

For interfaces, the comment should describe the contract, not the implementation:

```java
/**
 * Repository for persisting and retrieving user entities.
 *
 * <p>Implementations must guarantee that {@link #findById(Long)} returns
 * {@link Optional#empty()} for non-existent IDs rather than throwing.
 *
 * @see JpaUserRepository
 */
public interface UserRepository {
```

---

## Method Comments

Every public and protected method requires a Javadoc comment. Private methods with non-obvious behavior should also have comments (implementation comments are acceptable for private methods).

Required tags:
- `@param` for every parameter (even if "obvious" — it is not obvious to tools and new readers)
- `@return` for every non-void method (describe the value, not just the type)
- `@throws` / `@exception` for every checked exception and every unchecked exception that is part of the contract
- `@deprecated` if applicable

The first sentence must describe what the method does, phrased as a verb in third-person declarative form ("Returns the...", "Validates the...", "Computes the..."). Do NOT use "This method..." as a prefix.

```java
/**
 * Finds a user by their unique identifier.
 *
 * <p>Searches the user store by primary key. Returns an empty Optional
 * if no user exists with the given ID — never returns {@code null}.
 *
 * @param userId the unique identifier of the user to find, must be positive
 * @return an Optional containing the user if found, or empty if not found
 * @throws IllegalArgumentException if {@code userId} is not positive
 * @see #findByEmail(String)
 */
public Optional<User> findById(long userId) {
```

For overriding methods: if the override adds no new behavior, use `{@inheritDoc}` or omit the Javadoc entirely (javadoc will inherit it). If the override adds behavior, document the additions.

```java
/**
 * {@inheritDoc}
 *
 * <p>This implementation also logs the validation result to the audit trail.
 */
@Override
public ValidationResult validate(Request request) {
```

---

## Field Comments

All public and protected fields require Javadoc comments. Private fields should have comments when the field name alone does not fully convey its purpose, units, constraints, or valid range.

```java
/**
 * Maximum number of retry attempts before the operation is considered failed.
 * Defaults to 3. Must be between 1 and 10 inclusive.
 */
private static final int MAX_RETRIES = 3;

/**
 * Timeout duration for HTTP connections in milliseconds.
 * Configured via {@code app.http.timeout-ms} property.
 */
@Value("${app.http.timeout-ms:5000}")
private int connectionTimeoutMs;
```

For constants, always document the value's meaning, not just its name. `/** Maximum retries. */` on `MAX_RETRIES` adds nothing. `/** Maximum retry attempts before the circuit breaker opens. */` adds meaning.

---

## POJO / DTO / Entity Comments

This is a critical area where comments are frequently omitted but highly valuable. Every POJO, DTO, VO, Entity, and Record class must have:

1. Class-level Javadoc describing what this data object represents
2. Field-level comments for every field, describing business meaning, constraints, and mapping

```java
/**
 * Data transfer object for user registration requests.
 *
 * <p>Carries the validated input from the registration form to the
 * {@link UserService#register(UserRegistrationDTO)} method.
 */
public class UserRegistrationDTO {

    /** User's chosen display name. Must be 2-50 characters, alphanumeric and underscores only. */
    @NotBlank
    @Size(min = 2, max = 50)
    private String username;

    /** User's email address. Used as the primary login credential and for account recovery. */
    @Email
    @NotBlank
    private String email;

    /** Plaintext password. Will be hashed with BCrypt before storage. Must be at least 8 characters. */
    @NotBlank
    @Size(min = 8)
    private String password;

    /** ISO 3166-1 alpha-2 country code. Determines tax jurisdiction and content availability. */
    @Size(min = 2, max = 2)
    private String countryCode;
}
```

For JPA/Hibernate entities, also document the database mapping:

```java
/**
 * Persistent entity representing a product in the catalog.
 *
 * <p>Maps to the {@code products} table. Uses optimistic locking via
 * the {@link #version} field.
 *
 * @see ProductRepository
 */
@Entity
@Table(name = "products")
public class Product {

    /** Auto-generated primary key (BIGINT, identity strategy). */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Product SKU code. Unique across the catalog. Indexed for fast lookup. */
    @Column(unique = true, nullable = false, length = 32)
    private String sku;

    /** Current unit price in the catalog's base currency (USD). Stored as cents to avoid floating-point issues. */
    @Column(nullable = false)
    private Long priceInCents;

    /** Optimistic lock version. Managed by Hibernate — do not set manually. */
    @Version
    private Integer version;
}
```

---

## Enum Comments

Every enum type and every enum constant requires a Javadoc comment.

```java
/**
 * Represents the lifecycle states of an order in the fulfillment pipeline.
 *
 * <p>Orders progress through these states linearly, except for {@link #CANCELLED}
 * which can be reached from any state before {@link #SHIPPED}.
 */
public enum OrderStatus {

    /** Order has been created but payment has not been confirmed yet. */
    PENDING,

    /** Payment confirmed. Order is queued for warehouse processing. */
    CONFIRMED,

    /** Order has been picked, packed, and handed to the shipping carrier. */
    SHIPPED,

    /** Carrier has confirmed delivery to the recipient. Terminal state. */
    DELIVERED,

    /** Order was cancelled before shipping. Terminal state. Triggers refund if payment was confirmed. */
    CANCELLED
}
```

---

## Package and Module Comments

Packages should have a `package-info.java` file with a package-level Javadoc comment describing the package's purpose and contents:

```java
/**
 * User authentication and authorization domain.
 *
 * <p>This package contains the core authentication services, credential
 * validators, and session management components. All public APIs in this
 * package are thread-safe.
 *
 * <p>Key entry points:
 * <ul>
 *   <li>{@link com.example.auth.AuthenticationService} — primary authentication facade</li>
 *   <li>{@link com.example.auth.SessionStore} — session lifecycle management</li>
 * </ul>
 *
 * @since 1.0.0
 */
package com.example.auth;
```

For Java modules (JPMS), the `module-info.java` should also have a Javadoc comment.

---

## Implementation (Inline) Comments

Use `//` for single-line implementation comments. Place them on the line above the code they describe, not at the end of the line (unless very short).

Required inline comments:
- Before algorithm blocks: explain the approach
- Before non-obvious conditionals: explain why this condition matters
- Before error handling: explain what failure this catches and why
- Before workarounds: explain the bug/issue and link to the tracker
- On magic numbers that can't be made into named constants

```java
// Use binary search since the list is pre-sorted by insertion order
int index = Collections.binarySearch(sortedUsers, targetUser, BY_CREATION_DATE);

// Negative index means not found — convert to insertion point per binarySearch contract
if (index < 0) {
    index = -(index + 1);
}

// HACK: Vendor API returns HTTP 200 with error body instead of proper error codes.
// See: https://issues.example.com/PROJ-1234
if (response.getStatusCode() == 200 && response.getBody().contains("error")) {
    throw new VendorApiException(response.getBody());
}
```

---

## Tag Reference and Ordering

Standard Javadoc tag order (per Oracle convention):

1. `@param` (in parameter declaration order)
2. `@return`
3. `@throws` / `@exception` (in alphabetical order by exception class)
4. `@see`
5. `@since`
6. `@serial` / `@serialField` / `@serialData`
7. `@deprecated`

Inline tags: `{@code ...}` for code literals, `{@link ...}` for cross-references, `{@inheritDoc}` for inherited doc, `{@literal ...}` for HTML-sensitive text.

Use `{@code null}` not `null` or `<code>null</code>`. Use `{@link ClassName}` for the first reference to a related class in a comment, `{@code ClassName}` for subsequent references.

Use `<p>` to start new paragraphs within long Javadoc comments.