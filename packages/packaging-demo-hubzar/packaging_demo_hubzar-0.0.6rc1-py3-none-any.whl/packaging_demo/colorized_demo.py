"""This is a module docstring"""

try:
    from rich import print  # pylint: disable=[W0622]
except ImportError:
    ...

print("Hello: 1, 2, 3")
print({"a": 1, "b": 2})
