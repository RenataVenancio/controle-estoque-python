import sqlite3

def conectar():
    return sqlite3.connect("estoque.db")