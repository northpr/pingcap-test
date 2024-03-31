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
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    # Display chat messages from his tory on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    if prompt := st.chat_input("Chat to Assistant"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Add a placeholder for the "Please wait..." message
        placeholder = st.empty()
        placeholder.text("Generating result. . . . .")
        time.sleep(0.5)  # Adjust or remove this sleep as needed

        # Execute the SQL query or process the question
        query_result = api.get_sql_job_result(prompt)
        
        # Clear the "Please wait..." message
        placeholder.empty()
        
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
            response_content += f"\n**SQL Query:** '''\n{query_result['sql_query']}\n'''\n"
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            
            # Display the DataFrame as a table
            st.dataframe(df)

        # Rerender chat history to include the new messages
        for message in st.session_state.messages[-3:]:  # Display only the last interaction (user + assistant)
            if message['role'] == 'assistant' and "Clarified Task" in message['content']:
                with st.chat_message(message['role']):
                    st.markdown(message['content'])
            elif message['role'] == 'user':
                with st.chat_message(message['role']):
                    st.markdown(message['content'])

else:
    st.info("Please initialize the API using the sidebar settings.")