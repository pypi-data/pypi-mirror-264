# ainft-py

[![PyPi Version](https://img.shields.io/pypi/v/ainft-py.svg)](https://pypi.python.org/pypi/ainft-py/)

A python version of [ainft-js](https://github.com/ainft-team/ainft-js).

## Installation

```sh
pip install ainft-py
```

## Usage

```python
import os
from ainft import Ainft

ainft = Ainft(
    private_key=os.environ.get("AIN_PRIVATE_KEY"),
    api_url="https://ainft-api-dev.ainetwork.ai",
    blockchain_url="https://testnet-api.ainetwork.ai",
    chain_id=0,
)
```

## Requirements

Python version should be at least 3.8 but less than 3.12.
