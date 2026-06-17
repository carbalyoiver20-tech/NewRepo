# 📊 Sistema de Consulta de Impuestos - Módulo 8

### 👥 Integrantes del Proyecto
* **Yoiver Carbal Mancera**
* [Nombre de Integrante 2]
* [Nombre de Integrante 3]

---

## 🔑 1. Datos de Acceso y Credenciales (Para la Exposición)

Para ingresar al panel administrativo, el sistema valida las credenciales contra la tabla de usuarios en SQL Server. Se definieron los siguientes datos de prueba para la sustentación:

| Enlace de Acceso Local | Usuario Administrador (User/Email) | Contraseña de Acceso |
| :--- | :--- | :--- |
| `http://localhost:5000/login` | `admin@impuestos.gov.co` | `admin123` |

### 🔍 Filtro de Demostración en la Base de Datos:
Una vez adentro del panel, use este filtro exacto para demostrar el funcionamiento del CRUD en tiempo real con datos consistentes y visualización de totales en los paneles:
* **Año:** `2018`
* **Departamento:** `ANTIOQUIA`
* **Municipio:** `SONSON`

---

## 🛠️ 2. ¿Qué Tecnologías se Usaron?
* **Lenguaje Principal:** Python 3.14 (Backend completo del ecosistema).
* **Framework Web:** Flask (Manejo de sesiones seguras, validación de login y enrutamiento dinámico).
* **Base de Datos:** Microsoft SQL Server (`DatosColombiaDB26`) gestionado desde SSMS.
* **Conector de Base de Datos:** `pyodbc` (Ejecución de consultas, sentencias preparadas e inserciones relacionales).
* **Consumo de API:** Librería `requests` para migrar los Datos Abiertos de Colombia (datos.gov.co).
* **Pruebas de Software:** Framework `unittest` para verificar de forma automatizada la calidad del CRUD.
* **Componente Estadístico:** `matplotlib` para la generación de reportes y gráficas de barras nativas.

---

## 📂 3. Estructura y Mapa del Proyecto (Carpetas y Archivos)

Este es el mapa de directorios real que compone la arquitectura del sistema:

```text
C:\Yoiver\
│
├── app.py                  # Servidor y Rutas Web principales (Flask)
├── main.py                 # Script de carga inicial (API a SQL Server) y CRUD por consola
├── mostrar.py              # Script auxiliar para consultar datos rápido por consola
├── graficar.py             # Generación de reportes estadísticos visuales con Matplotlib
├── test_crud.py            # Suite de pruebas automatizadas unitarias (Módulo 8)
│
├── 📂 modelo/              # CARPETA: Lógica de negocio y persistencia
│   └── crud.py             # Funciones SQL (validar_usuario, obtener_registros, insertar_registro)
│
└── 📂 templates/           # CARPETA: Vistas e Interfaz Gráfica (Estructura Jinja2)
    ├── login.html          # Portada de acceso con el formulario de inicio de sesión
    ├── index.html          # Panel principal de búsqueda con tablas y filtros dinámicos
    ├── agregar.html        # Formulario transaccional para añadir un nuevo recaudo
    └── editar.html         # Formulario transaccional para actualizar registros existentes
📍 Ubicación de Componentes Clave:
Control de Autenticación: Se procesa en las rutas de app.py, cruzando los datos del formulario con la función validar_usuario() de modelo/crud.py.

Manejo de Consultas: Todo el mapeo relacional y las sentencias SQL (SELECT, INSERT, UPDATE, DELETE) ocurren exclusivamente dentro de modelo/crud.py sobre la tabla registros.

🛠️ 4. Explicación del CRUD e Integración API
Carga Inicial (main.py): Los datos fueron extraídos de la API de Socrata (datos.gov.co) mediante peticiones HTTP asíncronas e insertados en la tabla local registros mediante commits masivos de pyodbc.

Función Leer (obtener_registros): Recibe el Departamento, Año y Municipio como filtros, ejecuta un SELECT dinámico y devuelve la lista de datos procesados junto con la suma total del recaudo para pintar los contadores de la interfaz.

Función Insertar (insertar_registro): Recibe los campos estructurados del formulario web y ejecuta de forma segura un INSERT INTO en la base de datos SQL Server.

🚀 5. Comandos de Ejecución Rápida
Para poner en marcha todo el sistema local, ejecuta los siguientes comandos en tu terminal de Visual Studio Code:

Instalar dependencias y librerías:

Bash
pip install flask pyodbc requests matplotlib
Correr Pruebas de Integridad (Testing - Módulo 8):

Bash
python -m unittest test_crud.py
(Al ejecutarlo, debe mostrar las letras .. y el mensaje de OK, certificando el éxito del módulo de pruebas).

Generar Reporte Visual Estadístico:

Bash
python graficar.py
Arrancar la Aplicación Web:

Bash
python app.py

---

### 🚀 Paso 3: Sube todo limpio a GitHub
Ve a tu segunda pestaña de la terminal (la que está libre de comandos) y ejecuta esta secuencia para actualizar el repositorio remoto por completo:

```bash
git add .
git commit -m "Modulo 8: Proyecto completamente unificado, graficar.py añadido y README corregido"
git push origin master