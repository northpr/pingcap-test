import streamlit as st
import time
from tidb_connect import Chat2QueryAPI, print_pretty_result
from utils import AppUtils
import pandas as pd
from chatgpt_utils import create_summary_message, generate_completion

app_utils = AppUtils()
config = app_utils.load_config()
api_settings = app_utils.get_api_settings()
app_utils.initialize_state()

with st.sidebar:
    st.title("API Configuration")

    # API Configuration Section
    with st.expander("API Details", expanded=True):
        public_key = st.text_input("Public Key", value=api_settings['public_key'])
        private_key = st.text_input("Private Key", value=api_settings['private_key'], type="password")
        region = st.selectbox("Region", options=['ap-southeast-1', 'us-west-2'], index=0)
        app_id = st.text_input("App ID", value=api_settings['app_id'])
        cluster_id = st.text_input("Cluster ID", value=api_settings['cluster_id'])
        database = st.text_input("Database", value=api_settings['database'])

    # Display Settings Section
    with st.expander("Display Settings"):
        row_display = st.number_input("Number of Rows to Display", min_value=1, value=10, step=1)
        model_name = st.selectbox("Choose a Model", ['gpt-3.5-turbo', 'gpt-4-turbo-preview'], index=0)
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
        
        with st.spinner('Thinking...'):
            query_result = api.get_sql_job_result(prompt)

        if 'error' in query_result:
            response_content = f"Error: {query_result['error']}"
        else:
            df = pd.DataFrame(query_result['rows'], columns=query_result['columns'])
            df_id = f"df_{len(st.session_state.dataframes)}"
            st.session_state.dataframes[df_id] = df

            # Generate completion from ChatGPT
            messages = create_summary_message(
                query_result['clarified_task'],
                query_result['sql_query'],
                query_result['columns'],
                query_result['rows']
            )
            chat_gpt_response = generate_completion(messages)

            response_content = f"**ChatGPT Analysis:** \n\n{chat_gpt_response}\n\n" \
                               f"**SQL Query:**\n```sql\n{AppUtils.format_sql_query(query_result['sql_query'])}\n```"
            
            st.session_state.messages.append({"role": "assistant", "content": response_content})
            st.session_state.messages.append({"role": "dataframe", "content": df_id})

        for message in st.session_state.messages[-3:]:
            with st.chat_message(message['role']):
                if message['role'] == 'assistant':
                    st.markdown(message['content'])
                elif message['role'] == 'user':
                    st.markdown(message['content'])
                elif message['role'] == 'dataframe':
                    st.dataframe(st.session_state.dataframes[df_id].head(row_display), use_container_width=True, hide_index=True)

        # # Rerender chat history to include the new messages
        # for message in st.session_state.messages[-3:]:  # Display only the last interaction
        #     with st.chat_message(message['role']):
        #         if message['role'] == 'assistant':
        #             st.markdown(message['content'])
        #         elif message['role'] == 'user':
        #             st.markdown(message['content'])
        #         elif message['role'] == 'dataframe':
        #             # Display the dataframe using its unique ID
        #             df_id = message['content']
        #             st.dataframe(st.session_state.dataframes[df_id].head(row_display), use_container_width=True, hide_index=True)
else:
    st.info("Please initialize the API using the sidebar settings.")