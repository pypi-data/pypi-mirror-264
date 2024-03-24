# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import chevron
from scipy.stats import kstest

import warnings
warnings.filterwarnings("ignore")
plt.style.use('ggplot')
pd.set_option('max_columns', 200)
pd.set_option('max_rows', 200)
from plotnine import ggplot, aes, geom_line, geom_point, theme, xlab, ylab
import plotly.graph_objects as go

class adap:
    def __init__(self) -> None:
        pass

    def visualize(self, df, tag, timestamp, window=288):
        '''
        This is the main function to return visualization
        '''
        filter_df = df[[tag,timestamp]]
        filter_df[timestamp] = pd.to_datetime(filter_df[timestamp])
        # Preparing data for type A anomaly - Imposible value
        filter_df['anomaly'] = np.where(df[tag] >= 6666, 'Anomaly(Class-A)','Normal')

        # Preparing data for type B anomaly - Constant/low varience values
        filter_df['diff'] = df[tag].diff(1)
        window_size = window
        rolling_zeros = filter_df['diff'].rolling(window=window_size).apply(lambda x: (x == 0).sum(), raw=True)
        # Add the rolling zeros count to the dataframe
        filter_df['Rolling_Zeros_Count'] = rolling_zeros
        filter_df.loc[(filter_df[tag] != 0) & (filter_df['diff']==0) & (filter_df['Rolling_Zeros_Count'] >= window_size), 'anomaly'] = 'Anomaly(Class-B)'

        # Preparing data for type C anomaly - Large suddent spike
        # Calculate sigma and find value above 3 sigmas
        remove_6666 = filter_df.copy()
        remove_6666.loc[(remove_6666[tag] >= 6666), tag] = 0
        sigma = remove_6666[tag].std()
        mean = remove_6666[tag].mean()
        value_above_three_sigma = mean + (sigma * 3)
        filter_df.loc[(filter_df[tag] < 6666) & (sigma > 0) & (filter_df[tag] >= value_above_three_sigma), 'anomaly'] = 'Anomaly(Class-C)'

        # Preparing data for type F/G anomaly - Step Up/ Step down respectively
        def get_slop(x):
            slope = np.polyfit(range(len(x)),x,1)[0]
            return slope
    
        filter_df['slop'] = filter_df[tag].rolling(window, min_periods=2).apply(get_slop)
        slop_mean = filter_df['slop'].mean()
        slop_sd = filter_df['slop'].std()

        ##### NEED TO CALCULATE WITH WINDOW SLIDING
        filter_df.loc[(filter_df['slop'] > (slop_mean + (slop_sd * 5)) ), 'anomaly'] = 'Anomaly(Class-F)'
        filter_df.loc[(filter_df['slop'] > (slop_mean - (slop_sd * 5)) ), 'anomaly'] = 'Anomaly(Class-G)'

        # Preparing data for type E anomaly - Sudden zero
        filter_df.loc[(filter_df[tag] == 0) & (filter_df[tag].diff(1) != 0), 'anomaly'] = 'Anomaly(Class-E)'

        # Preparing data for type D anomaly - Drift
        # Using KS
        def ks(x):
            result = kstest(x, "uniform")
            return result.pvalue
        
        filter_df['ks'] = filter_df[tag].rolling(window).apply(ks)
        # filter_df.loc[(filter_df['ks'] < 0.05 ), 'anomaly'] = 'Anomaly(Class-D)'
        # result = kstest(filter_df[tag], "uniform")
        # print(result)

        # filter_df['ks'].plot()
        # plt.show()

        # Return the visualization
        return ggplot(filter_df) + aes(x=timestamp, y=tag, color='factor(anomaly)') + geom_point() + theme(figure_size=(20, 6)) + ylab(tag)
        return 0

if __name__ == '__main__':
    df = pd.read_csv('../../data/panalytic/data_1008_1_20220716_20240206.csv')
    df['a_c_4000_meters_capacity_slide_cntrl'].dropna(inplace=True)
    algo = adap()
    respose = algo.visualize(df[124800:125000], 'a_c_4000_meters_capacity_slide_cntrl', 'DateTime',12)
    print(respose)