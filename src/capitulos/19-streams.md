# Streams e Optional

O relatório de reposição do mercadinho quer os nomes dos produtos de
mercearia com estoque abaixo de dez, em ordem alfabética. Com os capítulos
17 e 18, o laço sai assim:

```java
List<String> reposicao = new ArrayList<>();
for (Produto p : estoque) {
    if (p.categoria() == Categoria.MERCEARIA && p.estoque() < 10) {
        reposicao.add(p.nome());
    }
}
reposicao.sort(Comparator.naturalOrder());
```

Funciona, e mistura três assuntos numa estrutura só: o critério, a
transformação de produto em nome e a coleta do resultado, todos dentro do
mesmo laço, com uma lista intermediária mutável de apoio. A biblioteca
padrão oferece uma segunda forma de escrever exatamente isso, em que cada
assunto vira uma etapa nomeada:

```java
List<String> reposicao = estoque.stream()
        .filter(p -> p.categoria() == Categoria.MERCEARIA)
        .filter(p -> p.estoque() < 10)
        .map(Produto::nome)
        .sorted()
        .toList();
```

## O que é um stream

Um stream é um fluxo de valores processado por uma cadeia de operações
declaradas, criado a partir de uma fonte, tipicamente uma coleção, pelo
método `stream()`. Ele não é uma coleção nova: não guarda elemento nenhum,
não substitui a lista de origem e serve para uma única passagem, do começo
ao fim. A cadeia inteira se chama pipeline, e tem anatomia fixa: uma fonte,
zero ou mais operações intermediárias e exatamente uma operação terminal.

Uma operação intermediária transforma o fluxo e devolve outro stream, o que
permite emendar a próxima: `filter` deixa passar quem cumpre o critério, um
`Predicate` do capítulo 18; `map` transforma cada elemento com uma
`Function`; `sorted` ordena, com a ordem natural ou com um `Comparator`;
`limit(n)` corta o fluxo nos primeiros `n`. Uma operação terminal encerra o
pipeline produzindo o resultado de fato: `toList()` coleta numa lista
imutável, `count()` conta, `forEach` consome um a um. A leitura do pipeline
é a razão de ele existir: cada linha diz uma coisa, na ordem em que
acontecem, e o critério, a transformação e a coleta pararam de dividir o
mesmo bloco de chaves.

## Avaliação preguiçosa

<div class="previsao">

Um pipeline declarado com uma impressão espiã dentro do critério:

```java
void main() {
    List<Integer> estoques = List.of(3, 40, 7, 25);
    estoques.stream()
            .filter(e -> {
                IO.println("avaliando " + e);
                return e < 10;
            });
    IO.println("relatório pronto");
}
```

Quantas linhas "avaliando" aparecem, e onde entra o "relatório pronto"?

</div>

```
relatório pronto
```

Nenhuma. O pipeline foi declarado e nunca executado, porque não tem operação
terminal: as intermediárias são preguiçosas, e essa é a avaliação
preguiçosa, o mesmo código adormecido do `Supplier` do capítulo 18, agora em
cadeia: declarar as etapas não processa nada, e é a operação terminal que
liga o motor e puxa os elementos através das etapas. Acrescentar `.count()`
ao pipeline acima faria as quatro linhas "avaliando" aparecerem antes do
"relatório pronto". As consequências práticas: efeito colateral dentro de
intermediária é promessa de confusão, porque roda quando e se o terminal
mandar; e um pipeline sem terminal é um engano silencioso que o compilador
aceita de bom grado. Stream sem terminal não faz nada, e essa frase vale
memorizada.

## reduce, e o dinheiro nos streams

Somar é o exemplo canônico de agregação, e agregação em stream tem nome:
`reduce` combina todos os elementos num único resultado, a partir de um
valor inicial e de uma operação de dois em um:

```java
BigDecimal totalDoDia = vendas.stream()
        .map(ItemDeVenda::subtotal)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
```

Lê-se: comece do zero e vá somando. O acumulador que o capítulo 18 proibiu
de capturar aparece aqui do jeito certo: o pipeline carrega o acumulado por
dentro, sem variável externa mutável.

<div class="armadilha">

O mesmo total, escrito por quem viu que existe uma soma pronta para números:

```java
double totalDoDia = vendas.stream()
        .mapToDouble(item -> item.subtotal().doubleValue())
        .sum();
IO.println(totalDoDia);
```

Com três vendas de dez centavos, o fechamento imprime:

```
0.30000000000000004
```

</div>

O atalho converteu cada `BigDecimal` para `double` no meio do caminho, e o
capítulo 3 voltou inteiro: um décimo não tem escrita binária exata, a soma
acumula as sobras, e o caixa fecha com diferença de fração de centavo que
ninguém rastreia. O `mapToDouble` e o `sum` existem e servem para medidas;
dinheiro atravessa o pipeline como `BigDecimal` do começo ao fim, com o
`reduce` somando pelo método `add`. É a mesma regra de sempre, cobrada num
lugar novo, e ela cai em teste porque a conversão escondida no meio do
pipeline é fácil de não ver em revisão.

## Collectors: agrupar e resumir

`toList()` é a coleta simples; as coletas com forma vivem na classe
`Collectors`, uma fábrica de coletores para os resumos que relatórios
pedem. O agrupamento é o mais usado deles:

```java
Map<Categoria, List<Produto>> porCategoria = estoque.stream()
        .collect(Collectors.groupingBy(Produto::categoria));

Map<Categoria, Long> contagemPorCategoria = estoque.stream()
        .collect(Collectors.groupingBy(Produto::categoria, Collectors.counting()));
```

`groupingBy` monta um `Map` cujas chaves saem da função dada e cujos valores
são os elementos de cada grupo; a segunda forma troca a lista de cada grupo
por outro resumo, aqui a contagem. O relatório de vendas por categoria, que
o capítulo 17 montou com `getOrDefault` num laço, encolhe para uma
expressão, e as duas versões seguem corretas: o pipeline não aposenta o
laço, dá a ele um concorrente mais legível quando o assunto é transformar e
resumir coleções.

## Optional: a ausência com tipo

Buscar o produto mais barato da mercearia tem um caso que o capítulo 5
ensinou a temer: a mercearia pode estar vazia. O stream não devolve `null`
nem lança erro; devolve o tipo feito para isso:

```java
Optional<Produto> maisBarato = estoque.stream()
        .filter(p -> p.categoria() == Categoria.MERCEARIA)
        .min(Comparator.comparing(Produto::preco));
```

`Optional<T>` é um recipiente de zero ou um valor: a ausência deixa de ser
um `null` à espreita e vira parte do tipo, que o compilador obriga a
encarar. O que se faz com ele é sempre uma das poucas formas:

```java
Produto escolhido = maisBarato.orElse(produtoPadrao);
Produto exigido = maisBarato.orElseThrow(
        () -> new IllegalStateException("Mercearia sem produtos."));
maisBarato.ifPresent(p -> IO.println("Oferta: " + p.nome()));
```

`orElse` entrega o valor ou o substituto; `orElseThrow` entrega ou lança a
exceção do `Supplier`, para quando a ausência é violação; `ifPresent` age só
na presença, com um `Consumer`; e `map` transforma o conteúdo sem abri-lo,
devolvendo outro `Optional`. `IllegalStateException`, prima da
`IllegalArgumentException` do capítulo 7, sinaliza estado inválido em vez de
argumento inválido. Existe também o método `get`, que lança quando vazio, e
a regra sobre ele é curta: quem usa `get` sem conferir presença reinventou o
`NullPointerException` com mais letras.

As convenções de uso valem tanto quanto a classe. `Optional` nasceu para
tipo de retorno, dizendo "esta busca pode não encontrar", como o
`findFirst` e o `min` dos streams dizem; campo `Optional` e parâmetro
`Optional` são desenho torto, porque a pergunta certa nesses lugares é
outra, e a resposta de entrevista resume: `Optional` documenta ausência
possível no retorno, e o resto continua sendo modelagem.

<div class="aprofundamento">

**Streams paralelos.** Trocar `stream()` por `parallelStream()` divide o
trabalho entre os processadores da máquina, e é tentador como toda linha
única. O custo escondido é o assunto inteiro do capítulo 22: dividir
trabalho cria os problemas de coordenação de lá, e pipeline paralelo com
efeito colateral é receita de resultado errado intermitente. Até lá, e na
maior parte do código real, o stream comum basta.

</div>

## Prática

1. Reescreva com pipeline os dois relatórios do capítulo 17: contagem de
   vendas por categoria e a versão agrupada com os produtos de cada uma.
   Compare linha a linha com as versões de laço.

2. Reproduza a previsão da preguiça, depois acrescente `.count()` e anote a
   ordem exata das impressões. Escreva em uma frase o papel da operação
   terminal.

3. Reproduza a armadilha do `mapToDouble` com três vendas de R$ 0,10, mostre
   a diferença, e escreva o teste de regressão com `reduce` e `compareTo`
   que a impede de voltar.

4. Escreva `maisCaroDaCategoria(List<Produto> estoque, Categoria c)`
   devolvendo `Optional<Produto>`, e trate a ausência das três formas:
   substituto, exceção e ação condicional. Decida por escrito qual das três
   o relatório do mercadinho deveria usar.

5. Monte o "top 3 mais vendidos": some as quantidades por produto num
   `Map`, e produza a lista dos três maiores com um pipeline sobre
   `entrySet()`, usando `sorted` com `Comparator` e `limit`.

## Ficha do capítulo

| Operação | Tipo | O que faz |
| --- | --- | --- |
| `filter(Predicate)` | intermediária | deixa passar quem cumpre o critério |
| `map(Function)` | intermediária | transforma cada elemento |
| `sorted()` / `sorted(Comparator)` | intermediária | ordena o fluxo |
| `limit(n)` | intermediária | corta nos primeiros `n` |
| `toList()` / `count()` / `forEach` | terminal | coleta, conta, consome |
| `reduce(inicial, operação)` | terminal | agrega tudo num resultado |
| `collect(Collectors.groupingBy(...))` | terminal | agrupa num `Map`, com resumo opcional |
| `min` / `max` / `findFirst` | terminal | devolvem `Optional` |

| Termo | Definição |
| --- | --- |
| stream | fluxo de valores processado por uma cadeia declarada; uma passagem só |
| operação intermediária | transforma o fluxo e devolve stream; preguiçosa |
| operação terminal | encerra o pipeline e produz o resultado; liga o motor |
| avaliação preguiçosa | nada roda até a terminal puxar os elementos |
| `Collectors` | fábrica de coletas com forma: agrupar, contar, resumir |
| `reduce` | agregação: valor inicial mais operação de dois em um |
| `Optional` | recipiente de zero ou um valor; a ausência como parte do tipo |
