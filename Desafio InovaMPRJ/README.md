# Desafio Técnico --- Inova MPRJ

Repositório desenvolvido para o **Desafio Técnico do Inova MPRJ**,
contendo protótipos de busca dirigida em documentos.

A proposta evolui de um cenário controlado com dados sintéticos para
testes com dados reais e interface gráfica, mantendo o analista
responsável pela validação dos resultados.

## Protótipos

### 1. Script_v1_Sintético_PowerShell

Primeira versão do protótipo, utilizando uma base de documentos
sintéticos.

Permite testar a busca em um cenário controlado, com documentos
relevantes previamente conhecidos.

### 2. Script_v2_Real_DiarioOficial_RioDeJaneiro_PowerShell

Evolução do protótipo utilizando dados reais do **Querido Diário**.

Permite avaliar o comportamento da busca com documentos reais do Diário
Oficial do Município do Rio de Janeiro.

### 3. Script_v3_Real_DiarioOficial_RioDeJaneiro_GUI

Versão com dados reais e **interface gráfica**, facilitando a realização
das buscas e a visualização dos documentos encontrados.

### 4. Colab simple_search

Notebook didático desenvolvido no **Google Colab** para apresentar,
passo a passo, o funcionamento do protótipo e os principais conceitos de
Python utilizados.

## Estrutura

``` text
desafio-inova-mprj/
│
├── Script_v1_Sintético_PowerShell/
│   └── README.md
│
├── Script_v2_Real_DiarioOficial_RioDeJaneiro_PowerShell/
│   └── README.md
│
├── Script_v3_Real_DiarioOficial_RioDeJaneiro_GUI/
│   └── README.md
│
└── Colab simple_search/
    └── README.md
```

Cada pasta possui seu próprio `README.md` com as instruções para
execução.

## Fonte dos dados reais

Os protótipos V2 e V3 utilizam dados públicos disponibilizados pelo
**Querido Diário**, projeto da Open Knowledge Brasil.

**Link da API:**

``` text
https://api.queridodiario.ok.org.br/gazettes
```

**ID (código IBGE) utilizado como filtro --- Rio de Janeiro, capital:**

``` text
3304557
```

## Evolução do protótipo

``` text
Dados sintéticos
       ↓
Busca dirigida
       ↓
Dados reais
       ↓
Interface gráfica
       ↓
Validação e evolução tecnológica
```

Os protótipos representam uma **prova de conceito** e não a arquitetura
definitiva da solução.

A evolução poderá incorporar mecanismos de busca semântica, embeddings,
reranking e LLM/RAG conforme os experimentos demonstrem ganho de valor e
o avanço da maturidade tecnológica.
