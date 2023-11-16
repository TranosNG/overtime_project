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

# # Execute a query
# # cursor.execute('SELECT * FROM modinat_Table')

# class Create:
#     def func_CreateData(self):

#         # Get the sql connection
#         connection = cursor.getConnection()

#         TITLE = input('Enter Title =')      
#         AGE = input('Enter Age =')        
#         ADDDRESS = input('Enter Adddress =')        
#         SALARY = input('Enter Salary =')       

#         try:
#            query = "Insert Into modinat_Table(TITLE, AGE, ADDDRESS, SALARY) Values(?,?)" 
#            cursor = connection.cursor()

#            # Execute the sql query
#            cursor.execute(query, [TITLE, AGE, ADDDRESS, SALARY])

#            # Commit the data
#            connection.commit()
#            print('Data Saved Successfully')

#         except:
#              print('Somethng worng, please check')

#         finally:
#            # Close the connection
#            connection.close()