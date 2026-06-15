import pyodbc

def obtener_conexion():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DatosColombiaDB26;'
        'Trusted_Connection=yes;'
    )