## Como executar

### 1. Abra o Google Colab

Acesse o **Google Colab** pelo navegador e faça login com uma conta Google.

Na página inicial, selecione:

**Arquivo → Fazer upload de notebook**

Selecione o arquivo:

```text
Colab_simple_search.ipynb
```

O notebook será aberto no navegador.

### 2. Execute os blocos na ordem

O notebook é dividido em blocos de explicação e código.

Para executar um bloco de código, clique no botão **▶** localizado ao lado esquerdo.

Execute os blocos na ordem em que aparecem no notebook.

### 3. Carregue a base de documentos

Ao executar o **Bloco 1 — Carregar os documentos**, será aberta uma opção para selecionar um arquivo do seu computador.

Selecione o arquivo JSON que será utilizado na busca.

Exemplos:

```text
corpus.json
corpus_real.json
```

Após o upload, o notebook mostrará a quantidade de documentos carregados.

### 4. Continue executando os blocos

Continue clicando em **▶** nos blocos seguintes.

O notebook irá, passo a passo:

```text
Carregar os documentos
        ↓
Preparar os textos
        ↓
Criar o índice
        ↓
Comparar a pergunta com os documentos
        ↓
Calcular os placares
        ↓
Ordenar os resultados
```

### 5. Faça uma busca

No **Bloco 12 — Fazer uma pergunta**, execute o código.

Será exibido:

```text
O que você quer procurar?
```

Digite uma pergunta e pressione **Enter**.

Exemplos:

```text
licitação de obras
contratos na área da saúde
fiscalização ambiental
```

Os documentos com maior pontuação serão apresentados primeiro.

> Para realizar outra busca, basta executar novamente o Bloco 12.

## Como funciona

O notebook foi desenvolvido para apresentar o funcionamento da busca de forma didática, inclusive para pessoas que estão começando em Python.

Cada etapa apresenta o conceito, o código e uma explicação dos principais comandos utilizados.

A busca compara a pergunta com os documentos utilizando palavras e pequenos trechos de caracteres (n-gramas), atribui uma pontuação e apresenta os documentos em ordem de relevância.

Ao final do notebook também são indicadas bibliotecas Python que poderiam substituir partes da implementação manual em versões posteriores.
