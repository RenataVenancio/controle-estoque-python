import sqlite3
import datetime

# Registrar log no banco de dados
def registrar_log_banco(usuario, acao):
    try:
        conexao = sqlite3.connect('estoque.db')
        cursor = conexao.cursor()

        data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
                        INSERT INTO logs (usuario, acao, data_hora)
                       VALUES (?, ?, ?)''', (usuario, acao, data_hora))
        
        conexao.commit()
    except Exception as e:
        print(f"Erro ao registrar log no banco: {e}")
    finally:
        conexao.close()

def registrar_log_arquivo(acao, descricao):
    with open("log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {acao}: {descricao}\n")

# Função unificada para registrar em ambos
def registrar_log(usuario, acao, descricao):
    registrar_log_banco(usuario, acao)
    registrar_log_arquivo(acao, descricao)

# # Exemplo de uso:
# if __name__ == "__main__":
#     registrar_log("admin", "LOGIN", "Admin acessou o sistema")
#     registrar_log("admin", "ADICIONAR", "Produto ID 123 foi adicionado")