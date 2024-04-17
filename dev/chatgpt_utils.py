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
    prompt = f"**Task:** {clarified_task}\n\n**Data Summary:**\n"
    prompt += "Total Items: {}, Columns: {}\n\n".format(len(rows), ", ".join(columns))
    return prompt

def create_summary_message(clarified_task, sql_query, columns, rows):
    client = get_openai_client()
    formatted_prompt = format_prompt(clarified_task, sql_query, columns, rows)
    system_message = "You're a friendly senior data analyst who can help you analyze based on a question and dataset to provide precise key action to be taken, anomaly, and short conclusion."
    
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': formatted_prompt}
    ]
    
    return messages

def generate_completion(messages, model_name="gpt-3.5-turbo"):
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )
    return response.choices[0].message.content
