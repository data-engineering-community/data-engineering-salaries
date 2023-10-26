#!/usr/bin/env python

import os
import json
import re
import pandas as pd
import importlib
job_title = importlib.import_module("job_title", package=None)

#dir path of input json files
input_dir = './archive'
json_files = []
final_df = pd.DataFrame()

#list all json in input dir
for file in os.listdir(input_dir):
    if file.endswith(".json"):
        json_files.append(os.path.join(input_dir, file))

for file in json_files:
    #open & load json
    print(f"Opening json file {file}")
    f = open(file, 'r')
    json_deserialized = json.load(f)
    print(f'Length of json is {len(json_deserialized)}')

    #convert json to pandas df
    print("Converting json to pandas df")
    df = pd.json_normalize(json_deserialized[1]["data"], record_path=["children"], max_level=1)
    print(f'These are the df columns before selecting columns of interest: {df.columns}')
    print(f'These are the df dimensions before selecting columns of interest: {df.shape}')

    #select columns of interest
    print("Selecting columns of interest")
    transformed_df = df[["data.id","data.author_fullname","data.created","data.body","data.permalink"]]

    #Convert UTC dates
    print("Converting UTC dates")
    transformed_df["data.created"] = pd.to_datetime(df["data.created"],unit='s')

    #Convert subreddit names to URLs
    print("Converting subreddit URLs")
    transformed_df["data.permalink"] = 'https://reddit.com' + df["data.permalink"]

    #replace double newline, carriage return and tab characters
    print("Replacing special characters")
    transformed_df['data.body']=transformed_df['data.body'].str.replace("^\n","",regex=True)
    transformed_df["data.body"] = transformed_df["data.body"].str.replace("\n\n","\n")
    transformed_df["data.body"] = transformed_df["data.body"].str.replace("\r","")
    transformed_df["data.body"] = transformed_df["data.body"].str.replace("\t","")

    #Split on newline character and save as new df
    print("Splitting body column")
    transformed_df_copy = transformed_df
    transformed_df_body = transformed_df["data.body"].str.split('\n',expand=True, regex=True)

    #Extract job title info
    print("Extracting job title info")
    job_title_df = job_title.extract_job_title(body_df=transformed_df_body, colIdx=0, colname='data.title')
    transformed_df2 = pd.concat([transformed_df, job_title_df], axis=1)
    final_df = final_df.append(transformed_df2)

    #TODO: Extract YOE

    #TODO: Extract location

#write to file
print("Writing to file")
final_df.to_csv(path_or_buf=input_dir+"/historical_data.csv")
