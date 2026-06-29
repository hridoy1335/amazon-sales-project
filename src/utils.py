"""Utility functions"""

def get_table_name(catalog: str, schema: str, table: str) -> str:
    return f"{catalog}.{schema}.{table}"
