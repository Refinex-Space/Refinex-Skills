# Testing Standards

> **Scope**: JUnit 5 conventions, Mockito usage patterns, Spring Boot test slicing (@WebMvcTest, @DataJpaTest), integration testing strategy, test naming, test data management, coverage expectations, contract testing basics.

## Table of Contents

1. Testing Philosophy
2. JUnit 5 Conventions
3. Mockito Standards
4. Spring Boot Test Slicing
5. Test Naming and Organization
6. Test Data Management
7. Coverage Expectations

---

## 1. Testing Philosophy

The test pyramid applies: many unit tests (fast, isolated), fewer integration tests (slower, test component wiring), very few end-to-end tests (slowest, test the full stack). A typical ratio is 70% unit / 20% integration / 10% E2E.

Every public method in a service class must have at least one happy-path test and one error-path test. Critical business logic (pricing, permissions, state transitions) must have exhaustive edge case testing.

Tests are first-class code. They follow the same naming, formatting, and documentation standards as production code. No `test1()`, `test2()` names. No copy-paste test methods with minor variations — use parameterized tests.

---

## 2. JUnit 5 Conventions

Use JUnit 5 (`jupiter`) exclusively in new projects. Do not mix JUnit 4 (`@Test` from `org.junit`) with JUnit 5 (`@Test` from `org.junit.jupiter.api`) in the same project.

Use `@DisplayName` for human-readable test descriptions in reports. Use `@Nested` to group related tests into logical sections within a test class.

```java
@DisplayName("OrderService")
class OrderServiceTest {

    @Nested
    @DisplayName("createOrder")
    class CreateOrder {

        @Test
        @DisplayName("should create order with valid input and sufficient inventory")
        void shouldCreateOrderWithValidInput() {
            // Arrange
            // Act
            // Assert
        }

        @Test
        @DisplayName("should throw when inventory is insufficient")
        void shouldThrowWhenInventoryInsufficient() {
            // Arrange
            // Act & Assert
            assertThrows(InsufficientInventoryException.class,
                () -> orderService.createOrder(request));
        }
    }
}
```

Use `assertAll()` to group related assertions — all assertions execute even if one fails, giving a complete picture of failures.

```java
assertAll("order properties",
    () -> assertEquals(OrderStatus.PENDING, result.getStatus()),
    () -> assertEquals(3, result.getItems().size()),
    () -> assertNotNull(result.getCreatedAt())
);
```

Use `@ParameterizedTest` with `@ValueSource`, `@CsvSource`, `@MethodSource`, or `@EnumSource` for data-driven tests that cover multiple inputs with the same assertion logic.

```java
@ParameterizedTest
@CsvSource({
    "0,    false",
    "1,    true",
    "99,   true",
    "100,  true",
    "101,  false",
    "-1,   false"
})
@DisplayName("should validate quantity within allowed range [1-100]")
void shouldValidateQuantity(int quantity, boolean expected) {
    assertEquals(expected, validator.isValidQuantity(quantity));
}
```

---

## 3. Mockito Standards

Use `@ExtendWith(MockitoExtension.class)` with JUnit 5 (not the JUnit 4 `@RunWith`).

Prefer `@Mock` for dependencies and `@InjectMocks` for the class under test. Use `@Spy` only when you need to stub specific methods while keeping real implementations for others — which is rare and often a sign that the class has too many responsibilities.

**Stubbing rules**: Use `when(...).thenReturn(...)` for simple stubs. Use `when(...).thenThrow(...)` for error scenarios. Use `doReturn(...).when(spy).method(...)` for spies. Never over-stub — only stub the calls that the test scenario requires. If a test needs more than 5 stubs, the class under test probably violates Single Responsibility.

**Verification rules**: Use `verify(mock).method(args)` to assert that an interaction occurred. Use `verify(mock, never()).method(...)` to assert it did not. Use `verifyNoMoreInteractions(mock)` sparingly — it makes tests brittle.

**Argument matchers**: Use `any()`, `eq()`, `argThat(...)` for flexible argument matching. When using matchers, all arguments must use matchers — mixing matchers with raw values causes Mockito errors.

```java
// Correct
verify(repository).save(argThat(order ->
    order.getStatus() == OrderStatus.PENDING &&
    order.getItems().size() == 3
));

// Wrong — mixing raw value with matcher
verify(repository).findByIdAndStatus(123L, eq(OrderStatus.PENDING)); // Error!
```

---

## 4. Spring Boot Test Slicing

Full `@SpringBootTest` loads the entire application context. It is slow and should be used only for integration tests that need the full stack. For focused tests, use sliced annotations.

**`@WebMvcTest(OrderController.class)`**: Loads only the web layer (controller, filters, advice). Mock service dependencies with `@MockBean`. Use `MockMvc` to test HTTP request handling, validation, serialization, and error responses without starting a real server.

**`@DataJpaTest`**: Loads only JPA components (entities, repositories, EntityManager). Uses an embedded database by default. Tests repository queries and entity mappings.

**`@DataJpaTest` with real database**: Use Testcontainers to run a real database instance in Docker for integration tests that need database-specific behavior (e.g., MySQL-specific queries).

```java
@DataJpaTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@Testcontainers
class OrderRepositoryTest {

    @Container
    static MySQLContainer<?> mysql = new MySQLContainer<>("mysql:8.0")
        .withDatabaseName("testdb");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", mysql::getJdbcUrl);
        registry.add("spring.datasource.username", mysql::getUsername);
        registry.add("spring.datasource.password", mysql::getPassword);
    }
}
```

**`@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)`**: Full integration test with a real HTTP server. Use `TestRestTemplate` or `WebTestClient` to make real HTTP calls. Reserve for end-to-end scenarios.

---

## 5. Test Naming and Organization

Test class names: `{ClassUnderTest}Test` for unit tests, `{ClassUnderTest}IT` for integration tests. Example: `OrderServiceTest`, `OrderControllerIT`.

Test method names must describe the scenario and expected outcome. Use the pattern: `should{ExpectedBehavior}When{Scenario}`. Examples: `shouldReturnOrderWhenIdExists`, `shouldThrowWhenQuantityExceedsLimit`.

Follow the Arrange-Act-Assert (AAA) or Given-When-Then structure within each test method. Separate the three sections with blank lines. Each test must test exactly one behavior.

Place test files in the same package as the class under test (under `src/test/java`). This allows testing package-private methods when necessary.

---

## 6. Test Data Management

Use test builders or factory methods to create test data. Do not construct test objects inline with 15 setter calls.

```java
// Test data builder
public class OrderTestFixtures {
    public static Order.Builder defaultOrder() {
        return Order.builder()
            .customerId(1L)
            .status(OrderStatus.PENDING)
            .totalAmount(new BigDecimal("99.99"))
            .createdAt(LocalDateTime.now());
    }
}

// Usage in tests
Order order = OrderTestFixtures.defaultOrder()
    .status(OrderStatus.CANCELLED)
    .build();
```

For database integration tests, use `@Sql` to load test data from SQL scripts, or use `TestEntityManager` to insert entities in `@BeforeEach`. Always clean up after tests — use `@Transactional` on test classes (auto-rolls back) or explicit cleanup in `@AfterEach`.

---

## 7. Coverage Expectations

Code coverage is a necessary but insufficient quality metric. High coverage does not guarantee well-tested code, but low coverage guarantees untested code.

**Minimum thresholds**: Overall line coverage ≥ 70%. Service layer (business logic) coverage ≥ 85%. Utility classes and converters ≥ 90%. Controller layer coverage via integration tests ≥ 60%. Configuration classes and POJOs: coverage not mandated.

Enforce coverage thresholds in CI with JaCoCo. Fail the build when coverage drops below the threshold for the service layer.

Focus on meaningful coverage, not coverage gaming. Writing `assertEquals(true, true)` to inflate numbers is worse than having lower coverage. Every test should assert a meaningful behavior.