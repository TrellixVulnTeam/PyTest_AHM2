#https://towardsdatascience.com/implementing-macd-in-python-cc9b2280126a
#Implementing MACD in Python

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import pyEX as p

ticker = 'AMD'
timeframe='6m'