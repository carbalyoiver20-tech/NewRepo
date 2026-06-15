from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from modelo import crud

app = Flask(__name__)

app.secret_key = 'proyecto_integrador_datos_colombia_2026'

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
    
    
    registros, total_recaudado = crud.obtener_registros(ano, departamento, municipio)
    
    lista_anos = crud.obtener_lista_anos()
    lista_deptos = crud.obtener_lista_departamentos()
    
    return render_template('index.html', 
                           registros=registros, 
                           total=total_recaudado, 
                           ano=ano, 
                           depto=departamento, 
                           muni=municipio,
                           lista_anos=lista_anos,
                           lista_deptos=lista_deptos)

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