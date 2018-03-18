import copy
import warnings
import os
import sys
import math
import datetime

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from fbprophet import Prophet

zip_to_metro_df = pd.read_csv("zip_to_metro.csv")

def aggregate_df(df_orig):
    summed_df = df_orig.groupby('ds').sum()
    summed_df["ds"] = summed_df.index
    summed_df = summed_df[:-1] #remove last week as it's not necessarily a complete week
    return summed_df

def prophet_predict_weekly_orders(df, holidays, fcst_periods):
    m = Prophet(yearly_seasonality=True, holidays=holidays)
    m.fit(df)
    future = m.make_future_dataframe(periods=fcst_periods, freq='W')
    fcst = m.predict(future)
    fcst.index = fcst.ds
    return m, fcst

def get_zip_codes_by_metro(df, metro_str):
    return set(zip_to_metro_df[zip_to_metro_df.metro==metro_str].zip.astype(int))

def filter_df_by_metro(df, metro_str):
    valid_zips = get_zip_codes_by_metro(df, metro_str)
    return df[df.zip_code.apply(lambda zip_code: zip_code!=None and int(zip_code) in valid_zips)]

def predict_by_metro(df, metro_str, holidays, fcst_periods=12):
    metro_df_orig = filter_df_by_metro(df,metro_str)
    print df    
    print metro_df_orig
    metro_df = aggregate_df(metro_df_orig)
    print metro_df
    m_metro, fcst_metro = prophet_predict_weekly_orders(metro_df, holidays, fcst_periods)
    return m_metro, fcst_metro, metro_df

def percent_deviation(pred, act):
	return abs(sum(pred)-sum(act))/sum(act)