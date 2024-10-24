import spacy
from spacy.lang.en import English
import os
from dotenv import load_dotenv
import pyodbc
import streamlit as st

load_dotenv()  # Load environment variables

# Load SpaCy NLP model
nlp = English()

# Configure Genai Key (if available)
genai_api_key = os.getenv("GOOGLE_API_KEY")

# Function to retrieve query from the SQL Server database
def read_sql_query(sql_query):
    conn_str = ""
    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql_query)
    
    # Get column names and rows
    column_names = [column[0] for column in cur.description]
    rows = cur.fetchall()

    conn.commit()
    conn.close()

    return rows, column_names

# Simple SQL Generator (fallback)
def simple_sql_generator(question, column_names):
    doc = nlp(question)
    tokens = [token.text.lower() for token in doc]

    # Detect basic intent for table counting
    if "table" in tokens and "count" in tokens:
        return "SELECT COUNT(*) AS table_count FROM information_schema.tables;"

    # Fallback for a basic SELECT from known columns
    elif any(col in tokens for col in column_names):
        return f"SELECT * FROM {column_names[0]} WHERE {column_names[1]} = 'Example';"  # Simple example query

    return "SELECT * FROM dbo.TBLEMPLOYEE;"  # Default fallback query

# Main Gemini API Query Generator
def get_gemini_response(question, prompt, column_names, retries=3):
    # Generate prompt with available columns for the user
    extended_prompt = prompt[0] + f"\n\nAvailable columns in the database are: {', '.join(column_names)}."

    if genai_api_key:
        import google.generativeai as genai
        genai.configure(api_key=genai_api_key)
        model = genai.GenerativeModel('gemini-pro')

        for attempt in range(retries):
            try:
                response = model.generate_content([extended_prompt, question])
                return response.text
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(5)  # Wait for a short period and retry
                    print(f"Error: {e}. Retrying... (Attempt {attempt + 1}/{retries})")
                else:
                    # If retries fail, return a fallback query
                    print(f"Quota exhausted or error occurred. Using fallback.")
                    return simple_sql_generator(question, column_names)
    else:
        # If API key is not set, use fallback
        return simple_sql_generator(question, column_names)

# Define Your Prompt for Gemini (or other LLMs)
prompt = [
    """
    You are an expert in converting English questions to SQL queries!
    The SQL database has multiple tables with the following structure:
    - Flight details: Airline, Reference_Number, Class
    - Employee: ID, Name, Department, Salary
    \nExamples:
    - 'How many tables are in the database?' → SELECT COUNT(*) AS table_count FROM information_schema.tables;
    - 'Show me all employees from department X.' → SELECT * FROM Employee WHERE Department = 'X';
    - 'Give me all airlines with reference number 123' → SELECT * FROM Flight WHERE Reference_Number = '123';
    Do not use `sql` word in the output and do not wrap the code with triple backticks.
    """
]

# Streamlit App Interface
st.set_page_config(page_title="Gemini SQL Query App")
st.header("Gemini SQL Query Generator")

# Input section
question = st.text_input("Input your question:", key="input")
submit = st.button("Ask the question")

# SQL data column names for demonstration
_, column_names = read_sql_query("SELECT TOP 1 * FROM dbo.TBLEMPLOYEE")

# If submit is clicked
if submit:
    try:
        response = get_gemini_response(question, prompt, column_names)
        st.write(f"Generated SQL Query: {response}")
        
        # Execute the query and display results
        query_result, columns = read_sql_query(response)
        
        st.subheader("Query Results")
        st.write(f"Columns: {columns}")
        
        for row in query_result:
            st.write(row)  # Display each result row

    except Exception as e:
        st.error(f"Error executing the query: {e}")
