---
name: code-comments
description: Use when adding, fixing, reviewing, or generating code comments, docstrings, Javadoc, JSDoc/TSDoc, rustdoc, SQL comments, or documentation comments for source, markup, configuration, or database files.
---

# Code Comments: Authoritative Multi-Language Commenting Standards

This skill enforces correct, standardized commenting across all major programming languages, markup languages, and configuration formats. It serves two purposes:

1. **Active mode** — When explicitly invoked, systematically add, correct, or supplement comments for a specific file or an entire directory tree.
2. **Passive mode** — When writing any code, proactively follow these standards so that every piece of generated code ships with proper comments from the start.

---

## Core Principles (All Languages)

These principles apply universally regardless of language:

1. **Every public API surface must be documented.** Classes, interfaces, public methods, exported functions, public fields — no exceptions. The documentation must describe _what_ and _why_, not _how_ (the code shows how).

2. **Comments describe intent, not mechanics.** `// increment i` on `i++` is noise. `// Retry with exponential backoff to handle transient network failures` is signal. If a comment restates the code literally, delete it.

3. **Use the language's standard doc-comment format.** Javadoc for Java, docstrings for Python, `///` for Rust, JSDoc for JavaScript/TypeScript, `<!-- -->` for XML/HTML, `#` for YAML. Never invent custom formats when a standard exists.

4. **Comments must stay synchronized with code.** A wrong comment is worse than no comment. When modifying code, update the adjacent comments in the same edit.

5. **Comment density scales with complexity, not length.** A 200-line CRUD handler may need few inline comments. A 30-line algorithm may need comments on every block. Density follows cognitive load, not line count.

6. **First sentence is the contract.** In doc comments, the first sentence (before any blank line or tag) should be a complete, standalone summary. Tools extract this as the short description.

7. **Language matters.** Write comments in the project's primary human language. If the project uses English, all comments in English. If Chinese, all in Chinese. Never mix within a file unless terms are domain-specific.

---

## Workflow: Active Commenting Mode

When a user explicitly asks you to comment a file or directory, follow this procedure.

### Step 1: Determine Scope

- **Single file** — The user points to one file. Read it, identify the language, then apply the relevant reference.
- **Directory** — The user points to a path. Recursively discover all commentable files. Process each file in a logical order (e.g., models/types first, then services, then controllers, then tests).

For directory-scope work, list the discovered files and their languages to the user before starting, so they can confirm or exclude any.

### Step 2: Load Language Reference

Before commenting any file, read the appropriate reference from `references/`:

| Language/Format                             | Reference File                | Standard                            |
| ------------------------------------------- | ----------------------------- | ----------------------------------- |
| Java                                        | `references/java.md`          | Javadoc (Oracle), Google Java Style |
| Python                                      | `references/python.md`        | PEP 257, Google/NumPy style         |
| TypeScript, JavaScript, React, Vue          | `references/typescript-js.md` | JSDoc, TSDoc, Vue SFC conventions   |
| Rust                                        | `references/rust.md`          | rustdoc conventions                 |
| XML, HTML, YAML, SQL, CSS, Shell, Go, C/C++ | `references/markup-config.md` | Language-specific standards         |

Read the reference **before** writing any comments. The references contain exact formatting rules, required tags, and calibrated examples. Do not rely on memory alone.

### Step 3: Analyze Existing Comments

For each file, perform a gap analysis:

- **Missing doc comments** — Public classes, methods, functions, fields, or exports without documentation comments.
- **Missing parameter/return docs** — Methods with parameters or return values that lack `@param`/`@return` (Java), `Args:`/`Returns:` (Python), etc.
- **Missing configuration comments** — YAML keys, XML elements, SQL tables/columns without explanatory comments.
- **Stale comments** — Comments that describe behavior the code no longer exhibits.
- **Noise comments** — Comments that restate the code literally and should be removed.
- **Missing inline comments** — Complex logic blocks (conditionals with non-obvious conditions, algorithms, regex, bitwise operations, error handling branches) that lack explanatory inline comments.

### Step 4: Apply Comments

Add, correct, or remove comments according to the language reference. For each file:

1. Add all missing doc comments (class, method, field, function, module level).
2. Add all missing parameter, return, throws/raises, and exception documentation.
3. Add inline comments for complex logic blocks, non-obvious conditions, and important branching.
4. Remove noise comments that restate the obvious.
5. Fix stale comments that no longer match the code.
6. Ensure configuration files (YAML, XML, properties, SQL DDL) have explanatory comments on every significant section and non-obvious key.

### Step 5: Verify

After commenting, do a quick self-check per file:

- Every public/exported symbol has a doc comment? ✓
- Every method parameter and return value is documented? ✓
- No doc comment is a single word or trivially restates the name? ✓
- Complex logic has inline explanation? ✓
- Configuration keys/sections have contextual comments? ✓
- No stale or misleading comments remain? ✓

---

## Workflow: Passive Commenting Mode (During Code Writing)

When writing code for any task (not just commenting tasks), apply these rules automatically:

1. Write class/interface/struct doc comments immediately when creating the type.
2. Write method/function doc comments immediately when creating the method, including all `@param`, `@return`, `@throws` tags.
3. Add field/property comments for non-obvious fields (especially in POJOs, DTOs, database models, configuration classes).
4. Add inline comments before any block that involves non-trivial logic.
5. Add file-header comments for new files when the project convention requires them.
6. Add section comments in configuration files (YAML, XML, SQL) for logical groupings.

The goal is zero remediation — code should be properly commented when first written, not patched after the fact.

---

## Mandatory Comment Targets by Category

Regardless of language, these categories always require comments:

### Type Definitions (Classes, Interfaces, Structs, Enums, Traits, Protocols)

- Purpose and responsibility of the type
- Thread-safety or mutability notes if applicable
- Key usage patterns or lifecycle notes
- Type parameters if generic

### Methods and Functions

- Summary of behavior (what, not how)
- All parameters with description, constraints, and nullability
- Return value description (including possible null/empty/error states)
- Exceptions/errors that may be raised
- Side effects (I/O, state mutation, network calls)
- Preconditions and postconditions if non-obvious

### Fields and Properties

- Business meaning (not just the type — `userId` needs "Unique identifier for the user in the authentication system", not "the user ID")
- Units for numeric fields (milliseconds? bytes? pixels?)
- Valid ranges or constraints
- Default values and why
- POJO/DTO/Entity fields: always document, especially for ORM-mapped entities where the field maps to a database column

### Configuration (YAML, XML, Properties, ENV)

- Section headers explaining each logical group
- Every non-obvious key with its purpose, valid values, and default
- Environment-specific notes (dev vs prod differences)

### SQL

- Table and column comments in DDL
- Stored procedure/function header comments (purpose, parameters, return, exceptions)
- Complex query logic with inline comments
- Business rule comments in WHERE clauses and CASE expressions

### Inline Code Comments

Required before:

- Algorithm implementations (loop invariants, termination conditions)
- Regex patterns (what they match and why)
- Bitwise operations
- Error handling branches (why this error is caught and what recovery is attempted)
- Non-obvious conditional logic
- Performance-critical sections (why this approach was chosen)
- Workarounds and hacks (with issue tracker references)
- Magic numbers and constants

---

## Anti-Patterns to Detect and Fix

When analyzing existing comments, actively look for and fix these:

1. **The Parrot** — `// set the name` on `setName()`. Remove or replace with meaningful context.
2. **The Tombstone** — Commented-out code blocks with no explanation. Either restore with an explanation or delete entirely.
3. **The Liar** — Comment says one thing, code does another. Fix the comment to match reality.
4. **The Novel** — 20-line comment for a 3-line function. Trim to what adds value.
5. **The TODO Graveyard** — Ancient `// TODO` comments with no intent to complete. Flag to user.
6. **The Changelog** — Comments tracking modification history (`// Modified by X on date Y`). This belongs in version control, not in code.
7. **The AI Slop** — Auto-generated comments that are vague, generic, or use filler phrases like "This method handles the logic for..." without adding specifics.
