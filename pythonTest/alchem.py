from flask import Flask, jsonify, request
from sqlalchemy import create_engine, select
from sqlalchemy import Table, MetaData
from flask_cors import CORS
# from configparser import ConfigParser

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# config = ConfigParser()
# config.read("database.cfg")

# username = config["GLOBALTST"]["Master"]
# password = config["GLOBALTST"]["master"]

engine = create_engine("pervasive:///?odbc_connect=DRIVER={Pervasive ODBC Interface};SERVERNAME=DDM-SERVER;DBQ=GLOBALTST;UID={Master};PWD={master}")
connection = engine.connect()

# connection_string = "DRIVER={Pervasive ODBC Interface};SERVERNAME=DDM-SERVER;DBQ=GLOBALTST;UID=Master;PWD=master"
# engine = create_engine('mssql+pyodbc:///?odbc_connect=' + connection_string)
# connection = engine.connect()

@app.route('/dt/dict/job', methods=['GET'])
def dt_dict_job():
    metadata = MetaData()
    my_table = Table('JOB_HEADER', metadata, autoload=True, autoload_with=engine)
    limit_value = 10
    stmt = select([my_table]).limit(limit_value)
    result = connection.execute(stmt).fetchall()
    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True, port=8070)

connection.close()