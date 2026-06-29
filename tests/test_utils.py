"""Unit tests"""
import pytest
from src.utils import get_table_name

def test_get_table_name():
    result = get_table_name("dev", "sales", "orders")
    assert result == "dev.sales.orders"
