import requests
import pyodbc

conexion = None
try:
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DatosColombiaDB26;'  
        'Trusted_Connection=yes;' 
    )
    print("Conexión exitosa a SQL Server")
except Exception as e:
    print("Error al conectar a SQL Server:", e)

if conexion is not None:
    try:
       
        url = "https://www.datos.gov.co/resource/7s8e-7zcb.json"
        respuesta = requests.get(url)
        registros = respuesta.json() 
        
        print("Campos reales de la API:", registros[0].keys())
        
        cursor = conexion.cursor()
        insertados = 0

        print("Insertando registros en la base de datos...")
        
        for fila in registros:
        
            Departamento = str(fila.get('departamento', 'Desconocido'))
            
            
            try:
                ano = int(fila.get('ano', fila.get('vigencia', 0)))
            except (ValueError, TypeError): 
                ano = 0
            
            
            municipio = str(fila.get('municipio', 'Desconocido')) 
            
            
            try:
                
                txt1 = str(fila.get('impuestomes1', '0')).replace('.', '').strip()
                txt2 = str(fila.get('impuestomes2', '0')).replace('.', '').strip()
                txt3 = str(fila.get('impuestomes3', '0')).replace('.', '').strip()
                
                
                impuestomes1 = int(txt1) if txt1.isdigit() else 0
                impuestomes2 = int(txt2) if txt2.isdigit() else 0
                impuestomes3 = int(txt3) if txt3.isdigit() else 0
                
                trimestre = int(fila.get('trimestre', 1))
            except (ValueError, TypeError):
                impuestomes1 = 0
                impuestomes2 = 0
                impuestomes3 = 0
                trimestre = 1
            
            
            totalimpuesto = impuestomes1 + impuestomes2 + impuestomes3
          
        
            cursor.execute("""
                INSERT INTO registros (Departamento, ano, municipio, impuestomes1, impuestomes2, totalimpuesto, trimestre) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, Departamento, ano, municipio, impuestomes1, impuestomes2, totalimpuesto, trimestre)
            
            insertados += 1
            
        conexion.commit()
        print(f"¡Inserción terminada! Se guardaron {insertados} datos con éxito.")


        print("\n--- LEYENDO LOS REGISTROS DE LA BASE DE DATOS ---")
        cursor.execute("""
            SELECT CodigoDepartamento, Departamento, municipio, ano, totalimpuesto 
            FROM registros
        """)
        filas_guardadas = cursor.fetchall()
        
        print(f"{'ID':<6} | {'DEPARTAMENTO':<15} | {'MUNICIPIO':<15} | {'AÑO':<6} | {'TOTAL IMP.'}")
        print("-" * 70)
        
        for fila in filas_guardadas:
            id_dep      = fila[0] if fila[0] is not None else "N/A"
            dep         = fila[1] if fila[1] is not None else "Sin Datos"
            muni        = fila[2] if fila[2] is not None else "Sin Datos"
            ano_reg     = fila[3] if fila[3] is not None else 0
            total_imp   = fila[4] if fila[4] is not None else 0
            
    
            print(f"{id_dep:<6} | {dep:<15} | {muni:<15} | {ano_reg:<6} | ${total_imp:,.2f}")
            
        print("-" * 70)

      
        print("\n--- MODIFICAR UN REGISTRO ---")
        id_registro = int(input("Ingresa el ID del registro que deseas modificar (CodigoDepartamento): "))
        nuevo_municipio = input("Ingresa el nuevo nombre para el municipio: ")
        
        cursor.execute("""
            UPDATE registros
            SET municipio = ?
            WHERE CodigoDepartamento = ?
        """, nuevo_municipio, id_registro)
        
        conexion.commit()
        print(f"¡Registro con ID {id_registro} actualizado con éxito!")

      
        print("\n--- ELIMINAR UN REGISTRO ---")
        id_a_eliminar = int(input("Ingresa el ID del registro que deseas ELIMINAR: "))
        
        cursor.execute("""
            DELETE FROM registros
            WHERE CodigoDepartamento = ?
        """, id_a_eliminar)
        
        conexion.commit()
        print(f"¡Registro con ID {id_a_eliminar} eliminado con éxito!")

    except Exception as error_proceso:
        print(f"Ocurrió un error durante el proceso: {error_proceso}")
    finally:
        cursor.close()
        conexion.close()
        print("\nConexión cerrada limpiamente.")
else:
    print("No se pudo ejecutar el proceso debido a que la conexión inicial falló.")