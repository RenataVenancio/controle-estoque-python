import tkinter as tk
from tkinter import ttk
from ui.tela_produto import abrir_tela_produto
from ui.tela_usuario import abrir_tela_cadastro_usuario

def abrir_tela_boas_vindas(perfil_usuario):
    janela_boas_vindas = tk.Toplevel()
    janela_boas_vindas.title("Bem-vindo ao Sistema de Controle de Estoque")
    janela_boas_vindas.geometry("500x300")

    # Mensagem de boas-vindas
    ttk.Label(janela_boas_vindas, text="Bem-vindo ao Sistema de Controle de Estoque", font=("Arial", 14)).pack(pady=20)

    # Botão para Cadastrar Usuário (Sem ação no momento)
    botao_cadastrar_usuario = ttk.Button(janela_boas_vindas, text="Cadastrar Usuário", command=lambda: abrir_tela_cadastro_usuario(perfil_usuario))
    botao_cadastrar_usuario.pack(pady=20)

    # Botão para Gerenciar Produtos
    botao_gerenciar_produto = ttk.Button(janela_boas_vindas, text="Gerenciar Produtos", command=lambda: abrir_tela_produto(perfil_usuario))
    botao_gerenciar_produto.pack(pady=20)

    janela_boas_vindas.mainloop()
