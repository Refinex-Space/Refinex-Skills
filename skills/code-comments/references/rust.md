# Rust Commenting Standards Reference

Authoritative sources: The Rust Reference (Documentation comments), Rust API Guidelines (C-DOCS), The rustdoc Book, Rust Standard Library documentation style.

---

## Table of Contents

1. [Doc Comment Syntax](#doc-comment-syntax)
2. [Crate and Module Documentation](#crate-and-module-documentation)
3. [Struct, Enum, and Trait Documentation](#struct-enum-and-trait-documentation)
4. [Function and Method Documentation](#function-and-method-documentation)
5. [Field and Variant Documentation](#field-and-variant-documentation)
6. [Standard Sections](#standard-sections)
7. [Inline Comments](#inline-comments)

---

## Doc Comment Syntax

Rust has two doc comment forms:

- `///` — Outer doc comment. Documents the item that follows it. Used for structs, enums, functions, methods, fields, variants, traits, type aliases, constants, statics, and modules.
- `//!` — Inner doc comment. Documents the enclosing item. Used at the top of a crate root (`lib.rs` or `main.rs`) or at the top of a module file to document the crate/module itself.

Doc comments support full Markdown. Code blocks in doc comments are compiled and run as doctests by `cargo test`.

---

## Crate and Module Documentation

Every crate root must start with `//!` doc comments describing the crate's purpose, key features, and usage example.

```rust
//! # my_http_client
//!
//! A lightweight, async HTTP client with automatic retries and
//! connection pooling.
//!
//! ## Features
//!
//! - Automatic retry with exponential backoff for transient failures
//! - Connection pooling with configurable pool size
//! - Request/response interceptors for logging and auth
//!
//! ## Quick Start
//!
//! ```rust
//! use my_http_client::Client;
//!
//! #[tokio::main]
//! async fn main() -> Result<(), Box<dyn std::error::Error>> {
//!     let client = Client::builder()
//!         .base_url("https://api.example.com")
//!         .build()?;
//!
//!     let user: User = client.get("/users/1").send().await?.json().await?;
//!     println!("User: {}", user.name);
//!     Ok(())
//! }
//! ```

mod client;
mod config;
```

Module files use `//!` at the top:

```rust
//! Request building and execution.
//!
//! This module contains the [`RequestBuilder`] for constructing
//! HTTP requests and the [`Response`] type for handling results.

pub struct RequestBuilder { /* ... */ }
```

---

## Struct, Enum, and Trait Documentation

Every public struct, enum, and trait must have doc comments.

```rust
/// A connection pool that manages reusable HTTP connections.
///
/// The pool lazily creates connections up to `max_size`, then blocks
/// callers until a connection is returned. Idle connections are closed
/// after `idle_timeout`.
///
/// # Thread Safety
///
/// `ConnectionPool` is `Send + Sync` and safe to share across threads
/// via `Arc<ConnectionPool>`.
///
/// # Examples
///
/// ```
/// let pool = ConnectionPool::new(Config {
///     max_size: 10,
///     idle_timeout: Duration::from_secs(60),
/// });
///
/// let conn = pool.acquire().await?;
/// // use conn...
/// pool.release(conn);
/// ```
pub struct ConnectionPool {
    /// Maximum number of connections the pool will maintain.
    max_size: usize,

    /// Duration after which an idle connection is closed and removed.
    idle_timeout: Duration,

    /// Currently active connections, indexed by their unique ID.
    connections: Mutex<HashMap<ConnectionId, Connection>>,
}
```

For enums, document both the enum and each variant:

```rust
/// The result of a cache lookup operation.
///
/// Distinguishes between a cache miss (key not found), a cache hit
/// with a fresh value, and a cache hit with a stale value that should
/// be revalidated.
pub enum CacheResult<T> {
    /// The key was not found in the cache.
    Miss,

    /// The key was found and the value is within its TTL.
    Hit(T),

    /// The key was found but the value has exceeded its TTL.
    /// The stale value is provided for use while revalidation occurs.
    Stale(T),
}
```

For traits, document the trait's contract and each method:

```rust
/// A serialization format that can encode and decode values.
///
/// Implementations must guarantee that `decode(encode(value))` produces
/// a value equal to the original for any `T: Serialize + DeserializeOwned`.
pub trait Codec {
    /// Encodes a value into a byte vector.
    ///
    /// # Errors
    ///
    /// Returns `CodecError::Serialize` if the value cannot be serialized.
    fn encode<T: Serialize>(&self, value: &T) -> Result<Vec<u8>, CodecError>;

    /// Decodes a byte slice into a value of the specified type.
    ///
    /// # Errors
    ///
    /// Returns `CodecError::Deserialize` if the bytes do not represent
    /// a valid value of type `T`.
    fn decode<T: DeserializeOwned>(&self, bytes: &[u8]) -> Result<T, CodecError>;
}
```

---

## Function and Method Documentation

Every public function and method requires doc comments with these standard sections:

```rust
/// Retries the given asynchronous operation with exponential backoff.
///
/// Executes `operation` up to `max_attempts` times. On failure, waits
/// for an exponentially increasing duration before retrying. The base
/// delay is 100ms, doubling with each attempt up to a maximum of 10s.
///
/// # Arguments
///
/// * `operation` - The async closure to retry. Must return `Result<T, E>`.
/// * `max_attempts` - Maximum number of execution attempts (including
///   the first). Must be at least 1.
/// * `is_retryable` - Predicate that determines whether a given error
///   warrants a retry. Returning `false` causes immediate failure.
///
/// # Returns
///
/// The successful result of `operation`, or the last error if all
/// attempts are exhausted.
///
/// # Errors
///
/// Returns the error from the final failed attempt if all retries
/// are exhausted, or the first non-retryable error encountered.
///
/// # Panics
///
/// Panics if `max_attempts` is 0.
///
/// # Examples
///
/// ```
/// let result = retry(
///     || async { fetch_remote_config().await },
///     3,
///     |err| err.is_transient(),
/// ).await?;
/// ```
pub async fn retry<T, E, F, Fut>(
    operation: F,
    max_attempts: u32,
    is_retryable: impl Fn(&E) -> bool,
) -> Result<T, E>
where
    F: Fn() -> Fut,
    Fut: Future<Output = Result<T, E>>,
```

---

## Field and Variant Documentation

Every public field in a public struct and every variant in a public enum must have `///` comments. Private fields should be documented when non-obvious.

```rust
pub struct ServerConfig {
    /// Address to bind the HTTP server to (e.g., "0.0.0.0:8080").
    pub bind_address: SocketAddr,

    /// Maximum number of concurrent connections. 0 means unlimited.
    pub max_connections: usize,

    /// TLS configuration. If `None`, the server runs in plaintext mode.
    pub tls: Option<TlsConfig>,

    /// Request body size limit in bytes. Requests exceeding this
    /// limit receive a 413 Payload Too Large response.
    pub max_body_bytes: u64,
}
```

---

## Standard Sections

Rust doc comments use these standard section headers (per API Guidelines C-DOCS):

- `# Examples` — runnable code examples (compiled as doctests)
- `# Errors` — when the function returns `Result`, describe error conditions
- `# Panics` — conditions under which the function panics
- `# Safety` — for `unsafe` functions, describe the invariants the caller must uphold
- `# Arguments` — parameter descriptions (alternative to inline description)
- `# Returns` — return value description
- `# Thread Safety` or `# Concurrency` — thread safety guarantees

---

## Inline Comments

Use `//` for implementation comments. Place on the line above the code.

```rust
// Use a bloom filter for the first-pass check to avoid expensive
// disk reads for keys that definitely don't exist.
if !bloom_filter.might_contain(&key) {
    return Ok(None);
}

// SAFETY: The pointer is valid because we just allocated it above
// and have not deallocated or moved the underlying memory.
unsafe { ptr.as_ref() }
```