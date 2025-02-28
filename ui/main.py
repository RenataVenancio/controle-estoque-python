from tkinter import ttk
import tkinter as tk
import sys
import os

# Ajustar caminho do módulo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.tela_login import autenticar
from ui.tela_produto import abrir_tela_produto
from ui.navegacao import iniciar_interface

# def iniciar_interface(perfil_usuario):
#     root = tk.Tk()
#     root.title("Sistema de Control de Estoque")
#     root.geometry("800x600")

#     label = ttk.Label(root, text = "Bem vindo ao Sistema de Contole de Estoque", font=("Arial", 14))
#     label.pack(pady=20)

#     botao_produtos = ttk.Button(root, text="Gerenciar Produtos", command=lambda: abrir_tela_produto(perfil_usuario))
#     botao_produtos.pack(pady=10)

#     botao_sair = ttk.Button(root, text = "Sair", command=root.quit)
#     botao_sair.pack(pady=20)

#     root.mainloop()

def main():
    perfil_usuario = autenticar()
    if perfil_usuario:
        iniciar_interface(perfil_usuario)

if __name__ == "__main__":
    main()
    # perfil_usuario = autenticar()
    # if perfil_usuario:
    #     iniciar_interface(perfil_usuario)
