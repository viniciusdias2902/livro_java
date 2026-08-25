# A linguagem, a plataforma e as versões

```
89 c8
01 d0
c3
```

Um processador da família x86, a que equipa a maior parte dos computadores de
mesa e dos servidores, recebe ordens nesse formato. Cada linha acima é uma
instrução: a primeira copia um valor de um lugar para outro dentro do
processador, a segunda soma dois valores, a terceira devolve o resultado ao
ponto que pediu a soma. Esse formato tem nome: código de máquina, e é a única
coisa que um processador executa. Tudo o que um computador faz, de abrir uma
página a calcular um boleto ou gravar um arquivo, termina, em algum nível, em
sequências como essa.

A própria escrita dessas linhas, porém, usa duas convenções que precisam ser
desfeitas antes de qualquer outra coisa, porque as duas reaparecem pela vida
inteira de quem programa. Um processador é um circuito elétrico, e um circuito
distingue com segurança apenas dois estados: tensão presente ou tensão
ausente. Toda informação que um computador guarda, transmite ou executa é, por
isso, uma sequência desses dois estados, anotados no papel como 0 e 1. Cada
posição de uma sequência dessas é um bit, a menor unidade de informação que
existe; a escrita que usa apenas os símbolos 0 e 1 chama-se notação binária.
Em notação binária, as três instruções da abertura têm a forma que existe de
fato dentro da máquina:

```
10001001 11001000
00000001 11010000
11000011
```

Ler, escrever e conferir zeros e uns em quantidade é impraticável para uma
pessoa, e por isso quase nenhum material técnico os mostra assim. A abertura
usou a notação hexadecimal: um sistema de escrita de números com dezesseis
símbolos (os algarismos de 0 a 9, seguidos das letras de a a f) no lugar dos
dez algarismos da notação decimal, a da vida cotidiana. A escolha do dezesseis
tem motivo: quatro bits admitem 2 × 2 × 2 × 2 = dezesseis combinações, uma
para cada símbolo, de modo que cada símbolo hexadecimal corresponde
exatamente a quatro bits, e um par de símbolos descreve um grupo de oito bits,
chamado byte, a unidade em que quase tudo em computação é contado, de tamanho
de arquivo a memória. O `89` da primeira linha da abertura e o `10001001` da
primeira linha acima são o mesmo número: cento e trinta e sete, em notação
decimal. Entre as três escritas muda a notação, nunca a quantidade. E a
quantidade, aqui, nem é o que interessa: o processador não a trata como
número, e sim como ordem a cumprir. Notação de número volta ao livro no
capítulo 3, quando os valores que um programa manipula ganham forma escrita em
Java.

Duas propriedades do código de máquina explicam por que ninguém constrói
sistemas escrevendo essas linhas diretamente. A primeira é a escala: somar dois
números são três instruções; emitir uma nota fiscal são milhões, e um texto de
milhões de números não pode ser lido, revisado nem corrigido por uma pessoa. A
segunda é a dependência do processador: cada família tem seu próprio conjunto
de instruções, e as três linhas acima, levadas a um processador ARM, o dos
celulares e de parte dos notebooks atuais, não significam nada. Um programa
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
pertence à linguagem e tem um único significado, ou não pertence, e então o
compilador o recusa, apontando onde parou de entender. Não existe interpretação
aproximada, não existe "deu para entender o que se quis dizer". A consequência
prática aparece no primeiro dia e não vai embora: o computador executa o que
está escrito, não o que se pretendia escrever. Um texto quase correto não
produz um programa quase correto; produz uma recusa do compilador ou, pior,
um programa que faz, sem avisar ninguém, exatamente a coisa errada que está
escrita.

## O que é Java

Java é uma linguagem de programação publicada em 1995 pela Sun Microsystems,
empresa comprada pela Oracle em 2010. Hoje a linguagem é desenvolvida em um
projeto de código aberto (isto é, com o código-fonte publicado, para qualquer
um ler e propor mudança), o OpenJDK, do qual participam Oracle, Amazon,
Microsoft, Red Hat e outras empresas, e evolui por um processo público de
propostas: qualquer mudança na linguagem começa como um documento numerado,
discutido em aberto antes de virar código.

O nome, porém, cobre mais do que a notação do texto. O que se instala e se usa
sob o nome Java são três coisas. A primeira é a linguagem propriamente dita: as
regras que dizem o que é um texto Java válido e o que cada construção
significa. A segunda é a biblioteca padrão: um conjunto extenso de código
pronto, distribuído junto com a linguagem, para as tarefas que quase todo
programa tem, como imprimir no terminal, ler e gravar arquivos, medir tempo e
conversar com a rede. Boa parte do trabalho de escrever Java é chamar essa
biblioteca, e boa parte deste livro é apresentá-la.

A terceira é a plataforma de execução, e é ela que distingue Java da descrição
genérica dada até aqui. O compilador de Java não traduz o código-fonte para o
código de máquina de um processador específico. Traduz para uma forma
intermediária chamada bytecode: instruções definidas em especificação, não em
silício, que cumprem o mesmo papel do código de máquina sem pertencer a nenhum
processador real. Quem executa bytecode é a JVM (*Java Virtual Machine*, a
máquina virtual Java): um programa instalado em cada máquina, que lê essas
instruções e as cumpre usando o processador que houver ali. Existe uma JVM
para x86 com Windows, outra para ARM com macOS, e assim por diante, todas
lendo o mesmo bytecode. A consequência é o que define a plataforma: o mesmo
programa Java, compilado uma vez, roda em qualquer sistema que tenha uma JVM;
o que muda de uma máquina para outra é a JVM instalada nela, não o programa. O
capítulo 2 põe as duas peças para funcionar no terminal, com os comandos que
compilam e executam.

Essa arquitetura, somada a um compromisso incomum de compatibilidade (código
compilado há vinte anos continua rodando nas versões atuais), explica onde
Java está: em sistemas bancários, no comércio eletrônico de grande porte, em
ferramentas de infraestrutura que sustentam outros sistemas, e na origem dos
aplicativos Android, que usam a linguagem com outra plataforma de execução.
Java é uma escolha frequente para sistemas que precisam funcionar por décadas
e ser mantidos por pessoas que não estavam lá quando eles começaram. As
decisões de projeto da linguagem, inclusive as que geram reclamação, fazem
sentido lidas contra esse requisito.

## O JDK e as distribuições

Desenvolver em Java exige instalar um único conjunto de programas: o JDK, sigla
de Java Development Kit. Dele fazem parte o compilador de Java, a JVM e a
biblioteca padrão. Instalado o JDK, o terminal passa a ter o comando `java`, e
pedir a versão a ele é a primeira verificação a fazer em qualquer máquina:

```console
$ java -version
openjdk version "25.0.4" 2026-07-15 LTS
OpenJDK Runtime Environment Corretto-25.0.4.7.1 (build 25.0.4+7-LTS)
OpenJDK 64-Bit Server VM Corretto-25.0.4.7.1 (build 25.0.4+7-LTS, mixed mode, sharing)
```

O número no começo da primeira linha é a versão, 25 neste caso. O nome
Corretto, nas linhas seguintes, identifica a distribuição, e entender por que
existem várias exige apresentar a origem comum de todas. OpenJDK é o projeto
de código aberto onde a plataforma Java é desenvolvida: o código-fonte do
compilador, da JVM e da biblioteca padrão mora ali, e é ali que as propostas
públicas citadas na seção anterior viram código. O OpenJDK é também a
implementação-padrão da plataforma, a chamada *reference implementation*:
quando a especificação de uma versão fica pronta, é o código dele que a
realiza e contra o qual as demais são conferidas.

Só que código aberto não é código pronto para usar: alguém precisa compilá-lo
para cada sistema, testar, assinar o resultado e, sobretudo, continuar
publicando correções por anos, e esse trabalho contínuo custa dinheiro. Cada
empresa com interesse em Java o financia à sua maneira e distribui o
resultado, que é o que se chama de distribuição. A Amazon mantém o Corretto
porque roda Java em escala nos próprios servidores; a Microsoft faz o mesmo
para a nuvem dela; a Oracle vende suporte sobre o Oracle JDK; a Eclipse
Foundation publica o Temurin como distribuição comunitária, sem dono
comercial; a Azul vive de suporte ao seu Zulu. Todas partem do mesmo código
de origem, e por isso a linguagem, a biblioteca padrão e o comportamento dos
programas são os mesmos em qualquer uma; o que muda é quem publica correções,
por quanto tempo e sob quais termos de licença. Para este livro, qualquer
distribuição serve, e trocar de uma para outra não muda uma linha do que vem
pela frente.

## Instalação

Cada distribuição tem instalador próprio, e qualquer um funciona. Este livro
recomenda um caminho único, válido para Linux e macOS: o SDKMAN, um
gerenciador que instala, lista e troca versões de JDK pelo terminal. Dois
comandos o instalam, e um terceiro instala o JDK:

```console
$ curl -s "https://get.sdkman.io" | bash
$ source "$HOME/.sdkman/bin/sdkman-init.sh"
$ sdk install java 25.0.4-amzn
```

O identificador `25.0.4-amzn` nomeia a correção 25.0.4 do Corretto, a
distribuição da Amazon, exatamente a instalação da máquina em que este livro
roda: instalado por esse caminho, `java -version` responde as mesmas linhas
do exemplo acima. O número exato muda a cada trimestre; o comando abaixo
mostra os identificadores disponíveis no dia, e qualquer um que comece com
25, ou mais novo, atende ao livro:

```console
$ sdk list java
================================================================================
Available Java Versions for Linux 64bit
================================================================================
 Vendor        | Use | Version  | Dist | Status     | Identifier
--------------------------------------------------------------------------------
 Corretto      | >>> | 25.0.4   | amzn | installed  | 25.0.4-amzn
               |     | 21.0.9   | amzn |            | 21.0.9-amzn
 Java.net      |     | 26.ea.36 | open |            | 26.ea.36-open
 Temurin       |     | 25.0.4   | tem  |            | 25.0.4-tem
               |     | 21.0.9   | tem  |            | 21.0.9-tem
...
```

A lista real é bem mais longa, com a omissão marcada acima. A primeira coluna
traz a distribuição; a última, o identificador que o `sdk install java`
recebe. A linha marcada com `>>>` é a instalação que o comando `java` usa no
momento. Identificadores com `ea` no meio, como `26.ea.36`, são montagens de
acesso antecipado (*early access*) da versão ainda em desenvolvimento, e não
atendem ao livro.
Quando houver mais de um JDK na máquina, o SDKMAN também faz a troca:
`sdk default java`, seguido de um identificador, passa a apontar o comando
`java` para a instalação escolhida.

O SDKMAN não existe para Windows, e lá a recomendação é instalar antes o WSL,
sigla de Windows Subsystem for Linux: um Linux completo rodando dentro do
Windows, lado a lado com ele, sem particionar disco nem reiniciar para trocar
de sistema. Um comando faz a instalação, em um PowerShell aberto como
administrador (o `>` faz as vezes do `$` no PowerShell):

```
> wsl --install
```

Depois de reiniciar a máquina, o terminal do WSL é um terminal Linux comum, e
dentro dele valem os três comandos do SDKMAN mostrados acima, sem alteração
nenhuma.

São dois passos a mais antes do primeiro programa, e a escolha é deliberada.
Java se escreve em qualquer sistema, mas as máquinas onde ele roda depois de
pronto são quase todas Linux: o servidor que atende os usuários, a máquina que
compila e publica o projeto a cada mudança, o ambiente onde a bateria de testes
roda antes de uma versão sair. As ferramentas do ecossistema seguem esse fato.
Instrução de instalação, roteiro de publicação e documentação de projeto vêm
escritos como comandos de terminal Unix, a família de sistemas a que Linux e
macOS pertencem, e quem programa em Java lê e escreve esses comandos com
frequência, mais cedo do que costuma esperar. O WSL põe esse sistema à mão
desde o primeiro dia, no mesmo computador que já existe. Há ainda a razão
imediata: os comandos de terminal e as saídas impressas neste livro vêm de um
sistema assim, e no WSL a tela do leitor é a mesma da página.

Nada disso é imposto. Cada distribuição publica também um instalador para
Windows, e a linguagem, a biblioteca padrão e o comportamento dos programas
são idênticos lá; a diferença aparece nos comandos do sistema operacional que
cercam o Java, não nos comandos do Java. O que este livro afirma é que o
caminho mais curto, nesse ponto, ensina menos.

## Como as versões funcionam

Até 2017, uma versão nova de Java saía quando ficava pronta, em intervalos
irregulares: quase cinco anos separam a versão 6 da 7; a 8 é de 2014, a 9 de
2017. Desde a versão 9 o calendário é fixo: uma versão nova em março e outra em
setembro, todos os anos, estejam prontas as novidades que estiverem; o que não
entrou espera a versão seguinte. O número da versão, portanto, mede posição no
calendário, não tamanho de mudança: a distância entre a 24 e a 25 pode ser
maior ou menor do que entre a 23 e a 24.

Novidade de linguagem raramente estreia pronta. Entra primeiro como prévia
(*preview*, o nome que aparece na documentação em inglês): disponível para
teste, sujeita a mudar de forma, desligada a menos que se peça para ligá-la.
Depois de uma ou mais rodadas de prévia, a novidade é finalizada e passa a
valer sem pedido nenhum. Este livro se apoia em um recurso que percorreu esse
caminho e foi finalizado na versão 25; essa é a razão da exigência de versão
feita na prática deste capítulo.

Desde a versão 17, a cada dois anos a versão de setembro recebe a marca LTS,
de *long-term support*, suporte de longo prazo; antes dela o intervalo era
maior, como a tabela da ficha registra. Uma versão LTS continua recebendo correções
de erros e de segurança por anos; uma versão comum para de recebê-las seis
meses depois de lançada, quando a seguinte chega. São LTS as versões 11 (2018),
17 (2021), 21 (2023) e 25 (2025), e também a 8, de 2014, anterior ao
calendário atual e ainda viva em muitos sistemas antigos. Empresas que mantêm
sistemas em produção em geral ficam nas LTS e pulam de uma para a outra;
as versões intermediárias são usadas por quem quer testar as novidades no
semestre em que saem. Este livro usa a versão 25.

As correções chegam como números acrescentados ao da versão: 25.0.1, 25.0.2,
publicadas de três em três meses. Elas consertam defeitos e fecham brechas de
segurança, mas não acrescentam recurso nenhum. O primeiro número é o único que
decide o que o código-fonte pode usar.

<div class="previsao">

Nem toda máquina é a deste livro. Num computador herdado de outra pessoa, de
um estágio ou de um laboratório, o comando de verificação responde isto:

```console
$ java -version
openjdk version "21.0.8" 2025-07-15 LTS
OpenJDK Runtime Environment Temurin-21.0.8+9 (build 21.0.8+9-LTS)
OpenJDK 64-Bit Server VM Temurin-21.0.8+9 (build 21.0.8+9-LTS, mixed mode)
```

Três perguntas, todas respondíveis com o que este capítulo apresentou: essa
instalação ainda recebe correções? Ela atende ao que este livro exige? E o que
precisa acontecer para que atenda — a instalação existente se transforma, ou
não?

</div>

A primeira resposta é sim: 21 é a LTS de setembro de 2023, e a própria saída
mostra a correção 21.0.8, publicada em julho de 2025, sinal de que a versão
segue mantida. A segunda resposta é não: o livro exige a versão 25 ou mais
nova, e essa instalação está quatro versões e dois anos atrás dela. Receber
correções e estar atualizado são coisas diferentes: a saída acima é de uma
máquina bem cuidada e, ainda assim, insuficiente aqui. A terceira: instalar um
JDK da versão 25 ou mais nova, e nada se transforma sozinho. É uma segunda
instalação, e o comando `java` do terminal precisa passar a apontar para ela.
Uma máquina com JDK em dia para o sistema que ela roda pode estar anos
atrasada para este livro, e o número na primeira linha é o que decide.

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

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| código de máquina | instruções numéricas que um processador executa; específicas de cada família de processador |
| bit | a menor unidade de informação; vale 0 ou 1 |
| byte | grupo de oito bits; a unidade comum de contagem em computação |
| notação binária | escrita de números com dois símbolos, 0 e 1 |
| notação hexadecimal | escrita de números com dezesseis símbolos; cada um corresponde a quatro bits |
| linguagem de programação | notação de texto com regras exatas, escrita por pessoas e traduzida por programa |
| código-fonte | o texto escrito em uma linguagem de programação |
| compilador | programa que lê código-fonte, confere as regras da linguagem e produz a forma executável |
| bytecode | forma intermediária gerada pelo compilador de Java; igual em qualquer máquina |
| JVM | máquina virtual Java: programa instalado em cada máquina, que executa bytecode |
| biblioteca padrão | código pronto para tarefas comuns, distribuído junto com a linguagem |
| JDK | conjunto instalável que reúne o compilador, a JVM e a biblioteca padrão |
| OpenJDK | projeto de código aberto onde o JDK é desenvolvido; a implementação-padrão (*reference implementation*) da plataforma |
| distribuição | empacotamento do OpenJDK publicado e mantido por uma empresa |
| SDKMAN | gerenciador que instala, lista e troca versões de JDK pelo terminal |
| WSL | Windows Subsystem for Linux: um Linux completo dentro do Windows |
| prévia (*preview*) | novidade disponível para teste, sujeita a mudança, desligada a menos que se peça |
| LTS | versão com correções por anos; as demais recebem correções por seis meses |

| Versão LTS | Lançamento |
| --- | --- |
| 8 | 2014 |
| 11 | 2018 |
| 17 | 2021 |
| 21 | 2023 |
| 25 | 2025 |
