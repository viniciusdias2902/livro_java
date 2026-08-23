# Fluxo de controle e decomposição

Um programa de cinema precisa responder se um ingresso é de meia-entrada:

```java
void main() {
    int idade = 16;
    if (idade < 18) {
        IO.println("Meia-entrada.");
    } else {
        IO.println("Inteira.");
    }
}
```

```
$ java Ingresso.java
Meia-entrada.
```

Todos os programas dos capítulos anteriores executavam as mesmas linhas, na
mesma ordem, em toda execução. Este não: uma das duas impressões nunca
acontece, e qual delas roda depende de um valor. Escolher o caminho da
execução, repetir trechos e dar nome a pedaços do programa são as três
habilidades deste capítulo, e com elas os programas deixam de ser listas de
ordens para virar comportamento.

## if, else e a condição

`if` executa um bloco somente quando uma condição vale. Condição é uma
expressão de valor `boolean`, exatamente as que as comparações do capítulo 3
produzem: `idade < 18` vale `true` ou `false`, e o `if` consulta esse valor.
O bloco entre chaves logo após o `if` roda no caso `true`; o bloco do
`else`, que é opcional, roda no caso `false`. Encadear decisões é escrever
`else if`:

```java
if (nota >= 90) {
    IO.println("A");
} else if (nota >= 70) {
    IO.println("B");
} else {
    IO.println("C");
}
```

As comparações acontecem de cima para baixo e a primeira condição
verdadeira ganha: uma nota 95 imprime só `A`, porque o `else if` nem chega a
ser avaliado. A ordem das faixas, portanto, faz parte da lógica, e
invertê-la muda o programa.

As chaves são opcionais quando o bloco tem uma linha só, e este livro as
escreve sempre. O motivo cabe numa armadilha, mais adiante.

## Combinando condições

O capítulo 3 deixou uma promessa: os operadores que combinam decisões. São
três. `&&` é o "e": a expressão inteira só vale `true` com os dois lados
`true`. `||` é o "ou": basta um lado `true`. `!` é o "não": inverte o valor
que vem depois.

```java
boolean meia = idade < 18 || idade >= 60;
boolean pagaInteira = !meia;
```

`&&` e `||` avaliam com preguiça calculada, e isso tem nome: curto-circuito.
Quando o lado esquerdo já decide o resultado, o lado direito nem é avaliado:
um `&&` com esquerda `false` já é `false`, um `||` com esquerda `true` já é
`true`, e a execução segue sem tocar no resto. Não é só economia; é uma
técnica de proteção. A divisão inteira por zero derruba o programa com um
erro de execução chamado `ArithmeticException`, e o curto-circuito permite
blindar a conta na própria condição:

```java
if (pessoas != 0 && total / pessoas > 100) {
    IO.println("Rateio alto.");
}
```

Com `pessoas` valendo zero, o lado esquerdo é `false`, a divisão nunca
acontece e o programa segue. Invertida a ordem dos dois lados, a mesma linha
derruba o programa. Em curto-circuito, a ordem dos operandos é parte da
correção, não do estilo.

## Decisão em forma de valor

Duas construções decidem produzindo um valor, em vez de executar blocos. O
operador ternário escolhe entre duas expressões:

```java
int desconto = idade < 18 ? 50 : 0;
```

Lê-se: se a condição vale, o valor é o do meio; senão, o do fim. Ele serve
para escolhas curtas dentro de uma atribuição; encadear ternários dentro de
ternários compila, e é o jeito mais rápido de escrever uma linha que ninguém
mais consegue ler.

Para escolher entre vários casos a partir de um mesmo valor, existe o switch
expression:

```java
int minutosDeTreino = switch (dia) {
    case 1, 7 -> 60;
    case 6 -> 30;
    default -> 45;
};
```

O valor entre parênteses é comparado com cada `case`; a seta aponta o valor
produzido; casos podem ser agrupados com vírgula; e `default` cobre todo o
resto. O switch expression exige que algum caminho exista para qualquer
valor possível, e com um `int` na entrada isso obriga o `default`: sem ele,
erro de compilação. Essa exigência é uma proteção, e ela cresce de
importância no capítulo 12, quando os valores da entrada passam a ter dono.
Material antigo mostra um `switch` de outro formato, com dois-pontos no
lugar da seta e regras traiçoeiras de continuação; este livro usa apenas a
forma nova.

## Laços

Um laço repete um bloco enquanto uma condição valer. O `while` é a forma
crua:

```java
int restantes = 3;
while (restantes > 0) {
    IO.println(restantes);
    restantes--;
}
IO.println(0);
```

```
3
2
1
0
```

A condição é conferida antes de cada volta, inclusive a primeira: um
`while` com condição inicial `false` não roda nenhuma vez. E uma condição
que nunca vira `false` não para nunca; o programa fica preso, sem erro e sem
saída, até ser morto no terminal com `Ctrl+C`.

Quando a repetição tem contador, começo e passo, o `for` empacota as três
partes na primeira linha:

```java
for (int volta = 1; volta <= 5; volta++) {
    IO.println(volta * 7);
}
```

A primeira parte declara e inicia o contador, a segunda é a condição
conferida antes de cada volta, a terceira roda ao fim de cada volta. O
trecho imprime a tabuada do 7 até 35. Dentro de qualquer laço valem duas
palavras de controle, definidas aqui de passagem: `break` abandona o laço na
hora, e `continue` pula direto para a próxima volta.

<div class="armadilha">

Um contador fracionário, somando de um décimo em um décimo até chegar a um:

```java
void main() {
    double x = 0.0;
    while (x != 1.0) {
        x += 0.1;
    }
    IO.println("Cheguei.");
}
```

O programa compila e roda. O que acontece no terminal?

</div>

Nada, para sempre. O capítulo 3 mostrou que 0.1 não tem escrita binária
exata; somado dez vezes, o acumulado passa perto de 1.0 sem valer exatamente
1.0, a comparação `!=` nunca vira `false`, e o laço não termina. Nenhuma
mensagem aparece, porque nenhum erro aconteceu: o programa está fazendo o
que está escrito. A regra prática: contador de laço é inteiro; o `double`
entra na conta de dentro, nunca no controle da repetição.

## Métodos próprios e decomposição

Desde o capítulo 2, todo código deste livro mora em `main`. Um arquivo-fonte
compacto aceita outros métodos ao lado dele:

```java
int precoDoIngresso(int idade) {
    if (idade < 18 || idade >= 60) {
        return 20;
    }
    return 40;
}

void main() {
    IO.println(precoDoIngresso(16));
    IO.println(precoDoIngresso(30));
}
```

```
20
40
```

Três novidades moram aí. `int idade`, entre os parênteses da declaração, é
um parâmetro: uma variável que nasce a cada chamada, já valendo o argumento
que veio de fora. O capítulo 2 apresentou o argumento como o valor entregue
na chamada; o parâmetro é o outro lado do balcão, o nome que o recebe. A
palavra `return` devolve um valor ao ponto que chamou e encerra o método
naquele instante: na primeira chamada acima, o `return 20` roda e o
`return 40` nem é alcançado. E o `int` antes do nome do método declara o
tipo do valor devolvido, ocupando a posição onde `main` escreve `void`, a
marca de quem não devolve nada.

O nome disso tudo é decomposição: partir um programa em métodos pequenos,
cada um com um trabalho nomeado. O ganho não é estético. Um cálculo que
existe num único lugar é corrigido num único lugar, e um método com nome
honesto documenta o programa melhor do que comentário.

Cada método tem uma assinatura: o nome mais os tipos dos parâmetros, na
ordem. É a assinatura que identifica o método, e por isso dois métodos podem
ter o mesmo nome com parâmetros diferentes, o que se chama sobrecarga:

```java
int dobro(int valor) {
    return valor * 2;
}

double dobro(double valor) {
    return valor * 2;
}
```

<div class="previsao">

Com os dois métodos `dobro` acima no arquivo:

```java
void main() {
    IO.println(dobro(21));
    IO.println(dobro(21.0));
    IO.println(dobro('a'));
}
```

Três linhas de saída. Quais, e qual `dobro` atende cada chamada?

</div>

```
42
42.0
194
```

O compilador escolhe pela assinatura que casa com o argumento: `21` é `int`
e vai para o primeiro método, `21.0` é `double` e vai para o segundo. A
terceira chamada é o caso interessante: não existe `dobro` de `char`, e o
compilador aplica a promoção do capítulo 3, convertendo `'a'` para o seu
código 97 e chamando a versão de `int`, que devolve 194. A escolha acontece
na compilação, em silêncio, e uma sobrecarga nova pode mudar para onde
chamadas antigas vão. Sobrecarga é ferramenta boa para operações realmente
iguais sobre tipos diferentes, e má para qualquer outra coisa.

## Escopo

Uma variável não existe no programa inteiro. Ela nasce na linha da
declaração e morre no fim do bloco onde nasceu, e esse alcance chama-se
escopo. O contador declarado na primeira parte de um `for` vive só dentro
do laço; a variável declarada dentro de um `if` vive só ali; um parâmetro
vive só no corpo do seu método. Usar o nome fora do escopo produz o
`cannot find symbol` do capítulo 2, porque, para o compilador, fora do bloco
o nome simplesmente não existe.

O escopo é o que torna a decomposição segura. Dois métodos podem declarar
variáveis de mesmo nome sem conflito, porque cada nome vive no seu corpo;
quem escreve um método não precisa saber que nomes os outros usam. Em
programas de um arquivo isso parece pouco; num sistema, é o que permite que
partes escritas por pessoas diferentes convivam.

## Recursão

Um método pode chamar a si mesmo, e isso se chama recursão:

```java
int somaAte(int n) {
    if (n == 1) {
        return 1;
    }
    return n + somaAte(n - 1);
}
```

`somaAte(4)` devolve `4 + somaAte(3)`, que devolve `3 + somaAte(2)`, e
assim até `somaAte(1)`, que devolve 1 sem se chamar de novo: 10 ao todo. A
linha do `n == 1` é o caso base, a saída da repetição, e é a parte que não
pode faltar. Sem caso base, as chamadas se acumulam até a JVM desistir, com
um erro de execução chamado `StackOverflowError`; o aprofundamento abaixo
explica o nome. Todo problema recursivo tem uma versão com laço, e este
livro usa laços na maior parte do tempo; a recursão volta quando a estrutura
do problema for ela mesma recursiva.

<div class="aprofundamento">

**A pilha de chamadas.** A JVM guarda as variáveis de cada chamada de
método em andamento numa estrutura que cresce a cada chamada e encolhe a
cada `return`, a pilha de chamadas. É ela que dá a cada chamada as suas
próprias variáveis, inclusive nas mil chamadas simultâneas de uma recursão.
Recursão sem caso base enche a pilha até o limite, e o nome do erro,
"estouro de pilha" em inglês, descreve exatamente isso.

</div>

<div class="armadilha">

Um ponto e vírgula a mais, depois da condição:

```java
void main() {
    int saldo = -50;
    if (saldo >= 0);
    {
        IO.println("Saldo disponível.");
    }
}
```

```
Saldo disponível.
```

O saldo é negativo e a mensagem sai mesmo assim, sem erro nenhum.

</div>

O `;` logo após o `if` é uma instrução vazia, válida, e é ela o bloco do
`if`. As chaves seguintes formam um bloco solto, que roda sempre. O
compilador não reclama porque nada está errado para ele; o programa apenas
não diz o que parece dizer. O mesmo vale para o `while`: `while (x > 0);`
gira em silêncio para sempre. É por acidentes dessa família que este livro
escreve chaves mesmo em blocos de uma linha, e o hábito vale a pena desde o
primeiro dia.

## Prática

1. Escreva um método que receba um ano e devolva `true` para ano bissexto:
   divisível por 4 e não por 100, exceto quando divisível por 400. Imprima o
   resultado para 2024, 2025, 2100 e 2400.

2. Com um `for` de 1 a 100, imprima cada número, substituindo múltiplos de 3
   por `Fizz`, múltiplos de 5 por `Buzz` e múltiplos de ambos por
   `FizzBuzz`. Decida a ordem das condições e explique por escrito por que
   ela importa.

3. Escreva duas sobrecargas de um método `maior`: uma que compara dois `int`
   e uma que compara dois `double`. Depois chame `maior(3, 4.5)` e explique
   por escrito qual versão atendeu e por quê.

4. Reproduza o laço infinito do contador `double` e conserte de duas formas
   diferentes: com contador inteiro e com comparação de ordem no lugar da
   comparação de igualdade. Escreva qual das duas correções é a melhor e o
   motivo.

5. Escreva um método recursivo que conte de `n` até zero, imprimindo cada
   valor. Retire o caso base, execute, anote o nome do erro e explique por
   que ele é um erro de execução, e não de compilação.

6. Escreva um switch expression que receba o número de um mês e devolva
   quantos dias ele tem num ano comum, agrupando os meses de mesma duração.
   Fevereiro fica com 28.

## Ficha do capítulo

| Construção | O que faz |
| --- | --- |
| `if` / `else if` / `else` | executa o primeiro bloco cuja condição vale |
| `cond ? a : b` | operador ternário: escolhe um valor pela condição |
| `switch (v) { case ... -> ... }` | switch expression: escolhe um valor entre casos |
| `while (cond) { }` | repete enquanto a condição valer; confere antes de cada volta |
| `for (início; cond; passo) { }` | laço com contador empacotado |
| `break` / `continue` | abandona o laço / pula para a próxima volta |
| `return expr;` | devolve o valor e encerra o método |

| Termo | Definição |
| --- | --- |
| condição | expressão `boolean` consultada por `if`, laços e afins |
| `if` | executa um bloco somente com a condição valendo |
| curto-circuito | `&&` e `\|\|` não avaliam o lado direito quando o esquerdo decide |
| operador ternário | decisão em forma de expressão: `cond ? a : b` |
| switch expression | escolha entre vários casos, produzindo um valor |
| laço | repetição de um bloco controlada por condição |
| parâmetro | variável do método que recebe o argumento da chamada |
| `return` | devolve um valor e encerra o método no ato |
| assinatura | nome do método mais os tipos dos parâmetros |
| sobrecarga | métodos de mesmo nome com assinaturas diferentes |
| escopo | o trecho do programa em que um nome existe |
| recursão | método que chama a si mesmo, com caso base obrigatório |
