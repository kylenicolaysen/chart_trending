import requests
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import time
from dotenv import load_dotenv
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

load_dotenv()
today = datetime.today()
formatted_today = today.strftime('%Y-%m-%d')
tiingo_api_key = os.getenv('TIINGO_API_KEY')
auth = f'Token {tiingo_api_key}'
headers = {
    'Content-Type': 'application/json',
    'Authorization' : auth
    }


def get_data(ticker, today):
    requestResponse = requests.get(f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate=2023-12-03&endDate={today} ",
            headers=headers)
    print(f'{ticker}: {requestResponse}')
    data = requestResponse.json()
    df = pd.DataFrame(data)
    df['ticker'] = ticker
    return df


def get_performance(df):
    five_days = [0] * 4     #5 days
    one_month = [0] * 19   #20 days
    six_months = [0] * 129  #130 days
    for i in range(4, len(df)):
        five_days.append((df['close'][df.index[i]] - df['close'][df.index[i-4]]) / df['close'][df.index[i-4]] * 100)
    for i in range(19, len(df)):
        one_month.append((df['close'][df.index[i]] - df['close'][df.index[i-19]]) / df['close'][df.index[i-19]] * 100)
    for i in range(129, len(df)):
        six_months.append((df['close'][df.index[i]] - df['close'][df.index[i-129]]) / df['close'][df.index[i-129]] * 100)
    # print(f'{df['ticker'][df.index[0]]}: {df['close'][-10:]} \n {five_days[-10:]}')
    df['five_days'] = five_days
    df['one_month'] = one_month
    df['six_months'] = six_months
    df.to_pickle(f"./charts/chart_gen/data/{df['ticker'][df.index[0]]}_{formatted_today}.pkl")
    return df


def plot_perf(performance_df_list, group_title, hist_length, performance_length, interval=1):
    hist_length = hist_length * -1
    if performance_length == 'five_days':
        title_length = 'Five Days'
    elif performance_length == 'one_month':
        title_length = 'One Month'
    elif performance_length == 'six_months':
        title_length = 'Six Months'
    else:
        print('TITLE ERROR')
        title_length = '__'
    date_list = list(performance_df_list[0]['date'])
    formatted_date_list = []
    for i in date_list:
        date_obj = datetime.strptime(i, "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_date_list.append(date_obj.strftime("%m-%d"))
    plt.figure(figsize=(16, 12))
    plt.title(f'{title_length} Performance of {group_title} -- {hist_length * -1} Data Points -- {interval} Interval -- {formatted_today}')
    plt.xlabel('Date')
    plt.ylabel('Performance (%)')
    # print(performance_df_list[0].index[hist_length::interval])
    plt.xticks(performance_df_list[0].index[hist_length::interval], formatted_date_list[hist_length::interval], rotation=45)
    # print('DATE LIST:', formatted_date_list[hist_length::interval])
    # print('HIST LENGTH', hist_length)
    # print(interval)
    # plt.xticks(formatted_date_list[hist_length::interval], formatted_date_list[hist_length::interval], rotation=45)
    index_list = performance_df_list[0].index.to_list()
    plt.plot(index_list[hist_length:], ([0] * (hist_length*-1)), color='grey', linestyle='--')
    for performance_df in performance_df_list:
        line, = plt.plot(performance_df[performance_length][performance_df.index[hist_length:]], label=performance_df['ticker'][performance_df.index[0]], marker='.')
        performance_df['line-color'] = line.get_color()
    maxlim = plt.xlim()[1]
    for performance_df in performance_df_list:
        plt.text(maxlim-0.6, performance_df[performance_length][performance_df.index[-1]], performance_df['ticker'][performance_df.index[0]], size=14, color = performance_df['line-color'][performance_df.index[0]], va='center')
    plt.legend(loc='upper left')
    file_name = (f'{formatted_today}_{performance_length}_{group_title}.png')
    filepath = os.path.join(settings.MEDIA_ROOT, 'images', file_name)
    # plt.savefig(f'./charts/static/charts/images/{file_name}')
    plt.savefig(filepath)
    return file_name
    # plt.show()


def main(ticker_list, group_title, hist_length, interval):
    hist_length = int(hist_length)
    interval = int(interval)
    print('CURRENT WORKING DIRECTORY', os.getcwd())
    perf_data_list = []
    for ticker in ticker_list:
        try:
            performance_data = pd.read_pickle(f'./charts/chart_gen/data/{ticker}_{formatted_today}.pkl')
            # performance_data = pd.read_picker/
            print('File Found')
            # if performance_data['date'][performance_data.index[-1]] < formatted_today:
            #     print('File Outdated')
            #     data = get_data(ticker, formatted_today)
            #     performance_data = get_performance(data)
        except FileNotFoundError:
            logger.warning('FILE Not Found')
            print('File Not Found')
            data = get_data(ticker, formatted_today)
            # print('Downloaded data', data)
            performance_data = get_performance(data)
        finally:
            perf_data_list.append(performance_data)
    #five_days one_month six_months
    img_list = []
    img_list.append(plot_perf(perf_data_list, group_title, hist_length, 'five_days', interval))
    img_list.append(plot_perf(perf_data_list, group_title, hist_length, 'one_month', interval))
    img_list.append(plot_perf(perf_data_list, group_title, hist_length, 'six_months', interval))
    return img_list
    

if __name__ == '__main__':
    sector_group_title = 'SPDR Sectors'
    sector_tickers = ['XLV', 'XLC', 'XLY', 'XLP', 'XLE', 'XLF', 'XLI', 'XLU', 'XLK', 'SMH', 'QQQ', 'SPY']
    mag_group_title = 'Mag 7'
    mag7_tickers = ['AMZN', 'AAPL', 'GOOG', 'META', 'MSFT','NVDA', 'TSLA', 'SPY']
    main(sector_tickers, group_title, 15, 1)
    main(mag7_tickers, group_title, 15, 1)