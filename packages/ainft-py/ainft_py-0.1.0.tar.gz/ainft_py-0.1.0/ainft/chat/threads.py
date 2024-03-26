from __future__ import annotations

import json
from typing import Optional

from ain.ain import Ain

from ..types import SetOperation, TransactionInput, Thread, ThreadTransactionResult
from ..utils import *


class Threads:
    def __init__(self, ain: Ain):
        self._ain = ain

    async def store(
        self,
        *,
        thread_id: str,
        object_id: str,
        token_id: str,
        metadata: Optional[dict] = None,
    ) -> ThreadTransactionResult:
        """
        Store a thread.

        Args:
            thread_id: The ID of the thread,
                must be a 20-character alphanumeric starting with 'thread_' or a uuid4.

            object_id: The ID of the AINFT object.

            token_id: The ID of the AINFT token.

            metadata: The metadata can contain up to 16 key-value pairs,
                with the keys limited to 64 characters and the values to 512 characters.
        """
        app_id = get_app_id(object_id)
        user_addr = validate_user_address(self._ain.wallet)

        await self._validate(app_id, token_id, thread_id)

        return await self._send_tx_for_store_thread(**dict(
            thread_id=thread_id,
            app_id=app_id,
            token_id=token_id,
            address=user_addr,
            metadata=metadata,
        ))

    async def _validate(self, app_id: str, token_id: str, thread_id: str):
        await validate_app(app_id, self._ain.db)
        await validate_token(app_id, token_id, self._ain.db)
        validate_thread_id(thread_id)

    async def _send_tx_for_store_thread(self, **kwargs) -> ThreadTransactionResult:
        timestamp = int(now())
        tx_body = self._build_tx_body_for_store_thread(timestamp=timestamp, **kwargs)
        tx_result = await self._ain.sendTransaction(tx_body)

        if not is_tx_success(tx_result):
            raise RuntimeError(f"Failed to send transaction: {json.dumps(tx_result)}")

        return self._format_tx_result(
            tx_result=tx_result, timestamp=timestamp, **kwargs
        )

    def _build_tx_body_for_store_thread(
        self,
        app_id: str,
        token_id: str,
        thread_id: str,
        address: str,
        timestamp: int,
        metadata: Optional[dict],
    ) -> TransactionInput:
        thread_path = join_paths(
            [
                "apps",
                app_id,
                "tokens",
                token_id,
                "ai",
                "ainize_openai",
                "history",
                address,
                "threads",
                thread_id,
            ]
        )
        thread = {
            "messages": True,
            **({"metadata": metadata} if metadata else {}),
        }
        op = SetOperation(type="SET_VALUE", ref=thread_path, value=thread)
        return TransactionInput(
            operation=op,
            timestamp=timestamp,
            nonce=-1,
            address=address,
            gas_price=500,
        )

    def _format_tx_result(
        self,
        tx_result: dict,
        timestamp: int,
        thread_id: str,
        **kwargs,
    ) -> ThreadTransactionResult:
        metadata = kwargs.get("metadata", {})
        thread = Thread(id=thread_id, metadata=metadata, created_at=timestamp)
        return ThreadTransactionResult(thread=thread, **tx_result)
