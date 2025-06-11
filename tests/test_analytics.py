import unittest
import pandas as pd
import numpy as np
from data_manager import DataManager

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        """Configuração executada antes de cada teste"""
        self.data_manager = DataManager()
        
        # Limpar arquivos de teste
        self.data_manager._save_json(self.data_manager.maintenance_file, [])
        self.data_manager._save_json(self.data_manager.parts_status_file, {})
        pd.DataFrame({
            'data': pd.Series(dtype='datetime64[ns]'),
            'item1': pd.Series(dtype='str'),
            'item2': pd.Series(dtype='str'),
            'diferenca': pd.Series(dtype='float64')
        }).to_csv(self.data_manager.comparison_file, index=False)
        
        # Adicionar dados de teste
        self.registros_manutencao = [
            {
                "peca": "Motor",
                "tipo_manutencao": "Preventiva",
                "descricao": "Troca de óleo",
                "custo": 150.0
            },
            {
                "peca": "Motor",
                "tipo_manutencao": "Corretiva",
                "descricao": "Reparo no pistão",
                "custo": 500.0
            },
            {
                "peca": "Freios",
                "tipo_manutencao": "Preventiva",
                "descricao": "Troca de pastilhas",
                "custo": 200.0
            }
        ]
        
        for registro in self.registros_manutencao:
            self.data_manager.add_maintenance_record(registro)
    
    def test_custo_total_por_peca(self):
        """Testa o cálculo do custo total por peça"""
        historico = self.data_manager.get_maintenance_history()
        df = pd.DataFrame(historico)
        
        custo_por_peca = df.groupby('peca')['custo'].sum()
        
        self.assertEqual(custo_por_peca['Motor'], 650.0)
        self.assertEqual(custo_por_peca['Freios'], 200.0)
    
    def test_frequencia_manutencao(self):
        """Testa o cálculo da frequência de tipos de manutenção"""
        historico = self.data_manager.get_maintenance_history()
        df = pd.DataFrame(historico)
        
        freq_manutencao = df['tipo_manutencao'].value_counts()
        
        self.assertEqual(freq_manutencao['Preventiva'], 2)
        self.assertEqual(freq_manutencao['Corretiva'], 1)
    
    def test_media_custos(self):
        """Testa o cálculo da média de custos por tipo de manutenção"""
        historico = self.data_manager.get_maintenance_history()
        df = pd.DataFrame(historico)
        
        media_custos = df.groupby('tipo_manutencao')['custo'].mean()
        
        self.assertEqual(media_custos['Preventiva'], 175.0)  # (150 + 200) / 2
        self.assertEqual(media_custos['Corretiva'], 500.0)
    
    def test_analise_temporal(self):
        """Testa a análise temporal das manutenções"""
        historico = self.data_manager.get_maintenance_history()
        df = pd.DataFrame(historico)
        
        # Converter timestamp para datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Verificar se as datas estão em ordem cronológica
        datas = df['timestamp'].tolist()
        datas_ordenadas = sorted(datas)
        
        self.assertEqual(datas, datas_ordenadas)
    
    def test_analise_comparativa(self):
        """Testa a análise comparativa entre diferentes períodos"""
        # Adicionar comparações de teste
        self.data_manager.add_comparison("Motor", "Freios", 450.0)  # Diferença nos custos
        self.data_manager.add_comparison("Preventiva", "Corretiva", 325.0)  # Diferença média
        
        historico_comparacoes = self.data_manager.get_comparison_history()
        
        self.assertEqual(len(historico_comparacoes), 2)
        self.assertEqual(historico_comparacoes.iloc[0]['diferenca'], 450.0)

if __name__ == '__main__':
    unittest.main() 