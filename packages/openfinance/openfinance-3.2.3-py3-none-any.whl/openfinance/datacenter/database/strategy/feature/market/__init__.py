#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2024/02/05 20:25 

'''


from openfinance.datacenter.database.strategy.feature.base import FeatureManager

from openfinance.datacenter.database.strategy.feature.market.vix import Vix
from openfinance.datacenter.database.strategy.feature.market.north_moneyflow import NorthMoneyFlowVar
from openfinance.datacenter.database.strategy.feature.market.north_moneyflow_position import NorthMoneyFlowPosition

from openfinance.datacenter.database.strategy.feature.market.market_volume import MarketVolume


FeatureManager().register([
    Vix,
    NorthMoneyFlowVar,
    MarketVolume,
    NorthMoneyFlowPosition
])

FeatureManager().register_from_file(
    "openfinance/datacenter/database/strategy/feature/market/feature_id.json"
)