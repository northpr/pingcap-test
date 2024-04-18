
# Streamlit ChatGPT Integration with TiDB

A Streamlit application that integrates OpenAI's GPT models to interact with TiDB Cloud databases, providing a user interface to query data and generate insights dynamically.

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-tidb-gpt.git
   cd streamlit-tidb-gpt
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API keys and database credentials:
   - Rename `config.ini.example` to `config.ini`.
   - Update the `config.ini` with your OpenAI API key and TiDB credentials.

5. Run the application:
   ```bash
   streamlit run app.py
   ```

6. Navigate to `localhost:8501` in your web browser to view the application.

## Configuration

Configure your API and database settings through the Streamlit sidebar within the application interface. Ensure all details are correct to connect successfully to your TiDB instance.

## Features

- Interactive chat interface to query the database using natural language.
- Visualization of query results with options to customize data display.
- Integration with OpenAI's GPT models for generating analytical summaries based on query results.

## Removing the Repository

If you need to remove the repository from your development directory:

```bash
rm -rf .git
```

For more detailed information on configuration and extensions, refer to the provided documentation within the project.
