## Como executar

### 1. Crie uma pasta

Crie uma pasta no seu computador, por exemplo:

``` text
prototipo_busca_grafico/
```

Coloque dentro dela os arquivos com estes nomes:

``` text
prototipo_busca_grafico/
├── app_grafico.py
├── baixar_diario_real.py
└── simple_search.py
```

> É importante que `app_grafico.py` e `simple_search.py` estejam na
> mesma pasta.

### 2. Abra o terminal nessa pasta

No **Windows**, abra a pasta, clique na barra de endereço, digite `cmd`
e pressione **Enter**.

### 3. Baixe os documentos reais

No terminal, execute:

``` bash
python baixar_diario_real.py
```

O script consulta o **Querido Diário** e cria automaticamente a pasta
`data/` com o arquivo `corpus_real.json`.

Depois da execução, a estrutura ficará assim:

``` text
prototipo_busca_grafico/
├── app_grafico.py
├── baixar_diario_real.py
├── simple_search.py
└── data/
    └── corpus_real.json
```

> Esta etapa precisa de conexão com a internet.

### 4. Abra a interface gráfica

No mesmo terminal, execute:

``` bash
python app_grafico.py
```

A interface será aberta e tentará carregar automaticamente a base
disponível na pasta `data/`.

Digite uma pergunta no campo **Pergunta** e clique em **Buscar** ou
pressione **Enter**.

Exemplos:

``` text
licitação de obras
contratos na área da saúde
fiscalização ambiental
prestação de contas
```

Os documentos encontrados serão exibidos em uma tabela. Clique em um
resultado para visualizar o texto completo.

> Caso `python` não funcione, tente `python3` ou `py`.

## Como funciona

O `baixar_diario_real.py` consulta dados públicos do **Diário Oficial do
Município do Rio de Janeiro**, por meio do Querido Diário, e gera o
arquivo `corpus_real.json`.

O `simple_search.py` contém a lógica de busca e ordenação dos
documentos.

O `app_grafico.py` utiliza essa mesma lógica em uma interface gráfica
simples, permitindo carregar a base, realizar a busca e visualizar os
documentos encontrados.

Como os documentos reais não possuem respostas previamente classificadas
como corretas, este teste serve para verificar se os resultados
encontrados fazem sentido, e não para calcular métricas de desempenho
como precisão e recall.
