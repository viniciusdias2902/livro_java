# Lambdas e interfaces funcionais

O `Produto` saiu do capítulo 17 sabendo se comparar por nome, e o relatório
de reposição quer outra coisa: os produtos do estoque em ordem de preço. A
ordem natural do `Comparable` é uma só por tipo, e ordem de relatório muda a
cada relatório. O método `sort` de `List` aceita a ordem como argumento, e a
linha que a entrega apresenta a sintaxe deste capítulo:

```java
List<Produto> estoque = new ArrayList<>(estoqueCompleto);
estoque.sort((a, b) -> a.preco().compareTo(b.preco()));
```

O `new ArrayList<>(colecao)` copia a coleção recebida, deixando a original
em paz para o relatório ordenar à vontade. O trecho `(a, b) -> a.preco().compareTo(b.preco())` é uma lambda: uma função
sem nome, escrita como expressão, com os parâmetros antes da seta e o
resultado depois. Até aqui, todo comportamento do livro morava em métodos
com nome, dentro de tipos; a lambda deixa escrever um comportamento pequeno
no exato lugar onde ele é usado, e entregá-lo como argumento, como se
entrega um valor. É a peça que faltava para as coleções renderem o que
prometem, e o capítulo 19 é inteiro construído sobre ela.

## A sintaxe e o alvo

A lambda tem três formas, da mais curta para a mais completa:

```java
p -> p.estoque() == 0
(a, b) -> a.preco().compareTo(b.preco())
(Produto p) -> {
    IO.println(p.nome());
    return p.preco();
}
```

Um parâmetro dispensa parênteses; o corpo de uma expressão só dispensa
chaves e `return`; o corpo em bloco escreve os dois. Os tipos dos parâmetros
quase nunca aparecem, porque o compilador os infere, e a pergunta certa é de
onde: toda lambda nasce num contexto que espera um tipo específico, e esse
tipo é sempre uma interface funcional, a interface com um único método
abstrato. A lambda é um atalho para implementar exatamente esse método: os
parâmetros dela são os do método, o corpo dela é o corpo dele, e o
compilador confere tudo contra a assinatura. O `sort` espera um
`Comparator<Produto>`, cujo único método recebe dois produtos e devolve
`int`; a lambda da abertura é uma implementação dele, sem classe, sem nome e
sem cerimônia.

O `MeioDePagamento` tem um único método abstrato, portanto é uma interface
funcional sem saber, e um teste pode fabricar um meio de pagamento de
mentira numa linha:

```java
MeioDePagamento semTaxa = compra -> compra;
```

A anotação `@FunctionalInterface`, opcional e recomendada, marca a intenção
na interface e faz o compilador recusar um segundo método abstrato, no
espírito do `@Override`.

## As quatro famílias prontas

A biblioteca padrão traz interfaces funcionais de prateleira para os quatro
papéis que cobrem quase todo uso, todas no pacote `java.util.function`:

`Predicate<T>` testa e responde `boolean`. É o tipo do critério, e o
`removeIf` que o capítulo 17 deixou prometido o recebe:

```java
estoque.removeIf(p -> p.estoque() == 0);
```

`Function<T, R>` transforma um valor em outro: recebe `T`, devolve `R`.

```java
Function<Produto, String> etiqueta = p -> p.nome() + ", R$ " + p.preco();
```

`Consumer<T>` recebe um valor e não devolve nada, só age; o `forEach` das
coleções o aceita:

```java
estoque.forEach(p -> IO.println(p.nome()));
```

`Supplier<T>` é o espelho: não recebe nada e fornece um valor a cada
chamada, pelo método `get`.

As quatro cobrem o essencial e não esgotam o pacote. Quando a operação
recebe dois valores em vez de um, cada família tem a versão de dois
argumentos, com o prefixo `Bi`: `BiFunction<T, U, R>` transforma dois
valores num terceiro, `BiConsumer<T, U>` age sobre dois e
`BiPredicate<T, U>` testa dois. E quando o valor sai do mesmo tipo que
entrou, dois atalhos com nome próprio dizem isso na assinatura:
`UnaryOperator<T>` é a `Function<T, T>`, e `BinaryOperator<T>` é a
`BiFunction<T, T, T>`, a forma de toda soma e de todo "escolha um dos
dois".

```java
UnaryOperator<BigDecimal> comDesconto = valor -> valor.multiply(new BigDecimal("0.95"));
BinaryOperator<BigDecimal> soma = BigDecimal::add;
BiFunction<Produto, Integer, BigDecimal> subtotal = (produto, quantidade) -> produto.precoPara(quantidade);
```

Os nomes valem ser reconhecidos: é `BinaryOperator` que o capítulo 19 pede
para somar uma coleção inteira, e ler o nome na assinatura poupa a consulta
à documentação.

Uma última trilha existe por causa do autoboxing do capítulo 17.
`Predicate<Integer>` recebe um `Integer`, o que significa criar um objeto
por valor testado; `IntPredicate` recebe `int` direto, e a família tem uma
variante por primitivo, com `IntFunction`, `ToIntFunction`,
`IntUnaryOperator` e as demais. O nome diz onde o primitivo está: como
prefixo, ele é o que entra; depois de `To`, é o que sai. Em código de
domínio, feito de objetos, elas quase não aparecem; em processamento de
muitos números, poupam um objeto por elemento, e é por isso que os streams
do capítulo 19 têm uma trilha inteira dedicada a elas.

<div class="previsao">

Um fornecedor de produto padrão, declarado e depois usado:

```java
void main() {
    Supplier<Produto> padrao = () -> {
        IO.println("criando o produto padrão");
        return new Produto("0000000000000", "Sem cadastro", BigDecimal.ZERO);
    };
    IO.println("fornecedor pronto");
    Produto p = padrao.get();
    IO.println(p.nome());
}
```

Em que ordem saem as três impressões?

</div>

```
fornecedor pronto
criando o produto padrão
Sem cadastro
```

Declarar a lambda não executa o corpo: a linha do `Supplier` só guarda o
comportamento, e "criando" aparece apenas quando alguém chama `get`. Lambda
é um valor que carrega comportamento ainda não executado, e quem decide o
momento da execução é quem a recebe; essa inversão, modesta aqui, é o motor
central do capítulo 19.

## Comparator e a referência de método

`Comparator` merece seção própria porque é a interface funcional mais usada
fora das quatro famílias, e porque ela apresenta o segundo atalho da
sintaxe. A fábrica `Comparator.comparing` monta o comparador a partir da
função que extrai a chave de ordenação:

```java
estoque.sort(Comparator.comparing(Produto::preco));
estoque.sort(Comparator.comparing(Produto::preco).reversed());
estoque.sort(Comparator.comparing(Produto::categoria)
                       .thenComparing(Produto::nome));
```

`Produto::preco` é uma referência de método: quando a lambda inteira seria
só "chame este método", os dois-pontos duplos a escrevem sem inventar
parâmetros. `p -> p.preco()` e `Produto::preco` são o mesmo comportamento; a
referência existe para a leitura, e vale usá-la sempre que a lambda não faz
nada além da chamada. Há três formas: a referência a método de instância
pelo tipo, como `Produto::preco`; a referência a método estático, família
de `Integer::parseInt` e também de `IO::println`, e é por isso que
`estoque.forEach(IO::println)` compila; e a referência a método de um
objeto já existente, como `relatorio::append` com um `StringBuilder` em
mãos. E quando a ordem desejada é a natural do `Comparable`,
`Comparator.naturalOrder()` a entrega como comparador, com
`Comparator.reverseOrder()` fazendo o inverso.

Três parentes fecham a família. `Comparator.comparingInt`, `comparingLong`
e `comparingDouble` são as versões para chave primitiva: evitam embrulhar a
chave num wrapper a cada comparação e, no caso do `int`, comparam sem o
risco que a armadilha abaixo mostra. `nullsFirst(comparador)` e
`nullsLast(comparador)` embrulham um comparador para ele aceitar `null` em
vez de derrubar, decidindo em qual ponta os ausentes ficam, que é a
resposta pronta para a coluna opcional de um relatório.

Parente visual dessa sintaxe, e coisa completamente diferente, é o literal
de classe: `Produto.class`, o objeto que representa o próprio tipo em
execução. Ele estreia de verdade na seção seguinte e reina no capítulo 23.

<div class="armadilha">

O clube de fidelidade do mercadinho guarda o saldo de pontos como `int`, e
estorno deixa saldo negativo. O extrato ordena os saldos subtraindo:

```java
List<Integer> saldos = new ArrayList<>(List.of(10, 2_000_000_000, -300_000_000));
saldos.sort((a, b) -> a - b);
IO.println(saldos);
```

```
[10, 2000000000, -300000000]
```

A lista saiu em ordem nenhuma, sem erro nenhum.

</div>

A subtração devolve o sinal certo enquanto não estoura, e o estouro exige
exatamente o que o exemplo tem: sinais opostos com magnitudes grandes.
`2_000_000_000 - (-300_000_000)` passa do teto do `int`, sofre o overflow
do capítulo 3, dá a volta e sai negativo, dizendo ao `sort` que dois
bilhões vêm antes de trezentos milhões negativos. As magnitudes aqui são de
laboratório; o mecanismo não é. Com estoques, não negativos por invariante
desde o capítulo 7, a subtração nunca estoura; com qualquer chave que possa
ser negativa, saldo, variação, diferença, ela é defeito latente, e como
ninguém audita faixas a cada uso, a regra é uma só: comparador não subtrai.
`Integer.compare(a, b)` compara sem estourar, e
`Comparator.comparingInt` faz o mesmo por dentro.

## Captura, e o efetivamente final

Uma lambda enxerga as variáveis do escopo onde nasceu, e usá-las tem nome:
captura de variável.

```java
BigDecimal teto = new BigDecimal("10.00");
estoque.removeIf(p -> p.preco().compareTo(teto) > 0);
```

O `teto` não é parâmetro da lambda: veio capturado do método em volta. A
regra que governa a captura: uma variável local só pode ser capturada se
for efetivamente final, isto é, se nunca for reatribuída depois de receber
valor, tenha ou não a palavra `final` escrita.
O compilador recusa a captura de variável que muda:

```java
int contador = 0;
estoque.forEach(p -> {
    contador = contador + 1;
});
```

```console
$ javac Relatorio.java
Relatorio.java:9: error: local variables referenced from a lambda expression must be final or effectively final
        contador = contador + 1;
        ^
1 error
```

O motivo é o tempo: a lambda pode rodar muito depois, quando o método que a
criou já retornou e as variáveis locais dele já morreram com a pilha de
chamadas. O que a lambda captura é o valor, congelado; permitir
reatribuição criaria duas verdades sobre a mesma variável. Quando a vontade
é acumular algo dentro de uma lambda, o desenho certo quase sempre é outro:
ou o laço comum de sempre, ou as ferramentas de agregação do capítulo 19,
que existem exatamente para isso.

O capítulo 15 fica pago aqui: o teste de recusa, escrito lá com try e
`fail`, encolhe para a forma moderna, com a lambda segurando o código que
deve explodir e o literal de classe dizendo o tipo esperado:

```java
@Test
void recusaEstoqueNegativo() {
    assertThrows(IllegalArgumentException.class,
                 () -> new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"), -8));
}
```

## Compor comportamento

As interfaces funcionais da biblioteca trazem métodos default, no sentido
do capítulo 9, que combinam duas lambdas numa terceira. `Predicate` traz
três: `negate` inverte o critério, `and` exige os dois, `or` aceita
qualquer um.

```java
Predicate<Produto> semEstoque = p -> p.estoque() == 0;
Predicate<Produto> daMercearia = p -> p.categoria() == Categoria.MERCEARIA;

Predicate<Produto> reporNaMercearia = semEstoque.and(daMercearia);
Predicate<Produto> disponivel = semEstoque.negate();
```

Cada critério é escrito uma vez, com nome, e os compostos nascem da
combinação, em vez de repetir a condição inteira em cada uso; o critério
com nome também é testável sozinho. `Function` traz o par `andThen` e
`compose`:

```java
Function<Produto, BigDecimal> preco = Produto::preco;
Function<BigDecimal, String> naEtiqueta = valor -> "R$ " + valor;

Function<Produto, String> precoNaEtiqueta = preco.andThen(naEtiqueta);
```

`andThen` executa na ordem em que se lê: primeiro `preco`, depois
`naEtiqueta`. `compose` inverte a leitura, e `naEtiqueta.compose(preco)`
produz exatamente a mesma função, escrita de fora para dentro. `Consumer`
tem o próprio `andThen`, que encadeia duas ações sobre o mesmo valor.

## A forma longa: classe anônima

Antes das lambdas, na versão 8 da linguagem, o comparador da abertura se
escrevia assim:

```java
estoque.sort(new Comparator<Produto>() {
    @Override
    public int compare(Produto a, Produto b) {
        return a.preco().compareTo(b.preco());
    }
});
```

Isso é uma classe anônima: a classe declarada e instanciada na mesma
expressão, sem nome próprio, escrita como um `new` de uma interface ou de
uma classe seguido do corpo entre chaves. O compilador gera para ela uma
classe de verdade, de nome numerado, `Relatorio$1.class`, que aparece na
pasta de saída e nos stack traces, e é assim que se reconhece uma delas
num rastro de erro.

Código anterior a 2014 está cheio dessas cinco linhas de moldura para uma
de conteúdo, e ler a forma longa de relance é o que esta seção compra.
Duas diferenças em relação à lambda sobrevivem e decidem os poucos casos em
que a classe anônima continua sendo a escolha: ela pode implementar uma
interface de mais de um método abstrato, ou estender uma classe, o que a
lambda não faz; e ela tem `this` próprio, referindo o objeto anônimo,
enquanto dentro de uma lambda o `this` continua sendo o do objeto em volta.
Fora esses dois casos, código novo escreve lambda: a mecânica é a mesma, a
grafia é que encolheu.

## Prática

1. Ordene o estoque de quatro jeitos: por nome com a ordem natural, por
   preço com `comparing`, por preço decrescente e por categoria com desempate
   de nome. Imprima cada versão com `forEach` e referência de método.

2. Escreva um método `filtrar(List<Produto> produtos, Predicate<Produto>
   criterio)` que devolva a lista dos aprovados, e use-o três vezes com
   critérios diferentes, incluindo um capturando um teto de preço.

3. Reproduza a armadilha da subtração com os saldos de sinais opostos,
   mostre a ordem errada, e conserte das duas formas. Escreva o teste de
   regressão que teria pegado o defeito.

4. Converta os testes de recusa do capítulo 15 para `assertThrows`, e escreva
   um novo: `ItemDeVenda` com quantidade zero, conferindo também a mensagem,
   com o objeto exceção que `assertThrows` devolve.

5. Fabrique com lambda um `MeioDePagamento` de teste que cobre o dobro, use-o
   no `Caixa` sem criar classe nenhuma, e explique por escrito por que isso
   funciona à luz da definição de interface funcional. Depois reescreva o
   mesmo dublê como classe anônima e compare as duas versões linha a linha.

6. Declare três `Predicate<Produto>` com nome, um por critério, e monte
   com `and`, `or` e `negate` os quatro filtros que o relatório do
   mercadinho pede. Escreva um teste para cada critério isolado e explique
   em uma frase por que testar os compostos passa a ser desnecessário.

7. Escreva `UnaryOperator<BigDecimal>` para o desconto de 5% e
   `BinaryOperator<BigDecimal>` para a soma, e use os dois num laço que
   fecha o dia. Depois monte com `andThen` a função que vai de `Produto`
   até a linha da etiqueta e imprima o cartaz inteiro com `forEach`.

## Ficha do capítulo

| Interface | Método | Papel |
| --- | --- | --- |
| `Predicate<T>` | `test`: T → `boolean` | critério; `removeIf`, filtros |
| `Function<T, R>` | `apply`: T → R | transformação |
| `Consumer<T>` | `accept`: T → nada | ação sobre o valor; `forEach` |
| `Supplier<T>` | `get`: nada → T | fornecimento sob demanda |
| `Comparator<T>` | `compare`: T, T → `int` | ordem; `comparing`, `thenComparing`, `reversed` |
| `BiFunction<T, U, R>` | `apply`: T, U → R | transformação de dois valores |
| `UnaryOperator<T>` | `apply`: T → T | transformação que devolve o mesmo tipo |
| `BinaryOperator<T>` | `apply`: T, T → T | combinação de dois do mesmo tipo; toda soma |

| Termo | Definição |
| --- | --- |
| lambda | função sem nome escrita como expressão: `parâmetros -> corpo` |
| interface funcional | interface com um único método abstrato; o alvo de toda lambda |
| referência de método | `Tipo::metodo`: a lambda que só chamaria um método, sem a cerimônia |
| literal de classe | `Tipo.class`: o objeto que representa o tipo; reina no capítulo 23 |
| captura de variável | a lambda usando variáveis do escopo onde nasceu |
| efetivamente final | variável nunca reatribuída; condição para ser capturada |
| `negate` / `and` / `or` | combinam critérios num `Predicate` composto |
| `andThen` / `compose` | encadeiam funções; a ordem de leitura é a diferença |
| `comparingInt` / `nullsFirst` | chave primitiva sem embrulho / comparador que aceita `null` |
| variantes primitivas | `IntPredicate` e família: o primitivo sem virar objeto |
| classe anônima | classe declarada e instanciada na mesma expressão, sem nome |
