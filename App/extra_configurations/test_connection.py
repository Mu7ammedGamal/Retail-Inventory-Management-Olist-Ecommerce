import pyodbc
server ='DESKTOP-2SLCV1V'
database = 'Final_Project'
# dreate connection string for windows auth
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_connection=yes'
#conn = pyodbc.connect(conn_str)

try:
    # Estblish connection to database
    with pyodbc.connect(conn_str) as conn:
        print('Connection Successful')


except pyodbc.Error as e:

    print("Error connection to the database : ")
    print(e)