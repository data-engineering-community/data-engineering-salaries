import pandas as pd
import streamlit as st


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


salaries_df = load_data(st.secrets["public_gsheets_url"])
salaries_df.drop(columns=["Submission ID", "Respondent ID"], inplace=True)
salaries_df.dropna(how="all", inplace=True)
salaries_df.sort_values(by=["Submitted at"], ascending=False, inplace=True)
min_yoe = int(salaries_df["Years of Experience"].min())
max_yoe = int(salaries_df["Years of Experience"].max())

# Initialize session state variables
# https://docs.streamlit.io/library/advanced-features/session-state#initialization
session_state_variables = [
    "filter_job_title",
    "filter_work_arrangement",
    "filter_industry",
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
industry_list = ["", *sorted(list(salaries_df["Industry"].fillna("Unknown").unique()))]
currency_list = [*sorted(list(salaries_df["Currency"].unique()))]

# Apply filters if they exist
if st.session_state.filter_job_title:
    salaries_df = salaries_df[
        (salaries_df["Current Job Title"] == st.session_state.filter_job_title)
        | (salaries_df["Other"] == st.session_state.filter_job_title)
    ]
if st.session_state.filter_yoe:
    salaries_df = salaries_df.loc[
        salaries_df["Years of Experience"].between(*st.session_state.filter_yoe)
    ]
if st.session_state.filter_work_arrangement:
    salaries_df = salaries_df.loc[
        salaries_df["Work Arrangement"] == st.session_state.filter_work_arrangement
    ]
if st.session_state.filter_industry:
    salaries_df = salaries_df.loc[
        salaries_df["Industry"] == st.session_state.filter_industry
    ]
if st.session_state.filter_currency:
    salaries_df = salaries_df.loc[
        salaries_df["Currency"] == st.session_state.filter_currency
    ]

# Print results.
st.header("Data Engineering Salaries", divider="rainbow")
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Median Base Salary", value="{:0,.0f} {currency}".format(salaries_df["Base Salary"].median(), currency=st.session_state.filter_currency))
col2.metric(label="Median Bonus/Equity Amount", value="{:0,.0f} {currency}".format(salaries_df["Bonuses/Equity amount"].median(), currency=st.session_state.filter_currency))
col3.metric(label="Median Years of Experience", value=salaries_df["Years of Experience"].median())
st.dataframe(data=salaries_df, hide_index=True)
st.caption(f"Record count: {salaries_df.shape[0]}")

with st.sidebar:
    st.image("https://raw.githubusercontent.com/data-engineering-community/data-engineering-wiki/main/Assets/logo.svg", width=100)
    st.header("Filters", divider="gray")

    # Filters
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
    st.selectbox("Currency", options=currency_list, key="filter_currency")

hide_footer_style = """
<style>
footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
