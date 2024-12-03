import os

class Config:
    #connection string
    SQLALCHEMY_DATABASE_URI=(
        'mssql+pyodbc:///?odbc_connect='
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DESKTOP-2SLCV1V;'
        'database=Final_Project;'
        'Trusted_connection=yes;'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
c1 = Config()
print(c1.SQLALCHEMY_DATABASE_URI)    
print(c1.SQLALCHEMY_TRACK_MODIFICATIONS)    
