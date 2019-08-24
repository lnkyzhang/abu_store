# 基础库导入
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ipywidgets

import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy


from abupy import AbuFactorAtrNStop, AbuFactorPreAtrNStop, AbuFactorCloseAtrNStop, AbuFactorBuyBreak
from abupy import abu, EMarketTargetType, AbuMetricsBase, ABuMarketDrawing, ABuProgress, ABuSymbolPd
from abupy import EMarketTargetType, EDataCacheType, EMarketSourceType, EMarketDataFetchMode, EStoreAbu, AbuUmpMainMul
from abupy import AbuUmpMainDeg, AbuUmpMainJump, AbuUmpMainPrice, AbuUmpMainWave, feature, AbuFeatureDegExtend
from abupy import AbuUmpEdgeDeg, AbuUmpEdgePrice, AbuUmpEdgeWave, AbuUmpEdgeFull, AbuUmpEdgeMul, AbuUmpEegeDegExtend
from abupy import AbuUmpMainDegExtend, ump
# 关闭沙盒数据
abupy.env.disable_example_env_ipython()



# 初始化资金500万
read_cash = 5000000

# 买入因子依然延用向上突破因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak},
               {'xd': 42, 'class': AbuFactorBuyBreak}]

# 卖出因子继续使用上一节使用的因子
sell_factors = [
    {'class': AbuFactorAtrNStop, 'stop_loss_n': 1.0, 'stop_win_n': 3.0},
    {'class': AbuFactorPreAtrNStop, 'pre_atr_n': 1.5},
    {'class': AbuFactorCloseAtrNStop, 'close_atr_n': 1.5}
]
abupy.env.g_market_target = EMarketTargetType.E_MARKET_TARGET_CN
abupy.env.g_data_fetch_mode = EMarketDataFetchMode.E_DATA_FETCH_FORCE_LOCAL


def select_store_cache(use_csv):
    if use_csv:
        abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_CSV
    else:
        abupy.env.g_data_cache_type = EDataCacheType.E_DATA_CACHE_HDF5
    print(abupy.env.g_data_cache_type)


# use_csv = ipywidgets.Checkbox(True)
# _ = ipywidgets.interact(select_store_cache, use_csv=use_csv)
select_store_cache(True)


# 回测生成买入时刻特征
abupy.env.g_enable_ml_feature = True
# 回测开始时将symbols切割分为训练集数据和测试集两份，使用训练集进行回测
abupy.env.g_enable_train_test_split = True

# 每笔交易的买入基数资金设置为万分之30
abupy.beta.atr.g_atr_pos_base = 0.003

feature.clear_user_feature()
feature.append_user_feature(AbuFeatureDegExtend)


abu_result_tuple = None
def run_loop_back():
    global abu_result_tuple
    abu_result_tuple, _ = abu.run_loop_back(read_cash,
                                            buy_factors,
                                            sell_factors,
                                            choice_symbols=None,
                                            start='2012-08-08', end='2017-08-08')
    # 把运行的结果保存在本地，以便之后分析回测使用，保存回测结果数据代码如下所示
    abu.store_abu_result_tuple(abu_result_tuple, n_folds=5, store_type=EStoreAbu.E_STORE_CUSTOM_NAME,
                               custom_name='train_cn')
    ABuProgress.clear_output()

def run_load_train():
    global abu_result_tuple
    abu_result_tuple = abu.load_abu_result_tuple(n_folds=5, store_type=EStoreAbu.E_STORE_CUSTOM_NAME,
                                                 custom_name='train_cn')

def select(select):
    if select == 'run loop back':
        run_loop_back()
    else:
        run_load_train()





if __name__ == "__main__":
    # execute only if run as a script
    # _ = ipywidgets.interact_manual(select, select=['run loop back', 'load train data'])
    select('run loop back')

    AbuMetricsBase.show_general(*abu_result_tuple, only_show_returns=True)