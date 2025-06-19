import tkinter as tk
from tkinter import messagebox
import json
import random
import os


ARQUIVO_PALAVRAS = "palavras.json"
NUM_TENTATIVAS = 5
TAMANHO_PALAVRA = 5

# CORES PARA TEMAS
TEMAS = {
    "claro": {
        "bg": "#fafafa", "fg": "#222", "btn": "#e0e0e0", "btnfg": "#333",
        "verde": "#6aaa64", "amarelo": "#c9b458", "cinza": "#888",
        "borda": "#ccc"
    },
    "escuro": {
        "bg": "#222", "fg": "#fafafa", "btn": "#444", "btnfg": "#fafafa",
        "verde": "#538d4e", "amarelo": "#b59f3b", "cinza": "#444",
        "borda": "#555"
    }
}

class TermoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo Termo")
        self.tema_atual = "claro"
        self.tema = TEMAS[self.tema_atual]
        self.tentativas = NUM_TENTATIVAS
        self.tentativas_extra = 2
        self.letras = []
        self.palavra_atual = ""
        self.jogo_ativo = True
        self.chances_restantes = self.tentativas
        self.historico = []

        self.carregar_palavras()
        self.sortear_palavra()
        self.montar_interface()
        self.root.bind("<Return>", self.enviar_palavra)
        self.root.bind("<Key>", self.capturar_tecla)

    def carregar_palavras(self):
        try:
            with open(ARQUIVO_PALAVRAS, "r", encoding="utf-8") as f:
                self.palavras = json.load(f)["palavras"]
        except Exception:
            self.palavras = ["carta", "pedra", "salto", "prato", "verde"]  # Fallback

    def sortear_palavra(self):
        self.palavra_atual = random.choice(self.palavras).lower()
        self.letras = []
        self.chances_restantes = self.tentativas
        self.historico.clear()
        self.jogo_ativo = True

    def montar_interface(self):
        # Reset tela
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=self.tema["bg"])

        # Header
        topo = tk.Frame(self.root, bg=self.tema["bg"])
        topo.pack(pady=10)
        tk.Label(
            topo, text="Termo", font=("Arial", 22, "bold"),
            bg=self.tema["bg"], fg=self.tema["fg"]
        ).pack(side="left", padx=10)

        # Botão de tema
        btn_tema = tk.Button(
            topo, text="🌞" if self.tema_atual == "escuro" else "🌙",
            command=self.alternar_tema, bg=self.tema["btn"], fg=self.tema["btnfg"],
            bd=0, relief="flat"
        )
        btn_tema.pack(side="right", padx=10)

        # Grade de tentativas
        self.grade = []
        self.grade_frame = tk.Frame(self.root, bg=self.tema["bg"])
        self.grade_frame.pack(pady=10)
        for i in range(self.tentativas + self.tentativas_extra):
            linha = []
            for j in range(TAMANHO_PALAVRA):
                label = tk.Label(
                    self.grade_frame, text="", width=3, height=2,
                    font=("Arial", 20, "bold"),
                    relief="groove", bd=2, bg=self.tema["bg"], fg=self.tema["fg"],
                    highlightbackground=self.tema["borda"]
                )
                label.grid(row=i, column=j, padx=3, pady=2)
                linha.append(label)
            self.grade.append(linha)

        # Info de chances
        self.info = tk.Label(
            self.root,
            text=f"Tentativas restantes: {self.chances_restantes}",
            bg=self.tema["bg"], fg=self.tema["fg"],
            font=("Arial", 12)
        )
        self.info.pack(pady=(10,0))

        # Entrada oculta (usaremos o teclado do sistema)
        self.entrada = ""
        # Foco para teclado físico
        self.root.focus_force()

    def alternar_tema(self):
        self.tema_atual = "escuro" if self.tema_atual == "claro" else "claro"
        self.tema = TEMAS[self.tema_atual]
        self.montar_interface()
        self.preencher_historico()

    def capturar_tecla(self, event):
        if not self.jogo_ativo:
            return
        if event.keysym in ("BackSpace", "Delete"):
            self.entrada = self.entrada[:-1]
        elif event.keysym == "Return":
            pass  # Enter já tratado
        elif len(event.char) == 1 and event.char.isalpha() and len(self.entrada) < TAMANHO_PALAVRA:
            self.entrada += event.char.lower()
        self.atualizar_grade_input()

    def atualizar_grade_input(self):
        linha = len(self.historico)
        for j in range(TAMANHO_PALAVRA):
            char = self.entrada[j] if j < len(self.entrada) else ""
            self.grade[linha][j].config(text=char)

    def enviar_palavra(self, event=None):
        if not self.jogo_ativo or len(self.entrada) != TAMANHO_PALAVRA:
            return
        palavra = self.entrada
        self.entrada = ""
        resultado = self.checar_palavra(palavra)
        self.historico.append((palavra, resultado))
        self.atualizar_grade_resultado(palavra, resultado, len(self.historico)-1)
        if palavra == self.palavra_atual:
            self.jogo_ativo = False
            self.info.config(text="Parabéns! Você acertou! Próxima palavra?")
            self.continuar_ou_proxima()
        else:
            self.chances_restantes -= 1
            self.info.config(text=f"Tentativas restantes: {self.chances_restantes}")
            if self.chances_restantes == 0:
                self.jogo_ativo = False
                self.info.config(text=f"Fim! A palavra era: {self.palavra_atual.upper()}")
                self.tentar_ou_pular()

    def checar_palavra(self, palavra):
        resultado = ["cinza"] * TAMANHO_PALAVRA
        temp = list(self.palavra_atual)
        # Verdes
        for i in range(TAMANHO_PALAVRA):
            if palavra[i] == self.palavra_atual[i]:
                resultado[i] = "verde"
                temp[i] = None
        # Amarelos
        for i in range(TAMANHO_PALAVRA):
            if resultado[i] == "cinza" and palavra[i] in temp:
                resultado[i] = "amarelo"
                temp[temp.index(palavra[i])] = None
        return resultado

    def atualizar_grade_resultado(self, palavra, resultado, linha):
        for j in range(TAMANHO_PALAVRA):
            cor = self.tema[resultado[j]]
            self.grade[linha][j].config(text=palavra[j].upper(), bg=cor, fg="#fff")
        self.entrada = ""

    def preencher_historico(self):
        # Reaplicar histórico após troca de tema
        for i, (palavra, resultado) in enumerate(self.historico):
            for j in range(TAMANHO_PALAVRA):
                cor = self.tema[resultado[j]]
                self.grade[i][j].config(text=palavra[j].upper(), bg=cor, fg="#fff")

    def tentar_ou_pular(self):
        def tentar():
            self.chances_restantes = self.tentativas_extra
            self.info.config(text=f"Tentativas extras: {self.chances_restantes}")
            self.jogo_ativo = True
            top.destroy()

        def passar():
            self.sortear_palavra()
            self.montar_interface()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Fim de Jogo")
        top.configure(bg=self.tema["bg"])
        msg = tk.Label(
            top, text="Deseja tentar novamente com mais 2 chances ou passar para a próxima palavra?",
            bg=self.tema["bg"], fg=self.tema["fg"], font=("Arial", 12), wraplength=280
        )
        msg.pack(pady=10, padx=20)
        b1 = tk.Button(top, text="Tentar novamente (+2)", command=tentar, bg=self.tema["btn"], fg=self.tema["btnfg"])
        b1.pack(side="left", padx=10, pady=10)
        b2 = tk.Button(top, text="Próxima palavra", command=passar, bg=self.tema["btn"], fg=self.tema["btnfg"])
        b2.pack(side="right", padx=10, pady=10)
        top.grab_set()

    def continuar_ou_proxima(self):
        def proxima():
            self.sortear_palavra()
            self.montar_interface()
            top.destroy()

        top = tk.Toplevel(self.root)
        top.title("Parabéns!")
        top.configure(bg=self.tema["bg"])
        msg = tk.Label(
            top, text="Você acertou! Ir para a próxima palavra?",
            bg=self.tema["bg"], fg=self.tema["fg"], font=("Arial", 12), wraplength=280
        )
        msg.pack(pady=10, padx=20)
        b = tk.Button(top, text="Próxima palavra", command=proxima, bg=self.tema["btn"], fg=self.tema["btnfg"])
        b.pack(pady=10)
        top.grab_set()


if __name__ == "__main__":
    root = tk.Tk()
    app = TermoApp(root)
    root.mainloop()
