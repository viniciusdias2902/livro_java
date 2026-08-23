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

O trecho `(a, b) -> a.preco().compareTo(b.preco())` é uma lambda: uma função
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

O `MeioDePagamento` do capítulo 9 tem um único método abstrato, portanto é
uma interface funcional sem saber, e um teste do capítulo 15 pode fabricar
um meio de pagamento de mentira numa linha:

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
é valor que carrega código adormecido, e quem decide o momento de acordá-lo
é quem a recebe; essa inversão, modesta aqui, é o motor central do capítulo
19.

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
nada além da chamada. Há referência para método de instância, como essa,
para método estático, `Integer::parseInt`, e para um método de um objeto já
existente, `IO::println` sendo o exemplo que o `forEach` adora.

Parente visual dessa sintaxe, e coisa completamente diferente, é o literal
de classe: `Produto.class`, o objeto que representa o próprio tipo em
execução. Ele estreia de verdade duas seções adiante e reina no capítulo 23.

<div class="armadilha">

Um comparador de estoque escrito com a esperteza clássica de subtrair:

```java
List<Produto> porEstoque = new ArrayList<>(estoque);
porEstoque.sort((a, b) -> a.estoque() - b.estoque());
```

Para estoques comuns, a ordem sai perfeita em todos os testes. O mercadinho
herda o galpão do atacadista, com contagens gigantes, e o relatório passa a
sair embaralhado, sem erro nenhum. Por quê?

</div>

A subtração devolve o sinal certo enquanto não estoura: com `a.estoque()`
muito negativo ou `b.estoque()` gigante, `a - b` sofre o overflow do
capítulo 3, dá a volta e devolve o sinal errado, e o `sort` ordena errado
com a maior convicção. É a armadilha do overflow vestida de esperteza, e
some do código com qualquer uma das duas formas honestas:
`Integer.compare(a.estoque(), b.estoque())`, que compara sem subtrair, ou
`Comparator.comparingInt(Produto::estoque)`, que faz o mesmo por dentro.

## Captura, e o efetivamente final

Uma lambda enxerga as variáveis do escopo onde nasceu, e usá-las tem nome:
captura de variável.

```java
BigDecimal teto = new BigDecimal("10.00");
estoque.removeIf(p -> p.preco().compareTo(teto) > 0);
```

O `teto` não é parâmetro da lambda: veio capturado do método em volta. A
regra que governa a captura é a segunda definição do capítulo: uma variável
local só pode ser capturada se for efetivamente final, isto é, se nunca for
reatribuída depois de receber valor, tenha ou não a palavra `final` escrita.
O compilador recusa a captura de variável que muda:

```console
$ javac Relatorio.java
Relatorio.java:9: error: local variables referenced from a lambda expression must be effectively final
        contador = contador + 1;
        ^
```

O motivo é o tempo: a lambda pode rodar muito depois, quando o método que a
criou já retornou e as variáveis locais dele já morreram com a pilha do
capítulo 4. O que a lambda captura é o valor, congelado; permitir
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

<div class="aprofundamento">

**A forma longa.** Antes das lambdas, versão 8, o mesmo comparador se
escrevia criando no ato uma classe sem nome que implementa a interface, a
classe anônima: `new Comparator<Produto>() { public int compare(...) {...} }`,
cinco linhas de moldura para uma de conteúdo. Código anterior a 2014 está
cheio delas, e o apêndice de legado ensina a lê-las de relance; a lambda não
mudou o mecanismo, mudou a grafia.

</div>

## Prática

1. Ordene o estoque de quatro jeitos: por nome com a ordem natural, por
   preço com `comparing`, por preço decrescente e por categoria com desempate
   de nome. Imprima cada versão com `forEach` e referência de método.

2. Escreva um método `filtrar(List<Produto> produtos, Predicate<Produto>
   criterio)` que devolva a lista dos aprovados, e use-o três vezes com
   critérios diferentes, incluindo um capturando um teto de preço.

3. Reproduza a armadilha da subtração com valores que estouram, mostre a
   ordem errada, e conserte das duas formas. Escreva o teste de regressão
   do capítulo 15 que teria pegado o defeito.

4. Converta os testes de recusa do capítulo 15 para `assertThrows`, e escreva
   um novo: `ItemDeVenda` com quantidade zero, conferindo também a mensagem,
   com o objeto exceção que `assertThrows` devolve.

5. Fabrique com lambda um `MeioDePagamento` de teste que cobre o dobro, use-o
   no `Caixa` sem criar classe nenhuma, e explique por escrito por que isso
   funciona à luz da definição de interface funcional.

## Ficha do capítulo

| Interface | Método | Papel |
| --- | --- | --- |
| `Predicate<T>` | `test`: T → `boolean` | critério; `removeIf`, filtros |
| `Function<T, R>` | `apply`: T → R | transformação |
| `Consumer<T>` | `accept`: T → nada | ação sobre o valor; `forEach` |
| `Supplier<T>` | `get`: nada → T | fornecimento sob demanda |
| `Comparator<T>` | `compare`: T, T → `int` | ordem; `comparing`, `thenComparing`, `reversed` |

| Termo | Definição |
| --- | --- |
| lambda | função sem nome escrita como expressão: `parâmetros -> corpo` |
| interface funcional | interface com um único método abstrato; o alvo de toda lambda |
| referência de método | `Tipo::metodo`: a lambda que só chamaria um método, sem a cerimônia |
| literal de classe | `Tipo.class`: o objeto que representa o tipo; reina no capítulo 23 |
| captura de variável | a lambda usando variáveis do escopo onde nasceu |
| efetivamente final | variável nunca reatribuída; condição para ser capturada |
