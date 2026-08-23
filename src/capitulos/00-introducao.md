# Introdução: a linguagem, a plataforma e as versões

```
89 c8
01 d0
c3
```

Um processador da família x86 — a que equipa a maior parte dos computadores de
mesa e dos servidores — recebe ordens nesse formato. Cada linha acima é uma
instrução, escrita aqui pelos números que a codificam: a primeira copia um valor
de um lugar para outro dentro do processador, a segunda soma dois valores, a
terceira devolve o resultado ao ponto que pediu a soma. Esse formato tem nome:
código de máquina, e é a única coisa que um processador executa. Tudo o que um
computador faz — abrir uma página, calcular um boleto, gravar um arquivo —
termina, em algum nível, em sequências como essa.

Duas propriedades do código de máquina explicam por que ninguém constrói
sistemas escrevendo essas linhas diretamente. A primeira é a escala: somar dois
números são três instruções; emitir uma nota fiscal são milhões, e um texto de
milhões de números não pode ser lido, revisado nem corrigido por uma pessoa. A
segunda é a dependência do processador: cada família tem seu próprio conjunto
de instruções, e as três linhas acima, levadas a um processador ARM — o dos
celulares e de parte dos notebooks atuais —, não significam nada. Um programa
escrito assim vale para uma família de máquina e precisa ser reescrito para
cada outra.

Uma linguagem de programação existe para atravessar essa distância. É uma
notação de texto com regras exatas, desenhada para dois leitores ao mesmo
tempo: a pessoa que escreve e mantém o texto, e o programa que traduz esse
texto para uma forma que a máquina executa. Na linguagem deste livro, uma soma
se escreve assim:

```java
total = preco + multa;
```

O texto escrito em uma linguagem de programação chama-se código-fonte. O
programa que lê código-fonte, confere se ele segue as regras da linguagem e
produz a forma executável chama-se compilador.

"Regras exatas" tem um sentido preciso, e é ele que separa uma linguagem de
programação de uma língua natural. Para cada texto possível, ou o texto
pertence à linguagem e tem um único significado, ou não pertence — e então o
compilador o recusa, apontando onde parou de entender. Não existe interpretação
aproximada, não existe "deu para entender o que se quis dizer". A consequência
prática aparece no primeiro dia e não vai embora: o computador executa o que
está escrito, não o que se pretendia escrever. Um texto quase correto não
produz um programa quase correto; produz uma recusa do compilador ou — pior —
produz um programa que faz, sem avisar ninguém, exatamente a coisa errada que
está escrita.

## O que é Java

Java é uma linguagem de programação publicada em 1995 pela Sun Microsystems,
empresa comprada pela Oracle em 2010. Hoje a linguagem é desenvolvida em um
projeto de código aberto, o OpenJDK, do qual participam Oracle, Amazon,
Microsoft, Red Hat e outras empresas, e evolui por um processo público de
propostas — qualquer mudança na linguagem começa como um documento numerado,
discutido em aberto antes de virar código.

O nome, porém, cobre mais do que a notação do texto. O que se instala e se usa
sob o nome Java são três coisas. A primeira é a linguagem propriamente dita: as
regras que dizem o que é um texto Java válido e o que cada construção
significa. A segunda é a biblioteca padrão: um conjunto extenso de código
pronto, distribuído junto com a linguagem, para as tarefas que quase todo
programa tem — imprimir no terminal, ler e gravar arquivos, medir tempo,
conversar com a rede. Boa parte do trabalho de escrever Java é chamar essa
biblioteca, e boa parte deste livro é apresentá-la.

A terceira é a plataforma de execução, e é ela que distingue Java da descrição
genérica dada até aqui. O compilador de Java não traduz o código-fonte para o
código de máquina de um processador específico. Traduz para uma forma
intermediária, e quem executa essa forma é um programa instalado em cada
máquina. O nome da forma intermediária e o nome do programa que a executa abrem
o capítulo 1, junto com os comandos que os manipulam. O que importa nesta
introdução é a consequência: o mesmo programa Java, compilado uma vez, roda em
x86 e em ARM, em Windows, em Linux e em macOS. O que muda de uma máquina para
outra é a peça instalada nela, não o programa.

Essa arquitetura, somada a um compromisso incomum de compatibilidade — código
compilado há vinte anos continua rodando nas versões atuais —, explica onde
Java está: em sistemas bancários, no comércio eletrônico de grande porte, em
ferramentas de infraestrutura que sustentam outros sistemas, e na origem dos
aplicativos Android, que usam a linguagem com outra plataforma de execução.
Java é uma escolha frequente para sistemas que precisam funcionar por décadas e
ser mantidos por pessoas que não estavam lá quando eles começaram — e as
decisões de projeto da linguagem, inclusive as que geram reclamação, fazem
sentido lidas contra esse requisito.

## O JDK e as distribuições

Desenvolver em Java exige instalar um único conjunto de programas: o JDK, sigla
de Java Development Kit. Dele fazem parte o compilador de Java, o programa que
executa a forma intermediária e a biblioteca padrão. Instalado o JDK, o
terminal passa a ter o comando `java`, e pedir a versão a ele é a primeira
verificação a fazer em qualquer máquina:

```
$ java -version
openjdk version "25.0.1" 2025-10-21 LTS
OpenJDK Runtime Environment Temurin-25.0.1+8 (build 25.0.1+8-LTS)
OpenJDK 64-Bit Server VM Temurin-25.0.1+8 (build 25.0.1+8-LTS, mixed mode)
```

O número no começo da primeira linha é a versão — 25, neste caso. O nome
Temurin, nas linhas seguintes, identifica a distribuição: o JDK é desenvolvido
como código aberto no projeto OpenJDK, e o que se baixa e instala é um
empacotamento desse código feito por alguma empresa, compilado e testado para
cada sistema. Oracle JDK, Eclipse Temurin, Amazon Corretto, Azul Zulu e
Microsoft Build of OpenJDK são distribuições. A linguagem, a biblioteca padrão
e o comportamento dos programas são os mesmos em todas, porque o código de
origem é o mesmo; o que muda é quem publica correções, por quanto tempo e sob
quais termos de licença. Para este livro, qualquer distribuição serve. Os
exemplos do capítulo 1 mostram um Corretto por acaso da máquina em que foram
executados, e nada mudaria com outra.

## Como as versões funcionam

Até 2017, uma versão nova de Java saía quando ficava pronta, em intervalos
irregulares: quase cinco anos separam a versão 6 da 7; a 8 é de 2014, a 9 de
2017. Desde a versão 9 o calendário é fixo: uma versão nova em março e outra em
setembro, todos os anos, estejam prontas as novidades que estiverem — o que não
entrou espera a versão seguinte. O número da versão, portanto, mede posição no
calendário, não tamanho de mudança: a distância entre a 24 e a 25 pode ser
maior ou menor do que entre a 23 e a 24.

Novidade de linguagem raramente estreia pronta. Entra primeiro como prévia:
disponível para teste, sujeita a mudar de forma, desligada a menos que se peça
para ligá-la. Depois de uma ou mais rodadas de prévia, a novidade é finalizada
e passa a valer sem pedido nenhum. O primeiro programa deste livro usa um
recurso que percorreu esse caminho e foi finalizado na versão 25 — e essa é a
razão de o livro exigir a versão que exige.

A cada dois anos, a versão de setembro recebe a marca LTS — sigla em
inglês para suporte de longo prazo. Uma versão LTS continua recebendo correções
de erros e de segurança por anos; uma versão comum para de recebê-las seis
meses depois de lançada, quando a seguinte chega. São LTS as versões 11 (2018),
17 (2021), 21 (2023) e 25 (2025) — e também a 8, de 2014, anterior ao
calendário atual e ainda viva em muitos sistemas antigos. Empresas que mantêm
sistemas em produção em geral ficam nas LTS e pulam de uma para a outra;
as versões intermediárias são usadas por quem quer testar as novidades no
semestre em que saem. Este livro usa a versão 25.

As correções chegam como números acrescentados ao da versão: 25.0.1, 25.0.2,
publicadas de três em três meses. Elas consertam defeitos e fecham brechas de
segurança, mas não acrescentam recurso nenhum. O primeiro número é o único que
decide o que o código-fonte pode usar.

<div class="previsao">

Uma máquina responde isto ao comando de verificação:

```
$ java -version
openjdk version "21.0.8" 2025-07-15 LTS
OpenJDK Runtime Environment Temurin-21.0.8+9 (build 21.0.8+9-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.8+9 (build 21.0.8+9-LTS, mixed mode)
```

Três perguntas, todas respondíveis com o que esta introdução apresentou: essa
instalação ainda recebe correções? O primeiro programa deste livro funciona
nela? E o que precisa acontecer para que funcione?

</div>

A primeira resposta é sim: 21 é a LTS de setembro de 2023, e a própria saída
mostra a correção 21.0.8 publicada em julho de 2025 — a versão segue mantida. A
segunda resposta é não: o programa do capítulo 1 usa o recurso finalizado na
25, e um JDK 21 o recusa; o capítulo 1 mostra essa recusa por extenso. A
terceira: instalar um JDK da versão 25 ou mais nova. Atualizar, aqui, não
transforma a instalação existente — é uma segunda instalação, e o comando
`java` do terminal precisa passar a apontar para ela. Uma máquina com JDK em
dia para o sistema que ela roda pode estar anos atrasada para este livro, e o
número na primeira linha é o que decide.

<div class="aprofundamento">

**Numeração antiga.** Até a versão 8, o número público vinha precedido de
"1.": `java -version` imprimia `1.8.0_292` para o que todo mundo chamava de
Java 8. A grafia foi abandonada na versão 9, mas continua aparecendo em
máquinas antigas e em material antigo. 1.8 e 8 são a mesma versão.

</div>

## Prática

1. Rode `java -version` na máquina em que o livro será acompanhado e anote três
   coisas: o número da versão, se ela é LTS e se atende ao que o livro pede. Se
   o comando não existir ou a versão for menor que 25, instale uma distribuição
   da 25 ou mais nova e repita a verificação.

2. Sem consultar nada além do calendário fixo descrito neste capítulo, calcule
   qual número de versão estará recém-lançado em outubro do ano que vem e em
   que ano sai a primeira LTS depois da 25. Depois confira no site do OpenJDK.

3. Escolha duas distribuições e compare, nas páginas de cada uma, até quando
   cada uma promete correções para a versão 25. Anote a diferença.

4. Explique por escrito, em um parágrafo, por que o mesmo programa Java
   compilado roda em um processador x86 e em um ARM, dizendo qual peça muda de
   uma máquina para a outra e qual permanece a mesma.

## Ficha da introdução

| Termo | Definição |
| --- | --- |
| código de máquina | instruções numéricas que um processador executa; específicas de cada família de processador |
| linguagem de programação | notação de texto com regras exatas, escrita por pessoas e traduzida por programa |
| código-fonte | o texto escrito em uma linguagem de programação |
| compilador | programa que lê código-fonte, confere as regras da linguagem e produz a forma executável |
| biblioteca padrão | código pronto para tarefas comuns, distribuído junto com a linguagem |
| JDK | conjunto instalável que reúne o compilador, o executor da forma intermediária e a biblioteca padrão |
| OpenJDK | projeto de código aberto onde o JDK é desenvolvido |
| distribuição | empacotamento do OpenJDK publicado e mantido por uma empresa |
| prévia | novidade disponível para teste, sujeita a mudança, desligada a menos que se peça |
| LTS | versão com correções por anos; as demais recebem correções por seis meses |

| Versão LTS | Lançamento |
| --- | --- |
| 8 | 2014 |
| 11 | 2018 |
| 17 | 2021 |
| 21 | 2023 |
| 25 | 2025 |
