import pandas as pd


def extract_job_title(body_df, colIdx, colname):
    """
    Takes the body of the comments in the form of a pandas df and the column index of column containing job title info, 
    renames the column to the "colname" variable, and returns job title information. body_df, colIdx, colname are all required variables.
    """
    ######### EXTRACT JOB TITLE

    #standardize title column name
    body_df.rename(columns={body_df.columns[colIdx]: colname}, inplace=True)

    #remove rows that don't start with any of the following: 1., 1), 1:, Title, Current title, DE, AE, DA, ETL Dev
    patterns = ["1.", "1)", "1:", "1-", "Title", "Current Title", "Data Engineer", "Data Analyst", "Analytics Engineer", "ETL Developer"]
    filter_condition = ~body_df[colname].str.lower().str.startswith(tuple(pattern.lower() for pattern in patterns))
    body_df.loc[filter_condition] = ""

    #remove numbers like "1.", etc. from the beginning of the string
    body_df[colname] = body_df[colname].str.replace("^[ ]?1[.:)][ ]?","",regex=True)
    body_df[colname] = body_df[colname].str.lower().str.replace("^[ ]?(current)?[ ]?(title)?[ ]?[:]?[ ]","",regex=True)

    #correct some edge cases
    body_df[colname] = body_df[colname].str.replace(".*title:?\s?","", regex=True)
    #strip white spaces
    body_df[colname] = body_df[colname].str.strip()
    body_df[colname] = body_df[colname].str.replace("^de$","data engineer", regex=True)

    return(body_df[colname])