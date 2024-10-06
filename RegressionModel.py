import os
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sqlite3
import seaborn as sns

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
def buildRegressionModel(x_list, y_list, x_var, y_var, filename="plot.png"):
    # Convert lists to numpy arrays for regression
    x = np.array(x_list)
    y = np.array(y_list)

    sns.set_style("whitegrid")
    sns.set_palette("Purples")
    plt.figure(figsize=(8, 6))

    # Use Seaborn's regplot to create a linear regression plot with a confidence interval
    sns.regplot(x=x, y=y, scatter_kws={"color": "purple"}, line_kws={"color": "orange"})

    # Add labels and title
    plt.title(f'{y_var} vs {x_var}')
    plt.xlabel(f'{x_var}')
    plt.ylabel(f'{y_var}')

    # Define the path where the plot will be saved
    save_path = os.path.join('static', filename)  # Saving in the 'static/' directory

    # Save the plot to the defined path
    plt.savefig(save_path)

    # Close the figure to prevent display in non-GUI environments
    plt.close()

    print(f"Plot saved successfully at {save_path}!")
    return save_path

