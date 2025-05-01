import pyodbc
import json
from datetime import datetime

# Load Database Credentials from config.json
with open("config.json", "r") as f:
    config = json.load(f)
sql_config = config["sql"]

# Function to Establish Connection
def get_sql_connection():
    try:
        conn_str = f"""
            DRIVER={sql_config['driver']};
            SERVER={sql_config['server']};
            DATABASE={sql_config['database']};
            UID={sql_config['username']};
            PWD={sql_config['password']};
        """
        conn = pyodbc.connect(conn_str)
        print("Connected to Azure SQL Database!")
        return conn
    except Exception as e:
        print(f"Error connecting to SQL: {e}")
        return None

def store_prediction(run_id, client_id, raw_input, processed_input, prediction_prob, predicted_class):
    """
    Stores prediction in Azure SQL.
    """
    conn = None
    cursor = None
    try:
        # Ensure Connection is Correct

        conn = get_sql_connection()
        cursor = conn.cursor()

        # ✅ SQL Insert Query
        sql_query = """
        INSERT INTO Predictions 
        (Client_ID, run_id, prediction_date, input_data, preprocessed_data, prediction_probability, predicted_class)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        # Convert to JSON format
        raw_json = json.dumps(raw_input, default=str)
        processed_json = json.dumps(processed_input, default=str)

        # Execute Query
        cursor.execute(sql_query, (client_id, run_id, datetime.now(), raw_json, processed_json, prediction_prob, predicted_class))
        conn.commit()
        print("Prediction stored successfully in Azure SQL.")

    except Exception as e:
        print(f"Failed to store prediction in Azure SQL. Error: {e}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
