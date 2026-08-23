"""
Gera um corpus sintético de documentos administrativos/jurídicos, simulando
(em escala muito reduzida) o cenário descrito no desafio: um acervo com
documentos de vários tipos e assuntos, dos quais apenas uma fração pequena
é relevante para consultas específicas que um analista faria.

Por que dados sintéticos, e não um dataset público real?
- Não temos acesso a um acervo real do MPRJ (nem seria apropriado usar
  documentos reais/sensíveis num teste técnico).
- Dados sintéticos permitem controlar o "gabarito" (quais documentos são
  de fato relevantes para cada consulta), o que é indispensável para medir
  precisão/recall de forma objetiva.
- Limitação assumida: a linguagem, a repetição de vocabulário e o nível de
  ruído aqui são muito mais simples e homogêneos do que um acervo real de
  500 mil documentos heterogêneos. Isso é discutido no README.
"""

import random
import json
import os

random.seed(42)

BOILERPLATE = [
    "Ao Senhor Coordenador, encaminhamos o presente expediente para conhecimento e providências cabíveis.",
    "Em atenção ao ofício anterior, informamos que o assunto está em análise pela equipe responsável.",
    "Solicitamos que o presente documento seja juntado aos autos do processo administrativo correspondente.",
    "Ressaltamos a importância de resposta no prazo regulamentar, conforme normativo interno vigente.",
    "Encaminha-se cópia do expediente para ciência das partes interessadas.",
    "Registre-se que as informações aqui prestadas têm caráter preliminar e poderão ser complementadas.",
    "Este documento foi produzido no âmbito das atividades ordinárias do órgão.",
    "Solicita-se manifestação da área técnica competente sobre o teor deste expediente.",
]

DOC_TYPES = ["Ofício", "Memorando", "Parecer Técnico", "Ata de Reunião",
             "Notificação", "Relatório de Fiscalização", "Despacho"]

# Tópicos "de fundo" (irrelevantes para as 3 consultas-alvo), usados para
# gerar a maior parte do acervo e criar sobreposição de vocabulário
# genérico com os documentos relevantes (tornando a busca não-trivial).
BACKGROUND_TOPICS = {
    "recursos_humanos": [
        "O servidor solicitou licença capacitação para participar de curso de aperfeiçoamento.",
        "A escala de férias do setor foi atualizada conforme planejamento anual.",
        "Foi aberto processo seletivo interno para preenchimento de vaga administrativa.",
        "O ponto eletrônico apresentou instabilidade no último período de apuração.",
    ],
    "patrimonio": [
        "Foi realizado inventário anual dos bens móveis do almoxarifado central.",
        "Solicita-se manutenção preventiva do sistema de ar-condicionado do prédio anexo.",
        "O mobiliário da sala de reuniões será substituído no próximo trimestre.",
        "Registro de baixa patrimonial de equipamento de informática obsoleto.",
    ],
    "educacao": [
        "A escola municipal solicitou apoio para reforma da quadra poliesportiva.",
        "Foi realizada reunião pedagógica sobre o calendário letivo do próximo ano.",
        "O programa de merenda escolar teve seu cronograma de entregas revisado.",
        "Encaminhamento de relatório sobre evasão escolar na rede pública.",
    ],
    "seguranca_publica": [
        "A guarnição realizou ronda de rotina sem intercorrências registradas.",
        "Foi solicitado reforço de efetivo para evento público de grande porte.",
        "O boletim de ocorrência foi registrado e encaminhado à delegacia competente.",
        "Manutenção do sistema de câmeras de monitoramento da via pública.",
    ],
    "meio_ambiente_rotina": [
        "A poda de árvores na praça central foi autorizada pela secretaria competente.",
        "Foi emitida licença ambiental simplificada para pequeno empreendimento local.",
        "Relatório de monitoramento da qualidade do ar não indicou alterações relevantes.",
        "Campanha de coleta seletiva foi lançada em parceria com cooperativa local.",
    ],
}

# As 3 consultas-alvo (o que um analista, no cenário do desafio, já sabe
# que está procurando) e os documentos "relevantes" escritos com
# vocabulário DIFERENTE da consulta (paráfrase/sinônimos), simulando o
# desafio real de recuperação semântica.
QUERIES = {
    "q1_obras": {
        "query_text": "indícios de superfaturamento em contratos de obras públicas",
        "relevant_docs": [
            "A comissão de acompanhamento identificou valores muito acima da média de mercado "
            "para a execução de serviços de pavimentação na licitação em curso.",
            "O laudo técnico apontou divergência relevante entre o custo orçado e o preço "
            "efetivamente cobrado pela construtora no viaduto municipal.",
            "Denúncia recebida relata que os itens do orçamento da reforma do hospital regional "
            "estariam com preços muito superiores aos praticados por outras empresas do setor.",
            "A auditoria interna recomendou a suspensão cautelar dos pagamentos à empreiteira até "
            "esclarecimento das inconsistências encontradas na planilha de custos do empreendimento.",
            "O parecer técnico apontou que o valor pago pelo metro quadrado de pavimentação ficou "
            "muito acima do praticado em municípios vizinhos para serviço equivalente.",
            "A comissão de licitação recebeu impugnação alegando que o vencedor do certame cobrou "
            "preço substancialmente maior do que o segundo colocado para o mesmo escopo de serviço.",
        ],
    },
    "q2_saude": {
        "query_text": "denúncias de desvio de verba na área da saúde",
        "relevant_docs": [
            "Relato anônimo indica que recursos destinados à compra de medicamentos teriam sido "
            "direcionados a finalidade distinta da prevista no convênio com o hospital.",
            "A prestação de contas do posto de saúde apresentou inconsistências entre os valores "
            "repassados e os insumos efetivamente recebidos pela unidade.",
            "Foi instaurado procedimento para apurar possível uso irregular de recursos do fundo "
            "municipal utilizados fora da finalidade orçamentária aprovada.",
            "Servidor relatou pressão para assinar recebimento de equipamentos hospitalares que "
            "nunca chegaram a ser entregues à unidade.",
            "A comissão de fiscalização apurou que parte da verba repassada para a campanha de "
            "vacinação não foi aplicada na finalidade original prevista no plano de trabalho.",
            "Auditoria apontou pagamento a fornecedor de insumos hospitalares sem comprovação "
            "adequada da entrega dos materiais adquiridos com recurso público.",
        ],
    },
    "q3_ambiental": {
        "query_text": "descumprimento de prazo de resposta em fiscalização ambiental",
        "relevant_docs": [
            "A empresa notificada não apresentou resposta ao auto de infração dentro "
            "do prazo estabelecido pela fiscalização, configurando possível descumprimento.",
            "Passados mais de sessenta dias, o órgão responsável pela licença ainda não obteve "
            "manifestação da indústria sobre as irregularidades apontadas na vistoria.",
            "O relatório registra que o prazo regulamentar para resposta ao "
            "questionamento sobre despejo de efluentes foi ultrapassado sem justificativa.",
            "Reiteração de cobrança: a empresa segue sem se manifestar sobre o passivo identificado "
            "na inspeção realizada há mais de dois meses.",
            "O órgão ambiental registrou que o prazo para apresentação do plano de recuperação da "
            "área degradada já venceu sem qualquer manifestação da empresa responsável.",
            "A vistoria de acompanhamento constatou que a indústria segue sem responder à "
            "notificação anterior sobre o vazamento identificado na área industrial.",
        ],
    },
}


def _ocr_noise(text, rng, corruption_rate=0.06):
    """Simula ruído de OCR: troca, remove ou duplica caracteres aleatoriamente.
    Recebe uma instância própria de random.Random (rng) para que a aleatoriedade
    do ruído seja independente da aleatoriedade usada para gerar o corpus."""
    chars = list(text)
    out = []
    for ch in chars:
        r = rng.random()
        if r < corruption_rate * 0.4:
            continue  # caractere "perdido" na digitalização
        elif r < corruption_rate * 0.7:
            out.append(ch); out.append(ch)  # caractere duplicado
        elif r < corruption_rate:
            out.append(rng.choice("abcdefghijklmnopqrstuvwxyz"))  # caractere trocado
        else:
            out.append(ch)
    return "".join(out)


def build_corpus(n_background=360):
    docs = []
    doc_id = 0

    # Documentos de fundo (irrelevantes para as 3 consultas)
    topics = list(BACKGROUND_TOPICS.keys())
    for _ in range(n_background):
        topic = random.choice(topics)
        base_sentences = random.sample(BACKGROUND_TOPICS[topic], k=random.randint(1, 2))
        n_boiler = random.randint(1, 3)
        boiler = random.sample(BOILERPLATE, k=n_boiler)
        sentences = base_sentences + boiler
        random.shuffle(sentences)
        text = " ".join(sentences)
        docs.append({
            "doc_id": f"D{doc_id:04d}",
            "tipo": random.choice(DOC_TYPES),
            "topico": topic,
            "relevant_for": [],
            "texto": text,
        })
        doc_id += 1

    # Documentos relevantes (poucos, escritos com vocabulário parafraseado)
    for qid, qinfo in QUERIES.items():
        for rel_text in qinfo["relevant_docs"]:
            n_boiler = random.randint(1, 2)
            boiler = random.sample(BOILERPLATE, k=n_boiler)
            sentences = [rel_text] + boiler
            random.shuffle(sentences)
            text = " ".join(sentences)
            docs.append({
                "doc_id": f"D{doc_id:04d}",
                "tipo": random.choice(DOC_TYPES),
                "topico": qid,
                "relevant_for": [qid],
                "texto": text,
            })
            doc_id += 1

    random.shuffle(docs)
    return docs


def build_noisy_variant(docs, fraction=0.5, corruption_rate=0.06, seed=0):
    """Cria uma cópia do corpus onde uma fração dos documentos recebe
    ruído simulado de digitalização (OCR), mantendo os demais intactos.
    Usa um gerador aleatório próprio (seed) para permitir repetir o
    experimento com diferentes sementes de ruído sobre o MESMO corpus base."""
    rng = random.Random(seed)
    noisy = []
    for d in docs:
        d2 = dict(d)
        if rng.random() < fraction:
            d2["texto"] = _ocr_noise(d["texto"], rng, corruption_rate=corruption_rate)
            d2["ocr_noise_applied"] = True
        else:
            d2["ocr_noise_applied"] = False
        noisy.append(d2)
    return noisy


if __name__ == "__main__":
    docs = build_corpus()
    n_relevant = sum(1 for d in docs if d["relevant_for"])
    print(f"Total de documentos: {len(docs)}")
    print(f"Documentos relevantes (gabarito): {n_relevant} ({100*n_relevant/len(docs):.1f}% do acervo)")
    os.makedirs("data", exist_ok=True)
    with open("data/corpus.json", "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print("Corpus salvo em data/corpus.json")
