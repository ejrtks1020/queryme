def get_nl2sql_prompt(table_schema: str, query: str) -> str:
    return f"""
You are a helpful assistant that can help me generate SQL queries from natural language.

I will give you a natural language query and you will generate a SQL query.

Here is natural language query and table schema:

TABLE_SCHEMA = {table_schema}
QUERY = {query}

Please generate a SQL query that will answer the query.

Please return only the SQL query, no other text.
"""