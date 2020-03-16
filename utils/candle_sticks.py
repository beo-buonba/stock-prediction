import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from mpl_finance import candlestick_ohlc
from utils.graph_utils import IntegerIndexDateTimeFormatter, _updown_colors
from config import DATE_FORMAT_STRING

def plot_candle_sticks(ohlc, volumes, show_nontrading=False):
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
    fig = plt.figure()
    ax1 = fig.add_axes([0.15, 0.38, 0.70, 0.50])
    ax2 = fig.add_axes([0.15, 0.18, 0.70, 0.20], sharex=ax1)
    plt.xticks(rotation=45)
    ax2.set_axisbelow(True)
    ax4 = ax2.twinx()
    ax4.grid(False)

    colors = _updown_colors(ohlc)
    avg_dist_between_points = (ohlc['date'][ohlc.index[-1]] - ohlc['date'][ohlc.index[0]]) / float(len(ohlc['date']))
    width = 0.5 * avg_dist_between_points
    ax2.bar(ohlc['date'], volumes, width=width, color=colors)
    miny = 0.3 * min(volumes)
    maxy = 1.1 * max(volumes)
    ax2.set_ylim(miny, maxy)
    ax2.xaxis.set_major_formatter(formatter)



    # plot candle sticks to subplot
    candlestick_ohlc(ax1, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    return fig, ax1, formatter, ohlc
