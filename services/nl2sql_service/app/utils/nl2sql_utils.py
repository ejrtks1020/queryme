from typing import Union, Dict, Any
from enum import Enum

class RequestType(Enum):
    DATABASE = "database"
    DDL = "ddl"

def format_schema_info(schema_info: Union[str, Dict[str, Any]]) -> str:
    """
    스키마 정보를 문자열로 변환
    - str인 경우: DDL 스키마 텍스트 그대로 반환
    - dict인 경우: 데이터베이스에서 조회한 스키마를 DDL 형태로 변환
    """
    if isinstance(schema_info, str):
        # DDL 스키마 텍스트인 경우
        return schema_info
    
    if isinstance(schema_info, dict):
        # 데이터베이스에서 조회한 스키마인 경우
        schema_text = ""
        for table_name, columns in schema_info.items():
            schema_text += f"\n-- {table_name} 테이블\n"
            schema_text += f"CREATE TABLE {table_name} (\n"
            
            column_definitions = []
            for column in columns:
                column_def = f"    {column['field']} {column['type']}"
                
                if column['null'] == 'NO':
                    column_def += " NOT NULL"
                    
                if column['key'] == 'PRI':
                    column_def += " PRIMARY KEY"
                elif column['key'] == 'UNI':
                    column_def += " UNIQUE"
                
                if column['default'] is not None:
                    column_def += f" DEFAULT {column['default']}"
                
                if column['extra']:
                    column_def += f" {column['extra']}"
                
                column_definitions.append(column_def)
            
            schema_text += ",\n".join(column_definitions)
            schema_text += "\n);\n"
        
        return schema_text
    
    return str(schema_info)

def get_nl2sql_prompt(schema_info: Union[str, Dict[str, Any]], query: str) -> str:
    """
    자연어 쿼리를 위한 프롬프트 생성
    """
    table_schema = format_schema_info(schema_info)
    
    return f"""
You are a helpful assistant that can help me generate SQL queries from natural language.

I will give you a natural language query and you will generate a SQL query.

Here is natural language query and table schema:

TABLE_SCHEMA = {table_schema}
QUERY = {query}

Please generate a SQL query that will answer the query.

Please return only the SQL query, no other text.
"""