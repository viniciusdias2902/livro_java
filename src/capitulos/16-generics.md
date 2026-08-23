# Generics e type erasure

O capítulo 8 deixou anotado que uma variável `Object` aceita qualquer
objeto, e que a biblioteca padrão usava isso para escrever código que serve
a todos os tipos. O mercadinho tenta o mesmo truque numa prateleira de
capacidade fixa:

```java
class Prateleira {
    private final Object[] itens;
    private int quantidade = 0;

    Prateleira(int capacidade) {
        itens = new Object[capacidade];
    }

    public void guardar(Object item) {
        itens[quantidade] = item;
        quantidade++;
    }

    public Object pegar(int posicao) {
        return itens[posicao];
    }
}

void main() {
    Prateleira docas = new Prateleira(10);
    docas.guardar(new Produto("7891000100103", "Café 500g", new BigDecimal("19.90")));
    docas.guardar("anotação do repositor: conferir validade");
    Produto produto = (Produto) docas.pegar(1);
    IO.println(produto.nome());
}
```

```console
$ java Recebimento.java
Exception in thread "main" java.lang.ClassCastException: class java.lang.String cannot be cast to class Produto
	at Recebimento.main(Recebimento.java:24)
```

A prateleira aceita produto, aceita bilhete, aceita qualquer coisa, porque
`Object` aceita qualquer coisa; e tudo que sai dela sai como `Object`,
obrigando o downcast do capítulo 8 em cada leitura. O programa compila
inteiro e cai na leitura da posição errada, em execução, longe do `guardar`
que plantou o problema. O truque do `Object` tem exatamente esse custo:
o compilador, que passou o livro inteiro pegando engano de tipo, fica cego
dentro da prateleira. Generics é o mecanismo que devolve a visão a ele.

## O parâmetro de tipo

```java
class Prateleira<T> {
    private final Object[] itens;
    private int quantidade = 0;

    Prateleira(int capacidade) {
        itens = new Object[capacidade];
    }

    public void guardar(T item) {
        itens[quantidade] = item;
        quantidade++;
    }

    public T pegar(int posicao) {
        @SuppressWarnings("unchecked")
        T item = (T) itens[posicao];
        return item;
    }
}
```

O `<T>` depois do nome declara um parâmetro de tipo: um nome que representa
um tipo ainda não escolhido, usável dentro da classe onde qualquer tipo
seria usável. É o mesmo movimento do parâmetro de método do capítulo 4,
subido um andar: o método generaliza sobre valores, o parâmetro de tipo
generaliza sobre tipos. Quem escolhe o tipo é quem usa, entre os sinais de
menor e maior, e a escolha se chama argumento de tipo:

```java
Prateleira<Produto> docas = new Prateleira<>(10);
docas.guardar(new Produto("7891000100103", "Café 500g", new BigDecimal("19.90")));
docas.guardar("anotação do repositor");
```

```console
$ javac Recebimento.java
Recebimento.java:5: error: incompatible types: String cannot be converted to Produto
docas.guardar("anotação do repositor");
              ^
```

Com `T` valendo `Produto`, o `guardar` só aceita `Produto`, o bilhete do
repositor morreu em compilação com arquivo e linha, e o `pegar` devolve
`Produto` sem cast nenhum do lado de quem chama. O engano que era queda em
execução virou recusa do compilador, que é a direção de sempre deste livro.
O `<>` vazio do `new` pede a inferência do capítulo 3: o compilador copia o
argumento de tipo da declaração.

Dentro da classe sobrou uma cicatriz honesta: o array interno continua de
`Object`, e o `pegar` faz um cast para `T` que o compilador não consegue
provar, avisando com um alerta de compilação. A anotação
`@SuppressWarnings("unchecked")`, da família do `@Override`, silencia o
alerta naquele ponto, e só é decente quando a classe garante por construção
o que o compilador não vê: aqui, só `T` entra pelo `guardar`, então só `T`
sai. A razão de o compilador não conseguir provar é a seção do apagamento,
logo adiante.

Métodos também generalizam sozinhos, sem a classe inteira ser genérica. Um
método genérico declara o próprio parâmetro de tipo antes do retorno:

```java
static <T> T ultimoDe(T[] itens) {
    return itens[itens.length - 1];
}
```

Chamado com um array de `Produto`, devolve `Produto`; com um array de
`String`, devolve `String`; e o compilador infere o `T` pelo argumento, sem
ninguém escrever o `<>`.

## Type erasure: o tipo que a execução não vê

<div class="previsao">

Duas prateleiras de tipos diferentes, e a pergunta sobre o tipo real delas.
O método `getClass`, herdado de `Object`, devolve o tipo do objeto em
execução:

```java
Prateleira<Produto> estoque = new Prateleira<>(10);
Prateleira<String> avisos = new Prateleira<>(10);
IO.println(estoque.getClass() == avisos.getClass());
```

`true` ou `false`?

</div>

```
true
```

Para a execução, as duas prateleiras têm exatamente o mesmo tipo. Esse é o
type erasure, o apagamento de tipos: os parâmetros e argumentos de tipo
existem apenas para o compilador, que os usa para conferir tudo e depois os
apaga; o bytecode carrega uma `Prateleira` só, com `Object` onde havia `T`.
A consequência prática vem em três formas que aparecem cedo: não existe
`new T(...)` nem `new T[...]`, porque na execução `T` não existe;
`instanceof Prateleira<Produto>` é recusado pelo compilador, porque a
pergunta não teria como ser respondida; e o cast para `T` dentro da classe
gera o alerta da seção anterior, porque vira um cast para `Object` que não
confere nada. A segurança dos generics é integralmente de compilação, o que
não a diminui: é onde este livro sempre quis os erros.

<div class="aprofundamento">

**Por que apagar.** Generics chegaram na versão 5 da linguagem, quase uma
década depois do Java 1.0, e o apagamento foi o preço da compatibilidade: o
bytecode genérico roda em bibliotecas e JVMs que nunca souberam de `T`, e
todo o código anterior seguiu válido. A alternativa, tipos genéricos vivos
em execução, existe em outras linguagens e cobrou delas a migração que o
Java decidiu não cobrar.

</div>

## Invariância

Com tipos parametrizados vem uma regra que surpreende quem chega da
herança: `Prateleira<ProdutoPorPeso>` não é um subtipo de
`Prateleira<Produto>`, ainda que `ProdutoPorPeso` seja um `Produto`. Essa
propriedade se chama invariância: entre tipos genéricos, a relação de
subtipo dos argumentos não se propaga. O motivo é defesa, e o raciocínio
cabe em três linhas: se a atribuição fosse aceita, uma referência
`Prateleira<Produto>` para a prateleira dos queijos deixaria `guardar` um
`Produto` comum ali dentro, e a prateleira dos queijos passaria a conter um
não-queijo, com a bomba armada para o primeiro `pegar` tipado do outro
lado. O compilador recusa a atribuição para não ter que aceitar a
consequência.

<div class="armadilha">

Arrays fizeram a escolha oposta décadas antes, e ela continua na linguagem:

```java
void main() {
    ProdutoPorPeso[] queijos = new ProdutoPorPeso[3];
    Produto[] produtos = queijos;
    produtos[0] = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    IO.println("guardou");
}
```

O programa compila sem um aviso. O que acontece ao rodar?

</div>

```console
$ java Deposito.java
Exception in thread "main" java.lang.ArrayStoreException: Produto
	at Deposito.main(Deposito.java:4)
```

A atribuição de `queijos` para `produtos` compila, porque arrays propagam o
subtipo, e a JVM é obrigada a vigiar cada escrita em execução para impedir o
café na prateleira dos queijos: a vigilância falha o mais tarde possível,
com `ArrayStoreException` no ponto da escrita, que pode estar a um sistema
de distância da atribuição que criou o disfarce. É o mesmo problema que a
invariância dos generics mata em compilação, e a comparação das duas
escolhas é a melhor defesa da regra que surpreende.

## Wildcard: aceitar a família inteira

A invariância protege e atrapalha: um método de relatório que recebe
`Prateleira<Produto>` recusa a prateleira dos queijos, e escrever uma versão
por subtipo seria a duplicação que o capítulo 8 condenou. O curinga resolve:

```java
static BigDecimal valorTotal(Prateleira<? extends Produto> prateleira, int quantidade) {
    BigDecimal total = BigDecimal.ZERO;
    for (int i = 0; i < quantidade; i++) {
        total = total.add(prateleira.pegar(i).preco());
    }
    return total;
}
```

`? extends Produto` lê-se "prateleira de algum tipo que é `Produto`", e o
wildcard, o `?`, é exatamente isso: um argumento de tipo desconhecido, com
um limite declarado. O método aceita `Prateleira<Produto>` e
`Prateleira<ProdutoPorPeso>`, e paga com uma restrição coerente: dá para ler
como `Produto`, e não dá para `guardar` coisa nenhuma, porque o tipo exato
guardável é desconhecido. O espelho para escrita, `? super`, fica registrado
na ficha; no dia a dia, o `? extends` de leitura responde pela maioria
esmagadora dos usos, e o capítulo 17 o traz embutido nas assinaturas que o
mercadinho vai consumir.

## Prática

1. Implemente a `Prateleira<T>` completa, com validação de capacidade e de
   posição, e reproduza as duas versões da abertura: a queda com `Object` e
   a recusa de compilação com generics. Anote as duas mensagens.

2. Escreva um método genérico `trocar(T[] itens, int i, int j)` que inverta
   duas posições de qualquer array, e use-o com produtos e com textos.

3. Reproduza a armadilha do `ArrayStoreException` e depois tente escrever a
   linha equivalente com `Prateleira`. Anote a mensagem do compilador e
   explique por escrito qual dos dois momentos de erro custa mais caro num
   sistema.

4. Prove o apagamento de dois jeitos: a previsão do `getClass` e uma
   tentativa de `instanceof Prateleira<Produto>`. Registre a mensagem do
   compilador da segunda.

5. Escreva `contarBaratos(Prateleira<? extends Produto> p, int quantidade,
   BigDecimal teto)` devolvendo quantos produtos custam menos que o teto,
   usando `compareTo`. Confirme que aceita prateleiras de `Produto` e de
   `ProdutoPorPeso`.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| generics | tipos e métodos parametrizados por tipo, conferidos em compilação |
| parâmetro de tipo | o nome declarado em `<T>`, valendo por um tipo a escolher |
| argumento de tipo | o tipo escolhido no uso: `Prateleira<Produto>` |
| método genérico | método com parâmetro de tipo próprio: `static <T> T ultimoDe(T[])` |
| type erasure | o apagamento: argumentos de tipo existem só para o compilador |
| invariância | `Prateleira<Sub>` não é `Prateleira<Super>`; protege a escrita |
| wildcard | `?`: argumento de tipo desconhecido com limite; `? extends` lê, `? super` escreve |
| `@SuppressWarnings("unchecked")` | silencia o alerta de cast não provável; só com garantia por construção |
