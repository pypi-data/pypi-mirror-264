#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Date    ：2024/02/05 20:25 

'''
from openfinance.datacenter.database.strategy.feature.base import FeatureManager

from openfinance.datacenter.database.strategy.feature.company.divident_stability import DividentSpeed
from openfinance.datacenter.database.strategy.feature.company.divident_mean import DividentMean
from openfinance.datacenter.database.strategy.feature.company.news_sentiment import NewsSentiment
from openfinance.datacenter.database.strategy.feature.company.moneyflow_direction import MoneyFlowDirect
from openfinance.datacenter.database.strategy.feature.company.win_cost_distribution import WinCostDist

FeatureManager().register([
    DividentSpeed,
    DividentMean,
    NewsSentiment,
    MoneyFlowDirect,
    WinCostDist
])

FeatureManager().register_from_file(
    "openfinance/datacenter/database/strategy/feature/company/feature_id.json"
)