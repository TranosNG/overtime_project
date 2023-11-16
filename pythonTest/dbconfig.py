from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pyodbc


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Specify the connection details
server = 'JUNIOR-ERP-ADMI'
database = 'modinatDB'
trusted_connection = 'yes'  # Set to 'yes' for trusted connection
driver = 'SQL Server'  # The appropriate driver for your database

# Establish the connection
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
connection = pyodbc.connect(connection_string)

# Create a cursor
cursor = connection.cursor()

# Execute a query
cursor.execute('SELECT * FROM modinat_Table')

@app.route('/', methods=['GET'])
def hello():
      return "hello world" 

# Create operation
@app.route('/record', methods=['POST'])
def create_record():
    try:
        data = request.get_json()
        ID = data.get('ID')
        TITLE = data.get('TITLE')
        AGE = data.get('AGE')
        ADDDRESS = data.get('ADDDRESS')
        SALARY = data.get('SALARY')

        # SQL statement with parameters
        sql = "INSERT INTO modinat_Table (ID, TITLE, AGE, ADDDRESS, SALARY) VALUES (?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (ID, TITLE, AGE, ADDDRESS, SALARY))
        connection.commit()
        return "Record created successfully."
    except Exception as e:
        return "Error creating record: " + str(e)
    
# New route for handling form submission
@app.route('/new_record', methods=['GET', 'POST'])
def new_record():
    if request.method == 'POST':
        try:
            ID = request.form.get('ID')
            TITLE = request.form.get('TITLE')
            AGE = request.form.get('AGE')
            ADDDRESS = request.form.get('ADDDRESS')
            SALARY = request.form.get('SALARY')

            # SQL statement with parameters
            sql = "INSERT INTO modinat_Table (ID, TITLE, AGE, ADDDRESS, SALARY) VALUES (?, ?, ?, ?, ?)"
            # Execute the SQL statement with the parameters
            cursor.execute(sql, (ID, TITLE, AGE, ADDDRESS, SALARY))
            connection.commit()
            return "Record created successfully."
        except Exception as e:
            return "Error creating record: " + str(e)
    else:
        return render_template('new_record.html')


# Read operation
@app.route('/data/records', methods=['GET'])
def read_records():
    try:
        # SQL statement
        sql = "SELECT * FROM modinat_Table"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'ID': row[0], 'TITLE': row[1], 'AGE': row[2], 'ADDDRESS': row[3], 'SALARY': row[4]})
        # TO RENDER IN AN HTML TEMPLATE
        # return render_template('records.html', records=result)
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)

# Update operation
@app.route('/record/update', methods=['PUT'])
def update_record():
    try:
        data = request.get_json()
        modinatTable_id = data.get('id')
        ID = data.get('ID')
        TITLE = data.get('TITLE')
        AGE = data.get('AGE')
        ADDDRESS = data.get('ADDDRESS')
        SALARY = data.get('SALARY')

        # SQL statement with parameters
        sql = "UPDATE modinat_Table SET ID=?, TITLE=?, AGE=?, ADDDRESS=?, SALARY=? WHERE id=?"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (ID, TITLE, AGE, ADDDRESS, SALARY, modinatTable_id))
        connection.commit()
        return "Record updated successfully."
    except Exception as e:
        return "Error updating record: " + str(e)


# Delete operation
@app.route('/record/delete', methods=['DELETE'])
def delete_record():
    try:
        data = request.get_json()
        modinatTable_id = data.get('id')
        

        # SQL statement with parameter
        sql = "DELETE FROM modinat_Table WHERE id=?"
        # Execute the SQL statement with the parameter
        cursor.execute(sql, (modinatTable_id,))
        connection.commit()
        return "Record deleted successfully."
    except Exception as e:
        return "Error deleting record: " + str(e)



create_record()
# new_record()
read_records()
hello()
update_record()
delete_record()

# Run the Flask application
if __name__ == '__main__':
    # app.run(host='localhost', port=5000)
    app.run(debug=True)

# Close the cursor and connection
cursor.close()
connection.close()
