# Prompt para o Claude Code

Cole o texto abaixo como primeira mensagem, com o Claude Code aberto na pasta `livro/`.

---

Você vai escrever um livro didático de Java neste repositório. Leia o `CLAUDE.md` antes
de qualquer coisa — ele contém o contrato de voz, as regras de conteúdo e o registro
exigido, e tem precedência sobre qualquer inclinação sua para respostas curtas.

Duas coisas sobre este repositório que mudam como você deve trabalhar:

Primeiro, a saída principal é **prosa**, não código. O viés de concisão deste ambiente
é inadequado aqui. Cada capítulo tem entre 1500 e 2500 palavras de texto corrido, para
ser lido do início ao fim. Bullet não substitui parágrafo. Esqueleto não substitui
explicação.

Segundo, existe um verificador (`lint.py`) que confere mecanicamente parte das regras.
Ele é uma trava, não um objetivo: passar no lint não significa que o capítulo ensina
bem. Nunca altere `lint.py` para fazer um capítulo passar; corrija o capítulo.

## Trabalhe em três fases, e pare entre elas

### Fase 1 — esqueleto

Preencha, para **todos** os 29 capítulos do `manifesto.json`, os campos
`termos_introduzidos` (termos técnicos que o capítulo define pela primeira vez),
`termos_adiados` (termo → id do capítulo que o define) e `conceitos_de_carga` (as duas
ou três ideias sem as quais o capítulo não se sustenta).

Regra que decide os casos difíceis: se um capítulo precisa de um conceito que só aparece
depois, a solução é **reordenar capítulos**, nunca deixar o termo sem definição nem
enfraquecer o adiamento. Reordenar significa mudar a posição no `manifesto.json` e no
`src/SUMMARY.md` juntos.

Rode `python3 lint.py --esqueleto` até passar. Depois **pare** e me apresente:

- a ordem final dos capítulos, se você mudou alguma;
- toda reordenação, com a dependência que a motivou;
- os capítulos em que seu recorte é opinião e não consenso.

Não escreva prosa nesta fase.

### Fase 2 — capítulos, um por vez

Só comece depois que eu aprovar o esqueleto.

Para cada capítulo, em ordem:

1. Releia o capítulo anterior por inteiro, para manter continuidade do domínio (o mercadinho de bairro) e não redefinir o que já foi definido.
2. Escreva o capítulo no arquivo correspondente em `src/capitulos/`.
3. Rode `python3 lint.py` e corrija as violações.
4. Faça um commit isolado, com o número do capítulo na mensagem.
5. **Pare e me mostre o capítulo.** Um capítulo por vez, sempre. Não encadeie.

Os capítulos 1 e 2 (`src/capitulos/01-introducao.md` e `src/capitulos/02-execucao.md`)
já estão escritos e revisados. Use-os como referência de densidade, de registro e de
como os ambientes (`armadilha`, `aprofundamento`, `previsao`, `analogia`) são usados.
Não os reescreva.

### Fase 3 — auditoria

Ao terminar cada parte do livro, compare o que foi escrito com uma fonte externa — os
objetivos de prova da certificação Java SE e o sumário da documentação oficial da
linguagem — e liste os tópicos que essas fontes cobrem e o livro não, com sua
justificativa item a item para cada omissão. Omissão é o único defeito que o `lint.py`
não detecta e que eu não tenho como perceber sozinho, por não conhecer o assunto.

## Como escrever um capítulo

Abra com o problema concreto que o capítulo resolve. Não abra com definição, não abra
com sumário do que virá.

Mostre o código antes de explicá-lo. Em pelo menos um ponto por capítulo, mostre a
versão errada primeiro dentro de `<div class="previsao">`, com a pergunta sobre o que
será impresso, e revele a resposta só depois.

Nenhum termo técnico aparece antes de ter sido definido no livro ou definido na mesma
frase. Citar um termo de passagem para dizer que ele ainda não será tratado é violação,
não exceção — se precisar mencioná-lo, defina em uma linha ou reformule sem ele.

Feche com uma seção de prática (exercícios que o leitor faz sozinho, sem respostas) e
uma ficha de referência em tabela.

## Anti-exemplos

Estas construções reprovam o capítulo:

- "Você quer construir o mercadinho." → desejo atribuído ao leitor.
- "Trate isso como cerimônia obrigatória por enquanto." → adiamento sem prazo; nomeie o
  capítulo.
- "Sem classe, sem `public static`, sem `String[] args`." → três termos não definidos em
  uma frase que existia para esclarecer.
- "É só isso.", "Repare que...", "Guarde essa dor." → conversa, não livro.
- Uma metáfora sem o limite dela declarado no mesmo lugar.

## Quando parar e perguntar

Se uma regra do `CLAUDE.md` entrar em conflito com outra, ou se você precisar de um
conceito fora de ordem e a reordenação parecer cara, pare e me pergunte. Prefira
perguntar a decidir sozinho: uma decisão errada de ordem contamina todos os capítulos
seguintes.

Comece pela fase 1.
