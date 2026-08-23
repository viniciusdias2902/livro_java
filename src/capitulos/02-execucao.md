# Hello world e como o Java executa

Um arquivo de três linhas é suficiente para pôr um programa Java de pé:

```java
void main() {
    IO.println("Mercadinho aberto.");
}
```

O texto vai salvo em um arquivo chamado `Mercadinho.java`, e um único comando
no terminal o executa:

```
$ java Mercadinho.java
Mercadinho aberto.
```

Esse é o programa inteiro: uma linha impressa e o fim. A partir dele, este
capítulo provoca de propósito as duas falhas que vão acompanhar o leitor pelo
livro inteiro. Trocar uma letra dentro de `println` produz uma mensagem que
cita o arquivo, a linha e a coluna do problema. Mover um arquivo para uma
subpasta produz outra mensagem, que não cita linha nenhuma e reclama de um
nome. As duas se parecem com "não rodou", e é exatamente aí que mora a
dificuldade: elas vêm de programas diferentes, acontecem em momentos
diferentes e se consertam de jeitos diferentes. Quem trata as duas como a
mesma coisa procura o defeito no lugar errado, às vezes por horas. Separar
esses dois momentos é o trabalho deste capítulo, e é o que torna legíveis as
mensagens de erro de todos os capítulos seguintes.

O texto impresso, por sua vez, não é um exemplo qualquer. Um mercadinho de
bairro, com produtos e preços, estoque e validades, vendas e a caderneta de
fiado, é o sistema que este livro constrói do capítulo 7 ao 25; o prefácio
descreve esse plano. Ele entra em cena aqui do único jeito que a linguagem
vista até agora permite: como uma linha de saída. Até o capítulo 6, os
exemplos seguem pequenos e avulsos, porque as peças para mais do que isso
ainda não existem; o nome na tela fica como lembrete de para onde eles levam.

## As três linhas, uma a uma

A primeira linha declara um método. Um método é um bloco de código que tem
nome: escreve-se o bloco uma vez e ele pode ser executado, pelo nome, quantas
vezes forem necessárias. Declarar um método é escrevê-lo; chamar um método é
fazer a execução entrar nele. As chaves `{` e `}` marcam onde o corpo do
método começa e onde termina: tudo o que estiver entre elas é o que acontece
quando o método for chamado, e nada fora delas pertence a ele.

O nome `main` não foi escolha deste livro. `main` é o método por onde todo
programa Java começa: de tudo o que um arquivo declara, é esse o nome que a
execução procura e chama primeiro, e o programa termina quando esse método
termina. Um arquivo pode declarar outros métodos com outros nomes, mas a porta
de entrada é sempre essa, e um dos exercícios deste capítulo mostra o que
acontece quando ela não existe.

A palavra `void`, escrita antes do nome, declara que `main` não devolve nada a
quem o chamou. Um método pode produzir um resultado e entregá-lo ao ponto que
o chamou, para que a execução continue dali com esse resultado em mãos; `void`
é a marca de que este método não entrega resultado nenhum. Como um método
devolve, e o que muda no código de quem chama, é assunto do capítulo 4.

A linha do meio é uma chamada. `IO.println` é um método pronto: vem com o
Java, dentro da biblioteca padrão, e está disponível em qualquer arquivo como
este sem nenhuma linha extra. Ele recebe um argumento, que é o valor escrito
entre os parênteses e entregue ao método no momento da chamada, e escreve esse
valor na saída padrão, seguido de uma quebra de linha. Saída padrão é o canal
por onde um programa de terminal escreve seu resultado comum; é o que o
terminal mostra sem que ninguém peça nada. As aspas duplas marcam onde o texto
a imprimir começa e onde termina, e não aparecem na saída: o programa imprime
`Mercadinho aberto.`, não as aspas em volta. O `ln` no fim do nome é a quebra
de linha. Existe também `IO.print`, sem o `ln`, que escreve o mesmo valor e
deixa a saída parada na mesma linha. A diferença parece miúda até o primeiro
exercício em que duas mensagens saem grudadas uma na outra.

Resta explicar por que essas três linhas bastam como arquivo. Arquivo-fonte
compacto é o nome do arquivo `.java` que declara métodos diretamente, como
este. Antes da versão 25, o mesmo programa exigia linhas de moldura em volta
do método, e praticamente todo material publicado até hoje, de livros a
respostas em fórum, mostra essas linhas. O recurso que as dispensa passou por
rodadas de prévia e foi finalizado na versão 25; dela em diante, o compilador
fornece a moldura quando ela não está escrita. O que essa moldura declara, e
por que ela deixa de ser dispensável assim que um programa passa de um
arquivo, é assunto do capítulo 7. Há também uma segunda forma de escrever
`main`, que recebe o que foi digitado no terminal depois do nome do programa;
essa forma é o capítulo 5.

Duas linhas de um arquivo-fonte podem nunca chegar ao programa. Tudo o que vem
depois de `//` até o fim da linha, e tudo o que estiver entre `/*` e `*/`, é
comentário: texto para quem lê o arquivo, que o compilador descarta por
inteiro e que não influencia a execução de nenhuma forma. Os exercícios deste
capítulo pedem descrições por escrito, e o próprio arquivo `.java`, em
comentários, é um lugar razoável para elas.

## A versão do JDK decide se o arquivo compila

O calendário de versões do capítulo 1 cobra aqui sua primeira consequência
prática. O arquivo-fonte compacto só existe, como recurso finalizado, da
versão 25 em diante. Em um JDK anterior, o compilador recusa a primeira linha
do arquivo, e a recusa não menciona `main` nem `IO`, o que a torna difícil de
ligar à causa verdadeira. A mesma recusa pode ser reproduzida em um JDK novo,
mandando o compilador seguir as regras de uma versão antiga:

```
$ javac --release 24 Mercadinho.java
Mercadinho.java:1: error: implicitly declared classes are not supported in -source 24
void main() {
^
  (use -source 25 or higher to enable implicitly declared classes)
1 error
```

Vale conhecer essa mensagem de véspera, porque ela ensina uma regra de
leitura: mensagem estranha apontando para a primeira linha de um arquivo que
está correto é, quase sempre, sintoma de versão, não de código. Conferir a
versão instalada antes de procurar defeito no arquivo evita o desencontro:

```
$ java -version
openjdk version "26.0.2" 2026-07-21
OpenJDK Runtime Environment Corretto-26.0.2.10.1 (build 26.0.2+10-FR)
OpenJDK 64-Bit Server VM Corretto-26.0.2.10.1 (build 26.0.2+10-FR, mixed mode, sharing)
```

Da saída interessa o número no começo da primeira linha, que precisa ser 25 ou
maior; o resto identifica a distribuição, um Corretto nesta máquina, e não
muda nada do que este livro faz. Do capítulo 7 em diante, quando os arquivos
passam a trazer a moldura escrita por extenso, o livro roda também em JDKs
mais antigos; até lá, não.

## Dois programas, dois momentos

O comando da abertura, `java Mercadinho.java`, fazia dois trabalhos de uma
vez, e enquanto os dois dão certo não há como perceber que são dois. Estes
comandos os separam:

```
$ javac Mercadinho.java
$ ls
Mercadinho.class  Mercadinho.java
$ java Mercadinho
Mercadinho aberto.
```

`javac` é o compilador de Java: o compilador do capítulo 1, agora com nome e
comando próprios. Ele lê o texto de `Mercadinho.java`, confere se aquilo é
Java válido e grava o resultado da tradução em um arquivo novo, o
`Mercadinho.class`. O conteúdo desse arquivo não é texto Java nem código de
máquina de processador algum. É bytecode: até aqui uma ideia descrita no
papel, daqui em diante um arquivo concreto no disco, que pode ser copiado,
movido e apagado como qualquer outro. A extensão `.class` vem do nome de uma
declaração que o capítulo 7 apresenta.

Quem lê e executa esse arquivo é a JVM. O comando `java` inicia uma, entrega a
ela o bytecode indicado e sai do caminho: dali em diante, quem está rodando é
o programa. As duas ferramentas, `javac` para traduzir e `java` para executar,
vêm juntas no JDK, ao lado da biblioteca padrão onde mora `IO.println`.

A tradução em duas etapas é o mecanismo por trás da portabilidade prometida no
capítulo 1. O `Mercadinho.class` gerado aqui roda sem alteração em qualquer
máquina que tenha uma JVM da mesma versão ou mais nova, seja ela x86 ou ARM,
Windows, Linux ou macOS. O que se instala em cada máquina é a JVM certa para
ela; o bytecode entregue é o mesmo em todas. Um compilador que traduzisse
direto para o código de máquina produziria um programa mais rápido de iniciar
e preso a uma família de processador; o desenho do Java troca esse arranque
pela portabilidade.

O nome que aparece no comando `java` também sai desse desenho. Para um
arquivo-fonte compacto, o compilador dá ao bytecode gerado o mesmo nome do
arquivo: `Mercadinho.java` vira `Mercadinho.class`, e é `Mercadinho`, sem
extensão nenhuma, que se escreve depois de `java`. Renomear o arquivo antes de
compilar muda as duas coisas juntas.

## O erro que não deixa nada para trás

O compilador recusa o que não entende, e recusar quer dizer não gravar nada:

```
$ javac Mercadinho.java
Mercadinho.java:2: error: cannot find symbol
    IO.printn("Mercadinho aberto.");
      ^
  symbol:   method printn(String)
  location: class IO
1 error
$ ls
Mercadinho.java
```

Esse é um erro de compilação: o compilador aponta arquivo, linha, coluna e o
que não reconheceu, e o diretório continua sem nenhum `Mercadinho.class`. A
consequência vale ser dita por inteiro: um erro de compilação nunca alcança
quem usa o programa, porque não há programa a entregar. Tudo o que o
compilador consegue pegar, ele pega antes de existir qualquer coisa
executável, e esse é o motivo de tanta coisa neste livro ser desenhada para
transformar enganos em erros de compilação.

Duas leituras dessa mensagem valem virar hábito. A primeira: `cannot find
symbol` significa que o nome escrito não existe no lugar em que foi procurado;
na prática, um erro de digitação ou um nome que ainda não foi declarado. A
segunda: quando o compilador imprime várias mensagens de uma vez, a primeira
costuma ser a causa real e as demais costumam ser consequência dela. Corrigir
a de cima e compilar de novo economiza mais tempo do que tentar entender todas
de uma vez.

Nem toda recusa aponta a falta no lugar em que ela está. Retirar o ponto e
vírgula do fim da linha produz esta mensagem:

```
$ javac Mercadinho.java
Mercadinho.java:2: error: ';' expected
    IO.println("Mercadinho aberto.")
                                  ^
1 error
```

A coluna apontada é o fim da linha 2, não o começo da linha 3, porque o
compilador só percebe a ausência quando termina de ler o que veio antes. Toda
instrução Java termina em ponto e vírgula, e as chaves marcam onde o corpo do
método começa e acaba: essas duas regras respondem pela maior parte dos erros
de compilação da primeira semana, e as mensagens delas nem sempre apontam para
onde o dedo iria.

A outra família é a do erro que aparece com o programa já em execução, o erro
de execução. Esse o compilador não tem como prever, porque depende do que
acontece com o programa rodando, e a JVM só o encontra na hora. Os capítulos
seguintes apresentam os erros de execução mais comuns, um a um, à medida que
as construções que os provocam aparecem; o que este capítulo mostra é o
primeiro da lista, e ele nasce de uma pergunta simples: como a JVM encontra o
bytecode que deve executar?

<div class="previsao">

O diretório tem o fonte e o bytecode. O bytecode vai para uma subpasta e o
comando é repetido sem nenhuma outra mudança:

```
$ ls
Mercadinho.class  Mercadinho.java
$ mkdir saida
$ mv Mercadinho.class saida/
$ java Mercadinho
```

`Mercadinho.java` continua ali, intacto, e o programa nele está correto. O que
aparece no terminal?

</div>

O terminal responde isto:

```
Error: Could not find or load main class Mercadinho
Caused by: java.lang.ClassNotFoundException: Mercadinho
```

O fonte estar no diretório não ajuda em nada, porque `java Mercadinho` não lê
fonte nenhum: ele executa bytecode já pronto. E `Mercadinho`, nesse comando,
não nomeia um arquivo; nomeia o que a JVM tem de encontrar. Onde ela procura é
o classpath: a lista de lugares em que a JVM busca bytecode. Quando ninguém
diz nada, essa lista tem um item só, o diretório atual. O arquivo saiu do
diretório atual, então saiu da lista, e a JVM não tem por onde continuar.

Dizer onde procurar resolve:

```
$ java -cp saida Mercadinho
Mercadinho aberto.
```

`-cp`, que também se escreve `-classpath`, substitui a lista inteira pelo que
vem depois dele. Vale gravar o formato da mensagem: `could not find or load`
quase nunca quer dizer que o código não existe. Quer dizer que ele não está em
nenhum dos lugares da lista. Procurar o defeito dentro do fonte, nesse caso, é
procurar onde não está, e essa confusão responde por boa parte das primeiras
horas perdidas de quem começa. A partir do capítulo 14, quem monta o classpath
deixa de ser quem digita o comando e passa a ser a ferramenta de construção do
projeto; até lá, ele é digitado à mão, e digitá-lo à mão algumas vezes é o que
torna compreensível o que a ferramenta fará depois.

<div class="armadilha">

Dois comandos, o mesmo diretório, saídas diferentes:

```
$ javac Mercadinho.java
$ # edite o arquivo e troque o texto por "Mercadinho fechado para inventário."
$ java Mercadinho
Mercadinho aberto.
$ java Mercadinho.java
Mercadinho fechado para inventário.
```

`java Mercadinho.java` compila o fonte na memória e executa o que acabou de
compilar, sem gravar nada em disco. `java Mercadinho` ignora o fonte e executa
o `Mercadinho.class` que encontrar no classpath, que é o de antes da edição. O
sintoma é uma correção que não faz efeito: o código muda, o comando roda sem
erro nenhum, e a saída continua a antiga. Compilar antes de executar, sempre,
é o que elimina essa classe de engano.

</div>

<div class="aprofundamento">

**JIT.** A JVM começa interpretando o bytecode uma instrução por vez e, nos
trechos que se repetem muito, traduz esse bytecode para instruções do
processador da máquina e guarda o resultado para as próximas passagens. Esse
tradutor interno chama-se JIT, de *just-in-time*. É por isso que um mesmo
trecho de código pode ficar mais rápido depois de alguns milhares de
execuções, sem que nada tenha mudado no programa.

</div>

## Prática

1. Escreva um arquivo-fonte compacto que imprima três linhas, uma por chamada
   de `IO.println`, e execute-o sem compilar antes. Depois troque a última
   chamada por `IO.print` e descreva por escrito a diferença na saída.

2. Compile o arquivo com `javac`, apague o `.java` e execute o programa.
   Escreva em uma frase o que esse resultado prova sobre o que a JVM precisa
   ter em mãos.

3. Escreva `IO.printn` no lugar de `IO.println` e compile. Anote arquivo,
   linha e coluna citados. Depois execute o mesmo fonte com `java` direto e
   compare as duas mensagens: o que é igual, o que muda e por quê.

4. Compile, crie a subpasta `saida`, mova para lá o arquivo de bytecode e faça
   o programa rodar sem devolver o arquivo ao diretório atual.

5. Reproduza a armadilha: no mesmo diretório e sem editar nada entre um
   comando e outro, obtenha duas saídas diferentes. Escreva a menor regra de
   trabalho que torna esse engano impossível.

6. Escreva um arquivo-fonte compacto cujo único método se chame `principal` em
   vez de `main`. Descubra em qual dos dois momentos o problema aparece e
   explique por que ele aparece nesse momento e não no outro.

## Ficha do capítulo

| Comando | O que faz |
| --- | --- |
| `java Mercadinho.java` | compila em memória e executa; não grava bytecode |
| `javac Mercadinho.java` | grava `Mercadinho.class` e não executa nada |
| `java Mercadinho` | procura o bytecode de nome `Mercadinho` no classpath e executa |
| `java -cp saida Mercadinho` | mesma coisa, procurando em `saida` em vez do diretório atual |

| Termo | Definição |
| --- | --- |
| método | bloco de código com nome, que pode ser chamado por esse nome |
| `main` | método por onde a execução do programa começa |
| `void` | marca de que o método não devolve nada a quem o chamou |
| argumento | valor escrito entre parênteses na chamada e entregue ao método |
| `IO.println` | método pronto que escreve o argumento na saída padrão e quebra a linha |
| saída padrão | canal por onde o programa escreve seu resultado comum no terminal |
| arquivo-fonte compacto | arquivo `.java` que declara métodos diretamente, sem moldura em volta |
| `javac` | o compilador de Java; grava bytecode e não executa nada |
| bytecode | formato intermediário gravado pelo compilador, lido pela JVM |
| JVM | programa que lê bytecode e o executa; iniciado pelo comando `java` |
| classpath | lista de lugares onde a JVM procura bytecode; por omissão, o diretório atual |
| erro de compilação | recusa do compilador; cita arquivo e linha, e nada é gravado |
| erro de execução | falha encontrada pela JVM com o programa já rodando |
