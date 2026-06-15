import pyodbc

try:
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DatosColombiaDB26;'  
        'Trusted_Connection=yes;' 
    )
    
    cursor = conexion.cursor()
    
    
    cursor.execute("SELECT CodigoDepartamento, Departamento, municipio, ano, totalimpuesto FROM registros")
    filas = cursor.fetchall()
    
    print("\n--- REGISTROS EN LA BASE DE DATOS ---")
    
    
    print(f"{'ID':<6} | {'DEPARTAMENTO':<25} | {'MUNICIPIO':<25} | {'AÑO':<6} | {'TOTAL IMP.'}")
    print("-" * 85)
    
    for fila in filas:
       
        id_dep      = fila[0] if fila[0] is not None else "N/A"
        dep         = fila[1] if fila[1] is not None else "Sin Datos"
        muni        = fila[2] if fila[2] is not None else "Sin Datos"
        ano_reg     = fila[3] if fila[3] is not None else 0
        total_imp   = fila[4] if fila[4] is not None else 0
        
        
        print(f"{id_dep:<6} | {dep:<25} | {muni:<25} | {ano_reg:<6} | ${total_imp:,.2f}")
        
    print("-" * 85)
    print(f"Total: {len(filas)} registros encontrados.\n")

except Exception as e:
    print("Ocurrió un error al consultar los datos:", e)

finally:
    if 'conexion' in locals() and conexion is not None:
        cursor.close()
        conexion.close()