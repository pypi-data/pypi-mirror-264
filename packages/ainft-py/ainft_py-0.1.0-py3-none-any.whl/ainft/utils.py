from __future__ import annotations

from datetime import datetime
import re
import uuid
import unicodedata
from typing import Any


from ain.ain import Database, Wallet


def get_app_id(object_id: str) -> str:
    return f"ainft721_{object_id.lower()}"


def get_user_address(wallet: Wallet) -> str | None:
    return getattr(wallet.defaultAccount, "address", None)


def is_tx_success(tx_result: Any) -> bool:
    result = tx_result.get("result", {})
    if result.get("code") is not None and result["code"] != 0:
        return False
    if "result_list" in result:
        results = result["result_list"].values()
        return all(r.get("code") == 0 for r in results)
    return True


def join_paths(paths: list) -> str:
    return "/".join(paths)


def now() -> float:
    return datetime.now().timestamp()


def truncate_text(text: str, max_length: int) -> str:
    if max_length <= 0:
        raise ValueError("max_length must be greater than 0.")
    text = text.strip()
    text = unicodedata.normalize('NFC', text)
    if len(text) > max_length:
        return text[: max_length - 3] + "..."
    return text


def validate_user_address(wallet: Wallet) -> str:
    user_addr = get_user_address(wallet)
    if user_addr is None:
        raise ValueError(f"The default account not found.")
    return user_addr


async def validate_app(app_id: str, db: Database):
    app_path = join_paths(["apps", app_id])
    app = await db.ref(app_path).getValue()
    if app is None:
        raise ValueError(f"The app {app_id} does not exist.")


async def validate_token(app_id: str, token_id: str, db: Database):
    token_path = join_paths(["apps", app_id, "tokens", token_id])
    token = await db.ref(token_path).getValue()
    if token is None:
        raise ValueError(f"The token {token_id} does not exist.")


async def validate_thread(
    app_id: str, token_id: str, address: str, thread_id: str, db: Database
):
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
    thread = await db.ref(thread_path).getValue()
    if thread is None:
        raise ValueError(f"The thread {thread_id} does not exist.")


def validate_thread_id(thread_id: str):
    if not is_valid_thread_id(thread_id):
        raise ValueError(f"Invalid thread ID.")


def is_valid_thread_id(thread_id: str) -> bool:
    try:
        return str(uuid.UUID(thread_id, version=4)) == thread_id
    except ValueError:
        pass
    pattern = r"thread_[A-Za-z0-9]{20}$"
    if re.match(pattern, thread_id):
        return True
    return False


def validate_message_id(message_id: str):
    if not is_valid_message_id(message_id):
        raise ValueError(f"Invalid message ID.")


def is_valid_message_id(message_id: str) -> bool:
    if message_id.isdigit():
        return True
    pattern = r"msg_[A-Za-z0-9]{20}$"
    if re.match(pattern, message_id):
        return True
    return False
