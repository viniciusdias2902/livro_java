# Protocolo de revisão de capítulo

Depois de escrever e antes do lint e do commit, o capítulo passa por duas
leituras completas, com posturas distintas. Passar no `lint.py` não substitui
nenhuma das duas: o lint é trava mecânica, e todos os defeitos abaixo já
passaram por ele alguma vez.

## Passada 1 — leitor do zero

Ler como quem nunca viu o assunto e só leu os capítulos anteriores. De
preferência, esta passada é feita por um revisor de contexto limpo, que não
escreveu o texto.

- Alguma notação, símbolo ou convenção aparece sem ser desfeita ali mesmo?
  (Caso histórico: hexadecimal na abertura sem explicar binário, bit e byte.)
- Alguma previsão ou exercício exige conhecimento de capítulo futuro?
  Capítulo N nunca depende de N+1; referência para a frente é convite, nunca
  requisito. (Caso: previsão do capítulo 1 perguntando sobre o programa do 2.)
- Todo termo novo é definido antes do primeiro uso ou na mesma frase, no
  texto de fato, e não apenas no manifesto?
- Cada conceito central tem definição formal citável, além da demonstração
  prática? O teste: uma pergunta de entrevista sobre o conceito ("o que é
  uma estrutura de controle?") encontra resposta enunciada no texto, não só
  exemplificada.
- A previsão é respondível só com o que já foi lido, e a resposta vem logo
  depois da caixa?
- A prática é executável com o que o leitor tem instalado e sabe até aqui?

## Passada 2 — editor de registro

Ler frase a frase contra o contrato de voz do CLAUDE.md.

- Superlativo ou intensificador que não seja factual e verificável: trocar
  pela consequência concreta. ("A única coisa que um processador executa" é
  fato; "o conteúdo mais importante do livro" é ênfase vazia.)
- Travessão é raro; aparte se resolve com vírgula, parêntese, dois-pontos ou
  frase própria, variando a pontuação.
- Cacoete de blog ou tutorial: frases picotadas, "não foi sorteado", "merece
  memória", falso suspense. A referência de registro é o livro técnico
  estabelecido e a documentação oficial.
- Citações a capítulos anteriores: no máximo duas ou três, e só as que pagam
  uma promessa. Termo já definido se usa sem carimbo de origem.
- Segunda pessoa dentro do limite; metáfora só em caixa de analogia, com o
  limite declarado.
- Termo consagrado em inglês fica em inglês, com tradução na primeira
  aparição.
- Fio condutor: do capítulo 7 ao 24, o material novo foi aplicado ao
  mercadinho, em seção ou exercícios? E, no sentido oposto, nenhum exemplo
  foi forçado para dentro do domínio quando outro ensinaria melhor?
- Diagrama só onde há percurso, hierarquia ou ponteiro que a prosa carrega
  mal. Capítulo sem essa necessidade fica sem diagrama nenhum: diagrama é
  complemento didático, não decoração, e o que estiver ali para aparecer sai
  na revisão.

## Depois das duas passadas

1. Corrigir tudo o que as passadas apontaram.
2. `python3 lint.py` e corrigir o que ele apontar.
3. Commit isolado com o número do capítulo.
