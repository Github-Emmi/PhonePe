#!/usr/bin/env python
"""Test format_large_number function"""

from dashboard.utils.formatting import format_large_number

test_values = [
    0,
    100,
    1000,
    10000,
    100000,
    1000000,
    10000000,
    100000000,
    920496748996,
    1350490245223129.8,
    10258862968,
    None
]

print("Testing format_large_number:")
for val in test_values:
    try:
        result = format_large_number(val)
        print(f"  {val:>20} -> {result}")
    except Exception as e:
        print(f"  {val:>20} -> ERROR: {e}")
