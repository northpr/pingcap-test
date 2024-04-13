import openai
from configparser import ConfigParser

# Initialize OpenAI client
def get_openai_client():
    config = ConfigParser()
    config.read('config.ini')
    openai_api_key = config['API_Configuration']['openai_api_key']
    openai.api_key = openai_api_key
    return openai

def format_prompt(clarified_task, sql_query, columns, rows):
    prompt = f"**Task:** {clarified_task}\n**SQL Query:**\n```\n{sql_query}\n```\n**Data Summary:**\n"
    prompt += "Total Items: {}, Columns: {}\n\n".format(len(rows), ", ".join(columns))
    return prompt

def create_summary_message(clarified_task, sql_query, columns, rows):
    client = get_openai_client()
    formatted_prompt = format_prompt(clarified_task, sql_query, columns, rows)
    system_message = "Analyze dataset to provide key insights, actionable strategies, and brief conclusions."
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': formatted_prompt}
    ]
    
    return messages

def generate_completion(messages):
    client = get_openai_client()
    response = client.Completion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message['content']
