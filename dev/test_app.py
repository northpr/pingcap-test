import streamlit as st
import time
from tidb_connect import Chat2QueryAPI, print_pretty_result
import random
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

public_key = config['API_Configuration']['public_key']
private_key = config['API_Configuration']['private_key']
region = config['API_Configuration']['region']
app_id = config['API_Configuration']['app_id']
cluster_id = config['API_Configuration']['cluster_id']
database = config['API_Configuration']['database']

## https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps
def format_sql_query(sql_query):
    """
    Takes an SQL query string and formats it for Markdown with proper line breaks.
    
    Parameters:
    - sql_query: A string containing the raw SQL query.
    
    Returns:
    - A string containing the formatted SQL query.
    """
    
    # Break the SQL query into parts for better formatting
    sql_parts = sql_query.split(' FROM ')
    columns = sql_parts[0].replace('SELECT ', '').replace(',', ',\n')
    table_and_conditions = sql_parts[1].split(' WHERE ')
    table = table_and_conditions[0]
    conditions = table_and_conditions[1] if len(table_and_conditions) > 1 else ""

    # Assemble the parts with appropriate newlines for Markdown formatting
    formatted_sql_query = f"SELECT\n{columns}\nFROM\n{table}"
    if conditions:
        formatted_sql_query += f"\nWHERE\n{conditions}"
    
    return formatted_sql_query
with st.sidebar:
    st.title("API Configuration")
    public_key = st.text_input("Public Key", value=public_key)
    private_key = st.text_input("Private Key", value=private_key, type="password")
    region = st.selectbox("Region", options=['ap-southeast-1', 'us-west-2'], index=0)
    app_id = st.text_input("App ID", value=app_id)
    cluster_id = st.text_input("Cluster ID", value=cluster_id)
    database = st.text_input("Database", value=database)
    init_button = st.button("Initialize API")

if 'api_initialized' not in st.session_state:
    st.session_state.api_initialized = False

if init_button or st.session_state.api_initialized:
    st.session_state.api_initialized = True
    # Initialize the Chat2QueryAPI object with sidebar configurations
    api = Chat2QueryAPI(
        public_key=public_key,
        private_key=private_key,
        region=region,
        app_id=app_id,
        cluster_id=cluster_id,
        database=database
    )

            
    st.title('Text2Query Assistant 🔍🤖')

    # Initialize chat history
    if 'messages' not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How can I help?"}]

    # Display chat messages from his tory on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    if prompt := st.chat_input("Chat to Assistant"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner('Thinking . . .'):
            query_result = api.get_sql_job_result(prompt)
        print(query_result)

        
        # Prepare the response based on the query result
        response_content = ""
        if 'error' in query_result:
            response_content = f"Error: {query_result['error']}"
            st.session_state.messages.append({"role": "assistant", "content": response_content})
        else:
            # Use pandas to create a DataFrame from the query result
            df = pd.DataFrame(query_result['rows'], columns=query_result['columns'])
            
            # Add a message indicating the Clarified Task and SQL Query
            response_content = f"**Clarified Task:** {query_result['clarified_task']}\n"
            formatted_sql_query = format_sql_query(query_result['sql_query'])
            response_content += f"**SQL Query:**\n```sql\n{formatted_sql_query}\n```"
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            # Add dataframe placeholder to messages to ensure correct order
            st.session_state.messages.append({"role": "dataframe", "content": df})

        # Rerender chat history to include the new messages
        for message in st.session_state.messages[-3:]:  # Display only the last interaction (user + assistant + dataframe if present)
            if message['role'] == 'assistant' and "Clarified Task" in message['content']:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
            elif message['role'] == 'user':
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
            elif message['role'] == 'dataframe':
                # Create three columns to center the DataFrame
                st.dataframe(message['content'], use_container_width=True)
else:
    st.info("Please initialize the API using the sidebar settings.")