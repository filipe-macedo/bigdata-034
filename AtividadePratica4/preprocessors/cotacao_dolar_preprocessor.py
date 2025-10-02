"""
Preprocessador para dados de Cotação do Dólar
"""

from models.cotacao_dolar import CotacaoDolar

class CotacaoDolarPreprocessor:
    
    @staticmethod
    def processar_dados(dados_brutos):
        dados_processados = []
        
        for registro in dados_brutos:
            try:
                cotacao = CotacaoDolarPreprocessor._processar_registro(registro)
                if cotacao:
                    dados_processados.append(cotacao)
            except Exception as e:
                print(f"Erro ao processar registro: {e}")
                continue
        
        return dados_processados
    
    @staticmethod
    def _processar_registro(registro):
        data_hora_cotacao = registro.get('dataHoraCotacao')
        cotacao_compra = CotacaoDolarPreprocessor._converter_para_float(
            registro.get('cotacaoCompra')
        )
        cotacao_venda = CotacaoDolarPreprocessor._converter_para_float(
            registro.get('cotacaoVenda')
        )
        data_cotacao = registro.get('dataCotacao')
        tipo_boletim = registro.get('tipoBoletim')
        
        if not data_hora_cotacao or cotacao_compra is None or cotacao_venda is None:
            return None
        
        return CotacaoDolar(
            data_hora_cotacao=data_hora_cotacao,
            cotacao_compra=cotacao_compra,
            cotacao_venda=cotacao_venda,
            data_cotacao=data_cotacao,
            tipo_boletim=tipo_boletim
        )
    
    @staticmethod
    def _converter_para_float(valor):
        if valor is None:
            return None
        try:
            return float(valor)
        except (ValueError, TypeError):
            return None
