import csv
import sqlite3
import pandas as pd
import pythonmonkey as pm

# Uses pythonmonkey to call getFile from script.js and returns CSV file
file = pm.require('./script')
file.getFile()

# detect the delimiter that separates values in CSV file (referenced to chatGPT)
def detect_delimiter(csv_file):
    with open(csv_file, 'r') as file:
        # Use the csv.Sniffer to detect the delimiter
        sample = file.read(1024)  # Read a sample of the file
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(sample).delimiter
        return delimiter

# read the CSV file into a pandas DataFrame
def read_csv(csv_file):
    delimiter = detect_delimiter(csv_file)
    df = pd.read_csv(csv_file, delimiter=delimiter)
    return df

# create columns by type and store in dictionary (referenced to chatGPT)
def infer_sql_types(df):
    type_mapping = {}

    for column in df.columns:
        # Check the dtype of each column and map it to SQL data types
        if pd.api.types.is_integer_dtype(df[column]):
            sql_type = 'INTEGER'
        elif pd.api.types.is_float_dtype(df[column]):
            sql_type = 'REAL'  # Use REAL for float types in SQLite
        elif pd.api.types.is_datetime64_any_dtype(df[column]):
            sql_type = 'DATE'  # Handle datetime columns
        else:
            sql_type = 'TEXT'  # Default to TEXT for strings and other types

        # Store column name and inferred SQL type in dictionary
        type_mapping[column] = sql_type

    return type_mapping

# creates SQL table
def create_sql_table(connection, table_name, type_mapping):
    cursor = connection.cursor()
    table = f"CREATE TABLE IF NOT EXISTS {table_name} (" # start of SQL create

    for col, datatype in type_mapping.items():
            table += f"{col} {datatype}, "

    table = table.rstrip(", ") + ")" # end of SQL CREATE

    cursor.execute(table)
    cursor.close()


# inserts data into our created table
def insert_data_table(table_name, dataframe):
    cursor = connection.cursor()

    # Generate column placeholders for insertion query
    columns = ", ".join(dataframe.columns)
    placeholders = ", ".join(["?"] * len(dataframe.columns))
    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    # Insert the rows into the table
    cursor.executemany(insert_query, dataframe.values.tolist())
    connection.commit()


connection = sqlite3.connect("data.db")

dataframe = read_csv("25.csv")
type_map = infer_sql_types(dataframe)
create_sql_table(connection, "user_table", type_map)
insert_data_table("user_table", dataframe)

connection.close()

print("Data inserted successfully!")
