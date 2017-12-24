
# coding: utf-8

# #### Download data by
# wget https://s3.amazonaws.com/datasciencegroupcoursework/clean+data/data6270.csv

# In[ ]:

import datetime
import importlib as imlib
import numpy as np
import pandas as pd
import pdb
import re

import RSI as Lau
import ld1a17 as Dua
import dr_turnover_tao as Tao

from numpy import nan
from itertools import combinations
    
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
    
    a['RTN'] = daily_return(a)
    b['RTN'] = daily_return(b)
    a['Vola'] = ld1a17.VE(a)
    b['Vola'] = ld1a17.VE(b)
    a['TNOV'] = dr_turnover_tao.turnover(a)
    b['TNOV'] = dr_turnover_tao.turnover(b)
    a['RSI'] = Lau.get_rsi(a)
    b['RSI'] = Lau.get_rsi(b)
    
    
    merge_col = ['DATE','YYYYMM','PRC', 'RTN', 'Vola', 'VOL', 'TNOV', 'RSI']
    c = pd.merge(a[merge_col], b[merge_col], on = ['DATE','YYYYMM'])
    c = c.sort_values(['DATE']).reset_index(drop=True)

    mt = sorted(list(set(c.YYYYMM)))
    for mn in mt[11:len(mt)-6]:
        d = c[c.YYYYMM <= mn]
        e = c[(c.YYYYMM > mn) & (c.YYYYMM <= str(int(mn[0:4]) + int((6 + int(mn[4:6]))/12)) + str((6 + int(mn[4:6]))%12).zfill(2))]

        std2 = std_of_his_sprd(d.PRC_x, d.PRC_y)
        rtn, cnt, days = pair_trading(e, std2)
        pos_pairs = pos_pairs.append({'Stock1':88311810, 'Stock2':48273410, 'YYYYMM': mn, 'SSD_P': sum_sqr_diff_prc(d.PRC_x, d.PRC_y), 'MHD_P': sum_mah_diff_prc(d.PRC_x, d.PRC_y), 'Std2':std2, 'RTN':rtn, 'CNT':cnt, 'DAYS':days, 'SSD_V': Dua.ssd_v(d.Vola_x, d.Vola_y), 'MHD_V': Dua.smd_v(d.Vola_x, d.Vola_y), 'SSD_T': Tao.ssd_t(d.Vola_x, d.Vola_y), 'MHD_T': Tao.ssd_t(d.TNOV_x, d.TNOV_y),'SSD_R':Lau.get_sum_of_square_difference_of_rsi(d, d.RSI_x, d.RSI_y), 'MHD_R':Lau.get_maha_distance_of_rsi(d, d.RSI_x, d.RSI_y)}, ignore_index=True)
    
    return(pos_pairs)


# In[ ]:

dt = pd.read_csv('data6270.csv', dtype = {'PERMNO':np.object, 'COMNAM':np.object, 'SHRCD':np.object, 'SICCD':np.object, 'SECSTAT':np.object})


# In[ ]:

dt.PRC = abs(dt.PRC)
dt['DATE'] = dt.date.apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
dt['YYYYMM'] = dt.DATE.apply(lambda x: datetime.datetime.strftime (x, '%Y%m'))
#dt[0:5]


# In[ ]:

cl_list1 = pd.read_table('data+clean+1962-1989.txt', dtype={'#1962': object})
cl_list2 = pd.read_table('data+clean+1990-2009.txt', dtype={'#1990': object})

cl_list1 = cl_list1['#1962'].str.extract(":\s'?(\d.*\d)'?,").astype(str)
cl_list = cl_list1.append(cl_list2['#1990'].str.extract(":\s'?(\d.*\d)'?,").astype(str))


# In[ ]:

# List of stocks
stocks = list(set(dt.CUSIP) - set(cl_list))
pt = pd.DataFrame(columns = cols)
for comb in list(combinations(stocks[0:5], 2)):
    pt = pt.append(pairs(comb[0], comb[1], dt))
    
pt = pt.reindex
pt.to_csv('pairs.csv', sep = ',')


# In[ ]:

#store = HDFStore('store.h5')
#store['pairs'] = pt  # save it
#store['df']  # load it


# In[ ]:



