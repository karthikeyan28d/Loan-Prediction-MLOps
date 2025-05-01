import time
import pandas as pd
import numpy as np
import re
import pyodbc
from datetime import datetime
print(pyodbc.drivers())
import warnings
warnings.filterwarnings('ignore')

def create_sql_connection(server, database, username, password, driver='{ODBC Driver 17 for SQL Server}'):
    """
    Establish a connection to a SQL Server database using pyodbc.

    Parameters:
    - server (str): The SQL Server address (e.g., 'localhost' or server IP).
    - database (str): The name of the database you want to connect to.
    - username (str): SQL Server username.
    - password (str): SQL Server password.
    - driver (str): ODBC driver to use. Default is '{ODBC Driver 17 for SQL Server}'.s

    Returns:
    - conn: A pyodbc connection object if successful.
    """
    connection_string = f"""
        DRIVER={driver};
        SERVER={server};
        DATABASE={database};
        UID={username};
        PWD={password};
    """
    try:
        conn = pyodbc.connect(connection_string)
        print("Connection established successfully!")
        return conn
    except Exception as e:
        print(f"Failed to connect to the database. Error: {e}")
        return None



def query_data(conn, query):
    """
    Execute a SQL query and fetch results as a pandas DataFrame.
    
    Parameters:
    - conn: A pyodbc connection object.
    - query (str): The SQL query to be executed.
    
    Returns:
    - data: A pandas DataFrame containing the query result.
    """
    start_time = time.time()  # Start time measurement
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        
        # Fetch all results from the query
        rows = cursor.fetchall()
        
        # Get column names from cursor
        columns = [desc[0] for desc in cursor.description]
        
        # Create a pandas DataFrame from the results
        data = pd.DataFrame.from_records(rows, columns=columns)
        
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        return None
    
    finally:
        cursor.close()
    
    end_time = time.time()  # End time measurement
    execution_time = end_time - start_time  # Calculate execution time
    
    # Print the DataFrame and execution time
    print(f"Query executed in: {execution_time:.4f} seconds")
    
    return data  



def ingest_data_to_sql(conn, df, table_name="CustomerRaw", schema="Bronze", batch_size=10000):
    """
    Inserts data from a Pandas DataFrame into an Azure SQL Database table in batches.

    Parameters:
    - conn: Active pyodbc connection object.
    - df (pd.DataFrame): The DataFrame containing data to be inserted.
    - table_name (str): Target table in the SQL database.
    - schema (str): Schema name in SQL (Default: 'Bronze').
    - batch_size (int): Number of rows to insert per batch (Default: 5000).

    Returns:
    - None
    """
    try:
        cursor = conn.cursor()

        start_time = time.time()  # Start timer

        # **Step 1: Ensure DataFrame Columns Match SQL Table Columns**
        column_mapping = {  # No need to re-declare; it's static
            "ID": "ID",
            "Client_Income": "Client_Income",
            "Car_Owned": "Car_Owned",
            "Bike_Owned": "Bike_Owned",
            "Active_Loan": "Active_Loan",
            "House_Own": "House_Own",
            "Child_Count": "Child_Count",
            "Credit_Amount": "Credit_Amount",
            "Loan_Annuity": "Loan_Annuity",
            "Accompany_Client": "Accompany_Client",
            "Client_Income_Type": "Client_Income_Type",
            "Client_Education": "Client_Education",
            "Client_Marital_Status": "Client_Marital_Status",
            "Client_Gender": "Client_Gender",
            "Loan_Contract_Type": "Loan_Contract_Type",
            "Client_Housing_Type": "Client_Housing_Type",
            "Population_Region_Relative": "Population_Region_Relative",
            "Age_Days": "Age_Days",
            "Employed_Days": "Employed_Days",
            "Registration_Days": "Registration_Days",
            "ID_Days": "ID_Days",
            "Own_House_Age": "Own_House_Age",
            "Mobile_Tag": "Mobile_Tag",
            "Homephone_Tag": "Homephone_Tag",
            "Workphone_Working": "Workphone_Working",
            "Client_Occupation": "Client_Occupation",
            "Client_Family_Members": "Client_Family_Members",
            "Client_City_Rating": "Client_City_Rating",
            "Application_Process_Day": "Application_Process_Day",
            "Application_Process_Hour": "Application_Process_Hour",
            "Client_Permanent_Match_Tag": "Client_Permanent_Match_Tag",
            "Client_Contact_Work_Tag": "Client_Contact_Work_Tag",
            "Type_Organization": "Type_Organization",
            "Score_Source_1": "Score_Source_1",
            "Score_Source_2": "Score_Source_2",
            "Score_Source_3": "Score_Source_3",
            "Social_Circle_Default": "Social_Circle_Default",
            "Phone_Change": "Phone_Change",
            "Credit_Bureau": "Credit_Bureau",
            "Defaulters": "Defaulters"
        }

        df = df.rename(columns=column_mapping)
        sql_columns = list(column_mapping.values())
        df = df[sql_columns]

        print(f"Step 1 Complete: DataFrame prepared in {time.time() - start_time:.2f} sec")

        # **Step 2: Generate SQL placeholders for insertion**
        columns = ", ".join(sql_columns)
        placeholders = ", ".join(["?" for _ in sql_columns])
        sql_query = f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({placeholders})"

        print(f"Step 2 Complete: SQL Query Generated in {time.time() - start_time:.2f} sec")

        # **Step 3: Convert DataFrame to List of Tuples**
        data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]
        print(f"Step 3 Complete: DataFrame converted to tuples in {time.time() - start_time:.2f} sec")

        # **Step 4: Execute Batch Inserts**
        for i in range(0, len(data_tuples), batch_size):
            batch = data_tuples[i:i + batch_size]
            cursor.executemany(sql_query, batch)
            conn.commit()
            print(f"Inserted {i + len(batch)}/{len(df)} rows in {time.time() - start_time:.2f} sec")

        print(f"Successfully inserted {len(df)} records in {time.time() - start_time:.2f} sec!")

    except Exception as e:
        print(f"Error inserting data: {e}")

    finally:
        cursor.close()