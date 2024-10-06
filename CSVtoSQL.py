from flask import Flask, request, jsonify, render_template
import csv
import io
import sqlite3
import pandas as pd

from RegressionModel import database_to_python, buildRegressionModel

app = Flask(__name__, static_folder="static", template_folder="templates")

# Route to serve the HTML form for file upload
@app.route('/')
def index():
    return render_template('index.html')  # This renders the HTML form when accessed

# Route to handle file upload via POST
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        file_content = file.read().decode('utf-8')
        dataframe = pd.read_csv(io.StringIO(file_content))

        # Process the file and insert it into the database
        connection = sqlite3.connect("data.db")

        # create table name removing .csv from filename
        table_name = file.filename.rsplit('.', 1)[0]

        # Get x_var and y_var from form data
        x_var = request.form.get("x_var")
        y_var = request.form.get("y_var")
        print(f"x_var: {x_var}, y_var: {y_var}")

        if not x_var or not y_var:
            return jsonify({"error": "X and Y variables are required."}), 400

        type_map = infer_sql_types(dataframe)
        create_sql_table(connection, table_name, type_map)
        insert_data_table(connection, table_name, dataframe)
        connection.close()

        x_list, y_list = database_to_python(x_var, y_var, table_name)
        buildRegressionModel(x_list, y_list, x_var, y_var)

        return jsonify({"success": "File uploaded and data inserted into the database!"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

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
    df = pd.read_csv(io.StringIO(csv_file), delimiter=delimiter)

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
            table += f'"{col}" {datatype}, '

    table = table.rstrip(", ") + ")" # end of SQL CREATE

    cursor.execute(table)
    connection.commit()  # Don't forget to commit the creation of the table
    cursor.close()  # Close the cursor after executing the query


# inserts data into our created table
def insert_data_table(connection, table_name, dataframe):
    cursor = connection.cursor()

    # Generate column placeholders for insertion query, ensuring columns are quoted
    columns = ", ".join([f'"{col}"' for col in dataframe.columns])
    placeholders = ", ".join(["?"] * len(dataframe.columns))
    insert_query = f'INSERT INTO "{table_name}" ({columns}) VALUES ({placeholders})'

    # Insert the rows into the table
    cursor.executemany(insert_query, dataframe.values.tolist())
    connection.commit()
    cursor.close()  # Close the cursor after executing the insert query

if __name__ == '__main__':
    app.run(debug=True)
