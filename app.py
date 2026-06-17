from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from modelo import crud
import pyodbc
import matplotlib
# Configuración para evitar que matplotlib intente abrir ventanas en segundo plano
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

app.secret_key = 'proyecto_integrador_datos_colombia_2026'

def generar_grafica_base64(ano_filtro=None, depto_filtro=None, muni_filtro=None):
    """Genera la gráfica de barras adaptándose dinámicamente a los filtros de búsqueda"""
    try:
        conexion = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=localhost\\SQLEXPRESS;'
            'DATABASE=DatosColombiaDB26;'  
            'Trusted_Connection=yes;' 
        )
        cursor = conexion.cursor()
        
        # 1. Construir la consulta SQL con los filtros seleccionados
        query = """
            SELECT ano, SUM(CAST(totalimpuesto AS DECIMAL(38, 0))) as Total 
            FROM registros 
            WHERE 1=1
        """
        params = []
        
        if ano_filtro:
            query += " AND ano = ?"
            params.append(ano_filtro)
        if depto_filtro:
            query += " AND Departamento = ?"
            params.append(depto_filtro)
        if muni_filtro:
            query += " AND municipio = ?"
            params.append(muni_filtro)
            
        query += " GROUP BY ano ORDER BY ano"
        
        cursor.execute(query, params)
        filas = cursor.fetchall()
        
        anos = []
        totales = []
        for fila in filas:
            if fila[0] is not None and fila[1] is not None:
                anos.append(str(fila[0]))
                totales.append(float(fila[1]) / 1000000) # Convertir a millones de pesos
        
        cursor.close()
        conexion.close()
        
        # Si la búsqueda no arroja datos, no se dibuja gráfica
        if not anos:
            return None

        # 2. Diseñar la gráfica con Matplotlib
        plt.figure(figsize=(7, 3.5))
        barras = plt.bar(anos, totales, color='#1d3557', edgecolor='black', width=0.4)
        
        # Definir título dinámico basado en los filtros aplicados
        if depto_filtro and muni_filtro:
            titulo = f"Recaudo en {muni_filtro} ({depto_filtro})"
        elif depto_filtro:
            titulo = f"Recaudo en el Departamento de {depto_filtro}"
        else:
            titulo = "Histórico Global de Recaudo de Impuestos"
            
        plt.title(f"{titulo} (Millones de COP)", fontsize=11, fontweight='bold')
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        
        # Poner las etiquetas de valores arriba de cada barra de manera limpia
        for barra in barras:
            alto = barra.get_height()
            plt.text(barra.get_x() + barra.get_width()/2.0, alto + (alto * 0.01 if alto > 0 else 0.5), 
                     f"${alto:,.1f}M", ha='center', va='bottom', fontsize=9)
            
        plt.tight_layout()
        
        # 3. Guardar la gráfica en memoria binaria (Buffer) y codificarla a Base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        img_buffer.seek(0)
        plt.close() 
        
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return img_base64
    except Exception as e:
        print("Error generando gráfica dinámica web:", e)
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        
        # Validación con la base de datos local
        user = crud.validar_usuario(usuario, contrasena)
        if user:
            session['usuario'] = user[1]  
            return redirect(url_for('index'))
        else:
            error = "Usuario o contraseña incorrectos. Acceso denegado."
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('usuario', None) 
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
        
    ano = request.form.get('ano')
    departamento = request.form.get('departamento')
    municipio = request.form.get('municipio')
    
    # Obtener los registros filtrados desde el módulo CRUD
    registros, total_recaudado = crud.obtener_registros(ano, departamento, municipio)
    
    lista_anos = crud.obtener_lista_anos()
    lista_deptos = crud.obtener_lista_departamentos()
    
    # LLAMADA CORREGIDA: Pasamos los filtros del usuario para recalcular el gráfico en vivo
    grafica_data = generar_grafica_base64(ano, departamento, municipio)
    
    return render_template('index.html', 
                           registros=registros, 
                           total=total_recaudado, 
                           ano=ano, 
                           depto=departamento, 
                           muni=municipio,
                           lista_anos=lista_anos,
                           lista_deptos=lista_deptos,
                           grafica_data=grafica_data)

@app.route('/api/municipios', methods=['GET'])
def api_municipios():
    """Endpoint tipo API que le devuelve los municipios a JavaScript en tiempo real"""
    depto = request.args.get('departamento')
    if not depto:
        return jsonify([])
    municipios = crud.obtener_municipios_por_departamento(depto)
    return jsonify(municipios)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if 'usuario' not in session: 
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        departamento = request.form['departamento']
        municipio = request.form['municipio']
        ano = request.form['ano']
        totalimpuesto = request.form['totalimpuesto']
        
        crud.insertar_registro(departamento, municipio, ano, totalimpuesto)
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'usuario' not in session: 
        return redirect(url_for('login'))
    
    registro = crud.obtener_registro_por_id(id)
    if request.method == 'POST':
        departamento = request.form['departamento']
        municipio = request.form['municipio']
        ano = request.form['ano']
        totalimpuesto = request.form['totalimpuesto']
        
        crud.actualizar_registro(id, departamento, municipio, ano, totalimpuesto)
        return redirect(url_for('index'))
    return render_template('editar.html', registro=registro)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    if 'usuario' not in session: 
        return redirect(url_for('login'))
    crud.eliminar_registro(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)