import pandas as pd
import numpy as np
import math
#增加新列RSI
#sLength = len(df['PRC'])
#df['RSI'] = pd.Series(np.random.randn(sLength), index=df.index)
#将PRC列取正
#df['PRC'] = df['PRC'].abs()


#定义function: get_rsi  计算每只股票的RSI
#def get_rsi(df, cusip):     # df: dataframe    cusip:cusip号
def get_rsi(dt):
    window_length = 14
    #df1 = df[(df['CUSIP']== cusip)]
    closeprice = dt['PRC']    
    delta = closeprice.diff()
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up = pd.rolling_mean(up, window_length)
    roll_down = pd.rolling_mean(down.abs(), window_length)
    RS = (roll_up + 1) / (roll_down + 1)
    RSI = 100.0 - (100.0 / (1.0 + RS))
    return RSI
    #df['RSI'][(df['CUSIP']== cusip)] = RSI
    #return df
#################使用方法###################
# cusip = ['36720410', '05978R10']  #将CUSIP放入列表调用get_rsi循环
# for c in cusip:
    # df = get_rsi(df, c)
####################################




#定义function: 计算两支股票RSI的差的平方和
#def get_sum_of_square_difference_of_rsi(df, cusip_1, cusip_2):    #df:dataframe   cusip_1:股票1代码  cusip_2：股票2代码
def get_sum_of_square_difference_of_rsi(df, rsi1, rsi2):
    #df1 = df[(df['CUSIP']== cusip_1)]
    #rsi1 = df['RSI_x']
    rsi1
    l1 = list(rsi1)
    #df2 = df[(df['CUSIP']== cusip_2)]
    #rsi2 = df['RSI_x']
    rsi2
    l2 = list(rsi2)
    l = len(l1)
    ssd = 0
    for i in range(14, l):
        if (l1[i] != 'nan' and l2[i] != 'nan'):
            ssd += (l1[i] - l2[i])**2
    
    return ssd
#################使用方法###########################
# ssd = get_sum_of_square_difference_of_rsi(df, '36720410', '05978R10')
	
	
#定义function: 计算两支股票RSI的马氏距离
#def get_maha_distance_of_rsi(df, cusip_1, cusip_2):    #df:dataframe   cusip_1:股票1代码  cusip_2：股票2代码
def get_maha_distance_of_rsi(df, rsi1, rsi2):
    #df1 = df[(df['CUSIP']== cusip_1)]
    #rsi1 = df1['RSI']
    l1 = list(rsi1)
    l1 = l1[14:]
    a1 = np.array(l1)

    #df2 = df[(df['CUSIP']== cusip_2)]
    #rsi2 = df2['RSI']
    l2 = list(rsi2)
    l2 = l2[14:]
    a2 = np.array(l2)
    A = np.array([a1, a2])
    #cov
    X = np.cov(a1, a2)
    X = np.mat(X)
    # #mahalanobias distance
    S=0
    for i in range(len(a1)):
        S += math.sqrt(np.dot(X.I, A.T[i]).dot(A.T[i].T))
    return S
####################使用方法########################
# d = get_maha_distance_of_rsi(df, '36720410', '05978R10')
