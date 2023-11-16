from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import pyodbc
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config['JWT_SECRET_KEY'] = 'mysecretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) 
jwt = JWTManager(app)
revoked_tokens = ()

# Establish the connection
connection_string = 'DRIVER={Pervasive ODBC Interface};SERVERNAME=DDM-SERVER;DBQ=GLOBALTST;UID=Master;PWD=master'
conn = pyodbc.connect(connection_string)

# Create a cursor
cursor = conn.cursor()

# Read operation
@app.route('/data/jobs', methods=['GET'])
def read_records():
    try:
        # SQL statement
        sql = "SELECT EMPLOYEE, SUFFIX FROM JOB_DETAIL LIMIT 5"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'EMPLOYEE': row[0], 'SUFFIX': row[1]})
        
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)

# create overtime user account
@app.route('/api/ovt_reg', methods=['POST'])
def create_overTimeAccount():
    try:
        data = request.get_json()
        FIRST_NAME = data.get('FIRST_NAME')
        LAST_NAME = data.get('LAST_NAME')
        EMPL_POSITION = data.get('EMPL_POSITION')
        EMPLOYEE_NO = data.get('EMPLOYEE_NO')
        PHONE_NO = data.get('PHONE_NO')
        PWD = data.get('PWD')
        COFM_PWD = data.get('COFM_PWD')

        # checking if the employee no already exist
        cursor.execute(f"SELECT * FROM MT_OVT_REG WHERE EMPLOYEE_NO = '{EMPLOYEE_NO}'")
        existing_employeeNo = cursor.fetchone()

        if existing_employeeNo:
            return jsonify({'message': 'Employee No already exist'}), 400

        # SQL statement with parameters
        sql = "INSERT INTO MT_OVT_REG (FIRST_NAME, LAST_NAME, EMPL_POSITION, EMPLOYEE_NO, PHONE_NO, PWD, COFM_PWD) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (FIRST_NAME, LAST_NAME, EMPL_POSITION, EMPLOYEE_NO, PHONE_NO, PWD, COFM_PWD))
        conn.commit()
        return jsonify(data)
    except Exception as e:
        return "Error creating record: " + str(e)
    
# Login Endpoint
@app.route('/api/ovt_login', methods=['POST'])
def login():
    data = request.get_json()
    EMPLOYEE_NO = data.get('EMPLOYEE_NO')
    PWD = data.get('PWD')

    try:
        cursor = conn.cursor()

        # Check if the provided username and password match a user in the table
        cursor.execute(f"SELECT * FROM MT_OVT_REG WHERE EMPLOYEE_NO = '{EMPLOYEE_NO}' AND PWD = '{PWD}'")
        user = cursor.fetchone()

        if user:
            # Login successful
            access_token = create_access_token(identity=EMPLOYEE_NO)
            refresh_token = create_refresh_token(identity=EMPLOYEE_NO)
            return jsonify({'access_token': access_token},
                           {'refresh_token': refresh_token},
                           {'message': 'Login successful'}), 200
        else:
            # Invalid credentials
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'message': 'Error during login: ' + str(e)}), 500

    
    # Create operation
@app.route('/api/ovt_entries', methods=['POST'])
def create_overTimeRecord():
    try:
        data = request.get_json()
        EMPLOYEE_NO = data.get('EMPLOYEE_NO')
        DUTY_DESC = data.get('DUTY_DESC')
        OVT_DAY = data.get('OVT_DAY')
        OVT_DATE = data.get('OVT_DATE')
        START_HR = data.get('START_HR')
        END_HR = data.get('END_HR')
        WORK_ORD_NO = data.get('WORK_ORD_NO')

        #Joining the multiple entries into a string #For description_of-duties
        DUTY_DESC = data["DUTY_DESC"]
        DUTY_DESC_STR= (DUTY_DESC)
        # description_of_duties_str= ",".join(description_of_duties)

        #Joining the multiple entries into a string #For work_order_no
        WORK_ORD_NO = data["WORK_ORD_NO"]
        WORK_ORD_NO_STR= (WORK_ORD_NO)
        
        # SQL statement with parameters
        sql = "INSERT INTO MT_OVT_ENTRIES (EMPLOYEE_NO, DUTY_DESC, OVT_DAY, OVT_DATE, START_HR, END_HR, WORK_ORD_NO) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (EMPLOYEE_NO, DUTY_DESC_STR, OVT_DAY, OVT_DATE, START_HR, END_HR, WORK_ORD_NO_STR))
        conn.commit()
        return jsonify(data)
    except Exception as e:
        return "Error creating record: " + str(e)
    

# endpoint to retrieve authenticated users details
@app.route('/api/reg_entries', methods=['GET'])
@jwt_required()  # Requires authentication token
def overtime_details():
    current_user = get_jwt_identity()
    
    sql = "SELECT * FROM V_MT_REG_ENTRIES WHERE EMPLOYEE_NO = ? "
    cursor.execute(sql, current_user)
        # Fetch the first row as user details
    user_details = cursor.fetchall()

    if not user_details:
        return jsonify({'message': 'User not found'}), 404
    # Example response with user details
    usersResult = []
    for user in user_details:

        usersResult.append({
        'ID': user.ID,
        'FIRST_NAME': user.FIRST_NAME,
        'LAST_NAME': user.LAST_NAME,
        'EMPL_POSITION': user.EMPL_POSITION,
        'EMPLOYEE_NO': user.EMPLOYEE_NO,
        'PHONE_NO': user.PHONE_NO,
        'OVT_DAY': user.OVT_DAY,
        'DUTY_DESC': user.DUTY_DESC,
        'OVT_DATE': user.OVT_DATE,
        'START_HR': user.START_HR,
        'END_HR': user.END_HR,
        'WORK_ORD_NO': user.WORK_ORD_NO,
        'TOTAL_HR_WORKED': user.TOTAL_HR_WORKED,
        'TOTAL_PAY_AMT': user.TOTAL_PAY_AMT
        })
    response = jsonify(usersResult)
    return response






if __name__ == '__main__':
    app.run(debug=True, port=8080)

conn.close()


