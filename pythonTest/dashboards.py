from flask import Flask, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

connection_string = 'DRIVER={Pervasive ODBC Interface};SERVERNAME=DDM-SERVER;DBQ=GLOBALTRA;UID=Master;PWD=master'
conn = pyodbc.connect(connection_string)

# Create a cursor
cursor = conn.cursor()

@app.route('/', methods=['GET'])
def read_records():
    return ('Dashboards API!')

@app.route('/all/po_interval', methods=['GET'])
def Po_Interval():
    try:
        # SQL statement
        sql = "SELECT YEAR(V_PO_HEADER.DATE_ORDER) AS OrderYear,MONTH(V_PO_HEADER.DATE_ORDER) AS OrderMonth,SUM(CASE WHEN CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALAPPROVEDPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALAPPROVEDWEEK,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDWEEK,SUM(CASE WHEN V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALPOWEEK, SUM(CASE WHEN MONTH(V_PO_HEADER.DATE_ORDER) = MONTH(CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALPOMONTH, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND MONTH(V_PO_HEADER.DATE_ORDER) = MONTH(CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALAPPROVEDPOMONTH, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND MONTH(V_PO_HEADER.DATE_ORDER) = MONTH(CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDPOMONTH FROM V_TX_PO_CLOSR_STATUS LEFT JOIN V_PO_HEADER ON V_TX_PO_CLOSR_STATUS.PURCHASE_ORDER = V_PO_HEADER.PURCHASE_ORDER WHERE YEAR(V_PO_HEADER.DATE_ORDER) = YEAR(CURRENT_DATE()) AND MONTH(V_PO_HEADER.DATE_ORDER) = MONTH(CURRENT_DATE()) GROUP BY YEAR(V_PO_HEADER.DATE_ORDER),MONTH(V_PO_HEADER.DATE_ORDER)"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
           result.append({'OrderYear': row[0], 'OrderMonth': row[1], 'TOTALPODAY': row[2], 'TOTALAPPROVEDPODAY': row[3], 'TOTALUNAPPROVEDPODAY': row[4], 'TOTALAPPROVEDWEEK': row[5], 'TOTALUNAPPROVEDWEEK': row[6], 'TOTALPOWEEK': row[7],'TOTALPOMONTH': row[8],'TOTALAPPROVEDPOMONTH': row[9],'TOTALUNAPPROVEDPOMONTH': row[10]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
@app.route('/all/month_sum', methods=['GET'])
def month_sum():
    try:
        # SQL statement
        sql = "SELECT YEAR(V_PO_HEADER.DATE_ORDER) AS OrderYear, MONTHNAME(V_PO_HEADER.DATE_ORDER) AS OrderMonth, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' THEN 1 ELSE 0 END) AS TOTALAPPROVEDPOMONTH, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDPOMONTH FROM V_TX_PO_CLOSR_STATUS LEFT JOIN V_PO_HEADER ON V_TX_PO_CLOSR_STATUS.PURCHASE_ORDER = V_PO_HEADER.PURCHASE_ORDER WHERE YEAR(V_PO_HEADER.DATE_ORDER) = YEAR(CURRENT_DATE()) GROUP BY YEAR(V_PO_HEADER.DATE_ORDER), MONTHNAME(V_PO_HEADER.DATE_ORDER)"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
           result.append({'OrderYear': row[0], 'OrderMonth': row[1], 'TOTALAPPROVEDPOMONTH': row[2], 'TOTALUNAPPROVEDPOMONTH': row[3]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    

@app.route('/avg_po_approval', methods=['GET'])
def avg_po_approval():
    try:
        # SQL statement
        sql = "SELECT MONTHNAME(DATE_ORDER) AS month,FLOOR(AVG(days_to_approval)) AS average_days_to_approval FROM (SELECT PURCHASE_ORDER, DATE_ORDER,APPROVED_DATE, DATEDIFF(DAY, DATE_ORDER, APPROVED_DATE) AS days_to_approval FROM GAB_5326_APRVL) AS po_avg_days_to_approve WHERE YEAR(DATE_ORDER) = YEAR(CURRENT_DATE()) GROUP BY MONTHNAME(DATE_ORDER)"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
           result.append({'month': row[0], 'average_days_to_approval': row[1]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
if __name__ == '__main__':
    app.run(debug=True, port=8050)

    conn.close()