from __future__ import annotations

from typing import Literal

from ain.ain import Ain

from .chat import Chat


class Ainft:
    def __init__(
        self,
        *,
        private_key: str,
        api_url: str,
        blockchain_url: str,
        chain_id: Literal[0, 1],
    ):
        self._base_url = api_url
        self._blockchain_url = blockchain_url
        self._chain_id = chain_id

        self._ain = Ain(self._blockchain_url, self._chain_id)
        self._set_default_account(private_key)

        self.chat = Chat(self._ain)

    def _set_default_account(self, private_key: str):
        self._ain.wallet.clear()
        self._ain.wallet.addAndSetDefaultAccount(private_key)
