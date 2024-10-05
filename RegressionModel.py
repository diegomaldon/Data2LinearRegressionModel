import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sqlite3
import CSVtoSQL

# extract data from SQLite database to Python
def database_to_python(x_var, y_var):

    # connects to exercise database
    con=sqlite3.connect("data.db")
    cur=con.cursor()

    # selects data from exercise database
    my_query = f"SELECT {x_var}, {y_var} FROM user_table"
    cur.execute(my_query)

    # place data
    data = cur.fetchall()

    # place data into respective python list
    for row in data:
        x_list.append(row[0])
        y_list.append(row[1])

    # close the sql database connection
    con.close()



# build linear regression model
def buildRegressionModel(x_var, y_var):
    # initialize numpy arrays for prediction
    x = np.array(x_list).reshape(-1, 1)
    y = np.array(y_list)

    # Create and fit the linear regression model
    model = LinearRegression().fit(x, y)

    # Predict final grades using the model
    y_pred = model.predict(x)

    # Calculate R-squared score
    data = model.score(x, y)
    print(f"R-squared: {data}")

    # Plot study hours (second feature) vs final grade
    plt.scatter(x, y, color='blue', label='Data points')  # Study hours vs final grades
    plt.plot(x, y_pred, color='red', label='Regression line')  # Regression line for study hours

    plt.title(f'{y_var} vs {x_var}')
    plt.xlabel(f'{y_var}')
    plt.ylabel(f'{x_var}')
    plt.legend()
    plt.show()

# initialize lists to input data from sql database
x_list = []
y_list = []

x_var = input("Enter your X variable (Spelt exactly as on CSV): ")
y_var = input("Enter your Y variable (Spelt exactly as on CSV): ")

database_to_python(x_var, y_var)
buildRegressionModel(x_var, y_var)
print("plotted successfully")
