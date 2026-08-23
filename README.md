## Como executar

### 1. Crie uma pasta

Crie uma pasta no seu computador, por exemplo:

```text
prototipo_busca/
```

Coloque dentro dela apenas os arquivos:

```text
prototipo_busca/
├── corpus.py
└── simple_search.py
```

### 2. Abra o terminal nessa pasta

No **Windows**, abra a pasta, clique na barra de endereço, digite `cmd` e pressione **Enter**.

### 3. Gere a base de documentos

No terminal, execute:

```bash
python corpus.py
```

O `corpus.py` irá gerar automaticamente a pasta `data/` e o arquivo `corpus.json`.

Depois da execução, a estrutura ficará assim:

```text
prototipo_busca/
├── corpus.py
├── simple_search.py
└── data/
    └── corpus.json
```

### 4. Execute a busca

No mesmo terminal, execute:

```bash
python simple_search.py
```

Digite uma pergunta e pressione **Enter**.

Exemplos:

```text
indícios de superfaturamento em contratos de obras públicas
denúncias de desvio de verba na área da saúde
descumprimento de prazo de resposta em fiscalização ambiental
```

Para encerrar, digite:

```text
sair
```

> Caso `python` não funcione, tente `python3` ou `py`.

## Como funciona

A pergunta é comparada aos documentos por palavras e pequenos trechos de caracteres (n-gramas). Os documentos recebem uma pontuação e são apresentados em ordem de relevância.
