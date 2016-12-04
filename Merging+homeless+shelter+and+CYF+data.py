
# coding: utf-8

# This file merges together homeless shelter data and the children, youth, and families demographic data. It generates an event-level dataset for the homeless shelter data, with the children, youth, and families demographic data added in.
# 
# I then create a few visualizations to help understand this data.

# In[1]:

from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:

with open('datapath.txt', 'r') as f:
    datapath = f.readlines()[0].strip()


# In[3]:

foster_care_path = 'CYF Active 2010 to 2016-11-09(1).csv'


# In[4]:

foster_care = pd.read_csv(datapath + foster_care_path)


# In[5]:

homeless_path = 'HomelessShelters(1).csv'


# In[6]:

homeless = pd.read_csv(datapath + homeless_path)


# Drop CL_ID, should be redundent. Maybe could help merge with other datasets?

# In[7]:

foster_care.drop('CL_ID', axis=1, inplace=True)


# A bunch of the MCI_ID are zero. This seems to be a wastebasket MCI id

# In[8]:

foster_care[foster_care['MCI_ID'] == 0].shape


# In[9]:

foster_care = foster_care[foster_care['MCI_ID'] > 0.0]


# Data dictionary says "Ignore IDs that are less than 10 digits -- those are source system and you will not be able to link". I'm just dropping them.

# In[10]:

homeless = homeless[homeless['MCI_ID_OR_HMIS_CLIENT_ID'] >= 1e9]


# ### Merging in demographic info 

# The demographic columns (Birth date, gender, and race) are individual specific and consistent for each entry of the individual. That info is really easy to merge.

# In[11]:

demographic_col = [u'BRTH_DT', u'GENDER', u'RACE']


# This is an individual-based table of the three demographic factors.

# In[12]:

demo_lookup = pd.DataFrame([foster_care.groupby('MCI_ID')[i].unique().map(lambda x: x[0])
                            for i in demographic_col], index=demographic_col).T #There has to be a more pythonic way of doing this


# I did an inner join, so I'm going to just have the people that have interacted both with CYF and the shelter system.
# 
# This creates a homeless event level dataframe.

# In[13]:

homeless_joined = homeless.join(demo_lookup, on='MCI_ID_OR_HMIS_CLIENT_ID', how='inner')


# I didn't convert the dates yet...

# In[14]:

dt_episode_start = pd.to_datetime(homeless_joined['PROJ_INVOLVEMENT_EPISODE_START'], errors='coerce')
dt_birth_date = pd.to_datetime(homeless_joined['BRTH_DT'], errors='coerce')


# And now I can find the age in years when the homeless episode started.

# In[15]:

homeless_joined['age_at_episode_start'] = ((dt_episode_start
                                     - dt_birth_date).dt.days / 365)


# In[16]:

homeless_joined['GENDER'].unique()


# In[17]:

homeless.groupby('HUD_PROJECT_TYPE')['PROJ_INVOLVEMENT_EPISODE_START'].count() / homeless.shape[0]


# In[18]:

homeless_joined.groupby('HUD_PROJECT_TYPE')['PROJ_INVOLVEMENT_EPISODE_START'].count() / homeless_joined.shape[0]


# In[19]:

homeless_joined['HUD_PROJECT_TYPE'].unique()


# In[56]:


females = homeless_joined[homeless_joined['GENDER'] == 'Female']
males = homeless_joined[homeless_joined['GENDER'] == 'Male']
plt.hist([males['age_at_episode_start'].dropna(),
          females['age_at_episode_start'].dropna()],
         color=['blue', 'red'], label=['male', 'female'],
         stacked=True, bins=50, alpha=0.5)
plt.xlabel('age at episode start')
plt.ylabel('number of episodes')
title = 'Histogram of age at start of homelessness episode by gender'
plt.title(title)
plt.legend(loc='upper right')
#plt.savefig(title.strip() + '.png')
plt.show()


# In[21]:

young = homeless_joined[homeless_joined['age_at_episode_start'] <= 24.0]
females = young[young['GENDER'] == 'Female']
males = young[young['GENDER'] == 'Male']
plt.hist([males['age_at_episode_start'].dropna(),
          females['age_at_episode_start'].dropna()],
         color=['blue', 'red'], label=['male', 'female'],
         stacked=True, bins=50, alpha=0.5)
plt.xlabel('age at episode start')
plt.ylabel('number of episodes')
title = 'Histogram of youth at start of homelessness episode by gender'
plt.title(title)
plt.legend(loc='upper right')
plt.savefig(title.strip() + '.png')
plt.show()


# In[71]:

pd.to_datetime(not_cyf_homeless['PROJ_INVOLVEMENT_EPISODE_START'], errors='coerce').describe()


# In[72]:

pd.to_datetime(homeless_joined['PROJ_INVOLVEMENT_EPISODE_START'], errors='coerce').describe()


# In[66]:

not_cyf_homeless.groupby('HUD_PROJECT_TYPE')['PROJ_INVOLVEMENT_EPISODE_START'].count() / not_cyf_homeless.shape[0]


# In[ ]:



