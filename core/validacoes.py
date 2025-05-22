"""
Módulo com funções de validação de inputs
"""

def validar_inputs(valor_imovel, percentual_entrada, taxa_juros, anos_contrato):
    """Valida todos os inputs do usuário."""
    erros = []
    
    if valor_imovel <= 0:
        erros.append("O valor do imóvel deve ser positivo")
    if percentual_entrada <= 0:
        erros.append("O percentual da entrada deve ser positivo")
    if not 5 <= taxa_juros <= 12:
        erros.append("A taxa de juros deve estar entre 5% e 12%")
    if anos_contrato <= 0:
        erros.append("A duração do contrato deve ser positiva")
    
    return erros