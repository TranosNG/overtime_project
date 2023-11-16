from flask import Flask, jsonify
import pyodbc
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

connection_string = 'DRIVER={Pervasive ODBC Interface};SERVERNAME=DDM-SERVER;DBQ=GLOBALTRA;UID=Master;PWD=master'
conn = pyodbc.connect(connection_string)

# Create a cursor
cursor = conn.cursor()

@app.route('/data/jobs', methods=['GET'])
def read_records():
    return ('Welcome!')   
        
@app.route('/open/work', methods=['GET'])
def open_work():
    try:
        # SQL statement
        sql = "SELECT  V_MT_DT_JOB_PARENTS.JOB, V_MT_DT_JOB_PARENTS.PART, V_MT_DT_JOB_PARENTS.PRODUCT_LINE, V_MT_DT_JOB_PARENTS.DESCRIPTION,V_MT_DT_JOB_PARENTS.CUSTOMER,V_MT_DT_JOB_PARENTS.DATE_OPENED, V_MT_DT_JOB_PARENTS.DATE_DUE, V_MT_DT_JOB_PARENTS.SALES_ORDER,V_MT_JOB_CUSTOMERS.NAME_CUSTOMER,V_MT_DICT_LABOUR.PCSORDER_1, V_MT_DICT_LABOUR.PCSCOMPLTD_1, V_MT_DICT_LABOUR.PERCENT_COMPLTD,V_MT_DICT_LABOUR.L_STATUS, TX_JOBS_PEND_SEQ.PEND_LABOUR_SEQ FROM V_MT_DT_JOB_PARENTS INNER JOIN V_MT_JOB_CUSTOMERS ON V_MT_DT_JOB_PARENTS.CUSTOMER = V_MT_JOB_CUSTOMERS.CUSTOMER INNER JOIN V_MT_DICT_LABOUR ON  V_MT_DT_JOB_PARENTS.JOB = V_MT_DICT_LABOUR.JOB INNER JOIN TX_JOBS_PEND_SEQ ON V_MT_DICT_LABOUR.JOB = TX_JOBS_PEND_SEQ.JOB LIMIT 10"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'JOB': row[0],'PART': row[1],'PRODUCT_LINE': row[2],'DESCRIPTION': row[3], 'CUSTOMER': row[4],'DATE_OPENED': row[5],'DATE_DUE': row[6], 'SALES_ORDER': row[7], 'NAME_CUSTOMER': row[8], 'PCSORDER_1': row[9], 'PCSCOMPLTD_1': row[10], 'PERCENT_COMPLTD': row[11], 'L_STATUS': row[12], 'PEND_LABOUR_SEQ': row[13]})
        
        # cursor.close()
        # conn.close()
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
@app.route('/dt/dict/job', methods=['GET'])
def dt_dict_job():
    try:
        # SQL statement
        sql = "SELECT * FROM V_MT_DT_DICT LIMIT 50"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'JOB': row[0], 'SUFFIX': row[1], 'PART': row[2], 'DESCRIPTION': row[3], 'QTY_ORDER': row[4], 'WORKCENTER': row[5], 'LMO': row[6], 'WC_NAME': row[7], 'FLOW_SEQ': row[8], 'JOB_FLOW_WC_$': row[9], 'JOB_WC_$': row[10], 'LATEST_ET': row[11], 'PCSORDER_1': row[12], 'PCSCOMPLTD_1': row[13], 'PERCENT_COMPLTD': row[14], 'L_STATUS': row[15]})

        # cursor.close()
        # conn.close()
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        # SQL statement
        # sql = "SELECT * FROM V_MT_OPEN_WORK LIMIT 10"
        sql= "SELECT DISTINCT A1.CUSTOMER, C1.NAME_CUSTOMER FROM V_JOB_HEADER AS A1 LEFT JOIN V_CUSTOMER_MASTER AS C1 ON A1.CUSTOMER = C1.CUSTOMER WHERE A1.SUFFIX IN ('000', '') AND A1.PRODUCT_LINE IN ('10', '20', '25', '30', '35', '40', '45', '50', '52', '60', 'MB') AND A1.DATE_CLOSED = '1900-01-01' AND PART NOT LIKE '%INDIRECT%' ORDER BY A1.CUSTOMER LIMIT 10"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'CUSTOMER': row[0],'NAME_CUSTOMER': row[1]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
@app.route('/api/all/jobs', methods=['GET'])
def all_jobs():
    try:
        # SQL statement
        sql = "SELECT  V_MT_DT_JOB_PARENTS.JOB, V_MT_DT_JOB_PARENTS.PART, V_MT_DT_JOB_PARENTS.PRODUCT_LINE, V_MT_DT_JOB_PARENTS.DESCRIPTION,V_MT_DT_JOB_PARENTS.CUSTOMER,V_MT_DT_JOB_PARENTS.DATE_OPENED, V_MT_DT_JOB_PARENTS.DATE_DUE, V_MT_DT_JOB_PARENTS.SALES_ORDER,V_MT_DT_DICT.QTY_ORDER,V_MT_DT_DICT.WORKCENTER,V_MT_DT_DICT.WC_NAME,V_MT_DT_DICT.FLOW_SEQ,V_MT_DT_DICT.JOB_FLOW_WC_$,V_MT_DT_DICT.JOB_WC_$,V_MT_JOB_CUSTOMERS.NAME_CUSTOMER,V_MT_DICT_LABOUR.PCSORDER_1, V_MT_DICT_LABOUR.PCSCOMPLTD_1, V_MT_DICT_LABOUR.PERCENT_COMPLTD,V_MT_DICT_LABOUR.L_STATUS, TX_JOBS_PEND_SEQ.PEND_LABOUR_SEQ FROM V_MT_DT_JOB_PARENTS INNER JOIN V_MT_DT_DICT ON V_MT_DT_JOB_PARENTS.JOB = V_MT_DT_DICT.JOB INNER JOIN V_MT_JOB_CUSTOMERS ON V_MT_DT_JOB_PARENTS.CUSTOMER = V_MT_JOB_CUSTOMERS.CUSTOMER INNER JOIN V_MT_DICT_LABOUR ON  V_MT_DT_JOB_PARENTS.JOB = V_MT_DICT_LABOUR.JOB INNER JOIN TX_JOBS_PEND_SEQ ON V_MT_DICT_LABOUR.JOB = TX_JOBS_PEND_SEQ.JOB"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({'JOB': row[0],'PART': row[1],'PRODUCT_LINE': row[2],'DESCRIPTION': row[3], 'CUSTOMER': row[4],'DATE_OPENED': row[5],'DATE_DUE': row[6], 'SALES_ORDER': row[7],'QTY_ORDER': row[8], 'WORKCENTER': row[9], 'WC_NAME': row[10], 'FLOW_SEQ': row[11], 'JOB_FLOW_WC_$': row[12], 'JOB_WC_$': row[13], 'NAME_CUSTOMER': row[14], 'PCSORDER_1': row[15], 'PCSCOMPLTD_1': row[16], 'PERCENT_COMPLTD': row[17], 'L_STATUS': row[18], 'PEND_LABOUR_SEQ': row[19]})

        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
# Getting PO raised at interval
# @app.route('/all/po_interval', methods=['GET'])
# def Po_Interval():
#     try:
#         # SQL statement
#         sql = "SELECT YEAR(V_PO_HEADER.DATE_ORDER) AS OrderYear,MONTHNAME(V_PO_HEADER.DATE_ORDER) AS OrderMonth, SUM(CASE WHEN CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURDATE() THEN 1 ELSE 0 END) AS TOTALPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURDATE() THEN 1 ELSE 0 END) AS TOTALAPPROVEDPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURDATE() THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDPODAY, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURDATE()) + 1, CURDATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURDATE()), CURDATE()) THEN 1 ELSE 0 END) AS TOTALAPPROVEDWEEK, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURDATE()) + 1, CURDATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURDATE()), CURDATE()) THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDWEEK, SUM(CASE WHEN V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURDATE()) + 1, CURDATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURDATE()), CURDATE())THEN 1 ELSE 0 END) AS TOTALPOWEEK FROM V_TX_PO_CLOSR_STATUS LEFT JOIN V_PO_HEADER ON V_TX_PO_CLOSR_STATUS.PURCHASE_ORDER = V_PO_HEADER.PURCHASE_ORDER WHERE YEAR(V_PO_HEADER.DATE_ORDER) = YEAR(CURDATE()) AND MONTH(V_PO_HEADER.DATE_ORDER) = MONTH(CURDATE()) GROUP BY YEAR(V_PO_HEADER.DATE_ORDER), MONTHNAME(V_PO_HEADER.DATE_ORDER);"
#         # Execute the SQL statement
#         cursor.execute(sql)
#         rows = cursor.fetchall()
#         result = []
#         for row in rows:
#            result.append({'OrderYear': row[0], 'OrderMonth': row[1], 'TOTALPODAY': row[2], 'TOTALAPPROVEDPODAY': row[3], 'TOTALUNAPPROVEDPODAY': row[4], 'TOTALAPPROVEDWEEK': row[5], 'TOTALUNAPPROVEDWEEK': row[6], 'TOTALPOWEEK': row[7]})
#         return jsonify(result)
#     except Exception as e:
#         return "Error reading records: " + str(e)

@app.route('/all/po_interval', methods=['GET'])
def Po_Interval():
    try:
        # SQL statement
        sql = "SELECT COUNT(DISTINCT V_PO_HEADER.PURCHASE_ORDER) AS TOTALPOMONTH, MONTHNAME(V_PO_HEADER.DATE_ORDER) AS PO_MONTH, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' THEN 1 ELSE 0 END) AS APPROVEDPOMONTH, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' THEN 1 ELSE 0 END) AS UNAPPROVEDPOMONTH, SUM(CASE WHEN CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALPODAY, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALAPPROVEDPODAY,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND CAST(V_PO_HEADER.DATE_ORDER AS DATE) = CURRENT_DATE() THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDPODAY, SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Closed' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALAPPROVEDWEEK,SUM(CASE WHEN V_TX_PO_CLOSR_STATUS.STATUS = 'Open' AND V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALUNAPPROVEDWEEK, SUM(CASE WHEN V_PO_HEADER.DATE_ORDER >= DATEADD(day, -DAYOFWEEK(CURRENT_DATE()) + 1, CURRENT_DATE()) AND V_PO_HEADER.DATE_ORDER <= DATEADD(day, 7 - DAYOFWEEK(CURRENT_DATE()), CURRENT_DATE()) THEN 1 ELSE 0 END) AS TOTALPOWEEK FROM V_PO_HEADER JOIN V_TX_PO_CLOSR_STATUS ON V_TX_PO_CLOSR_STATUS.PURCHASE_ORDER = V_PO_HEADER.PURCHASE_ORDER WHERE YEAR(V_PO_HEADER.DATE_ORDER) = YEAR(CURDATE()) GROUP BY MONTHNAME(V_PO_HEADER.DATE_ORDER)"
        # Execute the SQL statement
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = []
        for row in rows:
           result.append({'TOTALPOMONTH': row[0], 'PO_MONTH': row[1], 'APPROVEDPOMONTH': row[2], 'UNAPPROVEDPOMONTH': row[3], 'TOTALPODAY': row[4], 'TOTALAPPROVEDPODAY': row[5], 'TOTALUNAPPROVEDPODAY': row[6], 'TOTALAPPROVEDWEEK': row[7], 'TOTALUNAPPROVEDWEEK': row[8], 'TOTALPOWEEK': row[9]})
        return jsonify(result)
    except Exception as e:
        return "Error reading records: " + str(e)
    
if __name__ == '__main__':
    app.run(debug=True, port=8000)

    conn.close()



    