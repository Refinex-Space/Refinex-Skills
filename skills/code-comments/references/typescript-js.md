# TypeScript / JavaScript / React / Vue Commenting Standards Reference

Authoritative sources: JSDoc 3 specification, TSDoc specification (Microsoft), Vue.js Style Guide, React documentation conventions, Google JavaScript Style Guide §7.

---

## Table of Contents

1. [JSDoc vs TSDoc](#jsdoc-vs-tsdoc)
2. [Module and File Comments](#module-and-file-comments)
3. [Class and Interface Comments](#class-and-interface-comments)
4. [Function and Method Comments](#function-and-method-comments)
5. [Type, Interface, and Enum Comments](#type-interface-and-enum-comments)
6. [React Component Comments](#react-component-comments)
7. [Vue SFC Comments](#vue-sfc-comments)
8. [Inline Comments](#inline-comments)
9. [Calibrated Examples](#calibrated-examples)

---

## JSDoc vs TSDoc

**JSDoc** (`/** ... */`) is the standard for JavaScript. It uses `@param {type} name` syntax because JavaScript has no static types. In TypeScript projects, type annotations in JSDoc are redundant since the compiler already knows the types. Use the tag without the type: `@param name - description`.

**TSDoc** is Microsoft's standardized subset of JSDoc for TypeScript. It omits type annotations from tags and uses `-` separators instead of spaces. TSDoc is what VS Code, TypeDoc, and API Extractor parse.

Rule: In TypeScript projects, use TSDoc syntax (`@param name - description`). In JavaScript projects, use JSDoc syntax with types (`@param {string} name - description`).

---

## Module and File Comments

File-level comments are placed at the top of the file, before any imports. They describe the file's purpose and key exports.

```typescript
/**
 * User authentication middleware and route guards.
 *
 * @module auth/middleware
 * @see {@link AuthService} for the underlying authentication logic
 */
```

Not every file needs a file-level comment. Use them when the file's purpose is not obvious from its name and exports, or when the file is an important entry point.

---

## Class and Interface Comments

Every exported class and interface requires a doc comment.

```typescript
/**
 * Manages WebSocket connections with automatic reconnection and heartbeat.
 *
 * @remarks
 * This class maintains a persistent WebSocket connection to the server,
 * automatically reconnecting with exponential backoff when the connection
 * drops. Heartbeat pings are sent every 30 seconds to detect stale
 * connections.
 *
 * @example
 * ```typescript
 * const ws = new WebSocketManager('wss://api.example.com/ws');
 * ws.on('message', (data) => console.log(data));
 * ws.connect();
 * ```
 */
export class WebSocketManager {
```

For interfaces and type aliases:

```typescript
/**
 * Configuration options for the HTTP client.
 *
 * @remarks
 * All timeout values are in milliseconds. Set to 0 to disable.
 */
export interface HttpClientConfig {
  /** Base URL prepended to all relative request paths. */
  baseUrl: string;

  /** Request timeout in milliseconds. Defaults to 30000 (30s). */
  timeout?: number;

  /** Maximum number of automatic retry attempts for failed requests. */
  maxRetries?: number;

  /** Custom headers to include in every request. */
  headers?: Record<string, string>;
}
```

---

## Function and Method Comments

Every exported function and every public method requires a doc comment. The summary line describes the function's behavior in third-person declarative form.

Required tags:
- `@param` for every parameter (with description, not just name)
- `@returns` for non-void functions (describe the value, conditions, and edge cases)
- `@throws` for errors that may be thrown
- `@example` for non-obvious usage patterns
- `@remarks` for extended explanation beyond the summary

```typescript
/**
 * Validates and normalizes a phone number to E.164 format.
 *
 * @param phoneNumber - Raw phone number string, may include spaces,
 *   dashes, parentheses, and country code prefix.
 * @param defaultCountryCode - ISO 3166-1 alpha-2 country code to assume
 *   if no country code is present in the phone number. Defaults to 'US'.
 * @returns The normalized phone number in E.164 format (e.g., '+14155551234'),
 *   or `null` if the input cannot be parsed as a valid phone number.
 * @throws {TypeError} If phoneNumber is not a string.
 *
 * @example
 * ```typescript
 * normalizePhone('(415) 555-1234')       // '+14155551234'
 * normalizePhone('+44 20 7946 0958')     // '+442079460958'
 * normalizePhone('invalid')               // null
 * ```
 */
export function normalizePhone(
  phoneNumber: string,
  defaultCountryCode: string = 'US',
): string | null {
```

For callbacks and event handlers, document what event triggers the handler and what the parameters represent:

```typescript
/**
 * Handles the form submission event.
 *
 * @remarks
 * Validates all fields, submits to the API, and navigates to the
 * success page on completion. Displays inline validation errors
 * if any field is invalid.
 *
 * @param event - The form submission event. Default behavior is prevented.
 */
const handleSubmit = async (event: FormEvent<HTMLFormElement>): Promise<void> => {
```

---

## Type, Interface, and Enum Comments

Every member of an exported interface, type, or enum should have a doc comment.

```typescript
/**
 * Represents the possible states of a background task.
 */
export enum TaskStatus {
  /** Task has been created but not yet started. */
  PENDING = 'pending',

  /** Task is currently executing. */
  RUNNING = 'running',

  /** Task completed successfully. */
  COMPLETED = 'completed',

  /** Task failed with an error. Check the `error` field for details. */
  FAILED = 'failed',

  /** Task was manually cancelled before completion. */
  CANCELLED = 'cancelled',
}
```

---

## React Component Comments

React components (functional or class-based) require doc comments on the component itself and on its props interface/type.

```tsx
/**
 * Displays a paginated data table with sortable columns and row selection.
 *
 * @remarks
 * Supports server-side pagination via the `onPageChange` callback.
 * Sorting is performed client-side on the current page's data.
 * Selected row IDs are maintained across page changes.
 *
 * @example
 * ```tsx
 * <DataTable
 *   columns={columns}
 *   data={users}
 *   totalCount={1000}
 *   onPageChange={(page) => fetchUsers(page)}
 *   onSelectionChange={(ids) => setSelectedIds(ids)}
 * />
 * ```
 */
export function DataTable<T extends { id: string }>({
  columns,
  data,
  totalCount,
  pageSize = 20,
  onPageChange,
  onSelectionChange,
}: DataTableProps<T>): ReactElement {
```

Props interface — every prop needs a comment:

```tsx
/** Props for the {@link DataTable} component. */
export interface DataTableProps<T extends { id: string }> {
  /** Column definitions specifying header labels, data keys, and sort behavior. */
  columns: ColumnDef<T>[];

  /** The data rows to display on the current page. */
  data: T[];

  /** Total number of rows across all pages. Used to calculate page count. */
  totalCount: number;

  /** Number of rows per page. Defaults to 20. */
  pageSize?: number;

  /** Callback invoked when the user navigates to a different page. */
  onPageChange?: (page: number) => void;

  /** Callback invoked when the set of selected row IDs changes. */
  onSelectionChange?: (selectedIds: string[]) => void;
}
```

Custom hooks also require doc comments:

```typescript
/**
 * Manages debounced search input with loading state.
 *
 * @param searchFn - Async function that performs the actual search.
 * @param debounceMs - Debounce delay in milliseconds. Defaults to 300.
 * @returns An object containing the current query, setter, results,
 *   loading state, and error.
 */
export function useSearch<T>(
  searchFn: (query: string) => Promise<T[]>,
  debounceMs: number = 300,
): SearchState<T> {
```

---

## Vue SFC Comments

Vue Single File Components require comments in three sections: `<template>`, `<script>`, and `<style>`.

### Template Section (`<template>`)

Use HTML comments (`<!-- -->`) to mark logical sections and explain non-obvious template logic:

```vue
<template>
  <!-- Search and filter controls -->
  <div class="toolbar">
    <SearchInput v-model="query" placeholder="Search users..." />
    <!-- Role filter: hidden for non-admin users per RBAC policy -->
    <RoleFilter v-if="isAdmin" v-model="selectedRole" />
  </div>

  <!-- User table: shows skeleton rows while loading -->
  <DataTable
    :columns="columns"
    :data="filteredUsers"
    :loading="isLoading"
  >
    <!-- Custom cell renderer for the status column -->
    <template #cell-status="{ value }">
      <StatusBadge :status="value" />
    </template>
  </DataTable>
</template>
```

### Script Section (`<script setup>` or `<script>`)

Follow TSDoc/JSDoc conventions for all exported or significant items:

```vue
<script setup lang="ts">
/**
 * User management dashboard page.
 *
 * Displays a searchable, filterable table of all users in the system.
 * Admins can edit roles, deactivate accounts, and export user data.
 */

/** Currently active search query. Debounced at 300ms before triggering API call. */
const query = ref('');

/** Users filtered by the current search query and role filter. */
const filteredUsers = computed(() => {
  // Case-insensitive substring match on name and email
  return users.value.filter((user) =>
    [user.name, user.email].some((field) =>
      field.toLowerCase().includes(query.value.toLowerCase())
    )
  );
});

/**
 * Deactivates a user account and revokes all active sessions.
 *
 * @param userId - The ID of the user to deactivate.
 * @throws {ApiError} If the user is the last admin (cannot deactivate).
 */
async function deactivateUser(userId: string): Promise<void> {
```

### Style Section

Use CSS comments to mark sections:

```vue
<style scoped>
/* Layout: toolbar and table container */
.toolbar { ... }

/* Override DataTable default padding for compact view */
:deep(.data-table__cell) { ... }
</style>
```

---

## Inline Comments

Use `//` for JavaScript/TypeScript inline comments. Place on the line above, not inline unless very short.

```typescript
// Clamp the value to the valid range to prevent overflow in downstream calculations
const normalized = Math.max(0, Math.min(value, MAX_VALUE));

// Batch database writes in chunks of 100 to stay within the connection pool limit
for (let i = 0; i < records.length; i += BATCH_SIZE) {
  const chunk = records.slice(i, i + BATCH_SIZE);
  await db.batchInsert(chunk);
}
```