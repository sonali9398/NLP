# working fine with single sql query


from dotenv import load_dotenv
load_dotenv()  # Load all the environment variables

import streamlit as st
import os
import pyodbc  # Use pyodbc to connect to SQL Server

import google.generativeai as genai

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    # return response.text

    corrected_response = response.text.replace("TBLEMPLOYEE", "dbo.TBLEMPLOYEE")
    return corrected_response

# Function to retrieve query from the SQL Server database
def read_sql_query(sql_query):
    # Connection string to connect to the SQL Server
    conn_str = ""
    conn = pyodbc.connect(conn_str)
    cur = conn.cursor()
    cur.execute(sql_query)
    
    # Get column names
    column_names = [column[0] for column in cur.description]
    print("Column Names:", column_names)  # Print column names for reference
    
    rows = cur.fetchall()
    
    conn.commit()
    conn.close()

    # Print each row for reference
    for row in rows:
        print(row)
    return rows

# Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name tickets and has the following columns - Airline, reference_number, 
    class \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM flight6 ;
    \nExample 2 - Tell me count of all the airline named?, 
    the SQL command will be something like this SELECT * FROM flight6 
    where airline="Indigo"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

# If submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    print("Generated SQL Query:", response)  # Print the generated SQL query for reference
    response = read_sql_query(response)  # Use the function to read from the SQL Server
    st.subheader("The Response is")
    for row in response:
        st.header(row)  # Display each row in Streamlit
