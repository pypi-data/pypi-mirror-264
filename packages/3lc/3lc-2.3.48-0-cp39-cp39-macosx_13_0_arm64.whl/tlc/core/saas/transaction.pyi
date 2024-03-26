import tlc
from _typeshed import Incomplete
from tlc.core.saas.api_key import ApiKey as ApiKey
from tlc.core.saas.runtime_config import MLOP_SERVICE_URL as MLOP_SERVICE_URL
from tlc.core.schema import Schema as Schema
from typing import Callable, Generic, Protocol, TypeVar

TRANSACTION_ROW_EDITS: str
logger: Incomplete

class TransactionData:
    type_name: Incomplete
    count: Incomplete
    id: str
    idempotent_id: str
    def __init__(self, type_name: str, count: int) -> None: ...

class TransactionDispatcher:
    transaction_dispatcher_instance: TransactionDispatcher | None
    process_unique_id: Incomplete
    def __init__(self, transaction_create_cb: Callable[[ApiKey, TransactionData], str], transaction_commit_cb: Callable[[ApiKey, TransactionData], None], transaction_rollback_cb: Callable[[ApiKey, TransactionData], None]) -> None: ...
    def create_transaction(self, transaction: TransactionData) -> str: ...
    def commit_transaction(self, transaction: TransactionData) -> None: ...
    def rollback_transaction(self, transaction: TransactionData) -> None: ...
    @staticmethod
    def instance() -> TransactionDispatcher: ...

class Transaction:
    data: Incomplete
    def __init__(self, type_name: str, count: int = 1) -> None: ...
    def create(self) -> None: ...
    def commit(self, transaction_type: str) -> None: ...
    def rollback(self) -> None: ...

class HasTransaction(Protocol):
    schema: Schema
    transaction_id: str
    url: tlc.Url
T = TypeVar('T', bound=HasTransaction)

class TransactionCloser(Generic[T]):
    resource: Incomplete
    transaction: Incomplete
    transaction_type: Incomplete
    def __init__(self, resource: T, transaction_type: str) -> None: ...
    def __enter__(self) -> T: ...
    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None: ...
