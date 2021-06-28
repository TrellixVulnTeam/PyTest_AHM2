# Задача простая — скачать котировки SPY,
# нарисовать график, посчитать число падений close-to-close
# больше 3х процентов за 7 лет.
# https://smart-lab.ru/blog/513608.php
# https://www.youtube.com/watch?v=W8rzwhcMS9Y

from pandas_datareader import data as pdr
from datetime import date as da
from datetime import timedelta as ti
import pandas as pd
import numpy as np
import fix_yahoo_finance as yf
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

shareName = "BNGO"

daysBefore = 60
endDate = da.today()
startDate = endDate - ti(daysBefore)
#startDate = '2021-01-01'
#endDate = da.today()  # '2021-03-15'

# дней   скользящих средних
n1 = 9
n2 = 13
n3 = 56

yf.pdr_override()  # это магия
dt = pdr.get_data_yahoo(shareName, startDate, endDate)  # скачиваем
# print(dt.head(10))  # смотрим первые 10 строк

# построение графика акции
# plt.figure(figsize=(13,8)) #размеры графика
# plt.xlabel(startDate+ " to " + endDate)
# plt.ylabel("Price")
# plt.title("Share: " + shareName)
# plt.plot(data['Adj Close'], label = 'Adj Close Price')
# plt.legend(loc='upper left')
# plt.show()
#

# создание скользящих средних
SMA_1 = pd.DataFrame()  # создание пустого датафрейма
SMA_1['Adj Close'] = dt['Adj Close'].rolling(window=n1).mean()  # среднее арифметическое
SMA_2 = pd.DataFrame()  # создание пустого датафрейма
SMA_2['Adj Close'] = dt['Adj Close'].rolling(window=n2).mean()

EMA_1 = pd.DataFrame()  # создание пустого датафрейма
EMA_1['Adj Close'] = dt['Adj Close'].ewm(span=n1, adjust=False).mean()
EMA_2 = pd.DataFrame()  # создание пустого датафрейма
EMA_2['Adj Close'] = dt['Adj Close'].ewm(span=n2, adjust=False).mean()
EMA_3 = pd.DataFrame()  # создание пустого датафрейма
EMA_3['Adj Close'] = dt['Adj Close'].ewm(span=n3, adjust=False).mean()

# добавление скользящих поверх графика
#plt.figure(figsize=(13, 8))  # размеры графика
#plt.xlabel(str(startDate) + " to " + str(endDate))
#plt.ylabel("Price")
#plt.title("Share: " + shareName)
#plt.plot(dt['Adj Close'], label='Adj Close Price', color='gray')
#plt.plot(EMA_1['Adj Close'], label="EMA " + str(n1), color='red')
#plt.plot(EMA_2['Adj Close'], label="EMA " + str(n2), color='blue')
## plt.plot(EMA_3['Adj Close'], label="EMA " + str(n3), color='green')
## plt.plot(SMA_1['Adj Close'], label="SMA " + str(n1), color='orange')
## plt.plot(SMA_2['Adj Close'], label="SMA " + str(n2), color='green')
#plt.legend(loc='upper left')
#plt.show()

# Алгоритм формирования сигналов
df = pd.DataFrame()
df['Adj Close'] = dt['Adj Close']  # добавляем исходную цену закрытия
df['EMA_1'] = EMA_1['Adj Close']
df['EMA_2'] = EMA_2['Adj Close']


# print(df.head(10))  # смотрим первые 10 строк

# для оценки результата используем флаговую переменную со значениями
# flag -1 = sell    0 = no cross yet   1 = buy
def dual_ema(df):
    # пустые листы в которые алгоритм будет записывать  цены при сигнале
    buy_signal_price = []
    sell_signal_price = []
    flag = 0  # в исходном состоянии пересечения не происходило

    for i in range(len(df)):
        # buy signal - пересечение EMA 1 снизу EMA 2 и после этого EMA1 будет больше EMA2
        if df['EMA_1'][i] > df['EMA_2'][i]:
            # проверяем еще одно условие что равен ли наш флаг 1
            if flag != 1:
                buy_signal_price.append(df['Adj Close'][i])
                # для sell листа вставляем пустые значений
                sell_signal_price.append(np.nan)
                flag = 1
            else: #какое либо из условий не выполняется оставляем пробелы в обеих колонках
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)
        elif df['EMA_1'][i] < df['EMA_2'][i]:
            # проверяем еще одно условие что равен ли наш флаг -1
            if flag != -1:
                sell_signal_price.append(df['Adj Close'][i])
                buy_signal_price.append(np.nan)
                flag = -1
            else:  # какое либо из условий не выполняется оставляем пробелы в обеих колонках
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)
        else:
            buy_signal_price.append(np.nan)
            sell_signal_price.append(np.nan)
    return (buy_signal_price,sell_signal_price)


#сохранение результатов
dual_ema=dual_ema(df)
df['Buy signal price'] = dual_ema[0]
df['Sell signal price'] = dual_ema[1]
print(df)

#визуализация стратегии

plt.figure(figsize=(13, 8))  # размеры графика
plt.xlabel(str(startDate) + " to " + str(endDate))
plt.ylabel("Price")
plt.title("Share: " + shareName)
plt.plot(dt['Adj Close'], label='Adj Close Price', color='gray', linewidth=3)
plt.plot(EMA_1['Adj Close'], label="EMA " + str(n1), color='red', linewidth=2)
plt.plot(EMA_2['Adj Close'], label="EMA " + str(n2), color='blue', linewidth=2)
plt.scatter(df.index, df['Buy signal price'], label = 'buy', color = 'green', marker='^', s=200)
plt.scatter(df.index, df['Sell signal price'], label = 'sell', color = 'red', marker='v', s=200)
plt.legend(loc='upper left')
plt.show()