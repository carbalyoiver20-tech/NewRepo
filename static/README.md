# Sistema de Análisis de Datos Abiertos - Impuesto de Transporte (MinEnergía)

Este es el proyecto integrador desarrollado para la gestión y consulta transaccional de los recaudos del impuesto de transporte en Colombia.

## 🚀 Características
- **Backend**: Servidor robusto construido en Node.js con Express.
- **Base de Datos**: Persistencia relacional real en Microsoft SQL Server (`DatosColombiaDB26`).
- **Seguridad**: Autenticación de usuarios mediante sesiones seguras para perfiles de Administrador.
- **Frontend Interactivo**: Interfaz web dinámica con filtros inteligentes (Año, Departamento, Municipio) integrados mediante llamadas asíncronas (`fetch`).

## 🛠️ Requisitos e Instalación
1. Clonar el repositorio.
2. Ejecutar `npm install` para descargar las dependencias.
3. Configurar y ejecutar el archivo `.sql` provisto en la carpeta `/sql` en tu instancia local de SQL Server.
4. Iniciar el servidor con `node app.js` (o tu comando de arranque).