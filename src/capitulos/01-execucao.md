# Hello world e como o Java executa

Um arquivo com três linhas:

```java
void main() {
    IO.println("Locadora aberta.");
}
```

Salvo como `Locadora.java` e executado por um comando, ele responde:

```
$ java Locadora.java
Locadora aberta.
```

Trocar uma letra dentro de `println` produz uma mensagem que cita o arquivo, a
linha e a coluna. Mover um arquivo para uma subpasta produz outra mensagem, que
não cita linha nenhuma e reclama de um nome. As duas se parecem com "não rodou",
mas vêm de programas diferentes, acontecem em momentos diferentes e se consertam
de jeitos diferentes. Separar esses dois momentos é o trabalho deste capítulo, e
é o que torna legíveis as mensagens de erro de todos os capítulos seguintes.

## As três linhas, uma a uma

Um método é um bloco de código que tem nome e pode ser chamado por esse nome.
`main` é o método por onde todo programa Java começa: de tudo o que o arquivo
declara, é esse nome que a execução chama primeiro, e o programa termina quando
esse método termina.

A palavra `void`, escrita antes do nome, diz que `main` não devolve nada a quem o
chamou. Um método pode devolver um resultado para o ponto que o chamou, e `void`
é justamente a marca de que este não devolve; como se devolve, e o que muda no
código de quem chama, é o capítulo 3.

`IO.println` é um método pronto, que vem junto com o Java e está disponível em
qualquer arquivo-fonte compacto sem nenhuma linha extra. Ele recebe um
argumento — o valor escrito entre os parênteses, entregue ao método no momento da
chamada — e escreve esse valor na saída padrão, seguido de uma quebra de linha.
Saída padrão é o canal por onde um programa de terminal escreve seu resultado
comum, e é o que o terminal mostra sem que ninguém peça nada. O `ln` no fim do
nome é a quebra de linha: existe também `IO.print`, que escreve o mesmo valor sem
passar para a linha seguinte.

Arquivo-fonte compacto é o nome do arquivo `.java` que declara métodos
diretamente, como este. Antes da versão 25 do Java, o mesmo programa exigia
linhas de moldura em volta do método, e praticamente todo material publicado até
hoje mostra essas linhas. Da versão 25 em diante o compilador fornece a moldura
quando ela não está escrita. O que essa moldura declara — e por que ela deixa de
ser dispensável assim que um programa passa de um arquivo — é o capítulo 5. Há
também uma segunda forma de escrever `main`, que recebe o que foi digitado no
terminal depois do nome do programa; essa forma é o capítulo 4.

Duas linhas do arquivo não chegam ao programa. Tudo o que vem depois de `//` até
o fim da linha, e tudo o que estiver entre `/*` e `*/`, é comentário: o
compilador descarta e nada disso influencia a execução. Os exercícios deste
capítulo pedem descrições por escrito, e o próprio arquivo `.java` é um lugar
razoável para elas.

## A versão do JDK importa mais aqui do que vai importar depois

O arquivo-fonte compacto foi finalizado na versão 25 do Java. Em um JDK anterior,
o compilador recusa a primeira linha do arquivo — e a recusa não fala de `main`
nem de `IO`, o que torna a mensagem difícil de ligar à causa. A mesma recusa se
reproduz em um JDK novo, mandando compilar para uma versão antiga:

```
$ javac --release 24 Locadora.java
Locadora.java:1: error: implicitly declared classes are not supported in -source 24
void main() {
^
  (use -source 25 or higher to enable implicitly declared classes)
1 error
```

Conferir a versão instalada antes de procurar defeito no código evita esse
desencontro:

```
$ java -version
openjdk version "26.0.2" 2026-07-21
OpenJDK Runtime Environment Corretto-26.0.2.10.1 (build 26.0.2+10-FR)
OpenJDK 64-Bit Server VM Corretto-26.0.2.10.1 (build 26.0.2+10-FR, mixed mode, sharing)
```

Das três linhas, o número que interessa é o da primeira, e ele precisa ser 25 ou
maior; o resto identifica quem montou aquele JDK e não muda nada do que este
livro faz. Do capítulo 5
em diante, quando os arquivos passam a trazer a moldura escrita, o livro roda em
JDKs mais antigos; até lá, não.

## Dois programas, dois momentos

O comando da abertura fazia dois trabalhos de uma vez. Estes dois comandos os
separam:

```
$ javac Locadora.java
$ ls
Locadora.class  Locadora.java
$ java Locadora
Locadora aberta.
```

`javac` é o compilador: o programa que lê o texto do arquivo `.java`, confere se
aquilo é Java válido e traduz o resultado. O que ele grava é o arquivo
`Locadora.class`, e o conteúdo desse arquivo não é texto Java nem código do
processador da máquina. É bytecode: um formato intermediário, projetado para ser
lido por um programa em vez de por um processador de silício. A extensão `.class`
vem do nome de uma declaração que o capítulo 5 apresenta.

O programa que lê bytecode e o executa é a JVM, a máquina virtual Java. O comando
`java` inicia uma JVM, entrega a ela o bytecode indicado e sai do caminho. Os
dois programas — `javac`, que traduz, e `java`, que executa — mais a biblioteca
onde mora `IO.println` vêm juntos no JDK, o conjunto que se instala para
desenvolver em Java.

A tradução em duas etapas tem uma consequência prática que aparece já no primeiro
mês de trabalho: o `Locadora.class` gerado aqui roda sem alteração em qualquer
máquina que tenha uma JVM da mesma versão ou mais nova, seja qual for o
processador e o sistema. O que muda de máquina para máquina é a JVM, não o
bytecode. Compilar direto para o processador daria um programa mais rápido de
começar e preso a uma máquina só.

O nome que aparece no comando `java` também sai desse arranjo. Para um
arquivo-fonte compacto, o compilador dá ao bytecode gerado o mesmo nome do
arquivo: `Locadora.java` vira `Locadora.class`, e é `Locadora` — sem extensão —
que se escreve depois de `java`. Renomear o arquivo antes de compilar muda as
duas coisas juntas.

## O erro que não deixa nada para trás

O compilador recusa o que não entende, e recusar quer dizer não gravar nada:

```
$ javac Locadora.java
Locadora.java:2: error: cannot find symbol
    IO.printn("Locadora aberta.");
      ^
  symbol:   method printn(String)
  location: class IO
1 error
$ ls
Locadora.java
```

Esse é um erro de compilação: o compilador aponta arquivo, linha, coluna e o que
não reconheceu, e o diretório continua sem nenhum `Locadora.class`. Um erro de
compilação nunca alcança quem usa o programa, porque não há programa a entregar.

Duas leituras dessa mensagem valem o hábito. A primeira: `cannot find symbol`
significa que o nome escrito não existe onde foi procurado, o que na prática é um
erro de digitação ou um nome que ainda não foi declarado. A segunda: quando o
compilador imprime várias mensagens, a primeira costuma ser a real e as demais
costumam ser consequência dela. Corrigir a de cima e compilar de novo economiza
mais tempo do que tentar entender todas de uma vez.

Nem toda recusa aponta a falta no lugar em que ela está. Retirar o ponto e
vírgula do fim da linha produz esta mensagem:

```
$ javac Locadora.java
Locadora.java:2: error: ';' expected
    IO.println("Locadora aberta.")
                                  ^
1 error
```

A coluna apontada é o fim da linha 2, não o começo da linha 3, porque o
compilador só percebe a ausência quando termina de ler o que veio antes. Toda
instrução Java termina em ponto e vírgula, e as chaves `{` e `}` marcam onde
começa e onde acaba o corpo do método: essas duas regras respondem pela maior
parte dos erros de compilação da primeira semana.

A outra família de erro é a que aparece com o programa já em execução — o erro de
execução. Esse o compilador não tem como prever, e a JVM só encontra na hora.

<div class="previsao">

O diretório tem o fonte e o bytecode. O bytecode vai para uma subpasta e o
comando é repetido sem nenhuma outra mudança:

```
$ ls
Locadora.class  Locadora.java
$ mkdir saida
$ mv Locadora.class saida/
$ java Locadora
```

`Locadora.java` continua ali, intacto, e o programa nele está correto. O que
aparece no terminal?

</div>

O terminal responde isto:

```
Error: Could not find or load main class Locadora
Caused by: java.lang.ClassNotFoundException: Locadora
```

O fonte estar no diretório não ajuda em nada, porque `java Locadora` não lê fonte
nenhum: ele executa bytecode já pronto. E `Locadora`, nesse comando, não nomeia
um arquivo — nomeia o que a JVM tem de encontrar. Onde ela procura é o classpath:
a lista de lugares em que a JVM busca bytecode. Quando ninguém diz nada, essa
lista tem um item só, o diretório atual. O arquivo saiu do diretório atual, então
saiu da lista, e a JVM não tem por onde continuar.

Dizer onde procurar resolve:

```
$ java -cp saida Locadora
Locadora aberta.
```

`-cp`, que também se escreve `-classpath`, substitui a lista inteira pelo que vem
depois dele. Vale gravar o formato da mensagem: `could not find or load` quase
nunca quer dizer que o código não existe. Quer dizer que ele não está em nenhum
dos lugares da lista. Procurar o defeito dentro do fonte, nesse caso, é procurar
onde não está — e essa confusão é responsável por boa parte das primeiras horas
perdidas de quem começa. A partir do capítulo 12, quem monta o classpath deixa de
ser quem digita o comando e passa a ser a ferramenta de construção do projeto;
até lá, ele é digitado à mão.

<div class="armadilha">

Dois comandos, o mesmo diretório, saídas diferentes:

```
$ javac Locadora.java
$ # edite o arquivo e troque o texto por "Locadora fechada para inventário."
$ java Locadora
Locadora aberta.
$ java Locadora.java
Locadora fechada para inventário.
```

`java Locadora.java` compila o fonte na memória e executa o que acabou de
compilar, sem gravar nada em disco. `java Locadora` ignora o fonte e executa o
`Locadora.class` que encontrar no classpath — que é o de antes da edição. O
sintoma é uma correção que não faz efeito: o código muda, o comando roda sem
erro, e a saída continua a mesma. Compilar antes de executar, sempre, é o que
evita isso.

</div>

<div class="aprofundamento">

A JVM começa interpretando o bytecode uma instrução por vez e, nos trechos que se
repetem muito, traduz esse bytecode para instruções do processador da máquina e
guarda o resultado para as próximas passagens. Esse tradutor tem nome: JIT, de
*just-in-time*. É por isso que um mesmo trecho de código pode ficar mais rápido
depois de alguns milhares de execuções, sem que nada tenha mudado no programa.

</div>

## Prática

1. Escreva um arquivo-fonte compacto que imprima três linhas, uma por chamada de
   `IO.println`, e execute-o sem compilar antes. Depois troque a última chamada
   por `IO.print` e descreva por escrito a diferença na saída.

2. Compile o arquivo com `javac`, apague o `.java` e execute o programa. Escreva
   em uma frase o que esse resultado prova sobre o que a JVM precisa ter em mãos.

3. Escreva `IO.printn` no lugar de `IO.println` e compile. Anote arquivo, linha e
   coluna citados. Depois execute o mesmo fonte com `java` direto e compare as
   duas mensagens: o que é igual, o que muda e por quê.

4. Compile, crie a subpasta `saida`, mova para lá o arquivo de bytecode e faça o
   programa rodar sem devolver o arquivo ao diretório atual.

5. Reproduza a armadilha: no mesmo diretório e sem editar nada entre um comando e
   outro, obtenha duas saídas diferentes. Escreva a menor regra de trabalho que
   torna esse engano impossível.

6. Escreva um arquivo-fonte compacto cujo único método se chame `principal` em
   vez de `main`. Descubra em qual dos dois momentos o problema aparece e explique
   por que ele aparece nesse e não no outro.

## Ficha do capítulo

| Comando | O que faz |
| --- | --- |
| `java Locadora.java` | compila em memória e executa; não grava bytecode |
| `javac Locadora.java` | grava `Locadora.class` e não executa nada |
| `java Locadora` | procura o bytecode de nome `Locadora` no classpath e executa |
| `java -cp saida Locadora` | mesma coisa, procurando em `saida` em vez do diretório atual |

| Termo | Definição |
| --- | --- |
| método | bloco de código com nome, que pode ser chamado por esse nome |
| `main` | método por onde a execução do programa começa |
| `void` | marca de que o método não devolve nada a quem o chamou |
| argumento | valor escrito entre parênteses na chamada e entregue ao método |
| `IO.println` | método pronto que escreve o argumento na saída padrão e quebra a linha |
| saída padrão | canal por onde o programa escreve seu resultado comum no terminal |
| arquivo-fonte compacto | arquivo `.java` que declara métodos diretamente, sem moldura em volta |
| compilador | programa que traduz o fonte; em Java, o comando `javac` |
| bytecode | formato intermediário gravado pelo compilador, lido pela JVM |
| JVM | programa que lê bytecode e o executa; iniciado pelo comando `java` |
| JDK | conjunto que traz `javac`, `java` e a biblioteca padrão |
| classpath | lista de lugares onde a JVM procura bytecode; por omissão, o diretório atual |
| erro de compilação | recusa do compilador; cita arquivo e linha, e nada é gravado |
| erro de execução | falha encontrada pela JVM com o programa já rodando |
