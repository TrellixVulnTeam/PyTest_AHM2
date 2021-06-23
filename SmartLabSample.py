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


shareName = "LEVI"

daysBefore = 360
endDate = da.today()
startDate = endDate- ti(daysBefore)

#дней   скользящих средних
n1 = 9
n2 = 16

yf.pdr_override()  # это магия
dt = pdr.get_data_yahoo(shareName, startDate, endDate)  # скачиваем
#print(dt.head(10))  # смотрим первые 10 строк

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

# добавление скользящих поверх графика
plt.figure(figsize=(13, 8))  # размеры графика
plt.xlabel(str(startDate) + " to " + str(endDate))
plt.ylabel("Price")
plt.title("Share: " + shareName)
plt.plot(dt['Adj Close'], label='Adj Close Price', color='gray')
plt.plot(EMA_1['Adj Close'], label="EMA " + str(n1), color='red')
plt.plot(EMA_2['Adj Close'], label="EMA " + str(n2), color='blue')
#plt.plot(SMA_1['Adj Close'], label="SMA " + str(n1), color='orange')
#plt.plot(SMA_2['Adj Close'], label="SMA " + str(n2), color='green')
plt.legend(loc='upper left')
plt.show()

# Алгоритм формирования сигналов
df = pd.DataFrame()
df['Adj Close'] = dt['Adj Close']  # добавляем исходную цену закрытия
