from banco import conectar

# Script para criar as tabelas necessárias para aplicação
def criar_tabelas():
    
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade INTERGER NOT NULL,
                    preco REAL NOT NULL,
                    estoque_minimo INTERGER NOT NULL
                   )''')
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS usuarios(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    usuario TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    perfil TEXT NOT NULL CHECK(perfil in ('admin', 'comum'))
                   )''')
    
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS logs(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL,
                    acao TEXT NOT NULL,
                    data_hora TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados e tabelas criados com sucesso!")