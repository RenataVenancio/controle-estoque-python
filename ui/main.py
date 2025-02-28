from tkinter import ttk
import tkinter as tk
import sys
import os

# Ajustar caminho do módulo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.tela_login import autenticar
from ui.navegacao import iniciar_interface

def main():
    perfil_usuario = autenticar()
    if perfil_usuario:
        iniciar_interface(perfil_usuario)

if __name__ == "__main__":
    main()
    