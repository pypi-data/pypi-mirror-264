from openfinance.datacenter.database.strategy.operator.base import OperatorManager
from openfinance.datacenter.database.strategy.operator.mean import Mean
from openfinance.datacenter.database.strategy.operator.acc import Acc
from openfinance.datacenter.database.strategy.operator.latest import Latest
from openfinance.datacenter.database.strategy.operator.yoy import Yoy
from openfinance.datacenter.database.strategy.operator.divide_latest import DivideLatest
from openfinance.datacenter.database.strategy.operator.moving_average import MovingAverage
from openfinance.datacenter.database.strategy.operator.macd import MAConDiv
from openfinance.datacenter.database.strategy.operator.rsi import RSI
from openfinance.datacenter.database.strategy.operator.obv import OnBalanceVolume
from openfinance.datacenter.database.strategy.operator.coefficient_variance import CoeffVar
from openfinance.datacenter.database.strategy.operator.latest_position_index import LatestPosition
from openfinance.datacenter.database.strategy.operator.hist import Hist

OperatorManager().register(
    [
        Mean,
        Acc,
        Latest,
        Yoy,
        DivideLatest,
        MovingAverage,
        MAConDiv,
        RSI,
        CoeffVar,
        OnBalanceVolume,
        LatestPosition,
        Hist
    ]
)
