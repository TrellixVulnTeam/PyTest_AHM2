# Задача простая — скачать котировки SPY,
# нарисовать график, посчитать число падений close-to-close
# больше 3х процентов за 7 лет.
# https://smart-lab.ru/blog/513608.php

from pandas_datareader import data as pdr
import pandas as pd
import numpy as np
import fix_yahoo_finance as yf
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

shareName = "DJI"
startDate = "2021-01-01"
endDate = "2021-06-22"

yf.pdr_override()  # это магия
data = pdr.get_data_yahoo(shareName, startDate, endDate)  # скачиваем
print(data.head(10))  # смотрим первые 10 строк

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
n1 = 9
n2 = 16
SMA_1 = pd.DataFrame()  # создание пустого датафрейма
SMA_1['Adj Close'] = data['Adj Close'].rolling(window=n1).mean()  # среднее арифметическое
SMA_2 = pd.DataFrame()  # создание пустого датафрейма
SMA_2['Adj Close'] = data['Adj Close'].rolling(window=n2).mean()

# добавление скользящих поверх графика
plt.figure(figsize=(13, 8))  # размеры графика
plt.xlabel(startDate + " to " + endDate)
plt.ylabel("Price")
plt.title("Share: " + shareName)
plt.plot(data['Adj Close'], label='Adj Close Price', color='black')
plt.plot(SMA_1['Adj Close'], label="SMA " + str(n1), color='red')
plt.plot(SMA_2['Adj Close'], label="SMA " + str(n2), color='blue')
plt.legend(loc='upper left')
plt.show()

#
