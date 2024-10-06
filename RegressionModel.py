import os
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sqlite3

# extract data from SQLite database to Python
# extract data from SQLite database to Python
def database_to_python(x_var, y_var, table_name):

    # connects to the database
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # Ensure table and column names are quoted
    my_query = f'SELECT "{x_var}", "{y_var}" FROM "{table_name}"'
    cur.execute(my_query)

    # place data
    data = cur.fetchall()

    # initialize lists to input data from sql database
    x_list = []
    y_list = []

    # place data into respective python list
    for row in data:
        x_list.append(row[0])
        y_list.append(row[1])

    return x_list, y_list
    # close the SQL database connection
    con.close()



# build linear regression model
def buildRegressionModel(x_list, y_list, x_var, y_var, filename=None):
    # If no filename is provided, generate one based on the variables
    if not filename:
        filename = f'{x_var}_vs_{y_var}_plot.png'

    # Initialize numpy arrays for prediction
    x = np.array(x_list).reshape(-1, 1)
    y = np.array(y_list)

    # Create and fit the linear regression model
    model = LinearRegression().fit(x, y)

    # Predict using the model
    y_pred = model.predict(x)

    # Plotting the data
    plt.scatter(x, y, color='blue', label='Data points')
    plt.plot(x, y_pred, color='red', label='Regression line')
    plt.title(f'{y_var} vs {x_var}')
    plt.xlabel(f'{x_var}')
    plt.ylabel(f'{y_var}')
    plt.legend()

    # Define the path where the plot will be saved
    save_path = os.path.join('static', filename)

    # Save the plot to the defined path
    plt.savefig(save_path)

    # Close the figure to prevent display in non-GUI environments
    plt.close()

    print(f"Plot saved successfully at {save_path}!")
    return filename  # Returning the filename, not the full path

