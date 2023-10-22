import pandas as pd


def extract_job_title(body_df, colIdx, colname):
    
    ######### EXTRACT JOB TITLE

    #standardize title column name
    body_df.rename(columns={body_df.columns[colIdx]: colname}, inplace=True)

    #remove rows that don't start with any of the following: 1., 1), 1:, Title, Current title, DE, AE, DA, ETL Dev
    patterns = ["1.", "1)", "1:", "1-", "Title", "Current Title", "Data Engineer", "Data Analyst", "Analytics Engineer", "ETL Developer"]
    filter_condition = ~body_df[colname].str.lower().str.startswith(tuple(pattern.lower() for pattern in patterns))
    body_df.loc[filter_condition] = ""

    # transformed_filtered=body_df.loc[filter_condition]
    # # transformed_filtered.to_csv(path_or_buf="./archive/test_filtered.csv", )
    # print(transformed_filtered.shape)

    #remove numbers like "1.", etc. from the beginning of the string
    body_df[colname] = body_df[colname].str.replace("^[ ]?1[.:)][ ]?","",regex=True)
    body_df[colname] = body_df[colname].str.lower().str.replace("^[ ]?(current)?[ ]?(title)?[ ]?[:]?[ ]","",regex=True)
    #transformed_filtered[colname] = transformed_filtered[colname].str.replace("⁠[ ]?title[:]?[ ]?","", regex=True)
    #transformed_filtered.to_csv(path_or_buf="./archive/test_filtered.csv", )

    #correct some edge cases
    body_df[colname] = body_df[colname].str.replace(".*title:?\s?","", regex=True)
    #strip white spaces
    body_df[colname] = body_df[colname].str.strip()
    body_df[colname] = body_df[colname].str.replace("^de$","data engineer", regex=True)

    return(body_df[colname])