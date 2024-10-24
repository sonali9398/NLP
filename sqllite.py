# Import module 
import sqlite3 
import google.generativeai as genai
import os
import pyodbc

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Connecting to sqlite 
conn = sqlite3.connect('test.db') 
conn_str = ""
conn = pyodbc.connect(conn_str)
  
# Creating a cursor object using the  
# cursor() method 
cursor = conn.cursor() 
  
# # Creating table 
# table ="""CREATE TABLE STUDENT(NAME VARCHAR(255), CLASS VARCHAR(255), 
# SECTION VARCHAR(255));"""
# cursor.execute(table) 
  
# # Queries to INSERT records. 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Krish', 'Data Science', 'A')''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Darius', 'Data Science', 'B')''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Sudhanshu', 'Devops', 'C')''') 
# cursor.execute('''INSERT INTO STUDENT VALUES ('Vikash', 'Data Science', 'C')''') 
  
# # Display data inserted 
# print("Data Inserted in the table: ") 
# data=cursor.execute('''SELECT * FROM STUDENT''') 
# for row in data: 
#     print(row) 
  
# # Commit your changes in the database     
# conn.commit() 
  
# Closing the connection 
conn.close()