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

# class Delete:
#     def func_DeleteData(self):
#         # Get the sql connection
#         connection = cursor.getConnection()

#         id = input('Enter Employee Id = ')
    
#         try:
#            # Get record which needs to be deleted
#            sql = "Select * From Employee Where Id = ?" 
#            cursor = connection.cursor()
#            cursor.execute(sql, [id])
#            item = cursor.fetchone()
#            print('Data Fetched for Id = ', id)
#            print('ID\t\t Name\t\t\t Age')
#            print('-------------------------------------------')       
#            print(' {}\t\t {} \t\t\t{} '.format(item[0], item[1], item[2]))
#            print('-------------------------------------------')
#            confirm = input('Are you sure to delete this record (Y/N)?')

#            # Delete after confirmation
#            if confirm == 'Y':
#                deleteQuery = "Delete From Employee Where Id = ?"
#                cursor.execute(deleteQuery,[id])
#                connection.commit()
#                print('Data deleted successfully!')
#            else:
#                 print('Wrong Entry')
#         except:
#             print('Somethng worng, please check')
#         finally:
#             connection.close()