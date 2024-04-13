import streamlit as st
import time
from tidb_connect import Chat2QueryAPI, print_pretty_result
from utils import AppUtils
import pandas as pd

app_utils = AppUtils()
config = app_utils.load_config()
api_settings = app_utils.get_api_settings()
app_utils.initialize_state()

with st.sidebar:
    st.title("API Configuration")
    public_key = st.text_input("Public Key", value=api_settings['public_key'])
    private_key = st.text_input("Private Key", value=api_settings['private_key'], type="password")
    region = st.selectbox("Region", options=['ap-southeast-1', 'us-west-2'], index=0)
    app_id = st.text_input("App ID", value=api_settings['app_id'])
    cluster_id = st.text_input("Cluster ID", value=api_settings['cluster_id'])
    database = st.text_input("Database", value=api_settings['database'])
    row_display = st.number_input("Number of Rows to Display", min_value=1, value=10, step=1)
    init_button = st.button("Initialize API")


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
    if 'dataframes' not in st.session_state:
        st.session_state.dataframes = {}
    # Display chat messages from his tory on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            if message['role'] == 'dataframe':
                # Fetch the dataframe by ID and display it
                df_id = message['content']
                st.dataframe(st.session_state.dataframes[df_id].head(row_display), use_container_width=True, hide_index=True)
            else:
                # Display text messages normally
                st.markdown(message['content'])
            
    if prompt := st.chat_input("Chat to Assistant"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.spinner('Thinking . . .'):
            query_result = api.get_sql_job_result(prompt)
        print(f"query_result:\n{(query_result)}")
        
        # Prepare the response based on the query result
        # response_content = ""
        if 'error' in query_result:
            response_content = f"Error: {query_result['error']}"
            st.session_state.messages.append({"role": "assistant", "content": response_content})
        else:
            # Use pandas to create a DataFrame from the query result
            df = pd.DataFrame(query_result['rows'], columns=query_result['columns'])
            df_id = f"df_{len(st.session_state.dataframes)}"  # Unique identifier for the dataframe
            st.session_state.dataframes[df_id] = df  # Store dataframe with unique ID

            # Add a message indicating the Clarified Task and SQL Query
            response_content = f"**Clarified Task:** {query_result['clarified_task']}\n"
            formatted_sql_query = AppUtils.format_sql_query(query_result['sql_query'])
            response_content += f"\n**SQL Query:**\n```sql\n{formatted_sql_query}\n```"
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            # Add dataframe placeholder to messages to ensure correct order
            st.session_state.messages.append({"role": "dataframe", "content": df_id})

        # Rerender chat history to include the new messages
        for message in st.session_state.messages[-3:]:  # Display only the last interaction
            with st.chat_message(message['role']):
                if message['role'] == 'assistant':
                    st.markdown(message['content'])
                elif message['role'] == 'user':
                    st.markdown(message['content'])
                elif message['role'] == 'dataframe':
                    # Display the dataframe using its unique ID
                    df_id = message['content']
                    st.dataframe(st.session_state.dataframes[df_id].head(row_display), use_container_width=True, hide_index=True)
else:
    st.info("Please initialize the API using the sidebar settings.")