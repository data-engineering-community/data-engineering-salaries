#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#TODO:
#Add logger & convert print statements to logging
#add comments


# In[39]:


import json
import re


# In[5]:


import pandas as pd
pd.options.display.max_rows = 4000


# In[6]:


f= open("./archive/quarterly_salary_discussion_jun_2023.json", 'r')
json_deserialized = json.load(f)


# In[7]:


print(len(json_deserialized))


# In[9]:


df = pd.json_normalize(json_deserialized[1]["data"], record_path=["children"], max_level=1)


# In[10]:


print(df.head())


# In[11]:


print(df.columns)


# In[12]:


print(df.shape)


# In[69]:


#select columns of interest
transformed_df = df[["data.id","data.author_fullname","data.created","data.body","data.permalink"]]


# In[70]:


#Convert UTC dates
transformed_df["data.created"] = pd.to_datetime(df["data.created"],unit='s')


# In[71]:


#Convert subreddit names to URLs
transformed_df["data.permalink"] = 'https://reddit.com' + df["data.permalink"]


# In[72]:


#replace double newline, carriage return and tab characters
transformed_df["data.body"] = transformed_df["data.body"].str.replace("\n\n","\n")
transformed_df["data.body"] = transformed_df["data.body"].str.replace("\r","")
transformed_df["data.body"] = transformed_df["data.body"].str.replace("\t","")


# In[75]:


#Split on newline character and save as new df
transformed_df_copy = transformed_df
transformed_df_body = transformed_df["data.body"].str.split('\n',expand=True)


# In[76]:


#drop extra column
#transformed_df = transformed_df.drop(labels='data.body', axis=1)
#print(transformed_df.shape)


# In[ ]:


######### EXTRACT JOB TITLE


# In[77]:


#standardize title column name
transformed_df_body.rename(columns={transformed_df_body.columns[0]: 'data.title'}, inplace=True)


# In[79]:


#remove rows that don't start with any of the following: 1., 1), 1:, Title, Current title, DE, AE, DA, ETL Dev
patterns = ["1.", "1)", "1:", "1-", "Title", "Current Title", "Data Engineer", "Data Analyst", "Analytics Engineer", "ETL Developer"]
filter_condition = ~transformed_df_body["data.title"].str.lower().str.startswith(tuple(pattern.lower() for pattern in patterns))
transformed_df_body.loc[filter_condition] = ""

# transformed_filtered=transformed_df_body.loc[filter_condition]
# # transformed_filtered.to_csv(path_or_buf="./archive/test_filtered.csv", )
# print(transformed_filtered.shape)


# In[81]:


#remove unnecessary strings like "1.", etc. from the beginning of the job title column values
transformed_df_body["data.title"] = transformed_df_body["data.title"].str.replace("^[ ]?1[.:)][ ]?","",regex=True)
transformed_df_body["data.title"] = transformed_df_body["data.title"].str.lower().str.replace("^[ ]?(current)?[ ]?(title)?[ ]?[:]?[ ]","",regex=True)
#transformed_filtered["data.title"] = transformed_filtered["data.title"].str.replace("⁠[ ]?title[:]?[ ]?","", regex=True)
#transformed_filtered.to_csv(path_or_buf="./archive/test_filtered.csv", )


# In[83]:


#correct some edge cases
transformed_df_body["data.title"] = transformed_df_body["data.title"].str.replace(".*title:?\s?","", regex=True)
#strip white spaces
transformed_df_body["data.title"] = transformed_df_body["data.title"].str.strip()
transformed_df_body["data.title"] = transformed_df_body["data.title"].str.replace("^de$","data engineer", regex=True)
transformed_df_body


# In[93]:


#Attach title column to original df
transformed_df2 = pd.concat([transformed_df, transformed_df_body['data.title']], axis=1)

