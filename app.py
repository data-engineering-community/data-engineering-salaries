import pandas as pd
import streamlit as st


st.set_page_config(
    page_title='Data Engineering Salaries',
    page_icon=':gear:',
    layout='wide',
    menu_items={
        'Report a bug': "https://github.com/data-engineering-community/data-engineering-salaries/issues/new"
        }
    )


# Read in data from the Google Sheet.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)
def load_data(sheets_url):
    csv_url = sheets_url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

salaries_df = load_data(st.secrets["public_gsheets_url"])

salaries_df.drop(columns=['Submission ID', 'Respondent ID'], inplace=True)

# Initialize session state variables
# https://docs.streamlit.io/library/advanced-features/session-state#initialization
session_state_variables = ['filter_job_title']
for key in session_state_variables:
    if key not in st.session_state:
        st.session_state[key] = ''

job_title_list = [ # Empty string = no filter
    "", "Junior Data Engineer", "Data Engineer", "Senior Data Engineer", "Lead Data Engineer",
    "Staff Data Engineer", "Principal Data Engineer", *list(salaries_df['Other'].unique())
]

# Apply filters if they exist
if st.session_state.filter_job_title:
    salaries_df = salaries_df[
        (salaries_df['Current Job Title'] == st.session_state.filter_job_title) | (salaries_df['Other'] == st.session_state.filter_job_title)
    ] 

# Print results.
st.dataframe(data=salaries_df, hide_index=True)

with st.sidebar:
    # Filters
    st.selectbox("Job Title", options=job_title_list, key='filter_job_title')

hide_footer_style = """
<style>
footer {visibility: hidden;}    
"""
st.markdown(hide_footer_style, unsafe_allow_html=True)
