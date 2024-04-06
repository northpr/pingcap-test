import streamlit as st
import time
from tidb_connect import Chat2QueryAPI, print_pretty_result
from utils import AppUtils
import pandas as pd

app_utils = AppUtils()
config = app_utils.load_config()
api_settings = app_utils.get_api_settings()

with st.sidebar:
    st.title("API Configuration")
    public_key = st.text_input("Public Key", value=api_settings['public_key'])
    private_key = st.text_input("Private Key", value=api_settings['private_key'], type="password")
    region = st.selectbox("Region", options=['ap-southeast-1', 'us-west-2'], index=0)
    app_id = st.text_input("App ID", value=api_settings['app_id'])
    cluster_id = st.text_input("Cluster ID", value=api_settings['cluster_id'])
    database = st.text_input("Database", value=api_settings['database'])
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
        st.session_state.messages = [{"role": "assistant", "content": app_utils.welcome_msg()}]

    # Display chat messages from his tory on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])
            
    if prompt := st.chat_input("Chat to Assistant"):
        # Reset the message state for each new prompt, removing any old 'dataframe' messages
        st.session_state.messages = [msg for msg in st.session_state.messages if msg['role'] != 'dataframe']

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
            formatted_sql_query = AppUtils.format_sql_query(query_result['sql_query'])
            response_content += f"\n**SQL Query:**\n```sql\n{formatted_sql_query}\n```"
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
                st.dataframe(message['content'], use_container_width=True, hide_index=True)
else:
    st.info("Please initialize the API using the sidebar settings.")