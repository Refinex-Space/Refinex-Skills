# Design Patterns Standards

> **Scope**: All 23 GoF patterns + modern variants. For each: when to use, when NOT to use, Java/Spring idiomatic implementation, and common misuses.

## Table of Contents

1. Core Principle: Patterns Are Tools, Not Goals
2. Creational Patterns (5 + Builder variant)
3. Structural Patterns (7)
4. Behavioral Patterns (11)
5. Pattern Selection Decision Guide

---

## 1. Core Principle: Patterns Are Tools, Not Goals

Never apply a pattern because "it is good practice." Apply a pattern when you have identified a specific design problem that the pattern solves. The cost of a misapplied pattern — indirection, complexity, extra classes — is worse than no pattern at all.

**The refactoring rule**: Prefer refactoring toward a pattern as complexity emerges over pre-emptively applying one. Start with the simplest possible implementation. When you feel the pain of adding a third payment method, then introduce Strategy. When you feel the pain of creating complex objects with 8+ parameters, then introduce Builder.

**The Spring ecosystem rule**: Many GoF patterns are already embedded in Spring. Before implementing a pattern manually, check if Spring provides it: Spring's `@Component` + dependency injection is Factory/Abstract Factory. Spring AOP is Proxy. `@EventListener` is Observer. `RestTemplate`/`WebClient` interceptors are Chain of Responsibility. `JdbcTemplate`/`JmsTemplate` is Template Method.

---

## 2. Creational Patterns

### Singleton

**Use when**: Exactly one instance is needed JVM-wide AND the instance manages shared state or a scarce resource (database connection pool, configuration registry, thread pool). **In Spring**: Almost every bean is singleton-scoped by default. Do NOT manually implement Singleton in Spring applications — use `@Component` or `@Bean`. **Manual implementation** (when not in Spring): Use an enum singleton — it is thread-safe, serialization-safe, and reflection-proof: `public enum AppConfig { INSTANCE; }`. **Never**: Use Singleton just to make a class "globally accessible." That is a global variable in disguise. If the class has no shared state, it does not need to be a singleton.

### Factory Method

**Use when**: Object creation logic involves conditional branching based on a type/parameter, and you want to decouple the caller from the concrete class. Example: `PaymentProcessorFactory.create(PaymentType type)` returns `CreditCardProcessor`, `AlipayProcessor`, etc. **In Spring**: Use `@Configuration` + `@Bean` methods, or `FactoryBean<T>` for complex creation. Use `@Conditional` for conditional bean creation. **Never**: Over-engineer simple `new` calls. If there is only one implementation and no foreseeable variation, a factory adds complexity without benefit.

### Abstract Factory

**Use when**: You need to create families of related objects that must be used together, and you want to swap entire families at once. Example: `UIComponentFactory` producing `Button`, `TextField`, `Dialog` — one factory for Material design, another for iOS design. **In Spring**: Auto-configuration with `@ConditionalOnClass`/`@ConditionalOnProperty` effectively acts as an abstract factory, creating related beans based on the environment. **Never**: Use Abstract Factory when you only have one product family. It is overkill until you genuinely need to swap families.

### Builder

**Use when**: An object has more than 4 constructor parameters, or has many optional parameters, or requires step-by-step construction with validation. This is the most commonly used creational pattern in modern Java. **Implementation**: Use a static inner `Builder` class with fluent setters returning `this`, and a `build()` method that validates and constructs. Alternatively, use Lombok `@Builder` (but see static-analysis-standards.md for Lombok caveats). **With records**: Records have a canonical constructor, but for complex records, provide a Builder that calls the canonical constructor. **Never**: Use Builder for simple 2-3 field objects. A constructor or static factory method is simpler and clearer.

### Prototype

**Use when**: Creating a new object is expensive (deep copying a complex object graph, or cloning a configuration template) and you have an existing instance to base it on. **Implementation**: Implement `Cloneable` and override `clone()` — but beware: `clone()` is shallow by default. For deep copy, serialize/deserialize or manually copy nested objects. Modern alternative: provide a copy constructor `public Order(Order source)` or a `toBuilder()` method. **Never**: Use Prototype when construction is cheap. The cloning mechanism adds complexity without benefit.

---

## 3. Structural Patterns

### Adapter

**Use when**: You need to make an existing class work with an interface it doesn't implement, typically when integrating third-party libraries or legacy code. **Example**: Wrapping a legacy `XmlReportGenerator` to implement your `ReportGenerator` interface. **In Spring**: Use `@Component` to register an adapter as a bean. `HandlerAdapter` in Spring MVC is a framework-level adapter. **Never**: Use Adapter when you own both sides and can simply change the interface. Adapter is for when you cannot modify the adaptee.

### Bridge

**Use when**: You want to decouple an abstraction from its implementation so both can vary independently. **Example**: `Notification` (abstraction: Email, SMS, Push) × `MessageFormatter` (implementation: PlainText, HTML, Markdown). Without Bridge, you'd need `EmailPlainTextNotification`, `EmailHtmlNotification`, etc. — combinatorial explosion. **Never**: Use Bridge for simple hierarchies where only one dimension varies. If there is no "cross-product" problem, you don't need Bridge.

### Composite

**Use when**: You need to treat individual objects and compositions of objects uniformly through a tree structure. **Example**: `MenuItem` that can be a leaf (a single action) or a composite (a submenu containing more items). File system operations on files and directories. **In Spring**: Spring Security's `FilterChain` is a composite of filters. **Never**: Force a tree structure where a flat list would suffice. Not every hierarchy needs Composite.

### Decorator

**Use when**: You need to add responsibilities to objects dynamically, without modifying their class. **Example**: `BufferedInputStream` decorating `FileInputStream`. A `LoggingService` wrapping `OrderService` to add audit logging. **In Spring**: AOP (`@Around` advice) is essentially the Decorator pattern at the proxy level. Use AOP for cross-cutting concerns (logging, metrics, security) instead of manual decorators. **Never**: Use Decorator when inheritance would be simpler and the class hierarchy is stable. Decorators add indirection.

### Facade

**Use when**: You want to provide a simplified interface to a complex subsystem. **Example**: An `OrderFacade` that coordinates `InventoryService`, `PaymentService`, `ShippingService`, and `NotificationService` behind a single `placeOrder()` method. **In Spring**: Application services (in DDD) are often facades over domain services. `@Service`-annotated classes that coordinate multiple repositories and services are facades. **Never**: Create a facade that simply delegates to a single service with no simplification. That is a useless layer.

### Proxy

**Use when**: You need to control access to an object — lazy initialization, access control, logging, caching, remote invocation. **In Spring**: Spring's entire AOP and transaction management is proxy-based. `@Transactional`, `@Cacheable`, `@Async` all work through JDK dynamic proxies or CGLIB proxies. Understand this: Spring proxies only intercept external method calls. Internal method calls (`this.method()`) bypass the proxy — this is why `@Transactional` on a private method or a self-invoked method does not work. **Never**: Use Proxy when direct access is fine and you have no cross-cutting concern. Proxies add overhead and can cause subtle bugs (e.g., Spring's proxy-based `@Transactional` self-invocation trap).

### Flyweight

**Use when**: You need to share a large number of fine-grained objects efficiently to save memory. **Example**: `Integer.valueOf()` caches instances from -128 to 127. `String.intern()` shares string instances. Character rendering where each character glyph is shared. **In Spring**: Singleton beans are conceptually flyweights — shared instances. `@Value` annotation injecting the same property across multiple beans avoids duplication. **Never**: Prematurely optimize with Flyweight. Only apply when memory profiling shows that object duplication is a real problem.

---

## 4. Behavioral Patterns

### Strategy

**Use when**: You have multiple algorithms/behaviors for a task and want to select one at runtime. This is the most common behavioral pattern. **Example**: Sorting algorithms, pricing calculations, validation rules, notification channels. **In Spring**: Inject a `Map<String, Strategy>` or `List<Strategy>` via `@Autowired`. Spring auto-discovers all implementations. Use `@Qualifier` or a custom `StrategySelector` to choose at runtime. **Implementation tip**: Strategy + Factory is a powerful combination. The factory selects the strategy; the strategy executes the algorithm.

### Observer (Event-Driven)

**Use when**: An object needs to notify other objects of state changes without knowing who or how many observers exist. **In Spring**: Use `ApplicationEventPublisher` + `@EventListener` (or `@TransactionalEventListener` for events that should fire after a transaction commits). Prefer Spring events over manual Observer implementations — they integrate with the transaction lifecycle. For microservices, use message brokers (Kafka, RabbitMQ) as distributed observers.

### Template Method

**Use when**: You have an algorithm skeleton with steps that vary across implementations. **Example**: Data export with fixed steps (validate → query → transform → write) where the transform and write steps vary by format. **In Spring**: `JdbcTemplate`, `RestTemplate`, `JmsTemplate` are classic template methods — the template handles boilerplate (connection, exception handling), you supply the variable logic via callbacks. **Prefer composition over inheritance**: Instead of abstract classes with template methods, consider Strategy with a procedural orchestrator. Composition is more flexible and testable.

### Chain of Responsibility

**Use when**: You want to pass a request along a chain of handlers where each handler decides to process or pass it along. **Example**: Approval workflows, validation chains, filter pipelines. **In Spring**: `Filter` chains in Spring Security, `HandlerInterceptor` chains in Spring MVC, `WebFilter` in WebFlux.

### Command

**Use when**: You need to encapsulate a request as an object — to queue operations, support undo/redo, or log commands for auditing. **Example**: Task queue processing, undo-capable editors, transaction logging. **In Spring**: `@Async` methods are essentially commands dispatched to a thread pool. CQRS command objects in DDD are the Command pattern.

### State

**Use when**: An object's behavior changes based on its internal state, and you want to avoid large switch/if-else blocks. **Example**: Order state machine (Pending → Confirmed → Shipped → Delivered), document workflow (Draft → Review → Published). **Implementation**: Define a `State` interface with methods for each action. Each concrete state implements the interface differently. The context object delegates to its current state. **In Spring**: Consider Spring State Machine for complex state transitions.

### Mediator

**Use when**: Communication between multiple objects becomes complex, and you want a central coordinator. **Example**: Chat room mediating messages between users. Form dialog coordinating validation between dependent fields. **Never**: Use Mediator when direct communication between two objects is simple. A mediator adds unnecessary indirection for simple interactions.

### Iterator

**Use when**: You need a standard mechanism to traverse a collection without exposing its internal structure. **In Java**: Already built into the language via `Iterable`/`Iterator` and the enhanced for-loop. Rarely need to implement manually. Custom iterators are needed for custom data structures (trees, graphs) or paginated database results.

### Visitor

**Use when**: You need to add operations to a class hierarchy without modifying the classes, especially for double dispatch. **Example**: AST (Abstract Syntax Tree) processing, document export to multiple formats. **Modern alternative**: With sealed classes (Java 17+) and pattern matching for switch (Java 21+), many Visitor use cases are better served by switch expressions — less boilerplate, no accept/visit ceremony.

### Memento

**Use when**: You need to capture and restore an object's state without violating encapsulation. **Example**: Undo/redo in editors, transaction rollback, checkpoint/restore. **Implementation**: The originator creates a memento (an opaque snapshot); the caretaker stores it; the originator can later restore from it. The memento should be immutable.

### Interpreter

**Use when**: You have a language/grammar to parse and evaluate. **Example**: SQL parsers, expression evaluators, rule engines. This is the least commonly used GoF pattern in typical business applications. Prefer established parsing libraries (ANTLR, JavaCC) over manual Interpreter implementations.

---

## 5. Pattern Selection Decision Guide

Instead of memorizing patterns, ask these questions:

**"I need to create objects flexibly"** → Factory Method (single product), Abstract Factory (product families), Builder (complex construction), Prototype (clone existing).

**"I need to compose or wrap objects"** → Decorator (add behavior), Composite (tree structure), Adapter (interface mismatch), Proxy (control access), Facade (simplify subsystem).

**"I need to vary behavior"** → Strategy (swap algorithms), State (behavior depends on state), Template Method (fixed skeleton, variable steps), Command (encapsulate as object).

**"I need to decouple communication"** → Observer (one-to-many notifications), Mediator (many-to-many coordination), Chain of Responsibility (sequential processing).

**"I need to traverse or process structures"** → Iterator (sequential access), Visitor (operations on hierarchies).

When two patterns seem appropriate, choose the simpler one. When no pattern fits, do not force one — sometimes a well-structured method is the right answer.