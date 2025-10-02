"""
Repositório para persistência no MongoDB
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from config import MONGODB_URI, DATABASE_NAME

class CotacaoDolarRepositorio:
    
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self._conectar()
    
    def _conectar(self):
        try:
            self.client = MongoClient(MONGODB_URI)
            self.client.admin.command('ping')
            print("✓ Conexão com MongoDB estabelecida!")
            
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db['cotacoes_dolar']
            
        except ConnectionFailure as e:
            print(f"✗ Erro ao conectar: {e}")
            raise
        except Exception as e:
            print(f"✗ Erro inesperado: {e}")
            raise
    
    def inserir_cotacoes(self, cotacoes):
        if not cotacoes:
            print("Nenhuma cotação para inserir")
            return 0
        
        try:
            documentos = [cotacao.to_dict() for cotacao in cotacoes]
            resultado = self.collection.insert_many(documentos)
            print(f"✓ {len(resultado.inserted_ids)} cotações inseridas!")
            return len(resultado.inserted_ids)
        except Exception as e:
            print(f"✗ Erro ao inserir: {e}")
            return 0
    
    def contar_cotacoes(self):
        try:
            total = self.collection.count_documents({})
            print(f"✓ Total: {total} cotações")
            return total
        except Exception as e:
            print(f"✗ Erro: {e}")
            return 0
    
    def buscar_ultimas(self, limite=10):
        try:
            return list(self.collection.find().sort('dataHoraCotacao', -1).limit(limite))
        except Exception as e:
            print(f"✗ Erro: {e}")
            return []
    
    def fechar_conexao(self):
        if self.client:
            self.client.close()
            print("✓ Conexão fechada")
