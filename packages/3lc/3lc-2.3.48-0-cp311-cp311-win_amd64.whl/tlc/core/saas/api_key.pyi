from _typeshed import Incomplete
from datetime import datetime
from pydantic.main import BaseModel
from tlc.core.saas.jwt_validator import JwtValidator as JwtValidator, JwtVerifyResponse as JwtVerifyResponse
from tlc.core.saas.runtime_config import USER_SERVICE_CLIENT as USER_SERVICE_CLIENT, USER_SERVICE_REGION as USER_SERVICE_REGION, USER_SERVICE_URL as USER_SERVICE_URL, USER_SERVICE_USER_POOL as USER_SERVICE_USER_POOL
from typing import Callable

logger: Incomplete

class RequestValidateKeyResponse:
    user_id: Incomplete
    tenant_id: Incomplete
    meta_dict: Incomplete
    ttl: Incomplete
    def __init__(self, user_id: str, tenant_id: str, meta_dict: dict, ttl: float) -> None: ...

class Key:
    key: Incomplete
    ttl: Incomplete
    user_id: Incomplete
    tenant_id: Incomplete
    user_info_dict: Incomplete
    expiry_datetime: Incomplete
    refresh_interval: Incomplete
    next_refresh: Incomplete
    def __init__(self, key: bytes, user_id: str, tenant_id: str, user_info_dict: dict, ttl: float, expiry_datetime: datetime, refresh_interval: float, refresh: Callable[[bytes], RequestValidateKeyResponse | None]) -> None: ...
    def valid(self, now: float) -> tuple[bool, str]: ...

USER_CONFIG_URL: Incomplete

class UserInfo(BaseModel):
    user_id: str
    tenant_id: str
    user_full_name: str
    user_email: str
    tenant_name: str

class ApiKey:
    api_key_instance: ApiKey | None
    soon_to_expire_warning: bool
    api_key: Incomplete
    jwt_keys: Incomplete
    email: bytes
    cognito_username: bytes
    error: Incomplete
    user_info: Incomplete
    def __init__(self, api_key: Key, request_validate_jwt: Callable[[bytes], RequestValidateKeyResponse | None] | None, error: str) -> None: ...
    def validate(self) -> tuple[bool, str]: ...
    def validate_jwt(self, jwt_key: bytes) -> bool: ...
    @staticmethod
    def instance() -> ApiKey: ...
