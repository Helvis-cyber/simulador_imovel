#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SIMULADOR DE ENTRADA DE IMÓVEL aMORA - VERSÃO TERMINAL
------------------------------------------------------
Arquivo: interfaces/terminal/main.py

Descrição: Este módulo é a interface de linha de comando do simulador de entrada de imóvel aMORA.
Ele permite que o usuário insira dados sobre o valor do imóvel, percentual de entrada, juros e duração do contrato,
e calcula as parcelas mensais corrigidas pelo IGPM e juros compostos. Os resultados são exibidos de forma formatada no terminal.
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao PATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

# Importa funções necessárias do módulo core
from core.calculos import (
    formatar_entrada_para_float,
    calcular_entrada,
    calcular_parcela_mensal,
    calcular_correcao_igpm,
    calcular_correcao_juros
)
from core.validacoes import validar_inputs
import locale

# Configura locale para formato monetário brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Fallback para Windows

def mostrar_resultados(entrada, total_guardar, parcela_base, parcelas_igpm, parcelas_juros, taxa_juros):
    """Exibe os resultados formatados no terminal."""
    print("\n" + "=" * 50)
    print("RESULTADOS DA SIMULAÇÃO".center(50))
    print("=" * 50)
    
    print(f"\n• Valor da entrada: {locale.currency(entrada, grouping=True)}")
    print(f"• Valor total a guardar: {locale.currency(total_guardar, grouping=True)}")
    print(f"• Parcela mensal BASE: {locale.currency(parcela_base, grouping=True)}")
    
    print("\n" + "-" * 50)
    print("PARCELAS CORRIGIDAS PELO IGPM (6% ao ano):")
    for ano, parcela in enumerate(parcelas_igpm, start=1):
        print(f"  Ano {ano}: {locale.currency(parcela, grouping=True)}")
    
    print("\n" + "-" * 50)
    print(f"PARCELAS CORRIGIDAS POR JUROS COMPOSTOS ({taxa_juros:.2f}% ao ano):")
    for ano, parcela in enumerate(parcelas_juros, start=1):
        print(f"  Ano {ano}: {locale.currency(parcela, grouping=True)}")
    print("=" * 50 + "\n")

def main():
    """Função principal que orquestra o fluxo do programa."""
    print("\n" + "=" * 50)
    print("SIMULADOR aMORA - VERSÃO TERMINAL".center(50))
    print("=" * 50)
    
    try:
        # Coleta de inputs
        print("\nPor favor, informe:")
        valor_imovel = formatar_entrada_para_float(input("  → Valor do imóvel (R$): ").strip())
        percentual_entrada = formatar_entrada_para_float(input("  → Percentual da entrada (%): ").strip())
        anos_contrato = int(input("  → Duração do contrato (anos): ").strip())
        taxa_juros = formatar_entrada_para_float(input("  → Taxa de juros anual (%): ").strip())

        # Validação
        erros = validar_inputs(valor_imovel, percentual_entrada, taxa_juros, anos_contrato)
        if erros:
            raise ValueError("\n".join(erros))

        # Cálculos
        entrada = calcular_entrada(valor_imovel, percentual_entrada)
        total_guardar = valor_imovel * 0.15
        parcela_base = calcular_parcela_mensal(total_guardar, anos_contrato)
        parcelas_igpm = calcular_correcao_igpm(parcela_base, anos_contrato)
        parcelas_juros = calcular_correcao_juros(parcela_base, anos_contrato, taxa_juros)

        # Exibição
        mostrar_resultados(entrada, total_guardar, parcela_base, parcelas_igpm, parcelas_juros, taxa_juros)

    except ValueError as e:
        print(f"\n⚠️ ERRO DE VALIDAÇÃO:\n{e}")
    except Exception as e:
        print(f"\n⚠️ ERRO INESPERADO:\n{str(e)}")
    finally:
        print("\nPressione Enter para sair...")
        input()

if __name__ == "__main__":
    main()