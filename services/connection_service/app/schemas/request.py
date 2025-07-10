from pydantic import BaseModel


class ConnectionCreateRequest(BaseModel):
    user_id: int
    connection_name: str
    database_name: str
    database_type: str
    database_url: str | None = None
    database_username: str
    database_password: str
    database_port: int | None = None
    database_host: str | None = None
    database_table: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_id": 1,
                "connection_name": "test_connection",
                "database_name": "test_data",
                "database_type": "mysql",
                "database_url": "mysql+pymysql://root:queryme1!@localhost:3306/test_data",
                "database_username": "root",
                "database_password": "password123!",
                "database_port": 3306,
                "database_host": "localhost",
                "database_table": "test"
            }
        }
    }

class ConnectionUpdateRequest(BaseModel):
    connection_id: int
    connection_name: str
    database_name: str
    database_type: str
    database_url: str | None = None
    database_username: str
    database_password: str
    database_port: int | None = None
    database_host: str | None = None
    database_table: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "connection_id": 1,
                "database_name": "test_data",
                "database_type": "mysql",
                "database_url": "mysql+pymysql://root:queryme1!@localhost:3306/test_data",
                "database_username": "root",
                "database_password": "password123!",
                "database_port": 3306,
                "database_host": "localhost",
                "database_table": "test"
            }
        }
    }

class ConnectionDeleteRequest(BaseModel):
    connection_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "connection_id": 1
            }
        }
    }