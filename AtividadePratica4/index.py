"""
Aplicação Principal - Sistema de Cotação do Dólar
"""

import os
from services.cotacao_dolar_servicos import CotacaoDolarServicos


def validar_variaveis_ambiente():
    """Valida se o .env está configurado"""
    mongodb_uri = os.getenv('MONGODB_URI')
    database_name = os.getenv('DATABASE_NAME')
    
    if not mongodb_uri or not database_name:
        print("\n✗ ERRO: Variáveis de ambiente não configuradas!")
        print("Configure o arquivo .env com suas credenciais MongoDB.")
        return False
    
    if not mongodb_uri.startswith('mongodb'):
        print("\n✗ ERRO: MONGODB_URI inválida!")
        return False
    
    return True


def validar_data(data):
    """Valida formato de data MM-DD-AAAA"""
    if not isinstance(data, str) or len(data) != 10:
        return False
    
    partes = data.split('-')
    if len(partes) != 3:
        return False
    
    try:
        mes, dia, ano = partes
        mes_num = int(mes)
        dia_num = int(dia)
        ano_num = int(ano)
        
        if not (1 <= mes_num <= 12):
            return False
        if not (1 <= dia_num <= 31):
            return False
        if not (2000 <= ano_num <= 2100):
            return False
        if len(mes) != 2 or len(dia) != 2 or len(ano) != 4:
            return False
        
        return True
    except ValueError:
        return False


def menu_principal():
    """Menu principal"""
    print("\n" + "="*60)
    print("SISTEMA DE COTAÇÕES DO DÓLAR - BANCO CENTRAL")
    print("="*60)
    print("\n1 - Coletar cotação por data específica")
    print("2 - Coletar cotações por período")
    print("3 - Ver estatísticas do banco")
    print("0 - Sair")
    print("="*60)


def coletar_por_data(servico):
    """Coleta cotação de uma data"""
    print("\n--- COLETAR POR DATA ---")
    print("Formato: MM-DD-AAAA (ex: 01-15-2024)")
    
    data = input("\nDigite a data: ").strip()
    
    if not validar_data(data):
        print("\n✗ Data inválida! Use o formato MM-DD-AAAA")
        return
    
    sucesso = servico.coletar_cotacao_por_data(data)
    if sucesso:
        print("\n✓ Operação concluída!")
    else:
        print("\n✗ Falha na operação")


def coletar_por_periodo(servico):
    """Coleta cotações de um período"""
    print("\n--- COLETAR POR PERÍODO ---")
    print("Formato: MM-DD-AAAA (ex: 01-15-2024)")
    
    data_inicial = input("\nData inicial: ").strip()
    if not validar_data(data_inicial):
        print("\n✗ Data inicial inválida!")
        return
    
    data_final = input("Data final: ").strip()
    if not validar_data(data_final):
        print("\n✗ Data final inválida!")
        return
    
    sucesso = servico.coletar_cotacao_por_periodo(data_inicial, data_final)
    if sucesso:
        print("\n✓ Operação concluída!")
    else:
        print("\n✗ Falha na operação")


def ver_estatisticas(servico):
    """Mostra estatísticas do banco"""
    print("\n--- ESTATÍSTICAS ---")
    total = servico.repositorio.contar_cotacoes()
    
    if total > 0:
        print("\nÚltimas cotações:")
        cotacoes = servico.repositorio.buscar_ultimas(5)
        for i, c in enumerate(cotacoes, 1):
            print(f"\n{i}. {c.get('dataHoraCotacao')}")
            print(f"   Compra: R$ {c.get('cotacaoCompra'):.4f}")
            print(f"   Venda: R$ {c.get('cotacaoVenda'):.4f}")


def executar():
    """Função principal"""
    print("\n" + "="*60)
    print("INICIANDO APLICAÇÃO")
    print("="*60)
    
    # Valida configuração
    if not validar_variaveis_ambiente():
        print("\nConfigure o arquivo .env antes de continuar.")
        return
    
    # Inicializa serviço
    try:
        servico = CotacaoDolarServicos()
    except Exception as e:
        print(f"\n✗ Erro ao conectar: {e}")
        print("\nVerifique:")
        print("  1. Se o .env está configurado corretamente")
        print("  2. Se as credenciais MongoDB estão corretas")
        print("  3. Se seu IP está liberado no MongoDB Atlas")
        return
    
    # Loop principal
    while True:
        try:
            menu_principal()
            opcao = input("\nOpção: ").strip()
            
            if opcao == '1':
                coletar_por_data(servico)
            elif opcao == '2':
                coletar_por_periodo(servico)
            elif opcao == '3':
                ver_estatisticas(servico)
            elif opcao == '0':
                print("\nEncerrando...")
                servico.fechar()
                print("✓ Aplicação encerrada!\n")
                break
            else:
                print("\n✗ Opção inválida!")
        
        except KeyboardInterrupt:
            print("\n\nInterrompido pelo usuário.")
            servico.fechar()
            break
        except Exception as e:
            print(f"\n✗ Erro: {e}")


if __name__ == "__main__":
    executar()
