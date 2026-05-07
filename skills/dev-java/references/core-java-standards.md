# Core Java Standards

> **Scope**: Java language-level standards that apply to every line of Java code regardless of framework. Covers generics, collections, Stream API, Optional, concurrency, I/O, reflection, SPI, modern Java features (records, sealed classes, pattern matching).

## Table of Contents

1. Generics
2. Collections
3. Stream API and Functional Programming
4. Optional
5. Concurrency
6. I/O and Resource Management
7. Reflection and SPI
8. Modern Java Features (Java 17+)
9. Equality, Hashing, and Comparison
10. String Handling

---

## 1. Generics

Always parameterize generic types. Raw types (`List` instead of `List<String>`) are Blocker-level violations — they bypass compile-time type safety and exist only for pre-Java-5 compatibility.

Use bounded wildcards to increase API flexibility: `<? extends T>` for producers (you read from them), `<? super T>` for consumers (you write to them). This is the PECS rule (Producer Extends, Consumer Super). If a parameter is both a producer and consumer, use the exact type — no wildcard.

Prefer `List<? extends Number>` over `List<Number>` for method parameters when the method only reads from the list. This lets callers pass `List<Integer>`, `List<Double>`, etc.

Never use raw types in new code, suppress `@SuppressWarnings("unchecked")` only with a comment explaining why the cast is safe, and prefer type inference (`var`, diamond operator `<>`) where the type is obvious from context.

For generic methods, place the type parameter declaration before the return type: `public <T extends Comparable<T>> T max(Collection<T> collection)`.

---

## 2. Collections

**Choosing the right implementation matters.** The wrong collection can cause O(n) operations where O(1) was available.

`ArrayList` is the default `List` choice. Use `LinkedList` only when you genuinely need constant-time insertions/removals at arbitrary positions AND you already hold the iterator — which is rare in practice. If in doubt, use `ArrayList`.

`HashMap` is the default `Map` choice. Use `ConcurrentHashMap` when multiple threads access the map and at least one modifies it. Use `LinkedHashMap` when iteration order must match insertion order. Use `TreeMap` when you need sorted keys. Never use `Hashtable` — it is legacy.

`HashSet` is the default `Set` choice. Use `LinkedHashSet` for insertion-order iteration, `TreeSet` for sorted iteration, `EnumSet` for enum-typed elements (extremely fast, backed by bitwise operations), `ConcurrentSkipListSet` for concurrent sorted access.

**Key rules:**

Always specify initial capacity for collections when the approximate size is known. `new ArrayList<>(expectedSize)` and `new HashMap<>(expectedSize, 0.75f)` avoid unnecessary rehashing/resizing.

Never modify a collection while iterating over it with an enhanced for-loop. Use `Iterator.remove()`, `Collection.removeIf()`, or collect items to remove in a separate list.

Prefer immutable collection factories (`List.of()`, `Set.of()`, `Map.of()`) for constant collections. They are unmodifiable, null-hostile (reject null elements), and serializable.

Use `Collections.unmodifiableList(new ArrayList<>(original))` to create a defensive copy when returning a mutable collection from a method.

When using a `Map` to group items, prefer `computeIfAbsent` over check-then-put:

```java
// Good
map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);

// Bad — race condition in concurrent context, verbose otherwise
if (!map.containsKey(key)) {
    map.put(key, new ArrayList<>());
}
map.get(key).add(value);
```

Never use `Arrays.asList()` and expect to add/remove elements — it returns a fixed-size list backed by the array. Use `new ArrayList<>(Arrays.asList(...))` or `List.of(...)` instead.

---

## 3. Stream API and Functional Programming

Streams are powerful but easily abused. They are best for data transformation pipelines (filter → map → collect). They are not a replacement for all loops.

**When to use streams:** Transforming a collection into another collection. Filtering, mapping, reducing, grouping, partitioning. Chaining multiple operations in a pipeline. When the declarative style improves readability.

**When NOT to use streams:** Simple iteration with side effects (prefer enhanced for-loop). When you need to modify local variables (streams require effectively final variables). When exception handling makes the lambda unreadable. When performance is critical and the overhead of stream creation matters (rare, but real for tiny collections in hot paths).

**Rules:**

Keep lambdas short — 1-3 lines. If a lambda exceeds 3 lines, extract it to a named method and use a method reference. `items.stream().filter(this::isValid).map(Item::getName)` reads better than an inline multi-line lambda.

Never use `Stream.forEach()` as a replacement for a for-loop with side effects. `forEach` is a terminal operation, not a loop construct. If you need side effects, a for-loop is clearer.

Always provide a terminal operation. A stream without `.collect()`, `.forEach()`, `.reduce()`, `.count()`, or similar does nothing — it is a bug.

Prefer `Collectors.toList()` (or `.toList()` in Java 16+) over `Collectors.toCollection(ArrayList::new)` unless you need a specific implementation.

Use `Collectors.groupingBy()` and `Collectors.partitioningBy()` for grouping operations. Avoid manual looping to build maps from streams.

Parallel streams are almost never the right choice. They add overhead for thread coordination. Only use them when: the data set is large (10,000+ elements), the operation per element is CPU-intensive, and you have benchmarked to confirm a speedup. Never use parallel streams with shared mutable state.

Avoid nested streams — they are hard to read and often indicate a design problem. If you find yourself writing `stream().flatMap(x -> x.getItems().stream().filter(...))` more than two levels deep, refactor.

---

## 4. Optional

`Optional` represents an explicitly absent value. It replaces `null` returns from methods, NOT null fields or null method parameters.

**Use Optional for:** Return types of methods that might not produce a result. Examples: `findById()`, `getFirstMatch()`, `parse()`.

**Never use Optional for:** Method parameters — it is worse than `@Nullable` because it adds wrapping overhead and ambiguity (is the Optional itself nullable?). Fields — use plain types and handle absence in constructors or factory methods. Collections — return an empty collection, not `Optional<List<T>>`.

**Rules:**

Never call `optional.get()` without first checking `isPresent()`. Better: use `orElse()`, `orElseGet()`, `orElseThrow()`, `map()`, `flatMap()`, or `ifPresent()`.

`orElse(computeDefault())` evaluates the default eagerly. Use `orElseGet(() -> computeDefault())` when the default is expensive to compute.

Chain `Optional` methods declaratively: `return repository.findById(id).map(Entity::toDto).orElseThrow(() -> new NotFoundException(id));`

Never create `Optional.of(null)` — it throws `NullPointerException`. Use `Optional.ofNullable()` when the value might be null.

---

## 5. Concurrency

Concurrent code is where most production bugs hide. Follow these rules strictly.

**Thread safety by default**: If a class may be accessed from multiple threads, document it explicitly (`@ThreadSafe` or Javadoc). If it is not thread-safe, document that too (`@NotThreadSafe`). The default assumption for an undocumented class is "not thread-safe."

**Prefer `java.util.concurrent` over `synchronized`**: Use `ConcurrentHashMap` instead of `Collections.synchronizedMap()`. Use `AtomicInteger`/`AtomicLong`/`AtomicReference` instead of `synchronized` blocks for simple counters and references. Use `ReentrantLock` when you need tryLock, timed lock, or interruptible lock.

**Thread pool rules**: Never create threads with `new Thread()` in production code. Always use `ExecutorService`. Never use `Executors.newFixedThreadPool()` or `Executors.newCachedThreadPool()` — they use unbounded queues or unbounded thread counts, which can cause OOM under load. Use `new ThreadPoolExecutor(...)` with explicit bounds for core/max pool size, queue capacity, and rejection policy.

```java
// Good — explicit bounds and named threads
ExecutorService executor = new ThreadPoolExecutor(
    corePoolSize, maxPoolSize,
    60L, TimeUnit.SECONDS,
    new LinkedBlockingQueue<>(queueCapacity),
    new ThreadFactoryBuilder().setNameFormat("order-processor-%d").build(),
    new ThreadPoolExecutor.CallerRunsPolicy()
);
```

**Virtual Threads (Java 21+)**: For I/O-bound tasks (HTTP calls, database queries, file I/O), prefer virtual threads over platform threads. Use `Executors.newVirtualThreadPerTaskExecutor()`. Do NOT use virtual threads for CPU-bound tasks — they offer no benefit there. Do NOT pin virtual threads by using `synchronized` on I/O operations — use `ReentrantLock` instead.

**`CompletableFuture` rules**: Always specify an `Executor` parameter to avoid running on `ForkJoinPool.commonPool()` (which is shared and can be starved). Always handle exceptions with `exceptionally()` or `handle()`. Chain with `thenApply`/`thenCompose` — not `thenAccept` followed by a get.

**Never**: Lock on a boxed primitive (`synchronized(Boolean.TRUE)`) — boxed primitives are cached and shared across the JVM. Lock on a `String` literal — same reason. Call `Thread.stop()`, `Thread.suspend()`, or `Thread.resume()` — they are deprecated and unsafe. Use `double-checked locking` without `volatile` — it is broken on most JVMs.

---

## 6. I/O and Resource Management

All `Closeable` and `AutoCloseable` resources must use try-with-resources. No exceptions. This is a Blocker-level rule.

```java
// Good
try (var reader = new BufferedReader(new FileReader(path))) {
    return reader.lines().collect(Collectors.toList());
}

// Bad — resource leak if an exception occurs between open and close
BufferedReader reader = new BufferedReader(new FileReader(path));
List<String> lines = reader.lines().collect(Collectors.toList());
reader.close();
```

Prefer NIO.2 (`java.nio.file.Path`, `Files`) over legacy `java.io.File`. Use `Files.readString()`, `Files.readAllLines()`, `Files.write()` for simple operations. Use `Files.newBufferedReader()` / `Files.newBufferedWriter()` for streaming.

Specify character encoding explicitly. Never rely on the platform default encoding. Use `StandardCharsets.UTF_8` in all file and stream operations.

For HTTP clients, prefer `java.net.http.HttpClient` (Java 11+) over `HttpURLConnection`. It supports async operations, HTTP/2, and is cleaner to use.

---

## 7. Reflection and SPI

Use reflection only when absolutely necessary — framework code, serialization libraries, plugin systems. Never use reflection in business logic.

If you must use reflection, cache `Method` and `Field` instances. Reflective lookups are expensive; the actual invocation after lookup is relatively cheap.

Use `MethodHandles` (Java 7+) over `java.lang.reflect.Method` when possible — they are JIT-friendly and faster after warmup.

For plugin/extension point design, prefer Java SPI (`ServiceLoader`) over custom classpath scanning. Define the service interface, create implementation classes, register them in `META-INF/services/`. In Spring, prefer `@Conditional`, `@AutoConfiguration`, or Spring's own SPI (`spring.factories` / `AutoConfiguration.imports`) instead of raw Java SPI.

---

## 8. Modern Java Features (Java 17+)

**Records** (Java 16+): Use records for DTOs, value objects, and any class that is just a transparent carrier of immutable data. Records automatically provide `equals()`, `hashCode()`, `toString()`, and canonical constructor. Do NOT use records for JPA entities (they require mutable state and no-arg constructors).

**Sealed classes** (Java 17+): Use sealed classes to model closed type hierarchies where the set of subtypes is fixed and known at compile time. `sealed interface Shape permits Circle, Rectangle, Triangle` enables exhaustive pattern matching in switch expressions.

**Pattern matching for instanceof** (Java 16+): Replace `if (obj instanceof String) { String s = (String) obj; ... }` with `if (obj instanceof String s) { ... }`. Reduces boilerplate and eliminates unsafe casts.

**Pattern matching for switch** (Java 21+): Use switch expressions with pattern matching for polymorphic dispatch. Combine with sealed classes for compile-time exhaustiveness checks.

**Text blocks** (Java 15+): Use text blocks for multi-line strings (SQL, JSON, HTML templates). Align the closing `"""` to control indentation.

**`var` type inference** (Java 10+): Use `var` when the type is obvious from the right-hand side: `var list = new ArrayList<String>()`. Do NOT use `var` when the type is non-obvious: `var result = service.process(input)` — the reader cannot tell the type without navigating to the method.

---

## 9. Equality, Hashing, and Comparison

If you override `equals()`, you must override `hashCode()`. Violating this contract breaks `HashMap`, `HashSet`, and any hash-based collection. This is a Blocker-level rule.

Use `Objects.equals(a, b)` instead of `a.equals(b)` when `a` might be null. Use `Objects.hash(field1, field2, ...)` for `hashCode()` implementations.

For records, `equals()` and `hashCode()` are generated automatically based on all components — no manual override needed.

For `Comparable` implementations, ensure consistency with `equals()`: if `a.compareTo(b) == 0`, then `a.equals(b)` should also be true (unless documented otherwise). Use `Comparator.comparing()` chains instead of manual comparison logic.

Never use `==` to compare objects (except primitives and enum values). Use `.equals()`. For `String` comparison, `"constant".equals(variable)` prevents `NullPointerException`.

---

## 10. String Handling

Use `StringBuilder` for string concatenation in loops. The compiler optimizes `+` for simple expressions, but loop concatenation creates O(n²) garbage.

Use `String.format()` or `MessageFormat` for complex formatting. Use `String.formatted()` (Java 15+) for inline formatting.

For string constants used as keys or identifiers, define them as `static final` fields, not inline literals. This prevents typo bugs and enables refactoring.

Use `String.isEmpty()` or `String.isBlank()` (Java 11+) instead of `str.length() == 0` or `str.trim().isEmpty()`. For null-safe checks, use `StringUtils.isBlank()` from Apache Commons or a similar utility — but prefer preventing null strings at the boundary.

Never use `new String("literal")` — it creates an unnecessary copy. String literals are interned by default.