# Regression Test Patterns

How to write regression tests that protect against specific failure modes
discovered during bug fixing. A good regression test fails without the fix
and passes with it — it encodes the exact failure mode, not just the correct
behavior.

---

## Core principles

1. **Test the failure mode, not the implementation.** The test should describe
   the bug, not the fix. If the fix changes, the test should still be relevant.

2. **Name the test after the bug.** `test_expired_token_rejected_correctly` is
   better than `test_token_fix` — it survives refactoring and communicates intent
   to future readers.

3. **Include a traceability comment.** Reference the fix plan so future readers
   can find the full investigation:

   ```python
   def test_expired_token_rejected_correctly():
       """Regression test: expired tokens must return 401, not 500.

       See: docs/exec-plans/completed/2024-01-15-fix-auth-expiry.md
       """
   ```

4. **One test per failure mode.** If the bug has multiple symptoms, write
   multiple tests — each covering one specific failure path.

---

## Patterns by bug type

### Boundary condition bugs

The bug: code fails at the boundary between valid and invalid input.

```python
# The boundary that was wrong: used < instead of <=
def test_maximum_value_is_accepted():
    """Values at the exact maximum should be accepted, not rejected."""
    result = validate(MAX_VALUE)  # This was the failing case
    assert result.is_valid

def test_one_above_maximum_is_rejected():
    """Values above maximum should be rejected."""
    result = validate(MAX_VALUE + 1)
    assert not result.is_valid
```

Test both sides of the boundary — the passing side and the failing side.

### Null / missing value bugs

The bug: code crashes on null, empty, or missing input it should handle.

```python
def test_handles_missing_email_field():
    """User creation should fail gracefully when email is missing."""
    response = create_user({"name": "Alice"})  # no email field
    assert response.status == 400
    assert "email" in response.error_message
```

### Race condition / timing bugs

The bug: code fails under concurrent access or timing-sensitive conditions.

```python
def test_concurrent_counter_increment():
    """Counter must be correct after concurrent increments.

    Previously failed due to non-atomic read-modify-write.
    """
    counter = Counter(initial=0)
    threads = [Thread(target=counter.increment) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert counter.value == 100
```

For timing bugs, the test should create the conditions that trigger the race —
not just test the happy path with a sleep().

### Data format / encoding bugs

The bug: code fails on specific character encodings, data formats, or edge-case
inputs.

```python
def test_handles_unicode_in_username():
    """Usernames with Unicode characters must be stored and retrieved correctly.

    Previously corrupted Non-ASCII characters due to missing encoding declaration.
    """
    user = create_user(name="José García")
    retrieved = get_user(user.id)
    assert retrieved.name == "José García"
```

### Regression in computation / logic

The bug: a calculation or logic path produces the wrong result.

```python
def test_discount_applied_before_tax():
    """Discount must be calculated on the pre-tax amount.

    Previously applied discount to post-tax total, resulting in
    over-discount for taxed items.
    """
    order = Order(subtotal=100.00, tax_rate=0.10, discount_rate=0.20)
    assert order.total == 88.00  # 100 * 0.80 * 1.10
    # Wrong result was 88.00 vs 90.00 depending on order of operations
```

Include the expected value AND a comment explaining why — so future readers
understand the math without re-deriving it.

### Configuration / environment bugs

The bug: code fails under specific configuration or environment conditions.

```python
def test_works_without_optional_config():
    """Service must start correctly when OPTIONAL_FEATURE is not set.

    Previously crashed with KeyError when the environment variable was missing.
    """
    env = base_config()  # no OPTIONAL_FEATURE key
    service = Service(config=env)
    assert service.is_running
```

### Integration / contract bugs

The bug: two components disagree on their shared interface.

```python
def test_api_response_matches_client_expectation():
    """API must return 'user_id' (not 'userId') in the response body.

    Client expected snake_case but API was returning camelCase after
    the serializer migration.
    """
    response = api.get("/users/1")
    data = response.json()
    assert "user_id" in data
    assert "userId" not in data
```

---

## Verification pattern

After writing the regression test, verify it's a genuine regression test:

1. **Without the fix**: the test should FAIL
   - Temporarily revert your fix and run the test
   - If it passes without the fix, the test isn't testing the right thing

2. **With the fix**: the test should PASS
   - Reapply the fix and run the test

3. **In the full suite**: no other tests should break
   - Run the complete test suite with both the fix and the regression test

This verification ensures the test is actually guarding against the specific
failure mode, not just testing general correct behavior that happens to pass
regardless.

---

## Where to place regression tests

Follow the repo's existing test organization (documented in AGENTS.md or
discovered in Step 1 preflight). Common placements:

| Repo convention          | Placement                                          |
| ------------------------ | -------------------------------------------------- |
| Mirror structure         | Same test file as the module being tested           |
| Separate regression dir  | `tests/regressions/test_<issue_description>.py`    |
| Feature-organized        | In the test file for the affected feature           |

If the repo has no convention, place regression tests alongside the existing
tests for the affected module. Don't create a separate regression directory
unless the team already uses that pattern.
