import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

from ui.tela_produto import abrir_tela_produto
from ui.navegacao import iniciar_interface

# Ajustar caminho do módulo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.servico_usuario import ServicoUsuario
from infra.repositorio_usuario import RepositorioUsuarioSQLite

def autenticar():
    usuario = usuario_entry.get().strip()
    senha = senha_entry.get().strip()
    
    if not usuario or not senha:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return
    
    usuario_obj = servico_usuario.buscar_usuario(usuario)
    if usuario_obj and servico_usuario.autenticar(usuario,senha):
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        root.withdraw()

        # abrir_tela_produto(usuario_obj.perfil)
        iniciar_interface(usuario_obj.perfil)
        root.destroy()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos.")

# Criar instância do serviço de usuário
repositorio_usuario = RepositorioUsuarioSQLite()
servico_usuario = ServicoUsuario(repositorio_usuario)

root = tk.Tk()
root.title("Login")
root.geometry("300x200")

ttk.Label(root, text="Usuário:").pack(pady=5)
usuario_entry = ttk.Entry(root)
usuario_entry.pack(pady=5)

ttk.Label(root, text="Senha:").pack(pady=5)
senha_entry = ttk.Entry(root, show="*")
senha_entry.pack(pady=5)
senha_entry.bind("<Return>", lambda event: autenticar())

ttk.Button(root, text="Entrar", command=autenticar).pack(pady=10)

root.mainloop()