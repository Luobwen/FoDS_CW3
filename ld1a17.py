
# coding: utf-8

# In[12]:

from math import log
from math import sqrt
import pandas as pd 
import numpy as np
from pandas import Series,DataFrame

def VE(a):   
    a.OPENPRC = a.OPENPRC.fillna(a.PRC.shift())
    #a.OPENPRC[a.index[0]] = 1
    ve = (np.log(a.ASKHI)-np.log(abs(a.OPENPRC)))*(np.log(a.ASKHI)-np.log(abs(a.PRC)))+(np.log(a.BIDLO)-np.log(abs(a.OPENPRC)))*(np.log(a.BIDLO)-np.log(a.PRC))
   
    return(ve)

def ssd_v(t1, t2):
    # len of one cusip
    l=len(t1)
    ssd=0
    for i in range(l):
        ssd=ssd + (t1[i]-t2[i])**2
    return (ssd)


# # In[16]:

# f3=ssd_v()
# print(f3)


# In[17]:

# function2 = ssd_v()##########################################


# In[18]:

# t1 = VE(df,'12556910')
# t2 = VE(df,'15648910')


# In[19]:

def smd_v(t1, t2):
    npvector1, npvector2 = np.array(t1), np.array(t2)
    npvector = np.array([npvector1, npvector2])
    X = np.linalg.inv(np.cov(t1, t2))
    ma=0
    for i in range(len(npvector.T)):
        Y = npvector.T[i]
        ma = ma + sqrt(np.dot(X, Y).dot(Y.T))
    return (ma)


# In[20]:

# f3=smd_v()
# print(f3)


# In[21]:

# function3 = smd_v()###########################################

