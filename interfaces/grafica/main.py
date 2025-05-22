#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SIMULADOR DE ENTRADA DE IMÓVEL aMORA - VERSÃO GRÁFICA
-----------------------------------------------------
Arquivo: interfaces/grafica/main.py

Funcionalidades:
- Cálculo de entrada e parcelas com correção pelo IGPM ou juros compostos
"""

import sys
import os
from pathlib import Path
from PIL import Image, ImageTk  

# Adiciona o diretório raiz do projeto ao PATH
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

# Importações do core
from core.calculos import (
    formatar_entrada_para_float,
    calcular_entrada,
    calcular_parcela_mensal,
    calcular_correcao_igpm,
    calcular_correcao_juros
)
from core.validacoes import validar_inputs
import locale
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

# Configuração do locale para formato monetário
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  

class SimuladorImovel:
    """Classe principal que gerencia a interface gráfica."""

    def __init__(self, root):
        """Inicializa a aplicação."""
        self.root = root
        self.configurar_janela()
        self.criar_variaveis()
        self.criar_widgets()

    def configurar_janela(self):
        """Configura propriedades da janela principal."""
        self.root.title("Simulador aMORA v2.0")
        self.root.geometry("500x500")  
        self.root.resizable(False, False)
        
        # Tenta carregar o ícone da janela
        try:
            icon_path = Path(__file__).parent.parent.parent / "assets" / "aMORA_logo.png"
            self.root.iconphoto(True, tk.PhotoImage(file=icon_path))
        except Exception as e:
            print(f"Não foi possível carregar o ícone: {e}")
        
        # Centraliza a janela
        largura = 500
        altura = 500
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def criar_variaveis(self):
        """Cria as variáveis de controle para os inputs."""
        self.valor_imovel = tk.StringVar(value="500.000,00")
        self.percentual_entrada = tk.StringVar(value="5,00")
        self.anos_contrato = tk.IntVar(value=3)
        self.taxa_juros = tk.StringVar(value="8,00")

    def criar_widgets(self):
        """Cria e posiciona todos os elementos na interface."""
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'))

        # Frame principal
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho com logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Carrega e exibe o logo
        try:
            logo_path = Path(__file__).parent.parent.parent / "assets" / "aMORA_logo.png"
            logo_img = Image.open(logo_path)
            
            logo_img.thumbnail((120, 120), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            
            logo_label = ttk.Label(header_frame, image=self.logo)
            logo_label.pack()
        except Exception as e:
            print(f"Erro ao carregar logotipo: {e}")
            # Se não encontrar a imagem, exibe apenas o texto
            ttk.Label(
                header_frame,
                text="aMORA",
                font=('Arial', 16, 'bold'),
                foreground='#0066cc'
            ).pack()

        ttk.Label(
            header_frame,
            text="SIMULADOR DE FINANCIAMENTO",
            font=('Arial', 14, 'bold'),
            foreground='#0066cc'
        ).pack()

        ttk.Label(
            header_frame,
            text="Preencha os dados do imóvel",
            font=('Arial', 9),
            foreground='#666666'
        ).pack()

        # Campos de entrada
        campos = [
            ("Valor do imóvel (R$):", self.valor_imovel),
            ("Percentual da entrada (%):", self.percentual_entrada),
            ("Duração do contrato (anos):", self.anos_contrato),
            ("Taxa de juros anual (%):", self.taxa_juros)
        ]

        for i, (texto, var) in enumerate(campos, start=1):
            ttk.Label(main_frame, text=texto).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=5)
            
            entry = ttk.Entry(main_frame, textvariable=var, font=('Arial', 10))
            entry.grid(row=i, column=1, sticky=tk.EW, pady=5)

        # Botão de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            btn_frame,
            text="CALCULAR SIMULAÇÃO",
            command=self.executar_simulacao,
            style='TButton'
        ).pack(pady=10, ipadx=20, ipady=5)

        # Rodapé
        ttk.Label(
            main_frame,
            text="© 2023 Simulador aMORA - Versão 2.0",
            font=('Arial', 8),
            foreground='#999999'
        ).grid(row=6, column=0, columnspan=2, pady=(20, 0))

        # Configuração do grid
        main_frame.columnconfigure(1, weight=1)

    def validar_inputs(self):
        """Valida os valores inseridos pelo usuário."""
        try:
            valor_imovel = formatar_entrada_para_float(self.valor_imovel.get())
            percentual_entrada = formatar_entrada_para_float(self.percentual_entrada.get())
            taxa_juros = formatar_entrada_para_float(self.taxa_juros.get())
            anos_contrato = self.anos_contrato.get()

            erros = validar_inputs(valor_imovel, percentual_entrada, taxa_juros, anos_contrato)
            if erros:
                raise ValueError("\n".join(erros))
            
            return True
        except ValueError as e:
            messagebox.showerror(
                "Erro de Validação", 
                f"Corrija os seguintes campos:\n\n{str(e)}",
                icon='warning'
            )
            return False
        except Exception as e:
            messagebox.showerror(
                "Erro de Formato", 
                "Formato inválido!\n\nUse:\n• 350.000,00 para valores\n• 8,5 para porcentagens",
                icon='error'
            )
            return False

    def executar_simulacao(self):
        """Coordena todo o processo de simulação."""
        if not self.validar_inputs():
            return

        try:
            # Coleta e converte valores
            vi = formatar_entrada_para_float(self.valor_imovel.get())
            pe = formatar_entrada_para_float(self.percentual_entrada.get())
            ac = self.anos_contrato.get()
            tj = formatar_entrada_para_float(self.taxa_juros.get())

            # Cálculos
            entrada = calcular_entrada(vi, pe)
            total_guardar = vi * 0.15
            parcela_base = calcular_parcela_mensal(total_guardar, ac)
            parcelas_igpm = calcular_correcao_igpm(parcela_base, ac)
            parcelas_juros = calcular_correcao_juros(parcela_base, ac, tj)

            # Exibe resultados
            self.mostrar_resultados(entrada, total_guardar, parcela_base, parcelas_igpm, parcelas_juros, tj)

        except Exception as e:
            messagebox.showerror(
                "Erro inesperado", 
                f"Ocorreu um erro durante os cálculos:\n\n{str(e)}",
                icon='error'
            )

    def mostrar_resultados(self, entrada, total_guardar, parcela_base, parcelas_igpm, parcelas_juros, taxa_juros):
        """Exibe os resultados em uma nova janela."""
        # Janela de resultados
        resultados_window = tk.Toplevel(self.root)
        resultados_window.title("Resultados da Simulação")
        resultados_window.geometry("600x650")
        
        # Centraliza a janela de resultados
        largura = 600
        altura = 650
        largura_tela = resultados_window.winfo_screenwidth()
        altura_tela = resultados_window.winfo_screenheight()
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2
        resultados_window.geometry(f"{largura}x{altura}+{x}+{y}")

        # Frame principal
        main_frame = ttk.Frame(resultados_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        ttk.Label(
            main_frame,
            text="RESULTADOS DA SIMULAÇÃO",
            font=('Arial', 14, 'bold'),
            foreground='#0066cc'
        ).pack(pady=(0, 15))

        # Frame de valores base
        base_frame = ttk.LabelFrame(main_frame, text=" Valores Base ", padding=10)
        base_frame.pack(fill=tk.X, pady=5)

        ttk.Label(
            base_frame,
            text=f"Valor da entrada: {locale.currency(entrada, grouping=True)}",
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=2)

        ttk.Label(
            base_frame,
            text=f"Total a guardar: {locale.currency(total_guardar, grouping=True)}",
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=2)

        ttk.Label(
            base_frame,
            text=f"Parcela mensal base: {locale.currency(parcela_base, grouping=True)}",
            font=('Arial', 10)
        ).pack(anchor=tk.W, pady=2)

        # Frame de parcelas corrigidas
        correcoes_frame = ttk.Frame(main_frame)
        correcoes_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # IGPM
        igpm_frame = ttk.LabelFrame(correcoes_frame, text=" Correção pelo IGPM (6% ao ano) ", padding=10)
        igpm_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        for ano, parcela in enumerate(parcelas_igpm, start=1):
            ttk.Label(
                igpm_frame,
                text=f"Ano {ano}: {locale.currency(parcela, grouping=True)}",
                font=('Arial', 9)
            ).pack(anchor=tk.W, pady=2)

        # Juros Compostos
        juros_frame = ttk.LabelFrame(correcoes_frame, text=f" Juros Compostos ({taxa_juros:.2f}% ao ano) ", padding=10)
        juros_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        for ano, parcela in enumerate(parcelas_juros, start=1):
            ttk.Label(
                juros_frame,
                text=f"Ano {ano}: {locale.currency(parcela, grouping=True)}",
                font=('Arial', 9)
            ).pack(anchor=tk.W, pady=2)

        # Botão de fechar
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(
            btn_frame,
            text="FECHAR",
            command=resultados_window.destroy,
            style='TButton'
        ).pack(pady=10, ipadx=30, ipady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorImovel(root)
    root.mainloop()