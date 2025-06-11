import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import pandas as pd
from data_manager import DataManager

class TestMockOperations(unittest.TestCase):
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.data_manager = DataManager()
        
        # Mock de dados para testes
        self.mock_maintenance_data = [
            {
                "peca": "Motor",
                "tipo_manutencao": "Preventiva",
                "descricao": "Troca de óleo",
                "custo": 150.0,
                "timestamp": "2024-03-15T10:00:00"
            }
        ]
        
        self.mock_comparison_data = pd.DataFrame({
            'data': [pd.Timestamp.now()],
            'item1': ['Motor'],
            'item2': ['Freios'],
            'diferenca': [450.0]
        })
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_save_maintenance_mock(self, mock_json_load, mock_json_dump, mock_file):
        """Testa a gravação de dados de manutenção usando mock"""
        # Configurar mock para retornar lista vazia ao ler o arquivo
        mock_json_load.return_value = []
        
        registro = {
            "peca": "Freios",
            "tipo_manutencao": "Corretiva",
            "descricao": "Troca de pastilhas",
            "custo": 200.0
        }
        
        self.data_manager.add_maintenance_record(registro)
        
        # Verifica se o arquivo foi aberto para escrita
        mock_file.assert_called_with(self.data_manager.maintenance_file, 'w', encoding='utf-8')
        
        # Verifica se json.dump foi chamado
        self.assertTrue(mock_json_dump.called)
    
    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_comparison_operations_mock(self, mock_to_csv, mock_read_csv):
        """Testa operações de comparação usando mock"""
        # Configurar o mock de leitura
        mock_read_csv.return_value = self.mock_comparison_data
        
        # Adicionar nova comparação
        self.data_manager.add_comparison("Motor", "Freios", 450.0)
        
        # Verificar se to_csv foi chamado
        self.assertTrue(mock_to_csv.called)
        
        # Verificar se read_csv foi chamado com o arquivo correto
        mock_read_csv.assert_called_with(self.data_manager.comparison_file, parse_dates=['data'])
    
    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directory_creation_mock(self, mock_makedirs, mock_exists):
        """Testa a criação de diretórios usando mock"""
        # Simular que o diretório não existe
        mock_exists.return_value = False
        
        # Criar nova instância do DataManager
        DataManager()
        
        # Verificar se makedirs foi chamado
        mock_makedirs.assert_called_with('data', exist_ok=True)
    
    @patch('json.load')
    def test_load_json_mock(self, mock_json_load):
        """Testa a leitura de dados JSON usando mock"""
        # Configurar o mock para retornar dados simulados
        mock_json_load.return_value = self.mock_maintenance_data
        
        # Tentar carregar o histórico de manutenção
        historico = self.data_manager.get_maintenance_history()
        
        # Verificar se os dados retornados são os esperados
        self.assertEqual(historico, self.mock_maintenance_data)
        self.assertEqual(historico[0]["peca"], "Motor")
    
    @patch('pandas.DataFrame.to_csv')
    def test_error_handling_mock(self, mock_to_csv):
        """Testa o tratamento de erros usando mock"""
        # Configurar o mock para lançar uma exceção
        mock_to_csv.side_effect = Exception("Erro ao salvar arquivo")
        
        # Tentar adicionar uma comparação e verificar se a exceção é tratada
        with self.assertRaises(Exception):
            self.data_manager.add_comparison("Motor", "Freios", 450.0)

if __name__ == '__main__':
    unittest.main() 