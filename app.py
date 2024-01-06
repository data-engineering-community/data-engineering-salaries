import datetime

import pandas as pd
import numpy as np
import re
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Data Engineering Salaries",
    page_icon=":gear:",
    layout="wide",
    menu_items={
        "Report a bug": "https://github.com/data-engineering-community/data-engineering-salaries/issues/new"
    }
)


# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

def parse_tech_stack(raw: pd.Series) -> pd.DataFrame:
    REMOVE = ['etc','cloud','devops']
    RENAME = {
        'js': 'javascript',
        'k8s': 'kubernetes',
        'azurecloud': 'azure',
        'golang': 'go',
        'googlecloud': 'gcp',
        'oci': 'oracle',
        'postgressql': 'postgres',
        'postgresql': 'postgres',
        'sqlserver': 'mssql',
        'iics': 'informatica',
        'synapse': 'azuresynapse',
        'glue': 'awsglue',
        'lambda': 'awslambda',
        'datafactory': 'azuredatafactory',
        'bq': 'bigquery'
    }
    # remove nulls and strip whitespace
    raw = raw.dropna().str.strip()
    # split the string on commas and other punctuation
    # clean up the whitespace for each segment and remove empty segments
    # take a value count for each segment
    segment_counts = raw.str.split(r'[,\\/\n\.()]', regex=True).explode()\
        .str.strip()\
        .replace(r'\s+',' ', regex=True)\
        .replace('', np.nan)\
        .dropna()\
        .value_counts()\
        .reset_index().set_axis(['raw','cnt'], axis=1)
    # normalize segments by removing whitespace and capitalization
    # so that "MongoDB" and "mongo db" will both become "mongodb"
    # also use our RENAME map to combine acronyms and such
    normalized = segment_counts.raw.str.lower().str.replace(r'\s+','', regex=True).replace(RENAME)
    # combine the segments by that normalized form
    g = segment_counts.groupby(normalized)
    tokens = pd.DataFrame({
        # Use the most common capitalization as the 'title'
        'title': g.raw.apply(lambda n: list(n)[0]),
        'aliases': g.raw.apply(list),
        'cnt': g.cnt.sum(),
    }).query('cnt > 1').drop(index=REMOVE, errors='ignore')
    # Using the token table that we created, search for each alias in each response
    # creating a wide table of boolean values.
    # This will allow for being able to parse tech stack names out of responses
    # that aren't nicely delimited. For example:
    # 
    # input:        | Tech Stack                        |
    #         |-----|-----------------------------------|
    #         |  1  | "We use SQL and sometimes Python" |
    #         |  2  | "python, Azure"                   |
    #
    # output:       | SQL   | Python | Azure |
    #         |-----|-------|--------|-------|
    #         |  1  | True  | True   | False |
    #         |  2  | False | True   | True  |
    #
    wide = pd.DataFrame(index=raw.index)
    for _, token in tokens.iterrows():
        wide[token.title] = False
        for alias in token.aliases:
            # I couldn't surround the tech name with `\b` because apparently 
            # that doesn't work for things like "c#"
            regex = r'(?:^|\s|[\.,()/\\])'\
                + re.escape(alias) \
                + r'(?:$|\s|[\.,()/\\])'
            wide.loc[raw.str.contains(regex, regex=True), token.title] = True
    return wide


salaries_df = load_data(st.secrets["public_gsheets_url"])
salaries_df = salaries_df[["Submitted at", "Current Job Title", "Other", "Years of Experience", "City", "State", "Country", "Work Arrangement",
                           "Base Salary", "Currency", "Bonuses/Equity amount", "Industry", "Tech Stack", "Career plans in the next 3 months?"]]
salaries_df.dropna(how="all", inplace=True)
salaries_df['Submitted at'] = pd.to_datetime(
    salaries_df["Submitted at"]).dt.date
salaries_df.sort_values(by=["Submitted at"], ascending=False, inplace=True)
tech_stack_df = parse_tech_stack(salaries_df['Tech Stack'])
min_yoe = int(salaries_df["Years of Experience"].min())
max_yoe = int(salaries_df["Years of Experience"].max())
today = datetime.date.today()
one_year_ago = datetime.date.today() - datetime.timedelta(days=365)

# Initialize session state variables
# https://docs.streamlit.io/library/advanced-features/session-state#initialization
session_state_variables = [
    "filter_job_title",
    "filter_work_arrangement",
    "filter_industry",
    "filter_tech",
    "filter_city",
    "filter_state",
    "filter_country",
]
for key in session_state_variables:
    if key not in st.session_state:
        st.session_state[key] = ""
if "filter_yoe" not in st.session_state:
    st.session_state["filter_yoe"] = (min_yoe, max_yoe)
if "filter_currency" not in st.session_state:
    st.session_state["filter_currency"] = "USD"

# Create filter lists
job_title_list = [  # Empty string = no filter
    "",
    "Junior Data Engineer",
    "Data Engineer",
    "Senior Data Engineer",
    "Lead Data Engineer",
    "Staff Data Engineer",
    "Principal Data Engineer",
    *list(salaries_df["Other"].unique()),
]
work_arrangement_list = ["", *list(salaries_df["Work Arrangement"].unique())]
industry_list = [
    "", *sorted(list(salaries_df["Industry"].fillna("Unknown").unique()))]
tech_stack_list = [
    "", *tech_stack_df.sum().sort_values(ascending=False).index.tolist(),
]
currency_list = [*sorted(list(salaries_df["Currency"].unique()))]
city_list = [
    "", *sorted(list(salaries_df["City"].fillna("Unknown").unique()))]
state_list = [
    "", *sorted(list(salaries_df["State"].fillna("Unknown").unique()))]
country_list = [
    "", *sorted(list(salaries_df["Country"].fillna("Unknown").unique()))]

# Apply filters if they exist
if st.session_state.filter_job_title:
    salaries_df = salaries_df[
        (salaries_df["Current Job Title"] == st.session_state.filter_job_title)
        | (salaries_df["Other"] == st.session_state.filter_job_title)
    ]
if st.session_state.filter_yoe:
    salaries_df = salaries_df.loc[
        salaries_df["Years of Experience"].between(
            *st.session_state.filter_yoe)
    ]
if st.session_state.filter_work_arrangement:
    salaries_df = salaries_df.loc[
        salaries_df["Work Arrangement"] == st.session_state.filter_work_arrangement
    ]
if st.session_state.filter_industry:
    salaries_df = salaries_df.loc[
        salaries_df["Industry"] == st.session_state.filter_industry
    ]
if st.session_state.filter_tech:
    salaries_df = salaries_df.loc[
        salaries_df.join(tech_stack_df[st.session_state.filter_tech].rename('chosen_tech')).chosen_tech == True
    ]
if st.session_state.filter_currency:
    salaries_df = salaries_df.loc[
        salaries_df["Currency"] == st.session_state.filter_currency
    ]
if st.session_state.filter_city:
    salaries_df = salaries_df.loc[
        salaries_df["City"] == st.session_state.filter_city
    ]
if st.session_state.filter_state:
    salaries_df = salaries_df.loc[
        salaries_df["State"] == st.session_state.filter_state
    ]
if st.session_state.filter_country:
    salaries_df = salaries_df.loc[
        salaries_df["Country"] == st.session_state.filter_country
    ]
if "filter_date_range" not in st.session_state:
    salaries_df = salaries_df.loc[
        salaries_df["Submitted at"].between(one_year_ago, today)
    ]
elif st.session_state.filter_date_range and len(st.session_state.filter_date_range) == 2:
    salaries_df = salaries_df.loc[
        salaries_df["Submitted at"].between(
            *st.session_state.filter_date_range)
    ]

# Print results.
st.header("Data Engineering Salaries", divider="rainbow")

# Represents 2 columns that take 70% and 30% of the screen width respectively
col1, col2 = st.columns(spec=[0.7, 0.3])

with col1:
    salary_histogram = px.histogram(
        data_frame=salaries_df,
        x="Base Salary",
        labels={
            "Base Salary": f"Base Salary ({st.session_state.filter_currency})"}
    )
    st.plotly_chart(salary_histogram, use_container_width=True)

with col2:
    st.metric(label="Median Base Salary", value="{:0,.0f} {currency}".format(
        salaries_df["Base Salary"].median(), currency=st.session_state.filter_currency))
    st.metric(label="Median Bonus/Equity Amount", value="{:0,.0f} {currency}".format(
        salaries_df["Bonuses/Equity amount"].median(), currency=st.session_state.filter_currency))
    st.metric(label="Median Years of Experience",
              value=salaries_df["Years of Experience"].median())

st.dataframe(data=salaries_df, hide_index=True)
st.caption(f"Record count: {salaries_df.shape[0]}")

with st.sidebar:
    st.image("https://raw.githubusercontent.com/data-engineering-community/data-engineering-wiki/main/Assets/logo.svg", width=100)
    st.header("Filters", divider="gray")

    # Filters
    st.date_input(
        label="Date Range",
        value=(one_year_ago, today),
        max_value=datetime.date.today(),
        format="MM/DD/YYYY",
        key="filter_date_range"
    )
    st.selectbox("Job Title", options=job_title_list, key="filter_job_title")
    st.selectbox(
        "Work Arrangement", options=work_arrangement_list, key="filter_work_arrangement"
    )
    st.selectbox("Industry", options=industry_list, key="filter_industry")
    st.slider(
        "Years of Experience",
        min_value=min_yoe,
        max_value=max_yoe,
        step=1,
        key="filter_yoe",
    )
    st.selectbox("Tech Stack", options=tech_stack_list, key="filter_tech")
    st.selectbox("Currency", options=currency_list, key="filter_currency")
    st.selectbox("City", options=city_list, key="filter_city")
    st.selectbox("State", options=state_list, key="filter_state")
    st.selectbox("Country", options=country_list, key="filter_country")

hide_footer_style = """
<style>
footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
