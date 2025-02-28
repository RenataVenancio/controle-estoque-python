import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import openpyxl
import sys
import os

from core.produto import Produto

# Ajustar caminho do módulo
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from application.servico_produto import ServicoProduto
from infra.repositorio_produto import RepositorioProdutoSQLite
from infra.logs import registrar_log


# Criar instância do serviço de produto
repositorio = RepositorioProdutoSQLite()
servico_produto = ServicoProduto(repositorio)

def adicionar_produto(usuario):
    try:
        if validar_campos(nome_entry.get(), quantidade_entry.get(), preco_entry.get(), estoque_minimo_entry.get()):
            produto = servico_produto.adicionar_produto(
                nome_entry.get(),
                int(quantidade_entry.get()),
                float(preco_entry.get()),
                int(estoque_minimo_entry.get())
            )
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            registrar_log(usuario, "ADICIONAR", f"Produto {nome_entry.get()} adicionado")
            listar_produtos()
            limpar_campos()
            atualizar_dashboard()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def atualizar_produto(usuario):
    try:
        produto_id_str = id_entry.get().strip()

        if not produto_id_str.isdigit():
            messagebox.showerror("Erro", "Selecione um produto para atualizar.")
            return
        
        produto = Produto(
            id=int(produto_id_str),
            nome=nome_entry.get(),
            quantidade=int(quantidade_entry.get()),
            preco=float(preco_entry.get()),
            estoque_minimo=int(estoque_minimo_entry.get())
        )
        servico_produto.atualizar_produto(produto)
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
        registrar_log(usuario, "ATUALIZAR", f"Produto {produto.id} atualizado")
        listar_produtos()
        atualizar_dashboard()
        limpar_campos()
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def remover_produto(usuario):
    try:
        produto_id_str = id_entry.get().strip()
        if not produto_id_str.isdigit():
            messagebox.showerror("Erro", "Por favor, insira um ID válido para remover o produto.")
            return
        
        # Confirmação antes de excluir algum produto
        confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover o produto.")

        if confirmar:
            produto_id = int(id_entry.get())
            servico_produto.remover_produto(produto_id)
            messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
            registrar_log(usuario, "REMOVER", f"Produto {nome_entry.get()} removido")
            listar_produtos()
            limpar_campos()
            atualizar_dashboard()
        else:
            messagebox.showinfo("Cancelado", "A remoção do produto foi cancelada.")
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def listar_produtos(produtos=None):
    for row in tree.get_children():
        tree.delete(row)

    if produtos is None:
        produtos = servico_produto.listar_produtos()
    
    # id_entry.grid_remove()
    for produto in produtos:
        # tags = ("estoque_baixo",) if produto.quantidade < produto.estoque_minimo else ("")
        tags = ("estoque_baixo",) if int(produto.quantidade) < int(produto.estoque_minimo) else ("")
        tree.insert("", "end", values=(produto.id, produto.nome, produto.quantidade, produto.preco, produto.estoque_minimo), tags=tags)

def preencher_campos(event):
    selected_item = tree.selection()  # Obtém a seleção correta
    if not selected_item:
        return

    valores = tree.item(selected_item[0], "values")  # Pega os valores do item selecionado

    if valores:
        id_entry.delete(0, tk.END)
        id_entry.insert(0, valores[0])

        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, valores[1])

        quantidade_entry.delete(0, tk.END)
        quantidade_entry.insert(0, valores[2])

        preco_entry.delete(0, tk.END)
        preco_entry.insert(0, valores[3])

        estoque_minimo_entry.delete(0, tk.END)
        estoque_minimo_entry.insert(0, valores[4])

    # id_entry.grid()

def configurar_atalhos(event):
    if event.widget == id_entry:
        nome_entry.focus()
    elif event.widget == nome_entry:
        quantidade_entry.focus()
    elif event.widget == quantidade_entry:
        preco_entry.focus()
    elif event.widget == preco_entry:
        estoque_minimo_entry.focus()
    elif event.widget == estoque_minimo_entry:
        adicionar_produto()

def buscar_produto():
    termo = buscar_entry.get().strip()
    
    if not termo:
        listar_produtos()
        return
    
    try:
        produtos_encontrados = servico_produto.buscar_produto(termo)

        if produtos_encontrados:
            listar_produtos(produtos_encontrados)        
        else:
            messagebox.showinfo("Aviso", "Nenhum produto encontrado.")
            listar_produtos()
    
    except Exception as e:
        messagebox.showerror("Erro", str(e))

def limpar_campos():
    id_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    quantidade_entry.delete(0, tk.END)
    preco_entry.delete(0, tk.END)
    estoque_minimo_entry.delete(0, tk.END)
    buscar_entry.delete(0, tk.END)

    listar_produtos()

def validar_campos(nome, quantidade, preco, estoque_minimo):
        
    if not nome.strip():
        raise ValueError("O nome do produto não pode estar vazio.")
    if len(nome) > 100:
        raise ValueError("O nome deve ter no máximo 100 caracteres.")

    if not quantidade.isdigit() or int(quantidade) < 0:
        raise ValueError("A quantidade deve ser um número inteiro positivo.")

    try:
        preco = float(preco)
        if preco <= 0:
            raise ValueError("O preço deve ser um valor positivo.")
    except ValueError:
        raise ValueError("O preço deve ser um número válido.")

    if not estoque_minimo.isdigit() or int(estoque_minimo) < 0:
        raise ValueError("O estoque mínimo deve ser um número inteiro positivo ou zero.")

    return True 

def atualizar_dashboard():
    total_produtos = repositorio.contar_total_produtos()
    baixo_estoque = repositorio.contar_estoque_baixo()
    valor_total = repositorio.calcular_valor_total_estoque()

    total_produtos_label.config(text=f"Total de Produtos: {total_produtos}")
    baixo_estoque_label.config(text=f"Produtos em Baixo Estoque: {baixo_estoque}")
    valor_total_label.config(text=f"Valor Total em Estoque: {valor_total:.2f}")

def exportar_para_excel():
    try:
        # Abri uma janela para escolher onde o arquivo será salvo
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Arquivos Excel", "*.xlsx")])
        if not arquivo:
            return

        produtos = servico_produto.listar_produtos()

        # Criar a planilha
        wb = openpyxl.Workbook()

        # Aba 1: Todos os produtos
        aba_todos = wb.active
        aba_todos.title = "Todos os Produtos"

        # Cabeçalho
        colunas = ["ID", "Nome", "Quantidade", "Preço", "Estoque Mínimo"]
        aba_todos.append(colunas)

        # Dados
        for produto in produtos:
            aba_todos.append([produto.id, produto.nome, produto.quantidade, produto.preco, produto.estoque_minimo])

        # Aba 2: Produtos em baixo estoque
        aba_estoque_baixo = wb.create_sheet(title="Estoque Baixo")
        aba_estoque_baixo.append(colunas)

        for produto in produtos:
            if produto.quantidade < produto.estoque_minimo:
                aba_estoque_baixo.append([produto.id, produto.nome, produto.quantidade, produto.preco, produto.estoque_minimo])

        # Salvar o arquivo
        wb.save(arquivo)

        messagebox.showinfo("Sucesso", "Produtos exportados para Excel com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar para Excel: {e}")


def abrir_tela_produto(perfil_usuario):
    global id_entry, nome_entry, quantidade_entry, preco_entry, estoque_minimo_entry, buscar_entry, tree
    global total_produtos_label, baixo_estoque_label, valor_total_label
    
    janela = tk.Toplevel()
    janela.title("Gerenciamento de Produtos")
    janela.geometry("1050x550")

    # Frame para agrupar os campos
    form_frame = ttk.Frame(janela, padding=10)
    form_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)
    
    label_id = ttk.Label(form_frame, text="ID:")
    label_id.grid(row=0, column=0, sticky="e", padx=5, pady=5)
    label_id.grid_remove()

    id_entry = ttk.Entry(form_frame)
    id_entry.grid(row=0, column=1, padx=5, pady=5)
    id_entry.bind("<Return>", configurar_atalhos)
    id_entry.grid_remove()
    
    ttk.Label(form_frame, text="Nome:").grid(row=1, column=0, sticky="e",  padx=5, pady=5)
    nome_entry = ttk.Entry(form_frame)
    nome_entry.grid(row=1, column=1, padx=5, pady=5)
    nome_entry.bind("<Return>", configurar_atalhos)
    
    ttk.Label(form_frame, text="Quantidade:").grid(row=2, column=0, sticky="e",  padx=5, pady=5)
    quantidade_entry = ttk.Entry(form_frame)
    quantidade_entry.grid(row=2, column=1, padx=5, pady=5)
    quantidade_entry.bind("<Return>", configurar_atalhos)
    
    ttk.Label(form_frame, text="Preço:").grid(row=3, column=0, sticky="e",  padx=5, pady=5)
    preco_entry = ttk.Entry(form_frame)
    preco_entry.grid(row=3, column=1, padx=5, pady=5)
    preco_entry.bind("<Return>", configurar_atalhos)
    
    ttk.Label(form_frame, text="Estoque Mínimo:").grid(row=4, column=0, sticky="e",  padx=5, pady=5)
    estoque_minimo_entry = ttk.Entry(form_frame)
    estoque_minimo_entry.grid(row=4, column=1, padx=5, pady=5)
    estoque_minimo_entry.bind("<Return>", configurar_atalhos)

    ttk.Label(form_frame, text="Buscar (ID ou Nome):").grid(row=5, column=0, sticky="e",  padx=5, pady=5)
    buscar_entry = ttk.Entry(form_frame)
    buscar_entry.grid(row=5, column=1, padx=5, pady=5)

    # Frame para agrupar os botões
    button_frame = ttk.Frame(janela, padding=10)
    button_frame.grid(row=1, column=0, sticky="ew", padx=10)
    
    botao_adicionar = ttk.Button(button_frame, text="Adicionar", command=lambda: adicionar_produto(perfil_usuario), state="normal" if perfil_usuario == "admin" else "disabled")
    botao_adicionar.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    botao_adicionar.bind("<Return>", lambda event: adicionar_produto(perfil_usuario))

    botao_remover = ttk.Button(button_frame, text="Remover", command=lambda:remover_produto(perfil_usuario), state="normal" if perfil_usuario == "admin" else "disabled")
    botao_remover.grid(row=0, column=2, columnspan=2, pady=10, padx=10)
    botao_remover.bind("<Return>", lambda event: remover_produto(perfil_usuario))
    
    botao_atualizar = ttk.Button(button_frame, text="Atualizar", command=lambda: atualizar_produto(perfil_usuario), state="normal" if perfil_usuario == "admin" else "disabled")
    botao_atualizar.grid(row=0, column=4, columnspan=2, pady=10, padx=10)
    botao_atualizar.bind("<Return>", lambda event: atualizar_produto(perfil_usuario))

    botao_buscar = ttk.Button(button_frame, text="Buscar", command=lambda: buscar_produto(), state="normal")
    botao_buscar.grid(row=0, column=6, columnspan=2, pady=10, padx=10)
    botao_buscar.bind("<Return>", lambda event: buscar_produto())

    botao_limpar = ttk.Button(button_frame, text="Limpar Campos", command=limpar_campos)
    botao_limpar.grid(row=0, column=8, columnspan=2, pady=10, padx=10)
    
    botao_exportar = ttk.Button(button_frame, text="Exportar Lista Produtos", command=exportar_para_excel)
    botao_exportar.grid(row=0, column=10, columnspan=2, pady=10, padx=10)

    dashboard_frame = ttk.Frame(janela, padding=5)
    dashboard_frame.grid(row=2, column=0, sticky="w")

    total_produtos_label = ttk.Label(dashboard_frame, text="Total de Produtos: 0")
    total_produtos_label.grid(row=2, column=0, padx=10)

    baixo_estoque_label = ttk.Label(dashboard_frame, text="Produtos em Baixo Estoque: 0")
    baixo_estoque_label.grid(row=2, column=1, padx=10)

    valor_total_label = ttk.Label(dashboard_frame, text="Valor Total em Estoque: R$ 0.00")
    valor_total_label.grid(row=2, column=2, padx=10)
    
    # Frame para agrupar a tabela
    tree_frame = ttk.Frame(janela, padding=10)
    tree_frame.grid(row=3, column=0, columnspan=2, pady=10)
    
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side="right", fill="y")
    
    tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Quantidade", "Preço", "Estoque Mínimo"), show="headings", yscrollcommand=tree_scroll.set)
    tree_scroll.config(command=tree.yview)
    tree.bind("<ButtonRelease-1>", preencher_campos)  # Evento para preencher campos ao clicar na linha
    
    tree.tag_configure("estoque_baixo", background="red")

    for col in ("ID", "Nome", "Quantidade", "Preço", "Estoque Mínimo"):
        tree.heading(col, text=col)
    
    tree.pack(expand=True, fill="both")

    atualizar_dashboard()
    
    listar_produtos()  # Carregar produtos ao abrir a tela
    janela.mainloop()
