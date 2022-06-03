#!/usr/bin/env python
# coding: utf-8

# 
# Analysis Task
# 
# To perform these tasks, you can use any of the different Python libraries such as NumPy, SciPy, Pandas, scikit-learn, matplotlib, and BeautifulSoup.
# 
# - Import data into Python environment.
# - Provide the trend chart for the number of complaints at monthly and daily granularity levels.
# - Provide a table with the frequency of complaint types.
# 
# Which complaint types are maximum i.e., around internet, network issues, or across any other domains.
# - Create a new categorical variable with value as Open and Closed. Open & Pending is to be categorized as Open and Closed & Solved is to be categorized as Closed.
# - Provide state wise status of complaints in a stacked bar chart. Use the categorized variable from Q3. Provide insights on:
# 
# Which state has the maximum complaints
# Which state has the highest percentage of unresolved complaints
# - Provide the percentage of complaints resolved till date, which were received through the Internet and customer care calls.
# 
# The analysis results to be provided with insights wherever applicable.

# Importing Libraries and Data into python environment

# In[1]:


import pandas as pd 
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt 
date_fields = [['Date', 'Time']]
comcast_df =pd.read_csv(r"D:\Baldev\Data Science\Python\Project\Comcast_telecom_complaints_data\Comcast_telecom_complaints_data.csv",engine ='python',parse_dates = date_fields, dayfirst = True, keep_date_col = True)


# In[2]:


comcast_df


# In[3]:


comcast_df.head()


# In[4]:


comcast_df.tail()


# In[5]:


comcast_df.describe()


# In[6]:


comcast_df.info()


# In[7]:


comcast_df.columns


# #### Tickets in Daily Granularity 

# In[8]:


comcast_df.insert(loc=3,column='Day',value=comcast_df['Date_Time'].dt.day)


# In[9]:


comcast_df


# In[10]:


comcast_df.insert(loc=4,column='Month',value=comcast_df['Date_Time'].dt.month)


# In[11]:


comcast_df


# In[12]:


plt.style.use('fivethirtyeight')
plt.figure(figsize=(10,5))
byday = comcast_df.groupby('Day').count().reset_index()
lp = sns.lineplot(x= 'Day', y = 'Customer Complaint', data = byday,color="Blue", sort = False, marker = "*", markersize="18")
plt.title('Daily Ticket Count')
ax = lp.axes
plt.show()


# #### Tickets in monthly Granularity  

# In[13]:


bymonth=comcast_df.groupby('Month').count().reset_index()
bymonth


# In[14]:


plt.figure(figsize=(10,5))
lp = sns.lineplot(x= 'Month', y = 'Customer Complaint', data = bymonth,color="Red", sort = True, marker = "*", markersize="18")
plt.title('Monthly Ticket Count')
ax = lp.axes
plt.show()


# #### Frequency of complaint types

# In[15]:


comcast_df['Customer Complaint']= comcast_df['Customer Complaint'].str.lower()
comcast_df


# In[16]:


comcast_df.groupby(['Customer Complaint']).size().sort_values(ascending=False).to_frame().reset_index().rename(columns={0:'Count'})


# #### Creating a new categorical variable  as New_Status with value as Open and Closed. Open & Pending is to be categorized as Open and Closed & Solved is to be categorized as Closed.
# 

# In[64]:


comcast_df.Status.unique()


# In[18]:


comcast_df['Status']
    


# In[19]:


comcast_df['New_Status']= ["Open"if Status == "Pending" or Status == "Open" else 'Closed' for Status in comcast_df['Status']]


# In[20]:


comcast_df


# In[21]:


comcast_df.New_Status.unique()


# #### Provide state wise status of complaints in a stacked bar chart. Use the categorized variable
# 

# In[22]:


comcast_df['State']= comcast_df['State'].str.upper()


# In[23]:


state_wise_complaint=comcast_df.groupby('State').size().sort_values(ascending=False).to_frame().reset_index().rename(columns={0:"Count"})
state_wise_complaint


# In[24]:


state_complaints = pd.crosstab(index = comcast_df['State'],columns=comcast_df["New_Status"],values=comcast_df['New_Status'],aggfunc='count')


# In[25]:


state_complaints.fillna(0,inplace=True)


# In[26]:


state_complaints


# In[27]:


state_complaints['Total']= state_complaints['Closed']+state_complaints['Open']


# #### State wise status of complaints in a stacked bar chart, Where the no. of open,closed and total tickets are shown

# In[28]:


state_complaints


# In[29]:


n= state_complaints.sort_values('Closed',axis=0,ascending=True).plot(kind='barh',figsize= (14,12),width= 1.15)
plt.xlabel("No. of Tickets")


# In[32]:


state_complaints['Unresoleved %age']= state_complaints['Open']/state_complaints['Total']*100


# In[33]:


state_complaints


# #### Finding the state which has the highest percentage of unresolved complaints
# 

# In[48]:


Ticket_Status=comcast_df.groupby(["State","New_Status"]).size().unstack().fillna(0).max()
Ticket_Status


# In[49]:


# Total CLosed and open Tickets
labels = "Closed","Open"
explode = (0.07,0.05)
plt.pie(a,labels=labels,explode=explode,autopct='%1.2f%%')
plt.show()


# In[52]:


Closed_Ticket = comcast_df.groupby(["State","New_Status"]).size().unstack().fillna(0)
Closed_Ticket.sort_values('Closed',axis = 0,ascending=False)[:1]


# In[55]:


Closed_Ticket['Resolved_cmp_prct'] = Closed_Ticket['Closed']/Closed_Ticket['Closed'].sum()*100
Closed_Ticket['Unresolved_cmp_prct'] = Closed_Ticket['Open']/Closed_Ticket['Open'].sum()*100


# In[57]:


# Georgia state has highest Unresolved complaints when compared to other states
Closed_Ticket.sort_values('Unresolved_cmp_prct',axis = 0,ascending=False)[:1]


# #### Provide the percentage of complaints resolved till date, which were received through the Internet and customer care calls
# 

# In[62]:


Complaints_Resolved = comcast_df.groupby(['Received Via','New_Status']).size().unstack().fillna(0)
Complaints_Resolved['resolved'] = Complaints_Resolved['Closed']/Complaints_Resolved['Closed'].sum()*100
P=Complaints_Resolved['resolved']
P


# In[63]:


labels = "Customer Care Call","Internet "
explode = (0.07,0.05)
plt.pie(P,labels=labels,explode=explode,autopct='%1.2f%%')
plt.show()


# #### Project Ends

# In[ ]:




