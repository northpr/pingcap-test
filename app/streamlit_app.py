import streamlit as st
from streamlit_chat import message
from tidb_connect import Chat2QueryAPI, print_pretty_result  # Ensure you have this module ready
import pandas as pd

# Initialize your Chat2QueryAPI object with credentials
api = Chat2QueryAPI(
    public_key='414VD1N0',
    private_key='aefec559-36eb-4cd1-b6c3-59fa74303d41',
    region='ap-southeast-1',
    app_id='WizQVcwy',
    cluster_id='10954456779882628977',
    database='test'
)

# Setting page title and header
st.set_page_config(page_title="TiDB Text2Query Executor", page_icon=":robot_face:")
st.markdown("<h1 style='text-align: center;'>🔍 TiDB Text2Query Executor</h1>", unsafe_allow_html=True)

# Initialise session state variables
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Function to execute query and generate response
def execute_query_and_generate_response(user_query):
    # Here you would call the API and process the response
    result = api.get_sql_job_result(user_query)
    return result

# Display chat messages
for message_info in st.session_state.messages:
    if message_info["role"] == "user":
        message(message_info["content"], is_user=True)
    else:  # System response
        message(message_info["content"], is_user=False)

# Input for new query/message
with st.container():
    user_input = st.text_input("Type your SQL query or question here and press enter:", "")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Simulating API call and response for the example. Replace with your API call logic.
    response = execute_query_and_generate_response(user_input)
    
    # Assuming `response` is a string. If it's a dictionary or object, format it as needed.
    st.session_state.messages.append({"role": "system", "content": str(response)})
    
    # Clear input
    st.experimental_rerun()