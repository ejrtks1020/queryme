import os
import ast
from typing import Dict
from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings

PROFILE = os.getenv("PROFILE", "local")

def get_env_path(profile: str) -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        f'env/.env.{profile}'
    )


class ServiceEndpoint(BaseModel):
    host: str
    port: int
    
    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"


class GatewaySettings(BaseSettings):
    profile: str = PROFILE
    
    # Gateway server settings
    gateway_host: str = "0.0.0.0"
    gateway_port: int = 8080
    
    # Auth Service settings (환경 변수로 오버라이드 가능)
    auth_service_host_local: str = "localhost"
    auth_service_port_local: int = 8081
    auth_service_host_prod: str = "auth_service"
    auth_service_port_prod: int = 8080
    
    # Connection Service settings (환경 변수로 오버라이드 가능)
    connection_service_host_local: str = "localhost"
    connection_service_port_local: int = 8082
    connection_service_host_prod: str = "connection_service"
    connection_service_port_prod: int = 8080

    # NL2SQL Service settings (환경 변수로 오버라이드 가능)
    nl2sql_service_host_local: str = "localhost"
    nl2sql_service_port_local: int = 8083
    nl2sql_service_host_prod: str = "nl2sql_service"
    nl2sql_service_port_prod: int = 8080

    # DDL Session Service settings (환경 변수로 오버라이드 가능)
    ddl_session_service_host_local: str = "localhost"
    ddl_session_service_port_local: int = 8084
    ddl_session_service_host_prod: str = "ddl_session_service"
    ddl_session_service_port_prod: int = 8080

    # History Service settings (환경 변수로 오버라이드 가능)
    history_service_host_local: str = "localhost"
    history_service_port_local: int = 8085
    history_service_host_prod: str = "history_service"
    history_service_port_prod: int = 8080
    
    # Custom auth service settings (환경 변수로 오버라이드 가능)
    auth_service_host: str = ""
    auth_service_port: int = 0 

    connection_service_host: str = ""
    connection_service_port: int = 0

    nl2sql_service_host: str = ""
    nl2sql_service_port: int = 0

    ddl_session_service_host: str = ""
    ddl_session_service_port: int = 0

    history_service_host: str = ""
    history_service_port: int = 0

    cors_origins: list[str] = ["*"]

    @field_validator('cors_origins', mode='before')
    def parse_cors_origins(cls, v):
        try:
            if isinstance(v, str):
                return ast.literal_eval(v)
            elif isinstance(v, list):
                return v
            else:
                return []
        except:
            return []

    
    class Config:
        extra = "allow"
        env_file = [get_env_path(PROFILE)]
        env_file_encoding = "utf-8"
    
    def get_auth_service_url(self) -> str:
        """환경에 따른 Auth Service URL을 반환합니다."""
        # 직접 설정된 호스트/포트가 있으면 우선 사용
        if self.auth_service_host and self.auth_service_port:
            return f"http://{self.auth_service_host}:{self.auth_service_port}"
        
        # 프로필별 기본 설정 사용
        if self.profile == "local":
            return f"http://{self.auth_service_host_local}:{self.auth_service_port_local}"
        elif self.profile == "prod":
            return f"http://{self.auth_service_host_prod}:{self.auth_service_port_prod}"
        else:
            raise ValueError(f"Unknown profile: {self.profile}. Supported profiles: local, prod")
    
    def get_connection_service_url(self) -> str:
        """환경에 따른 Connection Service URL을 반환합니다."""
        if self.connection_service_host and self.connection_service_port:
            return f"http://{self.connection_service_host}:{self.connection_service_port}"
        
        if self.profile == "local":
            return f"http://{self.connection_service_host_local}:{self.connection_service_port_local}"
        elif self.profile == "prod":
            return f"http://{self.connection_service_host_prod}:{self.connection_service_port_prod}"
        else:
            raise ValueError(f"Unknown profile: {self.profile}. Supported profiles: local, prod")
    
    def get_nl2sql_service_url(self) -> str:
        """환경에 따른 NL2SQL Service URL을 반환합니다."""
        if self.nl2sql_service_host and self.nl2sql_service_port:
            return f"http://{self.nl2sql_service_host}:{self.nl2sql_service_port}"
        
        if self.profile == "local":
            return f"http://{self.nl2sql_service_host_local}:{self.nl2sql_service_port_local}"
        elif self.profile == "prod":
            return f"http://{self.nl2sql_service_host_prod}:{self.nl2sql_service_port_prod}"
        else:
            raise ValueError(f"Unknown profile: {self.profile}. Supported profiles: local, prod")
    
    def get_ddl_session_service_url(self) -> str:
        """환경에 따른 DDL Session Service URL을 반환합니다."""
        if self.ddl_session_service_host and self.ddl_session_service_port:
            return f"http://{self.ddl_session_service_host}:{self.ddl_session_service_port}"
        
        if self.profile == "local":
            return f"http://{self.ddl_session_service_host_local}:{self.ddl_session_service_port_local}"
        elif self.profile == "prod":
            return f"http://{self.ddl_session_service_host_prod}:{self.ddl_session_service_port_prod}"
        else:
            raise ValueError(f"Unknown profile: {self.profile}. Supported profiles: local, prod")
    
    def get_history_service_url(self) -> str:
        """환경에 따른 History Service URL을 반환합니다."""
        if self.history_service_host and self.history_service_port:
            return f"http://{self.history_service_host}:{self.history_service_port}"
        
        if self.profile == "local":
            return f"http://{self.history_service_host_local}:{self.history_service_port_local}"
        elif self.profile == "prod":
            return f"http://{self.history_service_host_prod}:{self.history_service_port_prod}"
        else:
            raise ValueError(f"Unknown profile: {self.profile}. Supported profiles: local, prod")
    
    def get_service_info(self) -> Dict:
        """서비스 정보를 반환합니다."""
        return {
            "profile": self.profile,
            "gateway": {
                "host": self.gateway_host,
                "port": self.gateway_port
            },
            "auth_service": {
                "url": self.get_auth_service_url()
            },
            "connection_service": {
                "url": self.get_connection_service_url()
            },
            "nl2sql_service": {
                "url": self.get_nl2sql_service_url()
            },
            "ddl_session_service": {
                "url": self.get_ddl_session_service_url()
            },
            "history_service": {
                "url": self.get_history_service_url()
            }
        }


# 싱글톤 패턴으로 설정 인스턴스 생성
settings = GatewaySettings()