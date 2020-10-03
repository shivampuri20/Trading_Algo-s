import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
start_date ='2016-01-01'
end_date = '2020-01-01'
goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)
#print(goog_data)

# df = pd.DataFrame(goog_data)
# df.to_excel('D:/file.xlsx')

goog_data_signal =pd.DataFrame(index=goog_data.index)
goog_data_signal['price']=goog_data['Adj Close']
goog_data_signal['daily_difference']=goog_data_signal['price'].diff()


goog_data_signal['signal'] = 0.0
goog_data_signal['signal'] = np.where(goog_data_signal['daily_difference'] > 0, 1.0, 0.0)         #we will buy when price is negative[0] and sell when price is postive[1]
goog_data_signal['positions'] = goog_data_signal['signal'].diff()
#print(goog_data_signal.head())

#data visualization
fig=plt.figure()   #defining figure
ax1=fig.add_subplot(111,ylabel= 'google price in $')
goog_data_signal['price'].plot(ax=ax1,color='r',lw=2.)  #plot price within range of days
ax1.plot(goog_data_signal.loc[goog_data_signal.positions==1.0].index,
         goog_data_signal.price[goog_data_signal.positions==1.0],'^',markersize=5,color='m')
ax1.plot(goog_data_signal.loc[goog_data_signal.positions==-1.0].index,
         goog_data_signal.price[goog_data_signal.positions==-1.0],'^',markersize=5,color='k')
#plt.show()


#backtesting
initial_capital =float(1000.0)
positions =pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
portfolio =pd.DataFrame(index=goog_data_signal.index).fillna(0.0)

positions['GOOG']=goog_data_signal['signal']
portfolio['positions']=(positions.multiply(goog_data_signal['price'],axis=0))

portfolio['cash']=initial_capital-(positions.diff().multiply(goog_data_signal['price'],axis=0)).cumsum()
portfolio['total'] = portfolio['positions'] + portfolio['cash']
portfolio.plot()
plt.show()