# Coleções: array vs. List, Set, Map

A `Prateleira` do capítulo 16 herda do array a limitação de nascença: a
capacidade é fixada no `new`, e um carrinho de compras não sabe de antemão
quantos itens vai ter. Crescer um array é criar outro maior e copiar tudo, e
esse serviço, junto com dezenas de outros, a biblioteca padrão já presta,
num conjunto de tipos que todo programa Java usa todos os dias:

```java
List<ItemDeVenda> carrinho = new ArrayList<>();
carrinho.add(new ItemDeVenda(cafe, 2));
carrinho.add(new ItemDeVenda(queijo, 1));
IO.println(carrinho.size());
IO.println(carrinho.get(0).subtotal());
```

Este capítulo apresenta as três estruturas que respondem pela quase
totalidade do uso real, `List`, `Set` e `Map`, com o critério de escolha
entre elas. Como cada uma funciona por dentro é assunto de estrutura de
dados, uma disciplina inteira que fica fora deste livro; o que entra aqui é
o que se usa e o que se pergunta em entrevista.

## List e ArrayList

`List` é uma interface, no sentido pleno do capítulo 9: o contrato de uma
sequência de tamanho variável, com posição, e os métodos que a armadilha do
array dispensava para sempre: `add` acrescenta no fim, `get(i)` lê pela
posição, `size()` conta, `remove` tira, `contains` procura usando `equals`.
`ArrayList` é a implementação padrão do contrato: guarda os elementos num
array interno e o troca por um maior quando enche, sozinha. A declaração
segue a lição de programar contra o contrato:

```java
List<ItemDeVenda> carrinho = new ArrayList<>();
```

A variável é do tipo da interface e o `new` escolhe a implementação, no
mesmo desenho do `MeioDePagamento`: o resto do código depende só de `List`,
e trocar a implementação um dia não toca linha nenhuma. O parâmetro de tipo
vem do capítulo 16, e é ele que faz `get` devolver `ItemDeVenda` sem cast e
o compilador recusar qualquer intruso no `add`.

A pergunta de entrevista mora na segunda implementação da ficha:
`LinkedList` guarda os elementos em nós encadeados, cada um apontando para o
seguinte, em vez de num array contíguo. Na teoria, inserir no meio dela é
mais barato; na prática, percorrer nós espalhados pela memória perde de
longe para varrer um array contíguo, e o `get(i)` dela precisa caminhar até
a posição. A resposta honesta, que serve para a entrevista e para o código:
`ArrayList` é a escolha padrão, praticamente sempre, e `LinkedList` é a
resposta de uma pergunta clássica, não uma ferramenta do dia a dia.

## Wrappers e autoboxing

`List<int>` não compila. Parâmetro de tipo aceita só tipo de objeto, e para
cada primitivo do capítulo 3 a biblioteca tem uma classe wrapper que o
embrulha como objeto: `Integer` para `int`, `Long`, `Double`, `Boolean` e
`Character` para os demais. O `Integer.parseInt` do capítulo 5 morava
exatamente nessa classe, e a promessa de apresentar a família vence aqui. A
conversão entre primitivo e wrapper é automática nas duas direções, e se
chama autoboxing:

```java
List<Integer> quantidades = new ArrayList<>();
quantidades.add(3);
int primeira = quantidades.get(0);
```

O `3` entra como `Integer` e sai como `int` sem cerimônia visível, e é fácil
esquecer que wrapper é objeto, com tudo que o capítulo 5 disse sobre
objetos:

<div class="armadilha">

Quatro caixas de leite e um limite de estoque:

```java
void main() {
    Integer contagem = 127;
    Integer limite = 127;
    IO.println(contagem == limite);

    Integer contagemMaior = 128;
    Integer limiteMaior = 128;
    IO.println(contagemMaior == limiteMaior);
}
```

```
true
false
```

O mesmo código, com 127 responde `true` e com 128 responde `false`.

</div>

`==` entre wrappers compara referências, como entre quaisquer objetos, e o
resultado depende de os dois lados serem o mesmo objeto. Para valores
pequenos eles costumam ser, pelo mecanismo do aprofundamento abaixo; de 128
em diante deixam de ser, e a comparação que passou em todos os testes
pequenos erra em produção com os números grandes. A regra é a do capítulo 5,
sem exceção para números: wrapper se compara com `equals`, e
`contagemMaior.equals(limiteMaior)` responde `true` sempre. Um parente dessa
armadilha: um `Integer` nulo atribuído a um `int` explode com
`NullPointerException` na conversão automática, e a linha nem parece tocar
em referência.

<div class="aprofundamento">

**O cache dos wrappers.** A conversão automática de `int` para `Integer`
reaproveita objetos prontos para os valores de −128 a 127, e por isso dois
`127` são o mesmo objeto e dois `128` não. O intervalo pequeno é justamente
o mais usado em teste, o que faz o `==` de wrapper parecer correto até o
primeiro valor grande de verdade.

</div>

## Set e HashSet: sem duplicatas

`Set` é o contrato do conjunto: coleção que recusa duplicata, onde duplicata
é definida pelo `equals`. `HashSet` é a implementação padrão, e o nome
entrega a mecânica: é a estrutura que usa o código de hash do capítulo 10
para achar a vizinhança de um elemento num salto, em vez de comparar com
todos. O estoque do mercadinho não deve ter o mesmo produto duas vezes, e o
`Set` transforma essa regra de disciplina em propriedade da estrutura: o
`add` de um produto igual a um presente devolve `false` e não insere.

O capítulo 10 prometeu mostrar ao vivo o preço de sobrescrever `equals` sem
`hashCode`, e o palco é este:

<div class="armadilha">

Um `Produto` com `equals` correto pelo código de barras e `hashCode`
esquecido, herdado de `Object`:

```java
void main() {
    Set<Produto> estoque = new HashSet<>();
    estoque.add(new Produto("7891000100103", "Café 500g"));
    IO.println(estoque.contains(new Produto("7891000100103", "Café 500g")));
}
```

```
false
```

Os dois objetos são iguais pelo `equals`, o produto está no conjunto, e o
`contains` diz que não.

</div>

O `HashSet` procura pelo hash primeiro: calcula o do produto perguntado,
salta para a vizinhança correspondente e só ali usa `equals`. Com o
`hashCode` herdado, os dois cafés iguais têm hashes de identidade
diferentes, a busca olha a vizinhança errada e o produto some sem sair do
lugar. Pior: por coincidência de vizinhança, uma execução aqui e ali pode
encontrar, e defeito intermitente é a pior espécie de defeito. É a cláusula
do capítulo 10 cobrada pela estrutura que confia nela, e a correção é a de
lá: sobrescreveu `equals`, sobrescreve `hashCode`, sobre os mesmos campos.

## Map e HashMap: de chave para valor

`Map` é o contrato do dicionário: pares de chave e valor, com busca pela
chave. É a estrutura do estoque de verdade, do código de barras para o
produto, e `HashMap` é a implementação padrão, com a mesma mecânica de hash
do `HashSet` aplicada às chaves:

```java
Map<String, Produto> estoque = new HashMap<>();
estoque.put("7891000100103", cafe);
estoque.put("7891000200100", queijo);

Produto achado = estoque.get("7891000100103");
Produto ausente = estoque.get("0000000000000");
IO.println(achado.nome());
IO.println(ausente);
```

```
Café 500g
null
```

`put` grava o par, sobrescrevendo o valor se a chave já existia, e `get`
devolve o valor ou `null` quando a chave não está lá: é o reencontro
marcado no capítulo 5, a busca que pode legitimamente não ter resposta.
Consultar antes com `containsKey`, ou usar `getOrDefault(chave, valorPadrao)`,
evita o `NullPointerException` de quem esquece o caso ausente. O idioma de
contagem, presente em todo sistema e em toda entrevista, junta as duas
pontas:

```java
Map<Categoria, Integer> vendasPorCategoria = new HashMap<>();
for (ItemDeVenda item : itensDoDia) {
    Categoria categoria = item.produto().categoria();
    int atual = vendasPorCategoria.getOrDefault(categoria, 0);
    vendasPorCategoria.put(categoria, atual + item.quantidade());
}
```

Percorrer um `Map` usa `keySet()`, o conjunto das chaves, ou `entrySet()`,
os pares inteiros, ambos aceitos pelo for-each.

## Ordem de iteração

<div class="previsao">

As vendas do dia entram no mapa na ordem em que aconteceram:

```java
Map<String, Integer> vendas = new HashMap<>();
vendas.put("Café 500g", 3);
vendas.put("Arroz 5kg", 1);
vendas.put("Sabão em pó", 2);
vendas.put("Queijo minas", 4);
for (String nome : vendas.keySet()) {
    IO.println(nome + ": " + vendas.get(nome));
}
```

Em que ordem os quatro produtos saem?

</div>

```
Arroz 5kg: 1
Queijo minas: 4
Café 500g: 3
Sabão em pó: 2
```

Em ordem nenhuma que se reconheça: nem a de inserção, nem a alfabética. A
ordem de iteração de um `HashMap` é consequência dos hashes das chaves, um
detalhe interno sem promessa nenhuma, que pode mudar entre execuções e
versões. Relatório que depende da ordem de um `HashMap` é bug agendado, e a
regra é declarar a ordem quando ela for requisito. `TreeMap` é a
implementação que mantém as chaves ordenadas, e a ordem vem de `Comparable`:
a interface de quem sabe se comparar com os da própria espécie, com um único
método, `compareTo`, devolvendo negativo, zero ou positivo, exatamente o
protocolo que o `BigDecimal` usa desde o capítulo 7. `String` e os wrappers
já a implementam, e trocar `new HashMap<>()` por `new TreeMap<>()` na
previsão faria os produtos saírem em ordem alfabética. A resposta de
entrevista, nos mesmos moldes da de `List`: `HashMap` por padrão, pela
busca em um salto; `TreeMap` quando a ordem das chaves é requisito do
problema, pagando a busca mais lenta.

Um tipo nosso entra no `TreeMap` implementando a interface:

```java
public class Produto implements Comparable<Produto> {
    @Override
    public int compareTo(Produto outro) {
        return nome.compareTo(outro.nome);
    }
}
```

E quando a ordem desejada não é a natural do tipo, ou o tipo não tem
nenhuma, o capítulo 18 traz a peça que falta.

## Coleções imutáveis

As três interfaces têm fábricas de exemplares que nascem prontos e não
mudam:

```java
List<String> diasDeFeira = List.of("terça", "sexta");
Map<String, Integer> corredores = Map.of("MERCEARIA", 3, "HORTIFRUTI", 1);
```

Uma coleção imutável recusa `add`, `remove` e `put` com um erro de execução
imediato e barulhento, `UnsupportedOperationException`, e essa é a graça:
ela transforma "ninguém deveria mexer nisto" em "ninguém consegue". Os usos
que pagam a passagem: constantes de domínio, como os dias de feira, e
retorno defensivo, devolvendo `List.copyOf(itens)` para quem pede a lista
interna, em vez da referência viva que a armadilha do capítulo 5 mostrou os
outros alterarem.

Resta um nome da ficha: o iterador é o objeto que percorre uma coleção,
entregando um elemento por vez, e é ele que o for-each usa por baixo em
tudo que este capítulo mostrou. O encontro direto com ele costuma acontecer
de um jeito específico: alterar a coleção no meio de um for-each derruba o
programa com `ConcurrentModificationException`, um erro barulhento de
propósito, porque a alternativa seria um percurso corrompido em silêncio. A
remoção por critério tem forma própria e curta no capítulo 18; até lá, a
regra é não remover de dentro do próprio for-each.

## Prática

1. Refaça o `Carrinho` do capítulo 8 sobre `List<ItemDeVenda>`, com `total()`
   em `BigDecimal`, e aposente os arrays paralelos de vez, como o capítulo
   11 prometeu.

2. Reproduza a armadilha dos wrappers com os valores 127 e 128, conserte com
   `equals` e escreva a regra em uma frase. Depois provoque o
   `NullPointerException` do unboxing com um `Integer` nulo.

3. Reproduza o desaparecimento no `HashSet` com um `Produto` sem `hashCode`,
   conserte sobrescrevendo, e rode dez vezes cada versão anotando os
   resultados. Explique por escrito por que a versão errada poderia passar
   num teste.

4. Monte o estoque como `Map<String, Produto>` com cinco produtos, escreva a
   consulta que responde "existe? qual o preço?" sem risco de
   `NullPointerException`, e o relatório de contagem por categoria com
   `getOrDefault`.

5. Imprima o mesmo estoque com `HashMap` e com `TreeMap`, compare as ordens,
   e implemente `Comparable<Produto>` por preço em vez de nome, decidindo
   com `compareTo` de `BigDecimal`. Anote o que muda na saída do `TreeMap`.

6. Escreva um método que receba `List<ItemDeVenda>` e devolva uma versão
   imutável dela, e prove com uma tentativa de `add` que a devolução é
   segura.

## Ficha do capítulo

| Chamada | O que faz |
| --- | --- |
| `add` / `get(i)` / `size()` / `remove` / `contains` | o essencial de `List` |
| `put` / `get` / `getOrDefault` / `containsKey` | o essencial de `Map`; `get` ausente devolve `null` |
| `keySet()` / `entrySet()` | as chaves / os pares, para percorrer |
| `List.of`, `Set.of`, `Map.of`, `List.copyOf` | coleções imutáveis prontas |

| Termo | Definição |
| --- | --- |
| `Collection` | o contrato-mãe de `List` e `Set`; `Map` é família própria |
| `List` / `ArrayList` | sequência com posição / implementação padrão, sobre array que cresce |
| `LinkedList` | nós encadeados; resposta de entrevista, raramente a escolha certa |
| `Set` / `HashSet` | conjunto sem duplicatas (por `equals`) / implementação por hash |
| `Map` / `HashMap` | pares chave-valor / implementação por hash, sem ordem prometida |
| `TreeMap` | chaves mantidas em ordem, via `Comparable` |
| `Comparable` / `compareTo` | a ordem natural de um tipo: negativo, zero, positivo |
| classe wrapper | o primitivo como objeto: `Integer`, `Double` e irmãos |
| autoboxing | conversão automática primitivo↔wrapper; `==` continua proibido |
| iterador | o objeto que percorre a coleção; motor do for-each |
| ordem de iteração | `HashMap`/`HashSet` não prometem nenhuma; `TreeMap` promete a das chaves |
| coleção imutável | nasce pronta e recusa alteração com erro imediato |
