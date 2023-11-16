from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors import cross_origin
import pyodbc
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash 
from datetime import timedelta


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, origins=['http://localhost:3000'], methods=['GET', 'POST'], allow_headers=['Content-Type'])


app.config['JWT_SECRET_KEY'] = 'mysecretkey'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1) 
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30) 
jwt = JWTManager(app)
# revoked_tokens = ()

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
cursor.execute('SELECT * FROM OpenWorkOrders')

# Aggregate operation
@app.route('/all/records', methods=['GET'])
def aggregate_records():
    try:
        # SQL statement
        sql = "SELECT * FROM OpenWorkOrders"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'Job': row[0], 'Suffix': row[1], 'Part': row[2], 'Description': row[3], 'Cust_No#': row[4], 'Customer_Name': row[5], 'Order_Qty': row[6], 'Flex_Schedule': row[7], 'WC_Code': row[8], 'LMO': row[9], 'Workcenter_Description': row[10], 'Pieces_Ordered': row[11], 'Pieces_Completed': row[12], 'Job Completion_Status': row[13], 'Last_Job_Record_Date': row[14], 'Work_Order_Due_Date': row[15]})
        # TO RENDER IN AN HTML TEMPLATE
        # return render_template('records.html', records=result)
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
        
# Aggregate Data operation
@app.route('/aggregate/data', methods=['GET'])
def aggregate_data_records():
    try:
        # SQL statement
        sql = "SELECT DISTINCT Customer_Name, SUM(Pieces_Ordered) AS Totl_Pieces_Ordered, SUM(Pieces_Completed) AS Totl_Pieces_Completed, CAST(SUM(Pieces_Completed) * 100.0/SUM(Pieces_Ordered) AS NUMERIC(11,2)) AS Pcent_Job_Progress FROM OpenWorkOrders WHERE Customer_Name <> '' GROUP BY Customer_Name ORDER BY pcent_Job_Progress DESC"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'Customer_Name': row[0], 'Totl_Pieces_Ordered': row[1], 'Totl_Pieces_Completed': row[2], 'Pcent_Job_Progress': row[3]})
        # TO RENDER IN AN HTML TEMPLATE
        # return render_template('records.html', records=result)
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
    # Getting all completed orders
@app.route('/completed/records', methods=['GET'])
def completed_records():
    try:
        # SQL statement
        sql = "SELECT * FROM OpenWorkOrders WHERE Job_Completion_Status = 'completed'"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'Job': row[0], 'Suffix': row[1], 'Part': row[2], 'Description': row[3], 'Cust_No#': row[4], 'Customer_Name': row[5], 'Order_Qty': row[6], 'Flex_Schedule': row[7], 'WC_Code': row[8], 'LMO': row[9], 'Workcenter_Description': row[10], 'Pieces_Ordered': row[11], 'Pieces_Completed': row[12], 'Job Completion_Status': row[13], 'Last_Job_Record_Date': row[14], 'Work_Order_Due_Date': row[15]})
        # TO RENDER IN AN HTML TEMPLATE
        # return render_template('records.html', records=result)
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
    # Create operation
@app.route('/overtime/record', methods=['POST'])
def create_overTimeRecord():
    try:
        data = request.get_json()
        EMPLOYEENO = data.get('EMPLOYEENO')
        DUTY_DESC = data.get('DUTY_DESC')
        OVT_DAY = data.get('OVT_DAY')
        OVT_DATE = data.get('OVT_DATE')
        START_HR = data.get('START_HR')
        END_HR = data.get('END_HR')
        WRK_ORD_NO = data.get('WRK_ORD_NO')

        #Joining the multiple entries into a string #For description_of-duties
        DUTY_DESC = data["DUTY_DESC"]
        DUTY_DESC_STR= (DUTY_DESC)
        # description_of_duties_str= ",".join(description_of_duties)

        #Joining the multiple entries into a string #For work_order_no
        WRK_ORD_NO = data["WRK_ORD_NO"]
        WRK_ORD_NO_STR= (WRK_ORD_NO)
        # work_order_no_str= ",".join(work_order_no)

        # SQL statement with parameters
        sql = "INSERT INTO OverTimeTable (EMPLOYEENO, DUTY_DESC, OVT_DAY, OVT_DATE, START_HR, END_HR, WRK_ORD_NO) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (EMPLOYEENO, DUTY_DESC_STR, OVT_DAY, OVT_DATE, START_HR, END_HR, WRK_ORD_NO_STR))
        connection.commit()
        return jsonify(data)
    except Exception as e:
        return "Error creating record: " + str(e)
    
    
  # Aggregate operation
@app.route('/overtime/hours', methods=['GET'])
def overtime_totl_hours():
    try:
        # SQL statement
        sql = "SELECT overtime_hour_to - overtime_hour_from AS Total_hour FROM OverTime_total_hours"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'Total_hour': row[0]})
        # TO RENDER IN AN HTML TEMPLATE
        # return render_template('records.html', records=result)
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
    
      # Getting all overtime records
@app.route('/all/overtime_records', methods=['GET'])
def Overtime_records():
    try:
        # SQL statement
        sql = "SELECT * FROM Overtime_totl_detail"
                # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
           result.append({'ID': row[0], 'EMPLOYEENO': row[1], 'OVT_DAY': row[2], 'DUTY_DESC': row[3], 'OVT_DATE': row[4], 'START_HR': row[5], 'END_HR': row[6], 'WRK_ORD_NO': row[7], 'TOTL_HR_WRKED': row[8], 'TOTL_PAY_AMT': row[9]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)

    
# create overtime user account
@app.route('/overtime/account', methods=['POST'])
def create_overTimeAccount():
    try:
        data = request.get_json()
        FIRSTNAME = data.get('FIRSTNAME')
        LASTNAME = data.get('LASTNAME')
        POSITION = data.get('POSITION')
        EMPLOYEENO = data.get('EMPLOYEENO')
        PHON_NO = data.get('PHON_NO')
        PWD = data.get('PWD')
        COFM_PWD = data.get('COFM_PWD')

        # checking if the employee no already exist
        cursor.execute(f"SELECT * FROM T_OVERTIME_ACCOUNT WHERE employeeNo = '{EMPLOYEENO}'")
        existing_employeeNo = cursor.fetchone()

        if existing_employeeNo:
            return jsonify({'message': 'Employee No already exist'}), 400

        # SQL statement with parameters
        sql = "INSERT INTO T_OVERTIME_ACCOUNT (FIRSTNAME, LASTNAME, POSITION, EMPLOYEENO, PHON_NO, PWD, COFM_PWD) VALUES (?, ?, ?, ?, ?, ?, ?)"
        # Execute the SQL statement with the parameters
        cursor.execute(sql, (FIRSTNAME, LASTNAME, POSITION, EMPLOYEENO, PHON_NO, PWD, COFM_PWD))
        connection.commit()
        return jsonify(data)
    except Exception as e:
        return "Error creating record: " + str(e)
        
@app.route('/overtime/login', methods=['POST'])
def login():
    data = request.get_json()
    EMPLOYEENO = data.get('EMPLOYEENO')
    PWD = data.get('PWD')

    try:
        cursor = connection.cursor()

        # Check if the provided username and password match a user in the table
        cursor.execute(f"SELECT * FROM T_OVERTIME_ACCOUNT WHERE EMPLOYEENO = '{EMPLOYEENO}' AND PWD = '{PWD}'")
        user = cursor.fetchone()

        if user:
            # Login successful
            access_token = create_access_token(identity=EMPLOYEENO)
            refresh_token = create_refresh_token(identity=EMPLOYEENO)
            return jsonify({'access_token': access_token},
                           {'refresh_token': refresh_token},
                           {'message': 'Login successful'}), 200
        else:
            # Invalid credentials
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        return jsonify({'message': 'Error during login: ' + str(e)}), 500
    
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(current_user)
    # return jsonify({'message': f'Protected route for user: {current_user}'}), 200

@app.route('/me', methods=['GET'])
@jwt_required()
def me():
    return{'user': "me"}

# endpoint to retrieve authenticated users details
@app.route('/api/overtime_user', methods=['GET'])
@jwt_required()  # Requires authentication token
def overtime_details():
    current_user = get_jwt_identity()
    
    sql = "SELECT * FROM MERGED_RECRDS WHERE EMPLOYEENO = ? "
    cursor.execute(sql, current_user)
        # Fetch the first row as user details
    user_details = cursor.fetchall()

    if not user_details:
        return jsonify({'message': 'User not found'}), 404
    # Example response with user details
    usersResult = []
    for user in user_details:

        usersResult.append({
        'FIRSTNAME': user.FIRSTNAME,
        'LASTNAME': user.LASTNAME,
        'POSITION': user.POSITION,
        'EMPLOYEENO': user.EMPLOYEENO,
        'PHON_NO': user.PHON_NO,
        'OVT_DAY': user.OVT_DAY,
        'DUTY_DESC': user.DUTY_DESC,
        'OVT_DATE': user.OVT_DATE,
        'START_HR': user.START_HR,
        'END_HR': user.END_HR,
        'WRK_ORD_NO': user.WRK_ORD_NO,
        'TOTL_HR_WORKED': user.TOTL_HR_WRKED,
        'TOTL_PAY_AMT': user.TOTL_PAY_AMT
        })

        # FIRSTNAME = user.FIRSTNAME
        # LASTNAME = user.LASTNAME
        # POSITION = user.POSITION
        # EMPLOYEENO = user.EMPLOYEENO
        # PHON_NO = user.PHON_NO
        # OVT_DAY = user.OVT_DAY
        # DUTY_DESC = user.DUTY_DESC
        # START_HR = user.START_HR
        # END_HR = user.END_HR
        # WRK_ORD_NO = user.WRK_ORD_NO
        # TOTL_HR_WORKED = user.TOTL_HR_WRKED
        # TOTL_PAY_AMT = user.TOTL_PAY_AMT
    # user_details = {
    #     # 'ID': user_details[0],
    #     'FIRSTNAME': user_details[0],
    #     'LASTNAME': user_details[1],
    #     'POSITION': user_details[2],
    #     'EMPLOYEENO': user_details[3],
    #     'PHON_NO': user_details[4],
    #     'OVT_DAY': user_details[5],
    #     'DUTY_DESC': user_details[6],
    #     'OVT_DATE': user_details[7],
    #     'START_HR': user_details[8],
    #     'END_HR': user_details[9],
    #     'WRK_ORD_NO': user_details[10],
    #     'TOTL_HR_WORKED': user_details[11],
    #     'TOTL_PAY_AMT': user_details[12]
    # }
    
    response = jsonify(usersResult)
    return response


# @app.route('/logout', methods=['DELETE'])
# @jwt_required
# def logout():
#     jti = get_raw_jwt()['jti']
#     revoked_tokens.add(jti)
#     return jsonify({'message': 'Logout successful'}), 200


# @jwt.token_in_blacklist_loader
# def check_token_revoked(decoded_token):
#     jti = decoded_token['jti']
#     return jti in revoked_tokens







aggregate_records()
aggregate_data_records()
completed_records()
create_overTimeRecord()
# overtime_details()
overtime_totl_hours()
Overtime_records()
# create_overTimeAccount()
# login()
    
    # Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    
# Close the cursor and connection
cursor.close()
connection.close()

