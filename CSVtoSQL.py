import sqlite3
import pandas as pd

# read the CSV file into a pandas DataFrame
csv_file = '/Users/danielcanhedo/PycharmProjects/LinearRegressionPractice/25.csv'  # Replace with inputted CSV file path
df = pd.read_csv(csv_file)

# connect to the SQLite database (it will create the database if it doesn't exist)
con = sqlite3.connect('data.db')  # Replace with your database file name
cur = con.cursor()

# Step 3: Create a table to hold the CSV data (replace with your desired table structure)
cur.execute('''
    CREATE TABLE IF NOT EXISTS user_data (
        date DATE,
        step_count INTEGER,
        mood INTEGER,
        calories_burned INTEGER,
        hours_of_sleep INTEGER,
        bool_of_active INTEGER,
        weight_kg INTEGER
        -- Add more columns here depending on your CSV structure
    )
''')

# Step 4: Insert data from the pandas DataFrame into the SQL table
df.to_sql('exercise_table', con, if_exists='append', index=False)

# Step 5: Commit the transaction and close the connection
con.commit()
con.close()

print("Data inserted successfully!")