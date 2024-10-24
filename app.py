# app.py

import streamlit as st
import openai
from database import execute_sql, mysql_engine
from config import OPENAI_API_KEY

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY

# Function to convert plain text query to SQL using OpenAI's new API
def convert_to_sql(plain_text_query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can switch to 'gpt-4' if you have access
            messages=[
                {"role": "system", "content": "You are an AI that converts natural language to SQL queries."},
                {"role": "user", "content": f"Convert the following natural language query into SQL: {plain_text_query}"}
            ],
            temperature=0
        )
        sql_query = response['choices'][0]['message']['content'].strip()
        return sql_query
    except Exception as e:
        return f"Error generating SQL: {str(e)}"

# Streamlit app UI
st.title("Gen AI SQL Query App")

# Input for user query
user_query = st.text_input("Enter your query in plain English:")

# Button to submit query
if st.button("Search"):
    if not user_query:
        st.error("Please enter a query.")
    else:
        # Display loading message
        st.write("Processing your query...")

        # Convert the user query into SQL
        sql_query = convert_to_sql(user_query)
        
        if "Error" in sql_query:
            st.error(sql_query)
        else:
            # Display the generated SQL query
            st.write("Generated SQL Query:", sql_query)

            # Fetch results from MySQL
            st.write("Fetching results from MySQL database...")
            mysql_results = execute_sql(sql_query, mysql_engine)

            # Display MySQL results
            if mysql_results:
                st.write("MySQL Results:")
                st.table(mysql_results)
            else:
                st.write("No results found in MySQL.")

            # Fetch results from PostgreSQL
            st.write("Fetching results from PostgreSQL database...")
            postgres_results = execute_sql(sql_query)

            # Display PostgreSQL results
            if postgres_results:
                st.write("PostgreSQL Results:")
                st.table(postgres_results)

            # Fetch results from SQL Server
            st.write("Fetching results from SQL Server database...")
            sql_server_results = execute_sql(sql_query)

            # Display SQL Server results
            if sql_server_results:
                st.write("SQL Server Results:")
                st.table(sql_server_results)
            else:
                st.write("No results found in SQL Server.")