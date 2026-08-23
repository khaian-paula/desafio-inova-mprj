"""
Interface gráfica (Tkinter) para o protótipo de busca. reaproveita as
funções de simple_search.py.

Funciona com qualquer um dos corpus gerados neste desafio:
- data/corpus.json (sintético, com os números oficiais citados na proposta)
- data/corpus_real.json (real, via API do Querido Diário)

Como rodar:
    python3 app_grafico.py
(ou python / py, dependendo do que funcionar na sua máquina)

Precisa estar na mesma pasta que simple_search.py, porque importa
as funções de busca dele em vez de reescrever a lógica.

Tkinter já vem junto com o Python padrão instalado do python.org.
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from simple_search import (
    buscar,
    contar_em_quantos_documentos_cada_termo_aparece,
)


class AppBusca:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Protótipo — Desafio Técnico Inova_MPRJ (não oficial)")
        self.raiz.geometry("900x650")

        self.documentos = []
        self.contagem_palavra = {}
        self.contagem_ngrama = {}
        self.resultados_atuais = []

        self._montar_interface()
        self._tentar_carregar_padrao()

    def _montar_interface(self):
        # --- barra superior: carregar base ---
        barra_topo = ttk.Frame(self.raiz, padding=10)
        barra_topo.pack(fill="x")

        ttk.Button(barra_topo, text="Carregar base de dados...",
                   command=self.carregar_base).pack(side="left")

        self.label_base = ttk.Label(barra_topo, text="Nenhuma base carregada")
        self.label_base.pack(side="left", padx=10)

        # --- barra de busca ---
        barra_busca = ttk.Frame(self.raiz, padding=(10, 0, 10, 10))
        barra_busca.pack(fill="x")

        ttk.Label(barra_busca, text="Pergunta:").pack(side="left")
        self.campo_pergunta = ttk.Entry(barra_busca)
        self.campo_pergunta.pack(side="left", fill="x", expand=True, padx=8)
        self.campo_pergunta.bind("<Return>", lambda evento: self.executar_busca())

        ttk.Button(barra_busca, text="Buscar", command=self.executar_busca).pack(side="left")

        # --- painel dividido: lista de resultados (em cima) + texto completo (embaixo) ---
        painel = ttk.PanedWindow(self.raiz, orient="vertical")
        painel.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        frame_lista = ttk.Frame(painel)
        colunas = ("doc_id", "tipo", "placar")
        self.tabela = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=8)
        self.tabela.heading("doc_id", text="Documento")
        self.tabela.heading("tipo", text="Tipo")
        self.tabela.heading("placar", text="Placar")
        self.tabela.column("doc_id", width=110)
        self.tabela.column("tipo", width=220)
        self.tabela.column("placar", width=100)
        self.tabela.pack(fill="both", expand=True, side="left")

        barra_rolagem = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscroll=barra_rolagem.set)
        barra_rolagem.pack(side="right", fill="y")

        self.tabela.bind("<<TreeviewSelect>>", self.mostrar_texto_completo)
        painel.add(frame_lista, weight=1)

        frame_texto = ttk.Frame(painel)
        ttk.Label(frame_texto, text="Texto completo do documento selecionado:").pack(anchor="w")
        self.texto_completo = tk.Text(frame_texto, wrap="word", height=14)
        self.texto_completo.pack(fill="both", expand=True, side="left")
        barra_rolagem_texto = ttk.Scrollbar(frame_texto, orient="vertical",
                                             command=self.texto_completo.yview)
        self.texto_completo.configure(yscroll=barra_rolagem_texto.set)
        barra_rolagem_texto.pack(side="right", fill="y")
        painel.add(frame_texto, weight=1)

        # --- barra de status ---
        self.label_status = ttk.Label(self.raiz, text="", padding=(10, 4))
        self.label_status.pack(fill="x")

    def _tentar_carregar_padrao(self):
        """Ao abrir o programa, tenta carregar sozinho o corpus sintético
        ou o real, se algum deles já existir na pasta data/ ao lado."""
        for caminho_padrao in ("data/corpus.json", "data/corpus_real.json"):
            if os.path.exists(caminho_padrao):
                self._carregar_arquivo(caminho_padrao)
                return

    def carregar_base(self):
        caminho = filedialog.askopenfilename(
            title="Escolha o arquivo de corpus (.json)",
            filetypes=[("Arquivo JSON", "*.json"), ("Todos os arquivos", "*.*")],
        )
        if caminho:
            self._carregar_arquivo(caminho)

    def _carregar_arquivo(self, caminho):
        try:
            with open(caminho, encoding="utf-8") as arquivo:
                self.documentos = json.load(arquivo)
        except Exception as erro:
            messagebox.showerror("Erro ao carregar arquivo", str(erro))
            return

        self.contagem_palavra, self.contagem_ngrama = contar_em_quantos_documentos_cada_termo_aparece(
            self.documentos
        )
        self.label_base.config(
            text=os.path.basename(caminho) + " — " + str(len(self.documentos)) + " documentos"
        )
        self.label_status.config(text="Base carregada. Digite uma pergunta e aperte Buscar.")

    def executar_busca(self):
        if not self.documentos:
            messagebox.showwarning("Sem base carregada",
                                    "Carregue um arquivo de corpus primeiro (botão no topo).")
            return

        pergunta = self.campo_pergunta.get().strip()
        if not pergunta:
            return

        self.resultados_atuais = buscar(
            pergunta, self.documentos, self.contagem_palavra, self.contagem_ngrama,
            quantos_resultados=10,
        )

        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        for placar, documento in self.resultados_atuais:
            self.tabela.insert(
                "", "end", iid=documento["doc_id"],
                values=(documento["doc_id"], documento["tipo"], "{:.1f}".format(placar)),
            )

        self.texto_completo.delete("1.0", "end")

        if len(self.resultados_atuais) == 0:
            self.label_status.config(text="Nenhum resultado encontrado para essa pergunta.")
        else:
            self.label_status.config(
                text=str(len(self.resultados_atuais)) +
                " resultado(s) encontrado(s). Clique num resultado para ver o texto completo."
            )

    def mostrar_texto_completo(self, evento):
        selecionado = self.tabela.selection()
        if not selecionado:
            return
        doc_id_selecionado = selecionado[0]

        documento_escolhido = None
        for placar, documento in self.resultados_atuais:
            if documento["doc_id"] == doc_id_selecionado:
                documento_escolhido = documento
                break
        if documento_escolhido is None:
            return

        self.texto_completo.delete("1.0", "end")
        cabecalho = "[" + documento_escolhido["doc_id"] + "] " + documento_escolhido["tipo"] + "\n"
        if documento_escolhido.get("fonte_original"):
            cabecalho += "Fonte: " + documento_escolhido["fonte_original"] + "\n"
        if documento_escolhido.get("data_publicacao"):
            cabecalho += "Data: " + documento_escolhido["data_publicacao"] + "\n"
        cabecalho += "\n"
        self.texto_completo.insert("end", cabecalho + documento_escolhido["texto"])


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AppBusca(raiz)
    raiz.mainloop()
