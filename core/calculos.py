"""
Módulo com todas as funções de cálculo do simulador
"""

import locale

# Configuração do locale para formato monetário
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

def formatar_entrada_para_float(valor):
    """Converte valores no formato brasileiro para float.
    Exemplo: '350.000,00' → 350000.00 | '8,5' → 8.5
    """
    if isinstance(valor, str):
        return float(valor.replace(".", "").replace(",", "."))
    return float(valor)

def calcular_entrada(valor_imovel, percentual_entrada):
    """Calcula o valor da entrada."""
    return valor_imovel * (percentual_entrada / 100)

def calcular_parcela_mensal(total_guardar, anos_contrato):
    """Calcula a parcela mensal base."""
    return total_guardar / (anos_contrato * 12)

def calcular_correcao_igpm(parcela_mensal, anos_contrato):
    """Aplica correção anual de 6% (IGPM)."""
    return [parcela_mensal * (1.06 ** (ano - 1)) for ano in range(1, anos_contrato + 1)]

def calcular_correcao_juros(parcela_mensal, anos_contrato, taxa_juros):
    """Aplica juros compostos conforme taxa informada."""
    return [parcela_mensal * ((1 + taxa_juros / 100) ** (ano - 1)) for ano in range(1, anos_contrato + 1)]