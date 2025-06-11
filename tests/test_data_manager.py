import unittest
import os
import shutil
import json
import pandas as pd
from datetime import datetime
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.test_data_dir = 'test_data'
        os.makedirs(self.test_data_dir, exist_ok=True)
        self.data_manager = DataManager()
        
        # Redirecionar arquivos para diretório de teste
        self.data_manager.maintenance_file = os.path.join(self.test_data_dir, 'maintenance.json')
        self.data_manager.comparison_file = os.path.join(self.test_data_dir, 'comparison_history.csv')
        self.data_manager.parts_status_file = os.path.join(self.test_data_dir, 'parts_status.json')
        
        # Inicializar arquivos
        self.data_manager._initialize_files()
    
    def tearDown(self):
        """Limpeza executada após cada teste"""
        shutil.rmtree(self.test_data_dir)
    
    def test_add_maintenance_record(self):
        """Testa a adição de registros de manutenção"""
        registro = {
            "peca": "Motor",
            "tipo_manutencao": "Preventiva",
            "descricao": "Troca de óleo",
            "custo": 150.0
        }
        
        self.data_manager.add_maintenance_record(registro)
        
        # Verifica se o registro foi salvo
        historico = self.data_manager.get_maintenance_history()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico[0]["peca"], "Motor")
        self.assertTrue("timestamp" in historico[0])
    
    def test_add_comparison(self):
        """Testa a adição de comparações"""
        self.data_manager.add_comparison("Item A", "Item B", 10.5)
        
        # Verifica se a comparação foi salva
        historico = self.data_manager.get_comparison_history()
        self.assertEqual(len(historico), 1)
        self.assertEqual(historico.iloc[0]["item1"], "Item A")
        self.assertEqual(historico.iloc[0]["item2"], "Item B")
        self.assertEqual(historico.iloc[0]["diferenca"], 10.5)
    
    def test_update_part_status(self):
        """Testa a atualização do status das peças"""
        part_id = "MOTOR001"
        status = "Em Uso"
        
        self.data_manager.update_part_status(part_id, status)
        
        # Verifica se o status foi atualizado
        part_status = self.data_manager.get_part_status(part_id)
        self.assertIsNotNone(part_status)
        self.assertEqual(part_status["status"], status)
        self.assertTrue("ultima_atualizacao" in part_status)
    
    def test_get_all_parts_status(self):
        """Testa a obtenção do status de todas as peças"""
        # Adiciona múltiplos status
        self.data_manager.update_part_status("MOTOR001", "Em Uso")
        self.data_manager.update_part_status("MOTOR002", "Em Manutenção")
        
        # Verifica se todos os status foram salvos
        status = self.data_manager.get_part_status()
        self.assertEqual(len(status), 2)
        self.assertTrue("MOTOR001" in status)
        self.assertTrue("MOTOR002" in status)
    
    def test_file_persistence(self):
        """Testa se os dados persistem após reinicialização"""
        # Adiciona dados
        self.data_manager.update_part_status("TESTE001", "Novo")
        
        # Cria nova instância do DataManager
        new_data_manager = DataManager()
        new_data_manager.maintenance_file = self.data_manager.maintenance_file
        new_data_manager.comparison_file = self.data_manager.comparison_file
        new_data_manager.parts_status_file = self.data_manager.parts_status_file
        
        # Verifica se os dados persistiram
        status = new_data_manager.get_part_status("TESTE001")
        self.assertIsNotNone(status)
        self.assertEqual(status["status"], "Novo")

    def test_invalid_maintenance_record(self):
        """Testa a validação de registros de manutenção inválidos"""
        registro_invalido = {
            "tipo_manutencao": "Preventiva",  # Faltando campo obrigatório 'peca'
            "descricao": "Troca de óleo",
            "custo": 150.0
        }
        
        with self.assertRaises(ValueError):
            self.data_manager.add_maintenance_record(registro_invalido)

    def test_invalid_comparison_values(self):
        """Testa a validação de valores inválidos em comparações"""
        with self.assertRaises(ValueError):
            self.data_manager.add_comparison("Item A", "Item B", "valor_invalido")

    def test_batch_maintenance_records(self):
        """Testa a adição de múltiplos registros de manutenção"""
        registros = [
            {
                "peca": "Motor",
                "tipo_manutencao": "Preventiva",
                "descricao": "Troca de óleo",
                "custo": 150.0
            },
            {
                "peca": "Freios",
                "tipo_manutencao": "Corretiva",
                "descricao": "Troca de pastilhas",
                "custo": 200.0
            }
        ]
        
        for registro in registros:
            self.data_manager.add_maintenance_record(registro)
        
        historico = self.data_manager.get_maintenance_history()
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[1]["peca"], "Freios")

    def test_comparison_data_types(self):
        """Testa se os tipos de dados nas comparações são mantidos corretamente"""
        self.data_manager.add_comparison("Item A", "Item B", 10.5)
        
        historico = self.data_manager.get_comparison_history()
        self.assertIsInstance(historico.iloc[0]["diferenca"], float)
        self.assertIsInstance(historico.iloc[0]["item1"], str)
        self.assertIsInstance(historico.iloc[0]["data"], pd.Timestamp)

    def test_part_status_updates(self):
        """Testa múltiplas atualizações de status para a mesma peça"""
        part_id = "MOTOR001"
        
        # Primeira atualização
        self.data_manager.update_part_status(part_id, "Em Uso")
        status1 = self.data_manager.get_part_status(part_id)
        
        # Segunda atualização
        self.data_manager.update_part_status(part_id, "Em Manutenção")
        status2 = self.data_manager.get_part_status(part_id)
        
        self.assertNotEqual(status1["ultima_atualizacao"], status2["ultima_atualizacao"])
        self.assertEqual(status2["status"], "Em Manutenção")

if __name__ == '__main__':
    unittest.main() 