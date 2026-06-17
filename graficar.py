import pyodbc
import matplotlib.pyplot as plt

try:
    # 1. Conectarse a tu base de datos de SQL Server
    conexion = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=localhost\\SQLEXPRESS;'
        'DATABASE=DatosColombiaDB26;'  
        'Trusted_Connection=yes;' 
    )
    cursor = conexion.cursor()
    
    # 2. Consultar el total usando DECIMAL para soportar números gigantes sin desborde
    query = """
        SELECT ano, SUM(CAST(totalimpuesto AS DECIMAL(38, 0))) as Total 
        FROM registros 
        GROUP BY ano
        ORDER BY ano
    """
    cursor.execute(query)
    filas = cursor.fetchall()
    
    anos = []
    totales = []
    
    for fila in filas:
        if fila[0] is not None and fila[1] is not None:
            anos.append(str(fila[0])) # Año en el eje X
            # Convertir el valor decimal a millones de pesos para leerlo limpio
            totales.append(float(fila[1]) / 1000000) 
        
    # 3. Diseñar la gráfica con Matplotlib
    plt.figure(figsize=(9, 5))
    
    # Dibujar barras con color azul oscuro corporativo
    barras = plt.bar(anos, totales, color='#1d3557', edgecolor='black', width=0.5)
    
    # Configurar los textos de la ventana
    plt.title('Histórico de Recaudo de Impuestos por Año (Base de Datos Local)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Año Fiscal', fontsize=12, fontweight='bold')
    plt.ylabel('Total Recaudado (En Millones de COP)', fontsize=12, fontweight='bold')
    plt.grid(axis='y', linestyle='--', alpha=0.7) 
    
    # Poner el valor numérico formateado arriba de cada barra
    for barra in barras:
        alto = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2.0, alto + 0.5, f"${alto:,.1f}M", ha='center', va='bottom', fontsize=10)

    print("📊 Generando gráfica en pantalla... ¡Revisa la ventana interactiva de Matplotlib!")
    plt.tight_layout()
    
    # 4. Mostrar ventana interactiva
    plt.show()

except Exception as e:
    print("Ocurrió un error al generar la gráfica:", e)

finally:
    if 'conexion' in locals() and conexion is not None:
        cursor.close()
        conexion.close()