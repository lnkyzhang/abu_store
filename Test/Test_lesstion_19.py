
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy


from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuMarketDrawing, ABuProgress, ABuSymbolPd, get_price, ABuIndustries
from abupy import EMarketDataFetchMode, EDataCacheType, EMarketSourceType, FuturesBaseMarket, TCBaseMarket, ABuDateUtil
from abupy import AbuDataParseWrap, StockBaseMarket, SupportMixin, ABuNetWork, Symbol, code_to_symbol



pd.set_option('display.width', 5000)
# 禁止沙盒数据
abupy.env.disable_example_env_ipython()
# 数据更新方式-本地
# abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_NORMAL   # 此选项有问题，会一直去访问网络
abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL
# 设置数据源(也可以自定义数据源)
abupy.env.g_market_source = EMarketSourceType.E_MARKET_SOURCE_tx
# 更新本地数据
# abu.run_kl_update(start='1990-01-01', end='2019-08-23', market=EMarketTargetType.E_MARKET_TARGET_CN, n_jobs=10)

print(abupy.env.g_data_fetch_mode)
print(abupy.env.g_market_source)
print(ABuSymbolPd.make_kl_df('600749').tail(100))
print(abupy.env.g_project_kl_df_data_csv)