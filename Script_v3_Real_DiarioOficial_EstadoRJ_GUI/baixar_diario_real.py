"""
Baixa trechos reais do Diário Oficial do Município do Rio de Janeiro via a
API pública do Querido Diário (Open Knowledge Brasil) e converte pro mesmo
formato do nosso corpus sintético, pra testar o simple_search_beginner.py
com texto de verdade.

IMPORTANTE — leia antes de rodar:
- Isso é só um teste exploratório. O arquivo gerado aqui NÃO tem gabarito
  de relevância (não sabemos, de antemão, quais desses trechos são "a
  resposta certa" pra nenhuma pergunta) — então não dá pra calcular
  precisão/recall com ele, só olhar se os resultados fazem sentido.
- Precisa de internet (diferente do corpus sintético, que roda 100% offline).
- Sem biblioteca externa: usa só urllib, que já vem no Python.

Como rodar:
    python3 baixar_diario_real.py
Isso cria data/corpus_real.json. Depois, pra testar com ele, edite a linha
CORPUS_PATH no simple_search_beginner.py para "data/corpus_real.json"
(ou copie esse arquivo por cima do data/corpus.json, fazendo antes uma
cópia de segurança do original).
"""

import urllib.request
import urllib.parse
import json
import os

TERRITORY_ID = "3304557"  # Rio de Janeiro (capital) — código do IBGE
BASE_URL = "https://api.queridodiario.ok.org.br/gazettes"

# Termos variados, pra trazer diversidade de assunto (parecido com os 3
# tópicos que usamos no corpus sintético: obras, saúde, meio ambiente)
TERMOS_DE_BUSCA = [
    "licitação obras",
    "saúde contrato",
    "fiscalização ambiental",
    "convênio",
    "prestação de contas",
]

QUANTIDADE_POR_TERMO = 15


def buscar_diarios(querystring, tamanho):
    url = (
        BASE_URL
        + "?territory_ids=" + TERRITORY_ID
        + "&querystring=" + urllib.parse.quote(querystring)
        + "&excerpt_size=600"
        + "&number_of_excerpts=1"
        + "&size=" + str(tamanho)
    )
    print("Buscando:", querystring, "...")
    requisicao = urllib.request.Request(url, headers={"User-Agent": "teste-inova-mprj/1.0"})
    with urllib.request.urlopen(requisicao, timeout=30) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))
    return dados


def montar_corpus():
    documentos = []
    doc_id = 0
    ids_ja_vistos = []  # evita duplicar o mesmo diário se aparecer em mais de uma busca

    for termo in TERMOS_DE_BUSCA:
        try:
            resultado = buscar_diarios(termo, QUANTIDADE_POR_TERMO)
        except Exception as erro:
            print("  Não deu pra buscar '" + termo + "':", erro)
            continue

        itens = resultado.get("gazettes", [])
        print("  " + str(len(itens)) + " resultados encontrados.")

        for item in itens:
            identificador_original = item.get("url", "")
            if identificador_original and identificador_original in ids_ja_vistos:
                continue
            if identificador_original:
                ids_ja_vistos.append(identificador_original)

            trechos = item.get("excerpts", [])
            texto = " ".join(trechos) if trechos else ""
            if not texto.strip():
                continue

            documentos.append({
                "doc_id": "REAL{:04d}".format(doc_id),
                "tipo": "Diário Oficial (RJ capital)",
                "relevant_for": [],  # sem gabarito — dado real, não sintético
                "texto": texto,
                "fonte_original": item.get("url", ""),
                "data_publicacao": item.get("date", ""),
                "termo_de_busca_usado": termo,
            })
            doc_id += 1

    return documentos


if __name__ == "__main__":
    docs = montar_corpus()
    print("\nTotal de documentos reais coletados:", len(docs))

    os.makedirs("data", exist_ok=True)
    with open("data/corpus_real.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print("Salvo em data/corpus_real.json")
    print("\nLembrete: esse arquivo não tem gabarito de relevância — é só pra")
    print("teste exploratório, não pra gerar métrica nova de precisão/recall.")
