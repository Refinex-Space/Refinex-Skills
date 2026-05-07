---
name: dev-java
description: Enforce production-grade Java development standards when writing, reviewing, or architecting Java code. Covers commenting, core Java idioms (Stream, collections, concurrency, generics), 23 GoF design patterns, SonarQube/Alibaba p3c/Lombok rules, Spring Boot MVC structure, Spring Cloud DDD microservices, MyBatis/JPA/transaction management, exception handling, logging, REST API design, testing, and security. Trigger whenever the user writes Java code, reviews Java code, designs a Spring Boot or Spring Cloud project, implements a design pattern, fixes code smells, discusses architecture, or asks about Java best practices. Also trigger when Java code is pasted for feedback or the user asks about package structure, DTO/VO/PO conventions, or coding standards.
---

# Java Development Standards

This skill ensures every line of Java code produced follows battle-tested, production-grade standards drawn from the Alibaba Java Coding Guidelines, Effective Java, SonarQube rules, Spring ecosystem conventions, and DDD principles.

## The failure mode this skill fights

Without this skill, AI-generated Java code tends toward "compiles and runs" quality — it works but violates naming conventions, ignores thread safety, swallows exceptions, uses raw types, nests logic too deeply, mixes concerns across layers, produces anemic domain models, and omits Javadoc. The code passes a smoke test but fails a code review. This skill exists to close the gap between "working code" and "production-ready code that a senior engineer would approve."

---

## How to use this skill

This skill operates in two modes:

### Mode 1: Code Generation
When writing new Java code, **before** you start coding, identify which domains apply and read the corresponding reference files. Then write code that satisfies every applicable standard. Do not write code first and retrofit standards later — the standards shape the design.

### Mode 2: Code Review
When reviewing or refactoring existing Java code, read the relevant reference files, then systematically check the code against each applicable rule. Report violations grouped by severity: **Blocker** (must fix before merge), **Critical** (should fix in this PR), **Major** (fix soon), **Suggestion** (consider improving).

---

## Domain routing table

Every Java task touches one or more domains. Read the reference file **before** writing or reviewing code in that domain. If multiple domains apply (they usually do), read all of them.

| The task involves…                                            | Read this reference                              |
| ------------------------------------------------------------- | ------------------------------------------------ |
| Any Java code (always read this first)                        | `references/core-java-standards.md`              |
| Comments, Javadoc, XML/YAML/Properties annotations            | `references/commenting-standards.md`             |
| Choosing or implementing a design pattern                     | `references/design-patterns-standards.md`        |
| Static analysis, code smells, Lombok, formatting              | `references/static-analysis-standards.md`        |
| Spring Boot monolith / MVC layered project                    | `references/spring-boot-mvc-standards.md`        |
| Spring Cloud microservices / DDD architecture                 | `references/spring-cloud-ddd-standards.md`       |
| Database access: MyBatis, JPA, JdbcTemplate, transactions     | `references/data-access-standards.md`            |
| Exception handling, logging, error responses                  | `references/exception-logging-standards.md`      |
| RESTful API design, versioning, pagination, HATEOAS           | `references/api-design-standards.md`             |
| Unit tests, integration tests, mocking, TDD                  | `references/testing-standards.md`                |
| Authentication, authorization, input validation, secrets      | `references/security-standards.md`               |
| Build tools, CI/CD, Docker, dependency management             | `references/devops-build-standards.md`           |

**Always-read rule**: `references/core-java-standards.md` applies to every Java task. For any non-trivial class, also read `references/commenting-standards.md`. These two are the baseline — skip them only for one-liner utility answers.

---

## Universal principles (apply to ALL Java code)

These principles are so fundamental that they live here in the SKILL.md rather than in reference files, because they must be in context for every task.

### 1. Naming is design

Names carry intent. A reader should understand what code does from its names alone, without reading the implementation.

- Classes: UpperCamelCase, noun or noun phrase. Include the pattern name if a design pattern is used (`OrderFactory`, `LoginProxy`, `ResourceObserver`).
- Methods: lowerCamelCase, verb or verb phrase. Boolean-returning methods start with `is/has/can/should`.
- Constants: UPPER_SNAKE_CASE. Only truly immutable values — not every `static final` qualifies.
- Packages: all lowercase, reverse domain. No underscores, no uppercase, no abbreviations (`com.company.project.module`).
- No meaningless names: `data`, `info`, `temp`, `obj`, `result` without qualification are code smells.
- No Hungarian notation, no type prefixes (`strName`, `iCount`), no single-letter variables except loop indices and lambdas.

### 2. Fail fast, fail loud

- Validate method parameters at entry. Use `Objects.requireNonNull()` for non-null contracts.
- Throw specific exceptions — never `throw new Exception()` or `throw new RuntimeException()` with a bare message.
- Never swallow exceptions. `catch (Exception e) { }` is a Blocker-level violation.
- Never use exceptions for flow control. Exceptions are for exceptional conditions, not business logic branching.

### 3. Immutability by default

- Prefer `final` for fields, parameters, and local variables.
- Use unmodifiable collections (`List.of()`, `Map.of()`, `Collections.unmodifiableList()`) for return values.
- DTOs and value objects should be records (Java 16+) or have all-final fields with no setters.
- Mutable state should be explicitly justified, never the default choice.

### 4. Composition over inheritance

- Prefer interface + delegation over class inheritance.
- Never inherit just to reuse code — that is what composition is for.
- Inheritance is for "is-a" relationships only, and even then, favor sealed classes (Java 17+) to control the hierarchy.

### 5. Minimize scope, minimize access

- Every field, method, and class should have the narrowest possible access modifier.
- Local variables should be declared at the point of first use, not at the top of the method.
- A method that doesn't need instance state should be `static`.
- A utility class should have a `private` constructor and only static methods.

### 6. SOLID is non-negotiable

- **S**ingle Responsibility: One class, one reason to change. If you struggle to name a class concisely, it does too much.
- **O**pen-Closed: Extend behavior through abstraction, not modification. Use Strategy, Template Method, or event listeners.
- **L**iskov Substitution: Subtypes must be substitutable for their base types without breaking contracts.
- **I**nterface Segregation: Prefer many small interfaces over one fat interface. A class should never be forced to implement methods it doesn't use.
- **D**ependency Inversion: Depend on abstractions, not concretions. In Spring, inject interfaces, not implementation classes.

---

## Code generation checklist

Before delivering any Java code to the user, verify:

1. **Naming**: Every class, method, field, parameter, and local variable follows the naming rules above.
2. **Comments**: Public classes and public methods have Javadoc. Complex logic has inline clarification. No obvious/redundant comments.
3. **Null safety**: No bare null returns from public methods. Use `Optional` for genuinely optional values. Validate inputs.
4. **Thread safety**: If the code may run in a concurrent context, state is either immutable, properly synchronized, or uses `java.util.concurrent` constructs.
5. **Resource management**: All `Closeable`/`AutoCloseable` resources use try-with-resources.
6. **Exception handling**: Checked exceptions are caught and handled or declared. No generic catches. No swallowed exceptions.
7. **Collections**: Typed with generics. No raw types. Correct choice of implementation (ArrayList vs LinkedList, HashMap vs ConcurrentHashMap).
8. **Streams**: Not abused for simple loops. Side-effect-free. Terminal operation present.
9. **Logging**: Uses SLF4J facade with parameterized messages. No `System.out.println()` or `e.printStackTrace()`.
10. **Formatting**: Consistent indentation (4 spaces). Line length ≤ 120 characters. One statement per line.

---

## Code review severity levels

When reviewing code, classify violations:

**Blocker** — Production incident risk. Must fix before merge.
Examples: swallowed exceptions, thread-unsafe shared mutable state, SQL injection vectors, hardcoded credentials, resource leaks.

**Critical** — Correctness or maintainability risk. Should fix in this PR.
Examples: raw types, missing null checks on external input, overly broad exception catches, missing `@Transactional` on service methods that need atomicity.

**Major** — Code quality issue. Fix within the sprint.
Examples: missing Javadoc on public API, god class (>500 lines), deep nesting (>3 levels), magic numbers, copy-paste code.

**Suggestion** — Improvement opportunity. Consider for next iteration.
Examples: could use a design pattern, could extract a helper method, could use a more specific collection type, could add a builder.

---

## Quick reference: common anti-patterns to catch

These are the most frequent violations in AI-generated and junior-developer Java code. Be vigilant:

1. **Anemic domain model**: Entity classes with only getters/setters and no behavior. Business logic scattered in service classes.
2. **God class**: A single class handling multiple responsibilities (>300 lines is a yellow flag, >500 is red).
3. **Primitive obsession**: Using `String` for email, phone, money instead of value objects.
4. **Exception swallowing**: `catch (Exception e) { log.error("error"); }` — loses the stack trace. Always log `e` as the second argument.
5. **Null ping-pong**: Methods returning null, callers checking for null, chains of null checks. Use `Optional` or throw.
6. **Magic strings/numbers**: `if (status == 1)` instead of `if (status == OrderStatus.ACTIVE)`.
7. **Transaction boundary leak**: `@Transactional` on a private method (doesn't work with Spring proxies) or on a controller (too broad).
8. **N+1 query**: Lazy-loading a collection in a loop. Use `JOIN FETCH` or batch fetching.
9. **Service-to-service direct coupling**: In microservices, calling another service synchronously in a transaction. Use events or async.
10. **Test-free delivery**: No unit tests for business logic. At minimum, test the happy path and one error path.

---

## Language and output conventions

- Code comments and Javadoc: match the language the user is communicating in. If the user writes in Chinese, comments should be in Chinese; if English, in English.
- Variable names, class names, method names: always in English, regardless of the user's language.
- When explaining standards, cite the specific rule source (e.g., "Alibaba Java Coding Guidelines §1.3.1" or "Effective Java Item 17").
- When generating code, include a brief comment block at the top stating which standards were applied.

---

## Reference files — table of contents

Each reference file begins with a scope declaration and a table of contents. They are self-contained for their domain. Here is a summary of what each covers, so you can decide which to read:

**core-java-standards.md** (~400 lines) — Java language-level standards: generics, collections, Stream API, Optional, concurrency (java.util.concurrent, virtual threads), I/O (NIO.2, try-with-resources), reflection, SPI, records, sealed classes, pattern matching. The foundation everything else builds on.

**commenting-standards.md** (~200 lines) — Javadoc for classes/interfaces/methods/fields, POJO annotation comments, inline comments, XML/YAML/Properties file comments, TODO/FIXME conventions, changelog headers.

**design-patterns-standards.md** (~400 lines) — All 23 GoF patterns + Builder variant, organized by creation/structural/behavioral. For each: one-sentence definition, when to use, when NOT to use, Java/Spring idiomatic implementation, and common misuses.

**static-analysis-standards.md** (~250 lines) — SonarQube critical rules, Alibaba p3c plugin alignment, Lombok safe usage (which annotations to use and which to avoid), Checkstyle/SpotBugs key rules, code formatting standards.

**spring-boot-mvc-standards.md** (~350 lines) — Project structure (layer-based and feature-based), Controller/Service/Repository conventions, configuration management, profile strategy, auto-configuration, starter dependencies, actuator, graceful shutdown.

**spring-cloud-ddd-standards.md** (~400 lines) — DDD tactical patterns (Entity, Value Object, Aggregate, Domain Event, Repository, Domain Service, Application Service), bounded context mapping, hexagonal architecture layout, Spring Cloud component selection (Gateway, Config, Circuit Breaker, Service Discovery), inter-service communication patterns, CQRS/Event Sourcing basics.

**data-access-standards.md** (~300 lines) — MyBatis XML mapper standards, MyBatis-Plus code generation and wrapper usage, JPA entity mapping and query optimization, JdbcTemplate usage patterns, transaction management (`@Transactional` semantics, propagation, isolation, read-only), N+1 prevention, connection pool configuration.

**exception-logging-standards.md** (~200 lines) — Exception hierarchy design, global exception handling (`@ControllerAdvice`), error response format, SLF4J + Logback configuration, log level semantics, structured logging, MDC for distributed tracing, log rotation and retention.

**api-design-standards.md** (~200 lines) — RESTful URL naming, HTTP method semantics, status code selection, request/response DTO design, pagination/sorting/filtering, API versioning, idempotency, rate limiting, OpenAPI/Swagger documentation.

**testing-standards.md** (~250 lines) — JUnit 5 conventions, Mockito usage patterns, Spring Boot test slicing (@WebMvcTest, @DataJpaTest), integration testing strategy, test naming, test data management, coverage expectations, contract testing basics.

**security-standards.md** (~200 lines) — Spring Security configuration, authentication/authorization patterns, input validation (@Valid, custom validators), OWASP Top 10 in Java context, secrets management, CORS, CSRF, SQL injection prevention, XSS prevention.

**devops-build-standards.md** (~200 lines) — Maven/Gradle conventions, multi-module project structure, dependency management (BOM, version catalogs), Docker image optimization, CI/CD pipeline stages, environment configuration, health checks.