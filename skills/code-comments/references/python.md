# Python Commenting Standards Reference

Authoritative sources: PEP 257 (Docstring Conventions), PEP 8 (Style Guide §Comments), Google Python Style Guide §3.8, NumPy Docstring Standard.

---

## Table of Contents

1. [Docstring Fundamentals](#docstring-fundamentals)
2. [Module Docstrings](#module-docstrings)
3. [Class Docstrings](#class-docstrings)
4. [Method and Function Docstrings](#method-and-function-docstrings)
5. [Property and Attribute Documentation](#property-and-attribute-documentation)
6. [Docstring Styles: Google vs NumPy vs reST](#docstring-styles)
7. [Inline Comments](#inline-comments)
8. [Calibrated Examples](#calibrated-examples)

---

## Docstring Fundamentals

A docstring is a string literal that occurs as the first statement in a module, class, function, or method definition. It becomes the `__doc__` attribute of that object.

Per PEP 257, always use `"""triple double quotes"""`. Even for one-liners.

One-line docstrings: the opening `"""`, the text, and the closing `"""` all on the same line. The text is a phrase ending in a period, describing the function's effect as a command ("Do X" not "Does X" or "Return X" not "Returns X" — though Google style prefers third person "Returns").

Multi-line docstrings: summary line on the first line (or the line after `"""`), a blank line, then the elaborated description. The closing `"""` is on its own line.

All public modules, functions, classes, and methods must have docstrings. Non-public methods should have a comment describing what they do.

---

## Module Docstrings

Every Python module (`.py` file) should start with a docstring describing the module's purpose and listing its key exports.

```python
"""User authentication and session management.

This module provides the core authentication logic including credential
validation, JWT token generation, and session lifecycle management.

Typical usage:
    from auth import AuthService

    service = AuthService(config)
    result = service.authenticate(credentials)

Classes:
    AuthService: Main authentication facade.
    AuthResult: Immutable result of an authentication attempt.

Functions:
    hash_password: BCrypt password hashing utility.
"""
```

For scripts (standalone programs), the module docstring should serve as the usage message.

---

## Class Docstrings

Every class requires a docstring immediately after the class definition, describing what instances of the class represent.

Required content:
- Summary of what the class represents
- Key attributes (public instance attributes)
- Thread-safety or mutability notes if relevant
- Usage example if the class has a non-obvious API

Insert a blank line after the class docstring (PEP 257 requirement for classes).

```python
class OrderProcessor:
    """Processes customer orders through the fulfillment pipeline.

    Coordinates validation, payment capture, inventory reservation,
    and shipment scheduling. Each instance is bound to a single
    warehouse region.

    This class is not thread-safe. Use one instance per thread or
    protect access with a lock.

    Attributes:
        region: The warehouse region code (e.g., 'us-east-1').
        max_retries: Maximum retry attempts for transient failures.
        processed_count: Running count of successfully processed orders.

    Example:
        processor = OrderProcessor(region='us-east-1')
        result = processor.process(order)
        if result.success:
            logger.info(f"Order {order.id} processed")
    """

    def __init__(self, region: str, max_retries: int = 3) -> None:
```

---

## Method and Function Docstrings

Every public method and function requires a docstring. The summary line uses imperative mood (PEP 257) or third-person declarative (Google style) — be consistent within a project.

Required sections:
- Summary line
- Extended description (if the summary is insufficient)
- Args / Parameters
- Returns
- Raises
- Yields (for generators)
- Notes (optional, for algorithms or important caveats)
- Examples (optional, for complex APIs)

```python
def calculate_shipping_cost(
    weight_kg: float,
    destination: str,
    express: bool = False,
) -> Decimal:
    """Calculate the shipping cost for a package.

    Applies the regional rate table to determine the base cost, then
    adds surcharges for express delivery and oversized packages
    (weight > 30kg).

    Args:
        weight_kg: Package weight in kilograms. Must be positive.
        destination: ISO 3166-1 alpha-2 country code of the
            destination (e.g., 'US', 'DE', 'JP').
        express: If True, apply express delivery surcharge
            (2x base rate). Defaults to False.

    Returns:
        The total shipping cost as a Decimal in USD, rounded to
        2 decimal places. Returns Decimal('0.00') for free
        shipping eligible orders.

    Raises:
        ValueError: If weight_kg is not positive.
        UnsupportedDestinationError: If the destination country
            is not in the rate table.

    Example:
        >>> calculate_shipping_cost(2.5, 'US')
        Decimal('8.50')
        >>> calculate_shipping_cost(2.5, 'US', express=True)
        Decimal('17.00')
    """
```

For `__init__` methods, document the constructor parameters in the `__init__` docstring (Google style) or in the class docstring. Do not duplicate in both places.

For `@property` methods, document them like attributes:

```python
@property
def is_expired(self) -> bool:
    """Whether this token has passed its expiration time."""
    return datetime.utcnow() > self._expires_at
```

---

## Property and Attribute Documentation

Instance attributes that are set outside `__init__` or whose meaning is not obvious from the name should be documented inline:

```python
def __init__(self, config: Config) -> None:
    """Initialize the processor with the given configuration.

    Args:
        config: Application configuration object.
    """
    self.config = config

    #: Number of items successfully processed since initialization.
    self.processed_count: int = 0

    #: Timestamp of the last successful processing run, or None if
    #: no items have been processed yet.
    self.last_run_at: datetime | None = None
```

The `#:` comment syntax (used by Sphinx) marks an attribute docstring. This is the standard way to document instance attributes outside of the class docstring.

---

## Docstring Styles

Choose one style per project and use it consistently. The three standard styles:

### Google Style (recommended for most projects)

```python
def fetch_user(user_id: int, include_deleted: bool = False) -> User | None:
    """Fetch a user by their unique identifier.

    Args:
        user_id: The unique identifier of the user.
        include_deleted: Whether to include soft-deleted users
            in the search. Defaults to False.

    Returns:
        The User object if found, or None if no user exists
        with the given ID.

    Raises:
        DatabaseError: If the database connection fails.
    """
```

### NumPy Style (common in scientific/data projects)

```python
def interpolate(x, y, method='linear'):
    """Interpolate data points using the specified method.

    Parameters
    ----------
    x : array_like
        The x-coordinates of the data points.
    y : array_like
        The y-coordinates of the data points. Must have the
        same length as `x`.
    method : str, optional
        Interpolation method: 'linear', 'cubic', or 'nearest'.
        Default is 'linear'.

    Returns
    -------
    callable
        An interpolation function that accepts x values and
        returns interpolated y values.

    Raises
    ------
    ValueError
        If `x` and `y` have different lengths.
    """
```

### reStructuredText (reST) Style (used by Sphinx default)

```python
def connect(host, port, timeout=30):
    """Connect to the remote server.

    :param host: Hostname or IP address of the server.
    :type host: str
    :param port: Port number to connect on.
    :type port: int
    :param timeout: Connection timeout in seconds, defaults to 30.
    :type timeout: int, optional
    :return: An active connection object.
    :rtype: Connection
    :raises ConnectionError: If the connection cannot be established.
    """
```

---

## Inline Comments

PEP 8 rules for inline comments:

- Use `#` followed by a single space.
- Inline comments (on the same line as code) should be separated by at least two spaces from the statement. Use sparingly.
- Block comments (on their own line) are preferred for anything more than a few words.
- Each line of a block comment starts with `#` and a single space.

Required inline comments:
- Before algorithm blocks
- Before regex patterns (explain what they match)
- Before non-obvious conditional logic
- Before error handling with specific recovery strategies
- On magic numbers or non-obvious constants
- Before workarounds with issue references

```python
# Use a sliding window approach to find the maximum sum subarray
# of length k. This is O(n) compared to the naive O(n*k) approach.
window_sum = sum(values[:k])
max_sum = window_sum

for i in range(k, len(values)):
    # Slide the window: add the new element, remove the leftmost
    window_sum += values[i] - values[i - k]
    max_sum = max(max_sum, window_sum)

# Match email addresses per RFC 5322 simplified pattern.
# Captures local-part (group 1) and domain (group 2).
EMAIL_PATTERN = re.compile(r'^([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$')
```