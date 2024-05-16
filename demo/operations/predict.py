import warnings
import itertools
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# 对编号为vid的视频进行次数为step的预测
def arima_forecast(time_series_path,vid,step):
    
    warnings.filterwarnings("ignore")

    # 从CSV文件中读取数据
    data_row = pd.read_csv(time_series_path, skiprows = int(vid) + 1, nrows=1,header=None,index_col=0)
    data = data_row.values.flatten()
    
    time_index = pd.date_range('2024-01-01', periods=len(data))
    ts = pd.Series(data, index=time_index)
    
    # 判断时间序列的平稳性
    def check_stationarity(timeseries):
        result = adfuller(timeseries)
        p_value = result[1]
        return p_value < 0.05

    # 自动确定ARIMA模型的d值
    def get_d_value(timeseries):
        d = 0
        while not check_stationarity(timeseries):
            timeseries = timeseries.diff().dropna()  # 对时间序列进行一阶差分
            d += 1
        return d

    d_value = get_d_value(ts)

    # pq的取值范围
    p_min = 0
    d_min = 0
    q_min = 0
    p_max = 5
    d_max = 0
    q_max = 5

    #BIC准则
    results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min,p_max+1)],
                            columns=['MA{}'.format(i) for i in range(q_min,q_max+1)])

    for p,d,q in itertools.product(range(p_min,p_max+1),
                                range(d_min,d_max+1),
                                range(q_min,q_max+1)):
        if p==0 and d==0 and q==0:
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
            continue
        try:
            model = sm.tsa.ARIMA(data, order=(p, d, q),)
            results = model.fit()
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
        except:
            continue

    results_bic = results_bic[results_bic.columns].astype(float)
    results_bic.stack().idxmin()

    # 取p和q的最优值
    train_results = sm.tsa.arma_order_select_ic(data, ic=['aic', 'bic'], trend='n', max_ar=8, max_ma=8)
    p_value, q_value = train_results.bic_min_order 


    # 拟合ARIMA模型并预测
    model = ARIMA(ts, order=(p_value, d_value , q_value))
    result = model.fit()
    forecast = result.forecast(step)
    rounded_forecast = forecast.round(3)

    x = list(range(1, len(data)+1))
    x1 = list(range(30, 30 + step +1))
    y = list(data)
    y1 = rounded_forecast.values.tolist()
    y1.insert(0, y[-1])
    return  x, y, x1, y1