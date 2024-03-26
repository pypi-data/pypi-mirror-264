import asyncio
import aiohttp
import json

from abc import ABC, abstractmethod

from typing import (
    Any,
    List,
    Dict
)
from openfinance.strategy.policy.lr_ranker import OperationPolicy

class MarketRunner(OperationPolicy):
    name = "MarketRunner"
    desc = "MarketRunner"

if __name__== "__main__":
    policy = MarketRunner.from_file(
        "openfinance/strategy/models/LR/market_danger.json"
    )

    features = policy.features(
        candidates=["上证指数"]
    )
    print(json.dumps(features, indent=4, ensure_ascii=False))