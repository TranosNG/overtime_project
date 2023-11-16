from flask import Flask, request, render_template, jsonify
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

# Execute a query
cursor.execute('SELECT * FROM OvertimeTable')

    # Create operation
@app.route('/overtime/record', methods=['POST'])
def create_overTimeRecord():
    try:
        data = request.get_json()
        name = data.get('name')
        position = data.get('position')
        employeeNo = data.get('employeeNo')
        date = data.get('date')
        decription_of_duties = data.get('decription_of_duties')
        time = data.get('time')
        work_order_no = data.get('work_order_no')

        # SQL statement with parameters
        sql = "INSERT INTO OverTimeTable (name, position, employeeNo, date, description_of_duties, time, work_order_no) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (name, position, employeeNo, date, decription_of_duties, time, work_order_no))
        connection.commit()
        return "Record created successfully."
    except Exception as e:
        return "Error creating record: " + str(e)