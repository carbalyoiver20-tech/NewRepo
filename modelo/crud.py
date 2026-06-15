from modelo.conexion import obtener_conexion

def validar_usuario(username, password):
    """Módulo de seguridad: Valida las credenciales en la base de datos."""
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario FROM usuarios WHERE usuario = ? AND contrasena = ?", (username, password))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

def obtener_registros(ano=None, departamento=None, municipio=None):
    """Read: Recupera y filtra los registros del impuesto de transporte."""
    conn = obtener_conexion()
    if not conn:
        return [], 0
    
    cursor = conn.cursor()
    query = "SELECT CodigoDepartamento, Departamento, municipio, ano, totalimpuesto FROM registros WHERE 1=1"
    parametros = []
    
    if ano and str(ano).strip() != "":
        query += " AND ano = ?"
        parametros.append(int(ano))
    if departamento and str(departamento).strip() != "":
        query += " AND Departamento LIKE ?"
        parametros.append(f"%{departamento}%")
    if municipio and str(municipio).strip() != "":
        query += " AND municipio LIKE ?"
        parametros.append(f"%{municipio}%")
        
    query += " ORDER BY ano DESC, Departamento ASC"
    
    cursor.execute(query, parametros)
    registros = cursor.fetchall()
    
    # Análisis de datos: Cálculo del total recaudado en la consulta actual
    total_recaudado = sum(int(reg[4]) for reg in registros if reg[4] is not None)
    
    cursor.close()
    conn.close()
    return registros, total_recaudado

def insertar_registro(departamento, municipio, ano, totalimpuesto):
    """Create: Inserta un nuevo registro de forma manual desde la interfaz."""
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        query = """INSERT INTO registros (Departamento, municipio, ano, totalimpuesto) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (departamento.upper(), municipio.upper(), int(ano), int(totalimpuesto)))
        conn.commit()
        cursor.close()
        conn.close()

def obtener_registro_por_id(id_registro):
    conn = obtener_conexion()
    if not conn:
        return None
    cursor = conn.cursor()
    cursor.execute("SELECT CodigoDepartamento, Departamento, municipio, ano, totalimpuesto FROM registros WHERE CodigoDepartamento = ?", (id_registro,))
    registro = cursor.fetchone()
    cursor.close()
    conn.close()
    return registro

def actualizar_registro(id_registro, departamento, municipio, ano, totalimpuesto):
    """Update: Modifica los valores de un registro existente."""
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        query = """UPDATE registros 
                   SET Departamento = ?, municipio = ?, ano = ?, totalimpuesto = ? 
                   WHERE CodigoDepartamento = ?"""
        cursor.execute(query, (departamento.upper(), municipio.upper(), int(ano), int(totalimpuesto), id_registro))
        conn.commit()
        cursor.close()
        conn.close()

def eliminar_registro(id_registro):
    """Delete: Elimina permanentemente un registro por su ID."""
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registros WHERE CodigoDepartamento = ?", (id_registro,))
        conn.commit()
        cursor.close()
        conn.close()

# ==========================================
#  CONSULTAS NUEVAS PARA FILTROS INTELIGENTES
# ==========================================

def obtener_lista_anos():
    """Trae todos los años únicos de la base de datos ordenados de mayor a menor."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT ano FROM registros WHERE ano IS NOT NULL ORDER BY ano DESC")
    anos = [int(row[0]) for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return anos

def obtener_lista_departamentos():
    """Trae todos los departamentos únicos ordenados alfabéticamente."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT Departamento FROM registros WHERE Departamento IS NOT NULL ORDER BY Departamento ASC")
    departamentos = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return departamentos

def obtener_municipios_por_departamento(departamento):
    """Trae los municipios únicos que pertenecen a un departamento específico."""
    conn = obtener_conexion()
    if not conn:
        return []
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT municipio FROM registros WHERE Departamento = ? AND municipio IS NOT NULL ORDER BY municipio ASC", (departamento,))
    municipios = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return municipios