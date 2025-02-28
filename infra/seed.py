# Arquivo para realizar a carga inicial na base de dados local
import sqlite3

def criar_seed():

    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()

    # Inserir usuários (admin e comum)
    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (nome, usuario, senha, perfil) VALUES
    ('Renata Alves', 'RenataAlves', '$2b$12$CV.WzWF9P4vKK4E2Yt2AeuDEOEgoGO4aqVFX/yLRhxbl5efZR5SEi', 'admin'),
    ('Funcionario Teste', 'FuncionarioTeste', '$2b$12$CV.WzWF9P4vKK4E2Yt2AeuDEOEgoGO4aqVFX/yLRhxbl5efZR5SEi', 'comum')
    """)
    
    # Insert produtos de escritórios
    cursor.execute("""
    INSERT OR IGNORE INTO produtos (nome, quantidade, preco, estoque_minimo) VALUES
    ('Cadeira Executiva', 10, 550.00, 2),
    ('Mesa de Escritório', 5, 1200.00, 1),
    ('Monitor 27"', 8, 1300.00, 2),
    ('Teclado sem fio', 15, 200.00, 3),
    ('Mouse sem fio', 20, 150.00, 5)
    """)
    
    conn.commit()
    conn.close()
    print("Carga Inicial, realizada com sucesso!")

if __name__ == "__main__":
    criar_seed()