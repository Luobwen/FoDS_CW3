
# coding: utf-8

# #### Download data by
# ###### SIC: SIC Code 20-39 - Manufacturing
# ###### SIC: SIC Code 40-49 - Transportation & Public Utilities
# ###### SIC: SIC Code 60-67 - Finance, Insurance, Real Estate
# 
# wget https://s3.amazonaws.com/datasciencegroupcoursework/clean+data/data6270.csv

# In[1]:

import datetime
import importlib as imlib
import numpy as np
import os
import pandas as pd
import pdb
import re

import RSI as Lau
import ld1a17 as Dua
import dr_turnover_tao as Tao

from numpy import nan
from itertools import combinations, takewhile
    
# Sum square difference of normalized price
def sum_sqr_diff_prc(prc1, prc2):
    prc1 = (prc1 - np.mean(prc1))/np.std(prc1)
    prc2 = (prc2 - np.mean(prc2))/np.std(prc2)
    if len(prc1) != len(prc2):
        return('Return length unequal.')
    else:
        return(sum((prc1 - prc2) ** 2))
    
def std_of_his_sprd(prc1, prc2):
    prc1 = (prc1 - np.mean(prc1))/np.std(prc1)
    prc2 = (prc2 - np.mean(prc2))/np.std(prc2)
    
    return(2 * np.std(prc1 - prc2))
    
# Sum square difference
def sum_mah_diff_prc(prc1, prc2):
    prc1 = (prc1 - np.mean(prc1))/np.std(prc1)
    prc2 = (prc2 - np.mean(prc2))/np.std(prc2)    
    if len(prc1) != len(prc2):
        return('Return length unequal.')
    else:
        cv = np.cov(prc1, prc2)
        
        return(sum(cv[0][0] * prc1 ** 2 + cv[0][1] * prc1 * prc2 + cv[1][1] * prc2 ** 2))
    
# Daily Return
def daily_return(st):
    st.DIVAMT[np.isnan(st.DIVAMT)] = 0    
    
    rtn = (st.PRC * (st.SHROUT/st.SHROUT.shift()) + st.DIVAMT) / st.PRC.shift() - 1
    rtn[np.isnan(rtn)] = 0
    
    return(rtn) 

def pair_trading(c, std2):
    c['Spread'] = (c.PRC_y - np.mean(c.PRC_y))/np.std(c.PRC_y) - (c.PRC_x - np.mean(c.PRC_x))/np.std(c.PRC_x)
    hold = 0
    prp_val = 1.0
    tr_ct = 0
    tr_dy = 0
    
    #pdb.set_trace()
    for index, row in c.iterrows():
        if (abs(hold) == 1):
            if (c.loc[index, 'Spread'] * c.loc[index-1, 'Spread'] < 0):
                hold = 0   
        
        if (abs(row['Spread']) >= std2) & (hold == 0):
            tr_ct = tr_ct + 1
            if (row['PRC_y'] > row['PRC_x']):
                hold = 1
            else:
                hold = -1

        if(hold == 1) :
            tr_dy = tr_dy + 1
            prp_val = prp_val * (1 + row['RTN_x']-row['RTN_y'])
        elif(hold == -1) :
            tr_dy = tr_dy + 1
            prp_val = prp_val * (1 + row['RTN_y']-row['RTN_x'])
    
    return prp_val, tr_ct, tr_dy


def pairs(cusip1, cusip2, dt):
    cols = ['Stock1', 'Stock2', 'YYYYMM', 'SSD_P', 'MHD_P', 'Std2', 'RTN', 'CNT', 'DAYS','SSD_V', 'MHD_V','SSD_T', 'MHD_T','SSD_R', 'MHD_R']
    pos_pairs = pd.DataFrame(columns = cols)
    
    im_cols = ['DATE','YYYYMM','PRC', 'SHROUT', 'DIVAMT', 'OPENPRC', 'ASKHI', 'BIDLO', 'VOL']
    a = dt[im_cols][dt.CUSIP == cusip1]
    b = dt[im_cols][dt.CUSIP == cusip2]

    strt = max(min(a.DATE), min(b.DATE))
    end = min(max(a.DATE), max(b.DATE))

    a = a[(a.DATE >= strt) & (a.DATE <= end)]
    b = b[(b.DATE >= strt) & (b.DATE <= end)]
    
    a = a.sort_values(['DATE']).reset_index(drop=True)
    b = b.sort_values(['DATE']).reset_index(drop=True)
    
    a['RTN'] = daily_return(a)
    b['RTN'] = daily_return(b)
    a['Vola'] = Dua.VE(a)
    b['Vola'] = Dua.VE(b)
    a['TNOV'] = Tao.turnover(a)
    b['TNOV'] = Tao.turnover(b)
    a['RSI'] = Lau.get_rsi(a)
    b['RSI'] = Lau.get_rsi(b)
    #pdb.set_trace()
    
    merge_col = ['DATE','YYYYMM','PRC', 'RTN', 'Vola', 'VOL', 'TNOV', 'RSI']
    c = pd.merge(a[merge_col], b[merge_col], on = ['DATE','YYYYMM'])
    c = c.fillna(0)
    #pdb.set_trace()

    mt = sorted(list(set(c.YYYYMM)))
    for mn in mt[11:len(mt)-6]:
        d = c[c.YYYYMM <= mn]
        e = c[(c.YYYYMM > mn) & (c.YYYYMM <= str(int(mn[0:4]) + int((6 + int(mn[4:6]))/12)) + str((6 + int(mn[4:6]))%12).zfill(2))]

        std2 = std_of_his_sprd(d.PRC_x, d.PRC_y)
        rtn, cnt, days = pair_trading(e, std2)
        pos_pairs = pos_pairs.append({'Stock1':cusip1, 'Stock2':cusip2, 'YYYYMM': mn, 'SSD_P': sum_sqr_diff_prc(d.PRC_x, d.PRC_y), 'MHD_P': sum_mah_diff_prc(d.PRC_x, d.PRC_y), 'Std2':std2, 'RTN':rtn, 'CNT':cnt, 'DAYS':days, 'SSD_V': Dua.ssd_v(d.Vola_x, d.Vola_y), 'MHD_V': Dua.smd_v(d.Vola_x, d.Vola_y), 'SSD_T': Tao.ssd_t(d.TNOV_x, d.TNOV_y), 'MHD_T': Tao.smd_t(d.TNOV_x, d.TNOV_y),'SSD_R':Lau.get_sum_of_square_difference_of_rsi(d, d.RSI_x, d.RSI_y), 'MHD_R':Lau.get_maha_distance_of_rsi(d, d.RSI_x, d.RSI_y)}, ignore_index=True)
    
    return(pos_pairs)


# In[2]:

filelist = []

for dirname, dirnames, filenames in os.walk('.'):
    for file in filenames:
        if(re.match(r'^data[09][0-9][09][0-9].csv$', file)):
            filelist.append(file)


# In[3]:

cl_list1 = pd.read_table('data+clean+1962-1989.txt', dtype={'#1962': object})
cl_list2 = pd.read_table('data+clean+1990-2009.txt', dtype={'#1990': object})

cl_list1 = cl_list1['#1962'].str.extract(":\s'?(\d.*\d)'?,").astype(str)
cl_list = cl_list1.append(cl_list2['#1990'].str.extract(":\s'?(\d.*\d)'?,").astype(str))


# In[4]:

stock_len = pd.Series()
for file in filelist:
    dt = pd.read_csv(file, usecols=['date', 'SICCD', 'CUSIP'], dtype = {'SICCD':np.object})
    #dt = dt[(dt.SICCD.str.contains('^6[0-7]'))]
    
    
    stock_len = stock_len.append(dt.groupby(['CUSIP']).size())
    print('Appending completed.')
        
stocks = list(stock_len.sort_values(ascending=False)[0:100].index)


# In[5]:

dt_fin = pd.DataFrame()
for file in filelist:
    dt = pd.read_csv(file, usecols = ['CUSIP', 'date','PRC', 'SHROUT', 'DIVAMT', 'OPENPRC', 'ASKHI', 'BIDLO', 'VOL'], dtype = {'CUSIP':np.object})
    dt_fin = dt_fin.append(dt[dt['CUSIP'].isin(stocks)])


# In[6]:

#dt_Fin = pd.read_csv('fin_stocks.csv')
#dt_Fin = dt[(dt.SICCD.str.contains('^6[0-7]'))]
#dt_Fin = dt[(dt.SICCD.str.contains('^4[0-9]'))]
#dt_Fin = dt[(dt.SICCD.str.contains('^[2-3][0-9]'))]

dt_fin.PRC = abs(dt_fin.PRC)
dt_fin['DATE'] =dt_fin.date.apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
dt_fin['YYYYMM'] = dt_fin.DATE.apply(lambda x: datetime.datetime.strftime (x, '%Y%m'))
#dt[0:5]


# In[7]:

#imlib.reload(Tao)
pairtrades = pd.DataFrame(columns = ['Stock1', 'Stock2', 'YYYYMM', 'SSD_P', 'MHD_P', 'Std2', 'RTN', 'CNT', 'DAYS','SSD_V', 'MHD_V','SSD_T', 'MHD_T','SSD_R', 'MHD_R'])
#with open('pairs_Fin.csv', 'a') as f:
    #pairtrades.to_csv(f, header=True)
    
df = pd.read_csv('pairs_Fin.csv', usecols = [1, 2], names = ["Stock1", "Stock2"], dtype = {1:np.object, 2:np.object})
combs = list(set(combinations(stocks, 2)) - set(list(zip(df.Stock1, df.Stock2))))
    
#pairtrades = pairtrades.reindex()
#pairtrades.to_csv('pairs.csv', sep = ',')


# In[18]:

for comb in combs:
    pairtrades = pairs(comb[0], comb[1], dt_fin)
    # pdb.set_trace()
    with open('pairs_Fin.csv', 'a') as f:
        pairtrades.to_csv(f, header=False)


# ##### Test

# In[ ]:

dt_Fin = dt_Fin[['CUSIP', 'date', 'PRC', 'SHROUT', 'DIVAMT', 'OPENPRC', 'ASKHI', 'BIDLO', 'VOL']]

dt_Fin.PRC = abs(dt_Fin.PRC)
dt_Fin['DATE'] =dt_Fin.date.apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
dt_Fin['YYYYMM'] = dt_Fin.DATE.apply(lambda x: datetime.datetime.strftime (x, '%Y%m'))

cl_list1 = pd.read_table('data+clean+1962-1989.txt', dtype={'#1962': object})
cl_list2 = pd.read_table('data+clean+1990-2009.txt', dtype={'#1990': object})

cl_list1 = cl_list1['#1962'].str.extract(":\s'?(\d.*\d)'?,").astype(str)
cl_list = cl_list1.append(cl_list2['#1990'].str.extract(":\s'?(\d.*\d)'?,").astype(str))
# List of stocks
stocks = list(set(dt_Fin.CUSIP) - set(cl_list))
stock_len = dt_Fin[dt_Fin.CUSIP.isin(stocks)].groupby(['CUSIP']).size()
stocks = list(stock_len.sort_values(ascending=False)[0:100].index)


# In[ ]:

stock_len = dt_Fin[dt_Fin.CUSIP.isin(stocks)].groupby(['CUSIP']).size()
stock_len = stock_len.sort_values(ascending=False)


# In[ ]:

stocks = list(stock_len.sort_values(ascending=False)[0:100].index)


# In[ ]:

dt = pd.read_csv(filelist[0], usecols=['date', 'SICCD', 'CUSIP'])


# In[ ]:

dt.info()


# In[ ]:

for file in filelist:
    dt = pd.read_csv(file, usecols=['date', 'SICCD', 'CUSIP'])
    with open('list_stocks.csv', 'a') as f:
        dt.to_csv(f, header=True)
        print('Appending completed.')


# In[ ]:

dt_Fin = pd.read_csv('list_stocks.csv')
dt_Fin = dt_Fin[(dt_Fin.SICCD.str.contains('^6[0-7]', na=False))]
stocks = list(set(dt_Fin.CUSIP) - set(cl_list))
stock_len = dt_Fin[dt_Fin.CUSIP.isin(stocks)].groupby(['CUSIP']).size()
stocks = list(stock_len.sort_values(ascending=False)[0:100].index)


# In[ ]:

# List of stocks
stocks = list(set(dt_Fin.CUSIP) - set(cl_list))
stock_len = dt_Fin[dt_Fin.CUSIP.isin(stocks)].groupby(['CUSIP']).size()
stocks = list(stock_len.sort_values(ascending=False)[0:100].index)

len(list(combinations(stocks, 2)))

