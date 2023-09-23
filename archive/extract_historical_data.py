# This script is a work in progress. Please feel free to use it as a starting point.
import json

import pandas as pd

# Testing with one file to start
with open("./quarterly_salary_discussion_jun_2023.json", 'r') as f:
    json_deserialized = json.load(f)
    print(len(json_deserialized))
    df = pd.json_normalize(json_deserialized[1]["data"], record_path=["children"], max_level=1)
    print(df.head())
    print(df.columns)
    print(df.shape)
    transformed_df = df[["data.id","data.author_fullname","data.created","data.body","data.permalink"]]
    transformed_df["data.created"] = pd.to_datetime(df["data.created"],unit='s')
    transformed_df["data.permalink"] = 'https://reddit.com' + df["data.permalink"]
    transformed_df.rename(columns={"data.id": "comment_id", "data.author_fullname": "submitter_id", "data.created": "submitted_at", "data.body": "comment_body", "data.permalink": "source"}, inplace=True)
    print(transformed_df.head())
