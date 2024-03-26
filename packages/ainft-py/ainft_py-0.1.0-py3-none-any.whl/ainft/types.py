from pydantic import BaseModel
from typing import Any, List, Literal, Optional, Union

SetMultiOperationType = Literal["SET"]
GetMultiOperationType = Literal["GET"]
SetOperationType = Literal[
    "SET_VALUE", "INC_VALUE", "DEC_VALUE", "SET_RULE", "SET_OWNER", "SET_FUNCTION"
]
GetOperationType = Literal["GET_VALUE", "GET_RULE", "GET_OWNER", "GET_FUNCTION"]


class SetOperation(BaseModel):
    type: SetOperationType
    ref: str
    value: Optional[Any] = None


class SetMultiOperation(BaseModel):
    type: SetMultiOperationType
    op_list: List[SetOperation]


class Thread(BaseModel):
    id: str
    metadata: Optional[dict] = None
    created_at: int


class Message(BaseModel):
    id: str
    """
    The ID of the message, 
    must be a 20-character alphanumeric starting with 'msg_' or a digit string.
    """
    thread_id: str
    """The ID of the thread."""
    role: Literal["user", "assistant"]
    """The role of the entity creating the message."""
    content: str
    """
    The content of the message. 
    If the content exceeds 200 characters, it will be automatically trimmed.
    """
    assistant_id: Optional[str] = None
    """If applicable, the ID of the assistant that authored this message."""
    run_id: Optional[str] = None
    """If applicable, the ID of the run associated with the authoring of this message."""
    metadata: Optional[dict] = None
    """
    The metadata can contain up to 16 key-value pairs,
    with the keys limited to 64 characters and the values to 512 characters.
    """
    created_at: int
    """The UNIX timestamp in seconds, used as a key."""


class TransactionInput(BaseModel):
    operation: Union[SetOperation, SetMultiOperation]
    timestamp: int
    nonce: Optional[int] = None
    address: Optional[str] = None
    gas_price: Optional[int] = None


class TransactionResult(BaseModel):
    tx_hash: str
    result: dict


class ThreadTransactionResult(TransactionResult):
    thread: Thread


class MessageTransactionResult(TransactionResult):
    messages: List[Message]
