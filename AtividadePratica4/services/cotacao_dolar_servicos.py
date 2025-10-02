"""
Serviços para coleta de dados da API
"""

import requests
from preprocessors.cotacao_dolar_preprocessor import CotacaoDolarPreprocessor
from repositories.cotacao_dolar_repositorio import CotacaoDolarRepositorio

class CotacaoDolarServicos:
    
    def __init__(self):
        self.preprocessador = CotacaoDolarPreprocessor()
        self.repositorio = CotacaoDolarRepositorio()
    
    def coletar_cotacao_por_data(self, data):
        print(f"\n{'='*60}")
        print(f"Coletando cotação para: {data}")
        print(f"{'='*60}\n")
        
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao='{data}'&$format=json"
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                dados_json = response.json()
                valores = dados_json.get('value', [])
                
                if not valores:
                    print("⚠ Nenhum dado encontrado")
                    return False
                
                print(f"✓ {len(valores)} registros encontrados")
                
                cotacoes = self.preprocessador.processar_dados(valores)
                
                if not cotacoes:
                    print("✗ Nenhum dado válido")
                    return False
                
                inseridos = self.repositorio.inserir_cotacoes(cotacoes)
                return inseridos > 0
            else:
                print(f"✗ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Erro: {e}")
            return False
    
    def coletar_cotacao_por_periodo(self, data_inicial, data_final):
        print(f"\n{'='*60}")
        print(f"Período: {data_inicial} até {data_final}")
        print(f"{'='*60}\n")
        
        url = (f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
               f"CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?"
               f"@dataInicial='{data_inicial}'&@dataFinalCotacao='{data_final}'&$format=json")
        
        try:
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                dados_json = response.json()
                valores = dados_json.get('value', [])
                
                if not valores:
                    print("⚠ Nenhum dado encontrado")
                    return False
                
                print(f"✓ {len(valores)} registros encontrados")
                
                cotacoes = self.preprocessador.processar_dados(valores)
                
                if not cotacoes:
                    print("✗ Nenhum dado válido")
                    return False
                
                inseridos = self.repositorio.inserir_cotacoes(cotacoes)
                return inseridos > 0
            else:
                print(f"✗ Erro na API: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Erro: {e}")
            return False
    
    def fechar(self):
        self.repositorio.fechar_conexao()
