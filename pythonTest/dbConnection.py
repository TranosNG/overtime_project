# import pyodbc
# import config

# # Return the sql connection 
# def getConnection():
#      connection = pyodbc.connect("Driver= {"+config.DATABASE_CONFIG["Driver"]+"} ;Server=" + config.DATABASE_CONFIG["Server"] + ";Database=" + config.DATABASE_CONFIG["Database"] + ";Trusted_connection=" + config.DATABASE_CONFIG["trusted_connection"])
#      return connection