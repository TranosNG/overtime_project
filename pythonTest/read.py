# import pyodbc

# # Specify the connection details
# server = 'JUNIOR-ERP-ADMI'
# database = 'modinatDB'
# trusted_connection = 'yes'  # Set to 'yes' for trusted connection
# driver = '{SQL Server}'  # The appropriate driver for your database

# # Establish the connection
# connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
# connection = pyodbc.connect(connection_string)

# # Create a cursor
# cursor = connection.cursor()

# class Read:
#     def func_ReadData(self):   
#         # Get the sql connection
#         connection = cursor.getConnection()
#         cursor = connection.cursor()

#         # Execute the sql query
#         cursor.execute('Select * from modinat_Table')

#         # Print the data
#         for row in cursor:
#             print('row = %r' % (row,))