# Math e Random

Com decisões, laços e entrada de teclado, um jogo de adivinhação está quase
ao alcance: o programa pensa num número, a pessoa chuta, o programa responde
se o segredo é maior ou menor. Falta uma peça que nenhum código dos capítulos
anteriores produz: um número que ninguém escolheu.

```java
void main() {
    Random sorteio = new Random();
    IO.println(sorteio.nextInt(1, 101));
    IO.println(sorteio.nextInt(1, 101));
}
```

```
$ java Sorteio.java
73
12
$ java Sorteio.java
41
89
```

Duas execuções, quatro valores diferentes. Sob o nome `Random`, a biblioteca
padrão oferece um gerador de números: `new Random()` cria um, do mesmo jeito
que `new StringBuilder()` criou o objeto de texto do capítulo 5, e cada
chamada de `nextInt(1, 101)` devolve um inteiro de 1 a 100. O que exatamente é o nome
`Random`, e por que `new Random()` tem essa forma, é assunto do capítulo 7;
este capítulo é sobre usá-lo bem, e sobre o punhado de contas prontas que
mora sob o nome `Math`.

## Sortear números

`nextInt` existe em duas formas. Com dois argumentos, `nextInt(inicio, fim)`
devolve um inteiro do início até antes do fim: `nextInt(1, 101)` produz de 1
a 100, nunca 101. Com um argumento, `nextInt(n)` devolve de 0 até antes de
`n`: `nextInt(6)` produz de 0 a 5. Nas duas formas o limite superior fica de
fora, no mesmo espírito dos índices de array do capítulo 5, que vão de zero
até o tamanho menos um. Além dos inteiros, `nextDouble()` devolve um
`double` de 0 até antes de 1, e `nextBoolean()` devolve `true` ou `false`
em cara ou coroa.

<div class="armadilha">

Um dado de seis faces para um jogo de tabuleiro:

```java
void main() {
    Random dado = new Random();
    for (int volta = 0; volta < 5; volta++) {
        IO.println(dado.nextInt(6));
    }
}
```

```
2
0
5
1
3
```

O programa compila, roda e imprime cinco lançamentos de aparência razoável.
O dado, porém, está viciado de um jeito que nenhuma dessas execuções denuncia.

</div>

`nextInt(6)` produz de 0 a 5: este dado tem uma face zero que não existe e
nunca tira seis. Nenhum erro acontece, os valores parecem plausíveis, e o
defeito só seria flagrado por quem contasse milhares de lançamentos. O
limite de fora é, com `Random`, a fonte clássica dos erros de *off-by-one*,
o engano de uma unidade num limite, e a correção tem duas grafias
equivalentes: `dado.nextInt(6) + 1` ou
`dado.nextInt(1, 7)`. Na dúvida, a forma de dois argumentos deixa a intenção
escrita: de 1 até antes de 7.

## Pseudoaleatório e a semente

<div class="previsao">

Dois geradores, criados com o mesmo argumento 42:

```java
void main() {
    Random primeiro = new Random(42);
    Random segundo = new Random(42);
    IO.println(primeiro.nextInt(1, 101));
    IO.println(primeiro.nextInt(1, 101));
    IO.println(segundo.nextInt(1, 101));
    IO.println(segundo.nextInt(1, 101));
}
```

Quatro sorteios. Que relação existe entre as duas primeiras linhas e as duas
últimas?

</div>

```
31
64
31
64
```

As duas sequências são idênticas, e idênticas em toda execução, em qualquer
máquina. Os números de `Random` não são sorteados: são calculados, um a
partir do anterior, numa sequência completamente determinada pelo valor
inicial. Por isso o nome técnico é número pseudoaleatório, e o valor que
determina a sequência inteira chama-se semente. `new Random(42)` fixa a
semente em 42; `new Random()`, sem argumento, tira a semente do relógio e de
outras fontes variáveis da máquina, e é isso que faz cada execução parecer
um sorteio novo.

Semente fixa parece derrotar o propósito, e é o contrário: é a ferramenta de
trabalho. Um defeito que só aparece com certos valores sorteados é um
defeito que some quando se tenta observá-lo; com a semente anotada, a
execução inteira se repete à vontade, valor por valor. O mesmo vale para
comparar duas versões de um programa sob os mesmos dados. A reprodutibilidade
volta ao livro no capítulo 15, quando os programas passam a ser testados
automaticamente.

<div class="aprofundamento">

**De onde saem os números.** Um gerador clássico guarda um valor interno e,
a cada pedido, o transforma com multiplicação, soma e resto, devolvendo um
pedaço do resultado. A sequência é longa o bastante para parecer sorteio,
mas quem conhece o valor interno prevê todos os próximos números. Para
sorteio valendo prêmio ou segurança existe `SecureRandom`, um gerador da
mesma família de uso cuja saída não se prevê; para jogos, simulações e
testes, `Random` basta e é mais rápido.

</div>

## Math: contas prontas

Sob o nome `Math` a biblioteca padrão reúne dezenas de contas prontas,
chamadas pelo próprio nome, sem `new`, do mesmo jeito que `IO.println`. O
porquê dessa diferença em relação a `Random` é assunto do capítulo 7. Este
livro usa um punhado delas, e declara desde já que não pretende cobrir as
demais; a lista completa vive na documentação oficial.

```java
void main() {
    IO.println(Math.max(7, 12));
    IO.println(Math.min(7, 12));
    IO.println(Math.abs(-15));
    IO.println(Math.round(2.5));
}
```

```
12
7
15
3
```

`max` e `min` escolhem entre dois valores, `abs` descarta o sinal, e `round`
arredonda para o inteiro mais próximo, devolvendo `long`; nos empates,
arredonda para cima, e por isso 2.5 foi a 3, enquanto `Math.round(-2.5)`
daria −2. `round` é o
arredondamento que o casting do capítulo 3 não faz: `(int) 2.9` trunca para
2, `Math.round(2.9)` vai a 3. Na ficha ficam ainda `pow` e `sqrt`, para
potência e raiz, à disposição de quem precisar; nenhum exercício deste livro
exige matemática além da aritmética.

## Tudo junto: o jogo

As peças dos capítulos 3 a 6 montam o jogo completo da abertura:

```java
void main() {
    Random sorteio = new Random();
    int segredo = sorteio.nextInt(1, 101);
    int chute = 0;
    while (chute != segredo) {
        chute = Integer.parseInt(IO.readln("Chute um número de 1 a 100: "));
        if (chute < segredo) {
            IO.println("O segredo é maior.");
        } else if (chute > segredo) {
            IO.println("O segredo é menor.");
        }
    }
    IO.println("Acertou!");
}
```

```
$ java Jogo.java
Chute um número de 1 a 100: 50
O segredo é maior.
Chute um número de 1 a 100: 75
O segredo é menor.
Chute um número de 1 a 100: 62
Acertou!
```

Quinze linhas: variáveis e conversão do capítulo 3 e do 5, decisão e laço do
capítulo 4, leitura do teclado do 5, sorteio deste. É o primeiro programa do
livro que ninguém executa duas vezes igual, e a prática abaixo o estica em
todas as direções.

## Prática

1. Corrija o dado da armadilha e prove a correção com força bruta: lance-o
   um milhão de vezes num laço, conte num array de contadores quantas vezes
   cada face saiu e imprima as contagens. Faces com contagens próximas, e
   nenhuma face zero, encerram a discussão.

2. Simule mil lançamentos de moeda com `nextBoolean` e imprima quantas caras
   e quantas coroas saíram. Rode três vezes e observe a variação em torno da
   metade.

3. Acrescente ao jogo um contador de tentativas e imprima-o na vitória.
   Depois limite a sete tentativas, encerrando com a revelação do segredo
   quando elas acabarem.

4. Rode o jogo com semente fixa e jogue duas partidas idênticas, provando
   que o segredo se repete. Explique por escrito por que essa versão é
   melhor para demonstrar o jogo numa aula e pior para jogar de verdade.

5. Sem usar `Math`, escreva um método que devolva o maior de três valores
   `int`, usando apenas o capítulo 4. Depois reescreva em uma linha com duas
   chamadas de `Math.max` e compare a legibilidade das duas versões por
   escrito.

## Ficha do capítulo

| Chamada | O que faz |
| --- | --- |
| `new Random()` | cria um gerador com semente tirada do relógio |
| `new Random(semente)` | cria um gerador de sequência reprodutível |
| `nextInt(a, b)` | inteiro de `a` até antes de `b` |
| `nextInt(n)` | inteiro de 0 até antes de `n` |
| `nextDouble()` | `double` de 0 até antes de 1 |
| `nextBoolean()` | `true` ou `false` |
| `Math.max(a, b)` / `Math.min(a, b)` | o maior / o menor de dois valores |
| `Math.abs(x)` | valor sem sinal |
| `Math.round(x)` | inteiro mais próximo, como `long` |
| `Math.pow(a, b)` / `Math.sqrt(x)` | potência e raiz quadrada |

| Termo | Definição |
| --- | --- |
| `Random` | gerador de números pseudoaleatórios; a sequência é determinada pela semente |
| número pseudoaleatório | valor calculado em sequência determinada, com aparência de sorteio |
| semente | valor inicial que determina toda a sequência do gerador |
| `Math` | conjunto de contas prontas da biblioteca padrão, chamadas pelo nome |
