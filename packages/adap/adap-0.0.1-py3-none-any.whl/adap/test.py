import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data1 = pd.DataFrame(np.random.rand(1000, 1) * 1, columns=['a'])
data2 = pd.DataFrame(np.random.rand(100, 1) + 1, columns=['a'])
data3 = pd.DataFrame(np.random.rand(1000, 1) * 1, columns=['a'])
data = pd.concat([data1, data2, data3], ignore_index=True)

def calc_slope(x):
    slope = np.polyfit(range(len(x)), x, 1)[0]
    return slope

# set min_periods=2 to allow subsets less than 60.
# use [4::5] to select the results you need.
data['result'] = data.rolling(25, min_periods=2).apply(calc_slope)
#print(data['result'].head(100))
data.plot()
plt.show()
