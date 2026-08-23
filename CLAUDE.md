# Instruções do repositório

Este repositório é um **livro didático**, não um projeto de software. O `lint.py` e o
`book.toml` existem para servir ao texto. A saída principal são capítulos de prosa.

## Registro — a correção mais importante

O viés padrão de concisão deste ambiente é **inadequado aqui**. Capítulo não é README:
é texto corrido, para ser lido do início ao fim, com explicação completa. Um capítulo
típico tem entre 1500 e 2500 palavras. Não resuma, não use bullet como substituto de
parágrafo, não entregue esqueleto no lugar de explicação.

Ao mesmo tempo, prosa de livro não é conversa. Proibido, e verificado por `lint.py`:

- Interjeição e comentário sobre o próprio texto: "é só isso", "repare que", "veja bem".
- Superlativo e dramatização: "custa caro", "a coisa mais importante".
- Desejo atribuído ao leitor: "você quer construir X".
- Adiamento sem prazo: "cerimônia obrigatória", "por ora aceite". Todo termo adiado
  nomeia o capítulo exato que o explica, e isso vai em `termos_adiados` no manifesto.
- Segunda pessoa em mais de uma frase a cada três.

## Contrato de voz

Regra enunciada com precisão → código nomeado que a exibe → custo do erro dito em voz
alta. Exemplo gravado:

> Uma variável de tipo referência não contém o objeto: contém o endereço dele. Quando
> você escreve `Pedido p = new Pedido()`, `p` não é o pedido — `p` guarda onde o pedido
> está. Fazer `Pedido q = p` copia o endereço, não o objeto: existe um pedido e dois
> nomes para ele, e mutação através de `q` é visível através de `p`. Metade dos bugs de
> quem chega de linguagens que escondem isso nasce aqui, e o compilador não vai te
> avisar de nenhum deles.

Sem metáfora. Proibidas em especial: variável como caixa, herança como família, objeto
como "coisa do mundo real".

Travessão é recurso raro: no máximo um a cada 250 palavras, verificado pelo lint.
Aparte se resolve com vírgula, parêntese, dois-pontos ou frase própria — variar a
pontuação é parte do ofício. A referência de registro é o livro técnico estabelecido
e a documentação oficial, nunca o tutorial de internet.

## Regras de conteúdo

- **Nenhum termo sem definição.** Nenhum termo técnico aparece antes de ter sido
  definido no livro ou definido na mesma frase. Citar um termo de passagem para dizer
  que ele ainda não será tratado é violação, não exceção. Exceção única: o apêndice
  de JDBC declara pré-requisitos externos na abertura (SQL e banco configurado, via
  docker-compose ou não) e não define termos de SQL nem de Docker.
- **Código antes da explicação.** Mostre o trecho, depois explique. Em pontos-chave,
  mostre a versão errada primeiro dentro de `<div class="previsao">`, com a pergunta
  sobre o que será impresso, antes de revelar.
- **Corpo ou nota.** Profundidade que muda o que o leitor escreve vai no corpo.
  Profundidade que apenas explica vira `<div class="aprofundamento">`, com duas ou três
  linhas e o nome do conceito. Nada de aprofundamento é cobrado em teste.
- **Armadilha** (`<div class="armadilha">`) é comportamento contraintuitivo que produz
  bug silencioso. Cai nos testes.
- **Domínio contínuo:** um mercadinho de bairro (produtos, preços, estoque, lotes e
  validades, vendas, caderneta de fiado), do capítulo 7 ao 25. Sem `Foo` e `Bar`.
- **Estrutura:** abre com o problema concreto, fecha com seção de prática e ficha de
  referência. Ambas obrigatórias, verificadas pelo lint.
- Java 25. Capítulos 2 a 6 usam arquivo-fonte compacto nos exercícios.

## Fluxo de trabalho

1. Preencher `termos_introduzidos`, `termos_adiados` e `conceitos_de_carga` de **todos**
   os capítulos em `manifesto.json`, antes de escrever qualquer prosa.
2. `python3 lint.py --esqueleto` até passar. Conflito de dependência se resolve
   **reordenando capítulos**, nunca enfraquecendo o adiamento.
3. Escrever um capítulo por vez, em ordem. Depois de cada um: `python3 lint.py`,
   corrigir, e um commit isolado com o número do capítulo na mensagem.
4. Antes de escrever o capítulo N, reler o N-1 para manter continuidade do domínio.

## O que o lint não pega

Omissão e explicação ruim. Um capítulo pode passar limpo e ensinar mal. Ao terminar
cada parte do livro, listar o que ficou de fora e por quê, para revisão humana.
