import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ohlc
from utils.graph_utils import IntegerIndexDateTimeFormatter
from config import DATE_FORMAT_STRING

def plot_candle_sticks(ohlc, show_nontrading=False):
    """
    Plot candle sticks graph
    :return:
    """
    ohlc['date'] = pd.to_datetime(ohlc['date'], format=DATE_FORMAT_STRING)
    ohlc['date'] = ohlc['date'].apply(mpl_dates.date2num)
    ohlc = ohlc.astype(float)

    # Formatting Date for plotting
    if show_nontrading:
        formatter = mpl_dates.DateFormatter(DATE_FORMAT_STRING)
    else:
        formatter = IntegerIndexDateTimeFormatter(list(ohlc['date']), DATE_FORMAT_STRING)
        ohlc['date'] = np.arange(len(ohlc['date']))

    # Define subplots, setting labels & titles
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')

    # plot candle sticks to subplot
    candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    return fig, ax, formatter, ohlc
