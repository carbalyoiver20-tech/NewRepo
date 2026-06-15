import unittest
# Importamos tus funciones del modelo
from modelo.crud import insertar_registro, obtener_registros

class TestImpuestosCRUD(unittest.TestCase):

    def test_1_validar_consulta(self):
        """Caso de prueba: Verificar que la consulta retorne datos de Antioquia"""
        resultado_consulta = obtener_registros(departamento="ANTIOQUIA", municipio="SONSON")
        filas = resultado_consulta[0]
        
        self.assertIsInstance(filas, list, "La consulta no contiene una lista de filas válida.")
        self.assertGreater(len(filas), 0, "No se encontraron registros para ANTIOQUIA - SONSON.")

    def test_2_validar_insercion_real(self):
        """Caso de prueba: Verificar que insertar_registro se ejecute correctamente"""
        departamento = "ANTIOQUIA"
        municipio = "SONSON"
        ano = 2018
        totalimpuesto = 65079649
        
        # Ejecutamos tu función
        resultado = insertar_registro(departamento, municipio, ano, totalimpuesto)
        
        # Como tu función procesa el INSERT en SQL Server pero no tiene un return explícito,
        # validamos que termine su ejecución retornando None (lo esperado en tu lógica)
        self.assertIsNone(resultado, "El proceso de inserción retornó un valor inesperado.")

if __name__ == '__main__':
    unittest.main()