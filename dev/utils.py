import configparser

class AppUtils:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.config = configparser.ConfigParser()

    def load_config(self):
        self.config.read(self.config_file)
        return self.config
    
    def save_config(self):
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def get_api_settings(self):
        return {
            'public_key': self.config['API_Configuration']['public_key'],
            'private_key': self.config['API_Configuration']['private_key'],
            'region': self.config['API_Configuration']['region'],
            'app_id': self.config['API_Configuration']['app_id'],
            'cluster_id': self.config['API_Configuration']['cluster_id'],
            'database': self.config['API_Configuration']['database']
        }
    
    @staticmethod
    def format_sql_query(sql_query):
        sql_parts = sql_query.split(' FROM ')
        columns = sql_parts[0].replace('SELECT ', '').replace(',', ',\n')
        table_and_conditions = sql_parts[1].split(' WHERE ')
        table = table_and_conditions[0]
        conditions = table_and_conditions[1] if len(table_and_conditions) > 1 else ""

        formatted_sql_query = f"SELECT\n{columns}\nFROM\n{table}"
        if conditions:
            formatted_sql_query += f"\nWHERE\n{conditions}"

        return formatted_sql_query
    
    @staticmethod
    def welcome_msg():
        """
        Generates a welcome message string with a description of the assistant's capabilities
        and sample questions.
        """
        return ("""
        👋 Welcome to the Text2Query Assistant! I can help you craft SQL queries based on your natural language questions. 
        Here are some examples of questions you can ask me:

        - Generate an SQL query to list all SUV models available in the Thailand market, including their model names and manufacturing years.
        - I want to see the stock of items that are lower than minimum stock.
        - Find all sales records for cars sold after January 1, 2023, including the salesperson's name and the car model name.
        - Determine the inventory levels of parts for cars with a manufacturing schedule planned to start in 2023.
        - Aggregate sales by car model and year for sales made in 2023, including total sales and average sale price.
        
        Go ahead and ask me a question to get started!
        """)
