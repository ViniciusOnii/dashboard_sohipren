import json
import pandas as pd
from datetime import datetime
import os

class DataManager:
    def __init__(self):
        self.maintenance_file = 'data/maintenance.json'
        self.comparison_file = 'data/comparison_history.csv'
        self.parts_status_file = 'data/parts_status.json'
        
        # Criar diretório de dados se não existir
        os.makedirs('data', exist_ok=True)
        
        # Inicializar arquivos se não existirem
        self._initialize_files()
    
    def _initialize_files(self):
        """Inicializa os arquivos de dados se não existirem"""
        if not os.path.exists(self.maintenance_file):
            self._save_json(self.maintenance_file, [])
        
        if not os.path.exists(self.comparison_file):
            # Definindo os tipos de dados explicitamente
            df = pd.DataFrame({
                'data': pd.Series(dtype='datetime64[ns]'),
                'item1': pd.Series(dtype='str'),
                'item2': pd.Series(dtype='str'),
                'diferenca': pd.Series(dtype='float64')
            })
            df.to_csv(self.comparison_file, index=False)
        
        if not os.path.exists(self.parts_status_file):
            self._save_json(self.parts_status_file, {})
    
    def _save_json(self, file_path, data):
        """Salva dados em formato JSON"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def _load_json(self, file_path):
        """Carrega dados do arquivo JSON"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Métodos para Manutenção
    def add_maintenance_record(self, record):
        """Adiciona um novo registro de manutenção"""
        # Validação dos campos obrigatórios
        campos_obrigatorios = ["peca", "tipo_manutencao", "descricao", "custo"]
        for campo in campos_obrigatorios:
            if campo not in record:
                raise ValueError(f"Campo obrigatório '{campo}' não encontrado no registro")
        
        # Validação do tipo de dados
        if not isinstance(record["custo"], (int, float)):
            raise ValueError("O campo 'custo' deve ser um número")
            
        data = self._load_json(self.maintenance_file)
        record['timestamp'] = datetime.now().isoformat()
        data.append(record)
        self._save_json(self.maintenance_file, data)
    
    def get_maintenance_history(self):
        """Retorna todo o histórico de manutenção"""
        return self._load_json(self.maintenance_file)
    
    # Métodos para Histórico de Comparações
    def add_comparison(self, item1, item2, diferenca):
        """Adiciona uma nova comparação ao histórico"""
        # Validação dos tipos de dados
        if not isinstance(diferenca, (int, float)):
            raise ValueError("O campo 'diferenca' deve ser um número")
        
        try:
            df = pd.read_csv(self.comparison_file, parse_dates=['data'])
        except pd.errors.EmptyDataError:
            # Se o arquivo estiver vazio, cria um DataFrame novo com os tipos corretos
            df = pd.DataFrame({
                'data': pd.Series(dtype='datetime64[ns]'),
                'item1': pd.Series(dtype='str'),
                'item2': pd.Series(dtype='str'),
                'diferenca': pd.Series(dtype='float64')
            })
        
        # Cria o novo registro com tipos explícitos e valores não-nulos
        nova_comparacao = pd.DataFrame({
            'data': [pd.Timestamp.now()],
            'item1': [str(item1)],
            'item2': [str(item2)],
            'diferenca': [float(diferenca)]
        })
        
        # Garante os tipos corretos
        nova_comparacao['data'] = nova_comparacao['data'].astype('datetime64[ns]')
        nova_comparacao['item1'] = nova_comparacao['item1'].astype('str')
        nova_comparacao['item2'] = nova_comparacao['item2'].astype('str')
        nova_comparacao['diferenca'] = nova_comparacao['diferenca'].astype('float64')
        
        # Concatena garantindo que os tipos de dados sejam preservados
        if len(df) == 0:
            df = nova_comparacao
        else:
            df = pd.concat([df, nova_comparacao], ignore_index=True)
        
        # Salva o DataFrame atualizado
        df.to_csv(self.comparison_file, index=False)
    
    def get_comparison_history(self):
        """Retorna todo o histórico de comparações"""
        try:
            return pd.read_csv(self.comparison_file, parse_dates=['data'])
        except pd.errors.EmptyDataError:
            return pd.DataFrame({
                'data': pd.Series(dtype='datetime64[ns]'),
                'item1': pd.Series(dtype='str'),
                'item2': pd.Series(dtype='str'),
                'diferenca': pd.Series(dtype='float64')
            })
    
    # Métodos para Estado das Peças
    def update_part_status(self, part_id, status):
        """Atualiza o status de uma peça"""
        data = self._load_json(self.parts_status_file)
        data[part_id] = {
            'status': status,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        self._save_json(self.parts_status_file, data)
    
    def get_part_status(self, part_id=None):
        """Retorna o status de uma peça específica ou de todas as peças"""
        data = self._load_json(self.parts_status_file)
        if part_id:
            return data.get(part_id)
        return data 