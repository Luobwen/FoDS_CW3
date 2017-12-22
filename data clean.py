
# coding: utf-8

# In[1]:


import pymongo
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017')


# In[67]:


def clean(collection):
    collection.remove({'$nor':[{'SHRCD':10},{'SHRCD':11}]})
    a=list(collection.aggregate([{'$match':{'$or':[{'PRC':0},{'PRC':''}]}},{'$group':{'_id':'$CUSIP','count':{'$sum':1}}}]))
    cusip=[]
    for i in a:
        print(i)
        t=i['_id']
        cusip.append(t)
    collection.remove({'$or':[{'PRC':0},{'PRC':''}]})
    for t in cusip:
        collection.remove({'CUSIP':t})
    return collection

def temp_insert(collection,ins):
    match={'SICCD':{'$gte':6000,'$lt':6800}}
    temp=collection.find(match)
    ins.insert(temp)
    match={'SICCD':{'$gte':2000,'$lt':5000}}
    temp=collection.find(match)
    ins.insert(temp)


# In[2]:


get_ipython().run_cell_magic('bash', '', '\nmongoimport --db test --collection stock --type csv --headerline --drop --file ./dataset1990-2009/19900101-19901231.csv')


# In[3]:


db = client.test
collection = db.stock


# In[5]:


collection.remove({'$nor':[{'SHRCD':10},{'SHRCD':11}]})


# In[42]:


a=list(collection.aggregate([{'$match':{'$or':[{'PRC':0},{'PRC':''}]}},{'$group':{'_id':'$CUSIP','count':{'$sum':1}}}]))


# In[43]:


for i in a:
    print(i)


# In[32]:


collection.find({'CUSIP':49915810}).count()


# In[44]:


#t=list(collection.find({'CUSIP':49915810,'$or':[{'VOL':0},{'PRC':0},{'PRC':''}]}))
#{'_id': 44981620, 'count': 4}
t=list(collection.find({'CUSIP':44981620,'$or':[{'PRC':0},{'PRC':''}]}))


# In[45]:


for j in t:
    print(j)


# In[47]:


for i in a:
    collection.remove({'CUSIP':i['_id']})


# In[51]:


ins=db.temp1
temp_insert(collection,ins)


# In[52]:


ins.count()


# In[65]:


get_ipython().run_cell_magic('bash', '', '\nmongoimport --db test --collection stock9193 --type csv --headerline --drop --file ./dataset1990-2009/19910101-19931231.csv')


# In[80]:


collection=db.stock9193
clean(collection)


# In[70]:


collection.count()


# In[81]:


ins=db.temp2
temp_insert(collection,ins)


# In[56]:


get_ipython().run_cell_magic('bash', '', '\nmongoimport --db test --collection stock9495 --type csv --headerline --drop --file ./dataset1990-2009/19940101-19951231.csv')


# In[82]:


collection=db.stock9495
clean(collection)


# In[83]:


ins=db.temp2
temp_insert(collection,ins)


# In[76]:


get_ipython().run_cell_magic('bash', '', '\nmongoimport --db test --collection stock9697 --type csv --headerline --drop --file ./dataset1990-2009/19960101-19971231.csv')


# In[84]:


collection=db.stock9697
clean(collection)


# In[85]:


ins=db.temp2
temp_insert(collection,ins)


# In[86]:


get_ipython().run_cell_magic('bash', '', 'mongoexport -d test -c temp2 -f _id,PERMNO,date,SHRCD,EXCHCD,SICCD,COMNAM,SHRCLS,PRIMEXCH,TRDSTAT,SECSTAT,CUSIP,DCLRDT,DLSTCD,DIVAMT,TRTSCD,BIDLO,ASKHI,PRC,VOL,SHROUT,CFACPR,CFACSHR,OPENPRC --type=csv -o ./data9197.csv    ')


# In[ ]:


#已执行
%%bash

mongoimport --db test --collection stock9899 --type csv --headerline --drop --file ./dataset1990-2009/19980101-19991231.csv
mongoimport --db test --collection stock0001 --type csv --headerline --drop --file ./dataset1990-2009/20000101-20011231.csv
mongoimport --db test --collection stock0204 --type csv --headerline --drop --file ./dataset1990-2009/20020101-20041231.csv
mongoimport --db test --collection stock0507 --type csv --headerline --drop --file ./dataset1990-2009/20050101-20071231.csv
mongoimport --db test --collection stock0809 --type csv --headerline --drop --file ./dataset1990-2009/20080101-20091231.csv


# In[87]:


collection=db.stock9899
clean(collection)


# In[88]:


ins=db.temp3
temp_insert(collection,ins)


# In[89]:


collection=db.stock0001
clean(collection)


# In[90]:


ins=db.temp3
temp_insert(collection,ins)


# In[93]:


collection=db.stock0204
clean(collection)


# In[94]:


ins=db.temp3
temp_insert(collection,ins)


# In[95]:


get_ipython().run_cell_magic('bash', '', 'mongoexport -d test -c temp3 -f _id,PERMNO,date,SHRCD,EXCHCD,SICCD,COMNAM,SHRCLS,PRIMEXCH,TRDSTAT,SECSTAT,CUSIP,DCLRDT,DLSTCD,DIVAMT,TRTSCD,BIDLO,ASKHI,PRC,VOL,SHROUT,CFACPR,CFACSHR,OPENPRC --type=csv -o ./data9804.csv    ')


# In[91]:


collection=db.stock0507
clean(collection)


# In[92]:


ins=db.temp4
temp_insert(collection,ins)


# In[96]:


collection=db.stock0809
clean(collection)
ins=db.temp4
temp_insert(collection,ins)


# In[97]:


get_ipython().run_cell_magic('bash', '', 'mongoexport -d test -c temp4 -f _id,PERMNO,date,SHRCD,EXCHCD,SICCD,COMNAM,SHRCLS,PRIMEXCH,TRDSTAT,SECSTAT,CUSIP,DCLRDT,DLSTCD,DIVAMT,TRTSCD,BIDLO,ASKHI,PRC,VOL,SHROUT,CFACPR,CFACSHR,OPENPRC --type=csv -o ./data0509.csv    ')

