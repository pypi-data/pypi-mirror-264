from _typeshed import Incomplete
from typing import Any

class JwtVerifyResponse:
    tlc_user_id: Incomplete
    ttl: Incomplete
    def __init__(self, tlc_user_id: str, ttl: float) -> None: ...

class JwtValidator:
    region: Incomplete
    userPoolId: Incomplete
    appClientId: Incomplete
    keys: Incomplete
    def __init__(self, region: str, userPoolId: str, appClientId: str) -> None: ...
    def verify_jwt(self, token: bytes) -> JwtVerifyResponse | None: ...
    def findJwkValue(self, kid: Any) -> dict | None: ...
    def decodeJwtToken(self, token: bytes, publicKey: Any) -> dict | None: ...
