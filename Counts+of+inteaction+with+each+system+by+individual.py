
# coding: utf-8

# In[1]:

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:

with open('datapath.txt', 'r') as f:
    datapath = f.readlines()[0].strip()


# In[22]:

cyf_path = 'CYF Active 2010 to 2016-11-09(1).csv'


# In[30]:

cyf = pd.read_csv(datapath + cyf_path, usecols=['MCI_ID'])


# In[9]:

homeless_path = 'HomelessShelters(1).csv'


# In[10]:

get_ipython().magic(u'ls $datapath')


# In[11]:

behavioral_path = 'Behavioral Health Services.csv'


# In[12]:

placement_path = 'rp_placements_clean.csv'


# In[35]:

homeless = pd.read_csv(datapath + homeless_path, usecols=['MCI_ID_OR_HMIS_CLIENT_ID'])
behavioral = pd.read_csv(datapath + behavioral_path, usecols=['MCI_UNIQ_ID'])
placement = pd.read_csv(datapath + placement_path, usecols=['MCI_ID'])


# In[32]:

datasets = [homeless, behavioral, placement, cyf]


# In[75]:

for i in range(len(datasets)):
    datasets[i] = datasets[i][datasets[i][datasets[i].columns[0]] >= 1e9]


# In[78]:

counts = [i.groupby(i[i.columns[0]])[i.columns[0]].count() for i in datasets]


# In[79]:

count_names = ['N_HOMELESS', "N_BEHAVIORAL", "N_PLACEMENTS", "N_CYF"]


# In[80]:

for i in range(len(counts)):
    counts[i].name = count_names[i] 


# In[82]:

homeless['IN_HOMELESS'] = 1
behavioral['IN_BEHAVIORAL'] = 1
placement['IN_PLACEMENT'] = 1
cyf['IN_CYF'] = 1


# In[83]:

homeless.drop_duplicates(subset=['MCI_ID_OR_HMIS_CLIENT_ID'], inplace=True)
behavioral.drop_duplicates(subset=['MCI_UNIQ_ID'], inplace=True)
placement.drop_duplicates(subset=['MCI_ID'], inplace=True)
cyf.drop_duplicates(subset=['MCI_ID'], inplace=True)


# In[99]:

all_datasets = pd.DataFrame()
for i in counts:
    all_datasets = all_datasets.join(i, how='outer')


# In[101]:

all_datasets.dropna().index.to_series().to_csv('MCI_IDS_in_all_systems.csv', index=False)


# In[92]:

all_datasets.fillna(0, inplace=True)


# In[102]:

all_datasets.to_csv('Number_of_interactions_by_MCI_ID.csv')


# In[ ]:



