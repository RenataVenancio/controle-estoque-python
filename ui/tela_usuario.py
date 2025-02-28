import tkinter as tk
from tkinter import ttk, messagebox
from application.servico_usuario import ServicoUsuario
from infra.repositorio_usuario import RepositorioUsuarioSQLite
from infra.logs import registrar_log
from core.usuario import Usuario

def abrir_tela_cadastro_usuario(usuario_logado):
    if usuario_logado != "admin":
        messagebox.showerror("Acesso Negado", "Apenas administradores podem gerenciar usuários.")
        return

    repositorio_usuario = RepositorioUsuarioSQLite()
    servico_usuario = ServicoUsuario(repositorio_usuario)

    def cadastrar_usuario():
        nome = nome_entry.get().strip()
        usuario = usuario_entry.get().strip()
        senha = senha_entry.get().strip()
        perfil = perfil_combobox.get().strip().lower()

        if not nome or not usuario or not senha or not perfil:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return

        if perfil not in ("admin", "comum"):
            messagebox.showerror("Erro", "Perfil inválido. Escolha 'admin' ou 'comum'.")
            return

        try:
            novo_usuario = Usuario(None, nome, usuario, senha, perfil)
            servico_usuario.adicionar_usuario(novo_usuario)
            registrar_log(usuario_logado, "CADASTRO", f"Usuário {usuario} cadastrado com perfil {perfil}")
            messagebox.showinfo("Sucesso", f"Usuário {usuario} cadastrado com sucesso!")
            listar_usuarios()
            limpar_campos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    def listar_usuarios():
        for item in tree.get_children():
            tree.delete(item)

        usuarios = servico_usuario.listar_usuario()
        for usuario in usuarios:
            tree.insert("", "end", values=(usuario.id, usuario.nome, usuario.usuario, usuario.perfil))

    def preencher_campos(event):
        selecionado = tree.selection()
        if not selecionado:
            return

        valores = tree.item(selecionado[0], "values")

        id_entry.delete(0, tk.END)
        id_entry.insert(0, valores[0])

        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, valores[1])

        usuario_entry.delete(0, tk.END)
        usuario_entry.insert(0, valores[2])

        perfil_combobox.set(valores[3])

    def limpar_campos():
        id_entry.delete(0, tk.END)
        nome_entry.delete(0, tk.END)
        usuario_entry.delete(0, tk.END)
        senha_entry.delete(0, tk.END)
        perfil_combobox.set("")

    # Criar a janela de gerenciamento de usuários
    janela_cadastro = tk.Toplevel()
    janela_cadastro.title("Gerenciamento de Usuários")
    janela_cadastro.geometry("850x500")


    # Frame para agrupar os campos de formulário
    form_frame = ttk.Frame(janela_cadastro, padding=10)
    form_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    
    # Formulário de Cadastro
    id_entry = ttk.Entry(form_frame, state="disabled")
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    id_entry.grid_remove()

    ttk.Label(form_frame, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
    nome_entry = ttk.Entry(form_frame)
    nome_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Usuário:").grid(row=2, column=0, padx=5, pady=5)
    usuario_entry = ttk.Entry(form_frame)
    usuario_entry.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Senha:").grid(row=3, column=0, padx=5, pady=5)
    senha_entry = ttk.Entry(form_frame, show="*")
    senha_entry.grid(row=3, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Perfil (admin/comum):").grid(row=4, column=0, padx=5, pady=5)
    perfil_combobox = ttk.Combobox(form_frame, values=["admin", "comum"])
    perfil_combobox.grid(row=4, column=1, padx=5, pady=5)

    # Frame para agrupar os botões
    button_frame = ttk.Frame(janela_cadastro, padding=10)
    button_frame.grid(row=1, column=0, sticky="ew", padx=10)
    ttk.Button(button_frame, text="Cadastrar", command=cadastrar_usuario).grid(row=5, column=0, columnspan=2, pady=20)

     # Frame para agrupar a tabela
    tree_frame = ttk.Frame(janela_cadastro, padding=10)
    tree_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")

    # Tabela de Usuários
    tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Usuário", "Perfil"), show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)
    tree.bind("<ButtonRelease-1>", preencher_campos)

    for coluna in ("ID", "Nome", "Usuário", "Perfil"):
        tree.heading(coluna, text=coluna)

    # tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tree.pack(expand=True, fill="both")

    listar_usuarios()
    janela_cadastro.mainloop()
