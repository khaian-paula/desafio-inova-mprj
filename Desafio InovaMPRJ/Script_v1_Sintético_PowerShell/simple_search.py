"""
Protótipo de busca por documento.

Como rodar:
    python3 simple_search.py
Digite uma pergunta e aperte Enter. Digite "sair" para encerrar.
"""

import json

CORPUS_PATH = "data/corpus.json"


def normalizar(texto):
    """Deixa tudo minúsculo e troca letra acentuada pela versão sem
    acento, pra 'obras' e 'Obras' contarem como a mesma palavra."""
    texto = texto.lower()
    troca_de_letras = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u",
        "ç": "c",
    }
    for letra_com_acento in troca_de_letras:
        letra_sem_acento = troca_de_letras[letra_com_acento]
        texto = texto.replace(letra_com_acento, letra_sem_acento)
    return texto


def tirar_pontuacao(texto):
    """Troca cada sinal de pontuação por um espaço, pra não grudar na
    palavra do lado (ex: 'obras.' vira 'obras ')."""
    sinais = [".", ",", ";", ":", "!", "?", "(", ")", '"', "'", "-", "/"]
    for sinal in sinais:
        texto = texto.replace(sinal, " ")
    return texto


def palavras(texto):
    """Transforma um texto numa lista de palavras."""
    texto = normalizar(texto)
    texto = tirar_pontuacao(texto)
    lista_de_palavras = texto.split()
    return lista_de_palavras


def sem_repetir(lista):
    """Recebe uma lista e devolve outra sem itens repetidos"""
    lista_nova = []
    for item in lista:
        if item not in lista_nova:
            lista_nova.append(item)
    return lista_nova


def n_gramas_de_caractere(texto, tamanho=4):
    """Quebra o texto em pedacinhos de 4 letras, um deslizando por cima do
    outro. Isso ajuda a encontrar documento mesmo com erro de digitação ou
    de digitalização."""
    texto = normalizar(texto)
    texto = texto.replace(" ", "")
    pedacos = []
    posicao = 0
    while posicao + tamanho <= len(texto):
        pedaco = texto[posicao:posicao + tamanho]
        pedacos.append(pedaco)
        posicao = posicao + 1
    return pedacos


def contar_em_quantos_documentos_cada_termo_aparece(documentos):
    """Pra cada palavra (e pra cada pedacinho de 4 letras) do acervo
    inteiro, conta em quantos documentos diferentes ela aparece."""
    quantos_docs_tem_a_palavra = {}
    quantos_docs_tem_o_ngrama = {}

    for documento in documentos:
        lista_de_palavras = palavras(documento["texto"])
        palavras_unicas_do_doc = sem_repetir(lista_de_palavras)
        for palavra in palavras_unicas_do_doc:
            if palavra in quantos_docs_tem_a_palavra:
                quantos_docs_tem_a_palavra[palavra] = quantos_docs_tem_a_palavra[palavra] + 1
            else:
                quantos_docs_tem_a_palavra[palavra] = 1

        lista_de_ngramas = n_gramas_de_caractere(documento["texto"])
        ngramas_unicos_do_doc = sem_repetir(lista_de_ngramas)
        for ngrama in ngramas_unicos_do_doc:
            if ngrama in quantos_docs_tem_o_ngrama:
                quantos_docs_tem_o_ngrama[ngrama] = quantos_docs_tem_o_ngrama[ngrama] + 1
            else:
                quantos_docs_tem_o_ngrama[ngrama] = 1

    return quantos_docs_tem_a_palavra, quantos_docs_tem_o_ngrama


def peso_por_raridade(termo, contagem_de_documentos, total_de_documentos):
    """Um termo que aparece em quase todo documento (ex: 'de', 'ofício')
    vale pouco pra decidir relevância. Um termo raro vale muito mais.
    Fazemos isso dividindo o total de documentos pela quantidade de
    documentos que têm esse termo, quanto menor essa quantidade, maior o
    resultado da divisão."""
    if termo in contagem_de_documentos:
        quantos_docs_tem = contagem_de_documentos[termo]
    else:
        quantos_docs_tem = 0
    peso = total_de_documentos / (quantos_docs_tem + 1)
    return peso


def soma_dos_pesos_em_comum(lista_a, lista_b, contagem_de_documentos, total_de_documentos):
    """Olha o que existe nas duas listas ao mesmo tempo, e soma o peso de
    cada item que aparece nas duas."""
    lista_a_unica = sem_repetir(lista_a)
    lista_b_unica = sem_repetir(lista_b)
    soma = 0
    for item in lista_a_unica:
        if item in lista_b_unica:
            soma = soma + peso_por_raridade(item, contagem_de_documentos, total_de_documentos)
    return soma


def pontuar_documento(pergunta, texto_do_documento, contagem_palavra, contagem_ngrama, total_de_documentos):
    """Placar do documento para uma pergunta = pontos de palavra em comum
    + uma fração dos pontos de pedacinho de 4 letras em comum."""
    palavras_da_pergunta = palavras(pergunta)
    palavras_do_documento = palavras(texto_do_documento)
    pontos_de_palavra = soma_dos_pesos_em_comum(
        palavras_da_pergunta, palavras_do_documento, contagem_palavra, total_de_documentos
    )

    ngramas_da_pergunta = n_gramas_de_caractere(pergunta)
    ngramas_do_documento = n_gramas_de_caractere(texto_do_documento)
    pontos_de_ngrama = soma_dos_pesos_em_comum(
        ngramas_da_pergunta, ngramas_do_documento, contagem_ngrama, total_de_documentos
    )

    placar_final = pontos_de_palavra + (pontos_de_ngrama * 0.3)
    return placar_final


def ordenar_do_maior_para_o_menor(lista_de_pares):
    """Recebe uma lista de [placar, documento] e devolve ela ordenada do
    maior placar pro menor"""
    restantes = []
    for par in lista_de_pares:
        restantes.append(par)

    ordenado = []
    while len(restantes) > 0:
        indice_do_maior = 0
        for i in range(len(restantes)):
            if restantes[i][0] > restantes[indice_do_maior][0]:
                indice_do_maior = i
        ordenado.append(restantes[indice_do_maior])
        restantes.pop(indice_do_maior)

    return ordenado


def buscar(pergunta, documentos, contagem_palavra, contagem_ngrama, quantos_resultados=5):
    total_de_documentos = len(documentos)
    resultados = []
    for documento in documentos:
        placar = pontuar_documento(
            pergunta, documento["texto"], contagem_palavra, contagem_ngrama, total_de_documentos
        )
        if placar > 0:
            resultados.append([placar, documento])

    resultados_ordenados = ordenar_do_maior_para_o_menor(resultados)
    return resultados_ordenados[:quantos_resultados]


def main():
    arquivo = open(CORPUS_PATH, encoding="utf-8")
    documentos = json.load(arquivo)
    arquivo.close()
    print("Corpus carregado:", len(documentos), "documentos.")

    contagem_palavra, contagem_ngrama = contar_em_quantos_documentos_cada_termo_aparece(documentos)
    print("Índice de raridade construído.")
    print("")

    continuar_perguntando = True
    while continuar_perguntando:
        pergunta = input("Digite sua pergunta (ou 'sair'): ")
        pergunta = pergunta.strip()

        if pergunta.lower() == "sair":
            continuar_perguntando = False
        elif pergunta == "":
            continue
        else:
            resultados = buscar(pergunta, documentos, contagem_palavra, contagem_ngrama, 5)
            if len(resultados) == 0:
                print("Nenhum documento encontrado para essa pergunta.")
                print("")
            else:
                print("")
                print("Top", len(resultados), "resultados:")
                posicao = 1
                for par in resultados:
                    placar = par[0]
                    documento = par[1]
                    print("  " + str(posicao) + ". [" + documento["doc_id"] + "] (placar=" +
                          str(round(placar, 1)) + ") " + documento["tipo"])
                    trecho = documento["texto"][:160]
                    if len(documento["texto"]) > 160:
                        trecho = trecho + "..."
                    print('     "' + trecho + '"')
                    posicao = posicao + 1
                print("")


if __name__ == "__main__":
    main()
