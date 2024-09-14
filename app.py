from flask import Flask, request, render_template, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL connection details from environment variables
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME')
}

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Route to show the form for inserting data into the test table
@app.route('/create', methods=['GET', 'POST'])
def create_data():
    if request.method == 'POST':
        try:
            # Get data from the HTML form
            name = request.form['name']
            description = request.form['description']

            # Connect to the MySQL database
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Insert data into the test table
            query = "INSERT INTO test (name, description) VALUES (%s, %s)"
            cursor.execute(query, (name, description))
            connection.commit()

            return redirect(url_for('show_data'))

        except Exception as e:
            return f'Error: {str(e)}'

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    return render_template('create.html')

# Route to fetch and display data from the test table
@app.route('/show')
def show_data():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Select all data from the test table
        cursor.execute("SELECT * FROM test")
        rows = cursor.fetchall()

        return render_template('show_data.html', data=rows)

    except Exception as e:
        return f'Error: {str(e)}'

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(host=os.getenv('FLASK_RUN_HOST'), port=int(os.getenv('FLASK_RUN_PORT')), debug=True)
