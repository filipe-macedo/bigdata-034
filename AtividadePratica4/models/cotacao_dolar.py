"""
Modelo de dados para Cotação do Dólar
"""

class CotacaoDolar:
    def __init__(self, data_hora_cotacao, cotacao_compra, cotacao_venda, data_cotacao=None, tipo_boletim=None):
        self.data_hora_cotacao = data_hora_cotacao
        self.cotacao_compra = cotacao_compra
        self.cotacao_venda = cotacao_venda
        self.data_cotacao = data_cotacao
        self.tipo_boletim = tipo_boletim
    
    def to_dict(self):
        return {
            'dataHoraCotacao': self.data_hora_cotacao,
            'cotacaoCompra': self.cotacao_compra,
            'cotacaoVenda': self.cotacao_venda,
            'dataCotacao': self.data_cotacao,
            'tipoBoletim': self.tipo_boletim
        }
    
    def __repr__(self):
        return f"CotacaoDolar(data={self.data_hora_cotacao}, compra={self.cotacao_compra}, venda={self.cotacao_venda})"
