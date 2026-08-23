# Variáveis, primitivos e operadores

Quatro linhas dentro de `main`, salvas em `Maioridade.java`:

```java
void main() {
    int idade = 17;
    int ano = 2026;
    int maioridade = ano + 18 - idade;
    IO.println(maioridade);
}
```

```
$ java Maioridade.java
2027
```

O capítulo 2 imprimia o que já estava escrito no arquivo. Este programa é
diferente: o valor 2027 não aparece em linha nenhuma do fonte. Ele nasceu de
uma conta feita durante a execução, sobre valores guardados com nome nas duas
primeiras linhas. Guardar valores e calcular com eles é o assunto deste
capítulo, e as regras desse jogo têm consequências práticas: duas delas
produzem resultados errados sem aviso nenhum, e este capítulo as provoca de
propósito.

## Variáveis

A linha `int idade = 17;` tem três partes: um tipo, um nome e um valor. Uma
variável é um nome que guarda um valor durante a execução; escrever a linha
acima é declarar a variável, e o sinal `=` faz a atribuição: calcula o que
está à direita e guarda no nome à esquerda. O `=` de Java não é a igualdade
da matemática, é uma ordem com direção. A linha seguinte é legal e útil:

```java
idade = idade + 1;
```

Lida como igualdade, a linha é absurda; lida como ordem, é rotina: calcule
`idade + 1` com o valor atual, guarde o resultado de volta em `idade`. A
variável passa a valer 18. Declarar duas vezes o mesmo nome no mesmo trecho,
por outro lado, é erro de compilação: a declaração acontece uma vez, e as
atribuições seguintes usam só o nome.

O tipo, primeira palavra da declaração, diz que espécie de valor o nome
guarda e o que se pode fazer com ele. `int` guarda números inteiros; guardar
outra coisa ali é recusado na hora:

```
$ javac Maioridade.java
Maioridade.java:2: error: incompatible types: possible lossy conversion from double to int
    int idade = 17.5;
                ^
1 error
```

O compilador leu o tipo declarado, conferiu o valor e recusou antes de
existir programa. Essa conferência é o serviço que os tipos prestam: um
engano de espécie de valor vira erro de compilação, com arquivo e linha,
em vez de virar resultado errado em execução. Boa parte do desenho de Java
existe para empurrar enganos nessa direção.

## Oito primitivos, cinco em uso

Os tipos mais simples da linguagem chamam-se primitivos: neles, a variável
guarda o próprio valor, direto. Existem oito; este livro trabalha com cinco,
e os outros três ficam registrados na ficha do capítulo por completude.

Cada primitivo ocupa um número fixo de bits na memória, e é esse número que
determina quantos valores cabem no tipo. O capítulo 1 apresentou o bit como
a menor unidade de informação, com dois estados possíveis; combinar bits
multiplica possibilidades: 2 bits formam 4 combinações, 3 bits formam 8, e
cada bit acrescentado dobra o total, de modo que N bits distinguem 2^N
valores. Um `int` ocupa 32 bits, o que dá 2³² combinações, cerca de 4,29
bilhões; metade delas fica com os negativos, e daí vem o intervalo de ±2,1
bilhões. Um `long` ocupa 64 bits, um `double` também 64, um `char` 16, e o
`boolean` é o único cujo tamanho a linguagem não define, deixando a escolha
para a JVM. Como oito bits formam um byte, os mesmos tamanhos aparecem por
aí como 4 bytes para `int` e 8 para `long`.

`int` guarda inteiros de −2.147.483.648 a 2.147.483.647. Um valor escrito
diretamente no código, como o `17` e o `2026` da abertura, chama-se literal.
Java aceita o separador `_` dentro de um literal numérico, e ele só existe
para olhos humanos: `2_147_483_647` é o mesmo número. As notações do
capítulo 1 também valem como literal: `0x1F` é a escrita hexadecimal e
`0b11111` a binária do mesmo 31 decimal. A base muda a escrita no fonte; o
valor guardado é um só.

`long` guarda inteiros de até cerca de ±9,2 quintilhões (9,2 × 10¹⁸), e seu
literal leva o sufixo `L`:
`8_000_000_000L`. É o tipo das contagens que passam dos dois bilhões, como
milissegundos acumulados ou habitantes do planeta.

`double` guarda números com parte fracionária, escritos com ponto, não com
vírgula: `19.90`. O nome do formato é ponto flutuante, e a última seção
deste capítulo mostra o que esse formato esconde.

`boolean` guarda apenas dois valores, `true` e `false`. Ele quase nunca é
escrito como literal no dia a dia: nasce das comparações, apresentadas logo
adiante, e comanda as decisões do capítulo 4.

`char` guarda um único caractere, entre aspas simples: `'A'`. Aspas simples
e aspas duplas não se trocam: `"A"`, com aspas duplas, é um valor de outra
espécie, apresentada no capítulo 5. Por dentro, `char` é um número. Cada
caractere de cada escrita do mundo tem um código na tabela Unicode, a tabela
que dá um número a cada caractere, e `'A'` é o 65. Essa natureza numérica
reaparece daqui a duas seções.

## Expressões e operadores

Uma expressão é qualquer trecho de código que produz um valor: `17` é uma
expressão, `idade` é uma expressão, `ano + 18 - idade` é uma expressão. Um
operador é o símbolo que combina valores dentro de uma expressão. Os
aritméticos são cinco: `+`, `-`, `*` para multiplicar, `/` para dividir e
`%` para o resto da divisão. A precedência é a da escola: `*`, `/` e `%`
antes de `+` e `-`, e parênteses decidem qualquer outra ordem. Em caso de
dúvida, parênteses resolvem: não custam nada e eliminam a ambiguidade para o
próximo leitor.

<div class="previsao">

Um rateio simples:

```java
void main() {
    int total = 7;
    int pessoas = 2;
    IO.println(total / pessoas);
    IO.println(total % pessoas);
}
```

Duas linhas de saída. Quais valores aparecem?

</div>

```
3
1
```

A divisão entre dois `int` produz um `int`: a parte fracionária é descartada,
sem arredondamento (7 dividido por 2 daria 3,5; o resultado é 3, e 3,9
viraria 3 do mesmo jeito). O `%` entrega o que a divisão descartou como
resto inteiro: 2 cabe 3 vezes em 7, sobra 1. O custo de não saber disso é
concreto: média de avaliações, porcentual de desconto e rateio de conta saem
errados, sem erro nenhum na tela, sempre que os dois lados da divisão são
inteiros. O conserto aparece na seção de promoção, logo adiante.

Três atalhos completam o conjunto. Os operadores compostos aplicam a conta
sobre a própria variável: `total += 2` soma 2 a `total`, e `-=`, `*=`, `/=`
seguem o padrão. `total++` soma 1 e `total--` subtrai 1; este livro os usa
como instrução isolada, que é o uso que não guarda surpresa.

As comparações produzem `boolean`: `==` pergunta se dois valores são iguais,
`!=` se são diferentes, e `<`, `<=`, `>`, `>=` comparam ordem.
`IO.println(idade >= 18)` imprime `false` para a `idade` da abertura. Vale
fixar a diferença de papéis: `=` guarda, `==` compara. Combinar comparações
entre si, com "e", "ou" e "não", pede operadores próprios, que chegam no
capítulo 4 junto das estruturas que decidem.

## Promoção e casting

Misturar tipos numa expressão é permitido, com uma regra fixa, e é ela que
conserta o rateio da previsão: na divisão `total / 2.0`, um lado é `int` e o
outro é `double`; antes da conta, o `int` é convertido para `double`, a
divisão acontece entre dois `double` e o resultado é 3.5, com a fração
preservada. Essa
conversão automática do tipo mais estreito para o mais largo da expressão
chama-se promoção, e segue a largura dos tipos: `int` promove para `long`,
e ambos promovem para `double`. O `char` entra nas contas como o número que
ele é: `'A' + 1` vale 66, um `int`.

A conversão no sentido contrário nunca é automática; ela existe, mas precisa
ser pedida por escrito, com o tipo de destino entre parênteses:

```java
double preco = 3.9;
int inteiro = (int) preco;
char letra = (char) 66;
```

Esse pedido chama-se casting. `(int) 3.9` vale 3: o casting de `double` para
`int` descarta a parte fracionária, sem arredondar. `(char) 66` vale `'B'`,
o caminho de volta da tabela Unicode. E um casting de `long` para `int` com
valor grande demais corta o que não cabe, em silêncio: o compilador aceita
porque a ordem foi explícita, e a responsabilidade pelo corte passa a ser de
quem escreveu.

## Quando a conta estoura

<div class="armadilha">

Uma multiplicação inocente:

```java
void main() {
    int populacao = 2_000_000_000;
    int dobro = populacao * 2;
    IO.println(dobro);
}
```

```
-294967296
```

O programa compila, roda e imprime um número negativo. Nenhuma mensagem de
erro aparece, em nenhum dos dois momentos.

</div>

O nome disso é overflow. Um `int` vive em 32 bits, e 32 bits comportam
exatamente os valores do intervalo dado na seção dos primitivos; uma conta
que passa do máximo dá a volta e continua a contagem do outro extremo, no
lado negativo. A JVM não trata isso como erro: é o comportamento definido, o
programa segue, e o valor errado se espalha pelas contas seguintes. É a
primeira das duas surpresas prometidas na abertura, e aparece em lugares
previsíveis: contadores que crescem sem parar, quantias em centavos somadas
aos milhões, multiplicações de valores já grandes.

A correção é usar um tipo mais largo, com um detalhe que engana: trocar só o
tipo da variável de destino não basta. `long dobro = populacao * 2` imprime
o mesmo valor errado, porque a conta entre dois `int` acontece em `int`, e o
estrago já está feito quando o resultado é guardado. `populacao * 2L`
resolve: com um `long` na expressão, a promoção sobe a conta inteira para
`long` antes de multiplicar.

<div class="aprofundamento">

**Complemento de dois.** Nos 32 bits de um `int`, o bit mais alto indica o
sinal, e os negativos são representados de um jeito que faz a soma funcionar
com um circuito só, chamado complemento de dois. Somar 1 ao maior positivo
produz o padrão de bits do menor negativo; por isso o estouro "dá a volta"
em vez de parar o programa.

</div>

## O que o ponto flutuante esconde

<div class="previsao">

Uma soma de uma linha:

```java
void main() {
    IO.println(0.1 + 0.2);
}
```

O que aparece no terminal?

</div>

```
0.30000000000000004
```

Esta é a segunda surpresa prometida na abertura. Um `double` guarda o número
em binário, a notação do capítulo 1, e nem todo número decimal tem escrita
binária exata. A notação binária também aceita casas depois da vírgula, cada
uma valendo a metade da anterior: 0,1 em binário é um meio, 0,01 é um
quarto, 0,11 é três quartos. Um décimo está para essa escrita como um terço
está para a decimal: 1/3 em decimal vira 0,333… sem fim, e 1/10 em binário
vira uma sequência periódica sem fim. O que cabe nos 64 bits de um `double` é a aproximação mais próxima;
as sobras de 0.1 e de 0.2, invisíveis na impressão de cada um, aparecem na
soma. Frações cujo denominador é potência de dois, como 0.5 e 0.25, são
exatas, e por isso `0.5 + 0.25` imprime `0.75` sem ruído.

Duas regras práticas saem daí, e as duas voltam nos exercícios. Primeira:
comparar `double` com `==` não é confiável, porque dois caminhos de cálculo
que deveriam dar no mesmo valor podem diferir na última casa da aproximação. Segunda:
dinheiro não se guarda em `double`; um sistema que soma centavos aproximados
espalha diferenças de um centavo que ninguém consegue rastrear. Como
dinheiro se representa em Java é assunto do capítulo 7, junto do sistema que
vai precisar disso. O lugar do `double` é a medida física, peso, distância,
temperatura, onde o valor já nasce aproximado por natureza.

## var

Quando o valor inicial já deixa o tipo evidente, a palavra `var` declara a
variável sem repeti-lo:

```java
var total = 7;
var preco = 19.90;
```

O compilador olha o valor inicial e infere o tipo: `total` é `int`, `preco`
é `double`. Isso se chama inferência de tipo, e vem com duas regras. A
declaração com `var` exige o valor inicial na mesma linha, porque é dele que
o tipo sai; e o tipo inferido é fixo dali em diante, exatamente como se
estivesse escrito, de modo que `total = 1.5` continua sendo recusado. `var`
não muda o que a variável é; muda só quanto se digita. Nestes primeiros
capítulos o livro escreve os tipos por extenso, para eles ficarem visíveis;
`var` volta a aparecer no capítulo 17, quando os nomes de tipo crescem.

## Prática

1. Escreva um programa que guarde uma temperatura em graus Celsius num
   `double` e imprima a conversão para Fahrenheit, calculada como a
   temperatura vezes 9, dividida por 5, mais 32. Confira com um valor
   conhecido: 100 °C são 212 °F.

2. Guarde duas avaliações inteiras, 7 e 8, e imprima a média. Obtenha
   primeiro o resultado errado, com divisão inteira; depois conserte usando
   promoção, sem mudar o tipo das duas variáveis.

3. Parta de um `int` valendo 2.147.483.647, some 1 e imprima. Depois refaça
   a conta de modo a obter o valor correto, e explique por escrito em que
   ponto da linha a correção agiu.

4. Imprima `0.1 + 0.2` e depois `0.5 + 0.25`. Explique por escrito,
   apoiando-se na comparação com 1/3 em decimal, por que uma soma sai com
   ruído e a outra não.

5. Imprima `'a'`, depois `'a' + 1`, depois `(char) ('a' + 1)`. Descreva o
   tipo do valor em cada uma das três impressões e o papel do casting na
   última.

6. Escreva o valor 255 como literal decimal, hexadecimal e binário, guarde
   os três em variáveis e imprima os três, provando que a base muda a
   escrita e não o valor.

## Ficha do capítulo

| Tipo | Bits | Guarda | Literal de exemplo |
| --- | --- | --- | --- |
| `int` | 32 | inteiros até ±2,1 bilhões | `42`, `2_147_483_647`, `0x2A`, `0b101010` |
| `long` | 64 | inteiros até cerca de ±9,2 × 10¹⁸ | `8_000_000_000L` |
| `double` | 64 | ponto flutuante | `19.90`, `0.5` |
| `boolean` | a JVM decide | `true` ou `false` | `true` |
| `char` | 16 | um caractere (código Unicode) | `'A'` |
| `byte`, `short`, `float` | 8, 16, 32 | versões menores de `int` e `double`; raras fora de arquivo e rede | |

| Operador | O que faz |
| --- | --- |
| `+` `-` `*` `/` `%` | aritmética; `/` entre inteiros descarta a fração, `%` dá o resto |
| `+=` `-=` `*=` `/=` | aplica a conta sobre a própria variável |
| `++` `--` | soma ou subtrai 1, como instrução |
| `==` `!=` `<` `<=` `>` `>=` | comparações; produzem `boolean` |
| `(tipo)` | casting: conversão explícita, cortando o que não couber |

| Termo | Definição |
| --- | --- |
| variável | nome que guarda um valor durante a execução |
| declaração | linha que cria a variável, com tipo e nome |
| atribuição | o `=`: calcula a direita e guarda no nome da esquerda |
| tipo | a espécie de valor que o nome guarda e as operações válidas sobre ele |
| primitivo | tipo cujo valor é guardado diretamente na variável |
| literal | valor escrito diretamente no código |
| expressão | trecho de código que produz um valor |
| operador | símbolo que combina valores numa expressão |
| promoção | conversão automática para o tipo mais largo da expressão |
| casting | conversão explícita, escrita como `(tipo)`, por conta de quem pede |
| overflow | conta que passa do limite do tipo e dá a volta, sem aviso |
| ponto flutuante | formato binário aproximado do `double` |
| `var` | declaração cujo tipo o compilador infere do valor inicial |
| inferência de tipo | dedução do tipo pelo compilador a partir do valor inicial |
