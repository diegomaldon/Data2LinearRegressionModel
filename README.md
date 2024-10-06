# Data 2 Linear Regression

## Background

This project was created by Diego Maldonado and Daniel Canhedo for the CuseHacks 2024 24hr hackathon project.

The project's goal is provide a web interface where a user can upload a CSV file, store its data in a SQLite database, and create a linear regression 
model based off of two provided variables.

## Installation
1. Download all repository files
2. Ensure prerequisites are installed:
     - Python 3.x
     - Flask
     - Pandas
     - SQLite
     - Seaborn
     - Matplotlib
     - NumPy
     - scikit-learn
3. Ensure files are in structure:
   CSV2LinearRegression/
    -├── static/
    -│   ├── styles.css
    -│   ├── script.js
    -│   └── icon.png
    -├── templates/
    -│   └── index.html
    -├── data.db (gets created automatically by the program)
    -├── CSVtoSQL.py
    -├── RegressionModel.py
    -└── README.md 

## Running the program
1. Run CSVtoSQL.py
2. In the terminal/console, copy and paste the development server (i.e. http://127.0.0.1:5000) into a web browser
3. Input an x-variable you would like to compare in the x-variable text box (ensure it is spelled exactly as it is on the CSV file)
4. Input a y-variable you would like to compare in the y-variable text box (ensure it is spelled exactly as it is on the CSV file)
5. Click or drag and drop a CSV file into the file upload box (ensure it is .csv)
6. That is it! Enjoy your linear regression graph!

## Future Improvements
- Improve front-end interface
- Expand upon error handling
- Create the ability to import multiple files at once

## Thank you!
A big thank you to the CuseHacks organizers for allowing us to partake in this awesome event!


  
