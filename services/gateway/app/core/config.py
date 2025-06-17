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
    gateway_port: int = 8081
    
    # Auth Service settings (환경 변수로 오버라이드 가능)
    auth_service_host_local: str = "localhost"
    auth_service_port_local: int = 8080
    auth_service_host_prod: str = "auth_service"
    auth_service_port_prod: int = 8080
    
    # Custom auth service settings (환경 변수로 오버라이드 가능)
    auth_service_host: str = ""
    auth_service_port: int = 0

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
            }
        }


# 싱글톤 패턴으로 설정 인스턴스 생성
settings = GatewaySettings()