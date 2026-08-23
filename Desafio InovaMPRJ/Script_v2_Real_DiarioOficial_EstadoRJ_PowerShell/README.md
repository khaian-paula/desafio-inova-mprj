## Como executar

### 1. Crie uma pasta

Crie uma pasta no seu computador, por exemplo:

``` text
prototipo_busca_real/
```

Coloque dentro dela apenas os arquivos:

``` text
prototipo_busca_real/
├── baixar_diario_real.py
└── simple_search.py
```

### 2. Abra o terminal nessa pasta

No **Windows**, abra a pasta, clique na barra de endereço, digite `cmd`
e pressione **Enter**.

### 3. Baixe os documentos reais

No terminal, execute:

``` bash
python baixar_diario_real.py
```

O `baixar_diario_real.py` consulta o **Querido Diário** e cria
automaticamente a pasta `data/` e o arquivo `corpus_real.json`.

Depois da execução, a estrutura ficará assim:

``` text
prototipo_busca_real/
├── baixar_diario_real.py
├── simple_search.py
└── data/
    └── corpus_real.json
```

> Esta etapa precisa de conexão com a internet.

### 4. Execute a busca

No mesmo terminal, execute:

``` bash
python simple_search.py
```

Digite uma pergunta e pressione **Enter**.

Exemplos:

``` text
licitação de obras
contratos na área da saúde
fiscalização ambiental
prestação de contas
```

Para encerrar, digite:

``` text
sair
```

> Caso `python` não funcione, tente `python3` ou `py`.

## Como funciona

O `baixar_diario_real.py` consulta dados públicos do **Diário Oficial do
Município do Rio de Janeiro**, por meio do Querido Diário, e gera o
arquivo `corpus_real.json`.

O `simple_search.py` utiliza esse arquivo para comparar a pergunta com
os documentos e apresentar os resultados em ordem de relevância.

Por utilizar dados reais sem um gabarito previamente definido, este
cenário é destinado a **testes exploratórios** e não ao cálculo de
métricas como precisão e recall.
