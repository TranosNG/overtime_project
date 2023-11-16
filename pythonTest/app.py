from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Specify the connection details
server = 'JUNIOR-ERP-ADMI'
database = 'testDB'
trusted_connection = 'yes'  # Set to 'yes' for trusted connection
driver = 'SQL Server'  # The appropriate driver for your database

# Establish the connection
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
connection = pyodbc.connect(connection_string)

# Create a cursor
cursor = connection.cursor()

@app.route("/", methods=['GET'])
def hello():
    cursor.execute('hello world')
    return 

@app.route('/overtime/account', methods=['POST'])
def create_overTimeAccount():
    try:
        data = request.get_json()
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        position = data.get('position')
        employeeNo = data.get('employeeNo')
        phone_number = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # SQL statement with parameters
        sql = "INSERT INTO OverTimeTable (firstName, lastName, position, employeeNo, phone_number, password, confirm_password) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (firstName, lastName, position, employeeNo, phone_number, password, confirm_password))
        connection.commit()
        return jsonify(data)
    except Exception as e:
        return "Error creating record: " + str(e)

hello()
# Run the Flask application
if __name__ == '__main__':
    # app.run(host='localhost', port=5000)
    app.run(debug=True)

# Close the cursor and connection
cursor.close()
connection.close()