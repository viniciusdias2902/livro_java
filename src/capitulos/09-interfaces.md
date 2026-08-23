# Interfaces e abstração

O caixa do mercadinho aceita dinheiro, cartão e fiado, e cada forma altera o
valor final da compra de um jeito: no dinheiro o mercadinho dá 5% de
desconto, no cartão repassa a taxa da máquina, no fiado o valor apenas vai
para a caderneta. A herança do capítulo 8 não modela isso bem, e vale tentar para ver a
recusa. Cartão não é um caso de dinheiro, então `Cartao extends Dinheiro`
mente sobre o domínio e herda um desconto que não existe no cartão. Uma
superclasse `Pagamento` com o cálculo dentro também não fecha, porque não há
cálculo comum para herdar: cada forma tem a própria aritmética e nenhum
campo compartilhado. A herança serve quando há implementação comum e
parentesco genuíno; aqui não há nem um nem outro. O que os três compartilham
é só uma promessa: dado o valor da compra, cada um sabe dizer o valor
final. Promessa sem implementação comum tem uma
construção própria na linguagem:

```java
interface MeioDePagamento {
    BigDecimal valorFinal(BigDecimal compra);
}

class Dinheiro implements MeioDePagamento {
    @Override
    public BigDecimal valorFinal(BigDecimal compra) {
        return compra.multiply(new BigDecimal("0.95"));
    }
}

class Cartao implements MeioDePagamento {
    @Override
    public BigDecimal valorFinal(BigDecimal compra) {
        return compra.multiply(new BigDecimal("1.02"));
    }
}
```

## interface, implements e o contrato

Uma interface declara um conjunto de métodos que um tipo promete oferecer,
sem dizer como: só as assinaturas e os tipos de retorno, sem corpo. Os
métodos de uma interface são `public` por definição, e uma classe adere à
promessa com `implements`, ficando obrigada pelo compilador a dar corpo a
cada método declarado; esquecer um é erro de compilação, não descuido
possível. Ao contrário do `extends`, que aceita uma superclasse só, uma
classe pode implementar quantas interfaces fizerem sentido, porque promessas
não conflitam como implementações conflitariam. Cada interface é um papel, e
um mesmo tipo pode exercer vários: o `ProdutoPorPeso` do capítulo 8 pode
implementar um contrato `Pesavel` sem deixar de ser um `Produto`, e cada
trecho do sistema o enxerga pelo papel que lhe interessa.

Uma interface também é um tipo, com tudo que isso implica desde o capítulo
3: existe variável do tipo `MeioDePagamento`, parâmetro, retorno e array
desse tipo, e guardar um `Dinheiro` numa variável assim é o upcast do
capítulo 8, sempre seguro. A única coisa que não existe é
`new MeioDePagamento()`, porque não há implementação para instanciar; toda
referência de tipo interface aponta para um objeto de alguma classe
concreta.

A palavra para o que a interface captura é contrato: a promessa observável
de um tipo, o que se pode chamar e o que cada chamada garante, separada de
qualquer detalhe de como se cumpre. `MeioDePagamento` é um contrato de uma
cláusula: entra o valor da compra, sai o valor final. `Dinheiro` e `Cartao`
são dois cumpridores com aritméticas próprias, e o resto do sistema não tem
por que saber qual é qual.

O contrato obriga os dois lados. Quem chama só pode contar com o que a
interface promete, e nada do que souber por fora; quem implementa deve
honrar a promessa por inteiro, inclusive as partes que o compilador não
confere. O compilador garante a assinatura, mas uma implementação que
devolvesse `null` como valor final estaria tecnicamente compilando e
concretamente quebrando o contrato, e derrubaria o caixa com o
`NullPointerException` do capítulo 5 longe da causa. Contrato bem escrito
diz também essas cláusulas de comportamento, nem que seja em comentário
sobre a interface, e o capítulo 15 mostra como transformá-las em verificação
executável.

## Programar contra o contrato

O ganho aparece no caixa:

```java
class Caixa {
    public BigDecimal fechar(BigDecimal compra, MeioDePagamento meio) {
        return meio.valorFinal(compra);
    }
}
```

O parâmetro é do tipo da interface, e o polimorfismo do capítulo 8 vale
igual para ela: a chamada `meio.valorFinal(compra)` é despachada para a
classe do objeto real. O `Caixa` compila sem conhecer `Dinheiro` nem
`Cartao`, e é essa ignorância deliberada que tem nome: acoplamento é o grau
em que um trecho de código depende dos detalhes de outro, e programar contra
a interface deixa o acoplamento no mínimo necessário. Quando o mercadinho
adotar Pix, a classe nova implementa `MeioDePagamento` e o `Caixa` a atende
sem uma linha editada, no mesmo espírito do carrinho do capítulo 8.

O caminho oposto é o que o capítulo 8 chamou de cheiro, e vale ver o custo
dele por extenso:

<div class="armadilha">

Um caixa escrito antes das interfaces, decidindo por tipo:

```java
public BigDecimal fechar(BigDecimal compra, Object meio) {
    if (meio instanceof Cartao) {
        return compra.multiply(new BigDecimal("1.02"));
    }
    return compra.multiply(new BigDecimal("0.95"));
}
```

O mercadinho adota Pix e alguém escreve a classe `Pix`. O programa compila e
todas as vendas seguem passando. O que acontece com uma compra de R$ 100,00
paga em Pix?

</div>

Sai por R$ 95,00. O `Pix` não casa com o `instanceof` de `Cartao`, escorrega
para o ramo final, e leva o desconto que era do dinheiro. Nenhum erro em
nenhum momento: o prejuízo de 5% em cada venda no Pix aparece no fechamento
do mês, longe da causa. A cascata de tipos exige que cada tipo novo lembre
de se apresentar em cada cascata do sistema; o contrato inverte a
obrigação, porque quem chega já traz o próprio comportamento. É a mesma
lição do polimorfismo, agora sem exigir parentesco de classe nenhum.

## Método default

Contrato publicado é compromisso: no dia em que `MeioDePagamento` ganhar um
método novo, toda classe que o implementa quebra de uma vez, com um erro de
compilação por implementador. Para evoluir sem quebrar, uma interface pode
dar corpo padrão a um método, com a palavra `default`:

```java
interface MeioDePagamento {
    BigDecimal valorFinal(BigDecimal compra);

    default String nomeNoRecibo() {
        return "Pagamento";
    }
}

class Pix implements MeioDePagamento {
    @Override
    public BigDecimal valorFinal(BigDecimal compra) {
        return compra;
    }

    @Override
    public String nomeNoRecibo() {
        return "Pix";
    }
}
```

<div class="previsao">

`Dinheiro` e `Cartao` continuam como estavam, sem saber que `nomeNoRecibo`
existe. O trecho abaixo roda:

```java
MeioDePagamento[] meios = { new Pix(), new Dinheiro() };
for (MeioDePagamento meio : meios) {
    IO.println(meio.nomeNoRecibo());
}
```

O que aparece para cada um dos dois?

</div>

```
Pix
Pagamento
```

Quem sobrescreveu responde com a própria versão; quem não sobrescreveu
responde com o corpo `default`, e continua compilando como antes da
mudança. O método default existe para isso, evolução de contrato publicado,
e não para virar depósito de lógica: interface que acumula corpos está
fazendo o trabalho da construção da próxima seção.

## Classe abstrata

Entre a interface, que não carrega implementação de estado nenhuma, e a
classe concreta, que carrega tudo, existe o meio-termo. Os cartões do
mercadinho, crédito e débito, têm taxas diferentes, mas o cálculo é o mesmo
e o campo da taxa também; só a descrição de cada um varia. Uma classe
abstrata guarda esse miolo comum:

```java
abstract class CartaoBase implements MeioDePagamento {
    private final BigDecimal taxa;

    CartaoBase(BigDecimal taxa) {
        this.taxa = taxa;
    }

    @Override
    public final BigDecimal valorFinal(BigDecimal compra) {
        return compra.multiply(BigDecimal.ONE.add(taxa));
    }

    public abstract String bandeira();
}

class CartaoDeCredito extends CartaoBase {
    CartaoDeCredito() {
        super(new BigDecimal("0.02"));
    }

    @Override
    public String bandeira() {
        return "crédito";
    }
}
```

Classe abstrata é a classe que não pode ser instanciada: `new CartaoBase()`
é erro de compilação, porque ela existe para ser estendida. Ela pode ter
tudo que classe tem, campos, construtores e métodos concretos, e mais uma
coisa que classe concreta não pode: o método abstrato, declarado sem corpo,
como `bandeira()`, que obriga cada subclasse a fornecer a própria versão.
`BigDecimal.ONE`, de passagem, é a constante 1 da própria classe, irmã do
`ZERO` do capítulo 8, e o `final` em `valorFinal` usa a regra do capítulo 8
para congelar o cálculo que as subclasses não devem alterar.

A régua para escolher entre as três construções cabe em três linhas.
Interface quando o que existe em comum é só a promessa: é o caso de
`MeioDePagamento`, e é por onde se começa. Classe abstrata quando
implementações irmãs compartilham código e estado de verdade, como os
cartões. Classe concreta para o que se instancia. Na prática as três
convivem: a interface no topo, uma abstrata opcional no meio onde a
duplicação doeu, concretas embaixo.

<div class="aprofundamento">

**Por que o default existe.** Interfaces não aceitavam corpo nenhum nas
primeiras versões de Java, e evoluir as interfaces centrais da biblioteca
padrão era impossível sem quebrar o mundo inteiro. O método default entrou
na versão 8 exatamente para isso, e boa parte dos métodos que os capítulos
17 a 19 usam chegou por essa porta, em interfaces que existiam desde os anos
noventa.

</div>

## Prática

1. Implemente `MeioDePagamento` com `Dinheiro`, `Cartao` e `Pix`, o `Caixa`
   programado contra a interface e uma volta de impressões que feche a mesma
   compra pelos três meios, exibindo nome do recibo e valor final.

2. Reproduza a armadilha da cascata: escreva a versão com `instanceof`,
   acrescente o `Pix` sem tocar nela e documente o valor errado. Depois
   escreva em um parágrafo onde exatamente a versão com interface elimina a
   categoria do erro, e não só o caso.

3. Acrescente `CartaoDeDebito` com taxa de 1% à hierarquia de `CartaoBase`,
   sem duplicar o cálculo. Explique por escrito por que `valorFinal` é
   `final` na base e o que uma subclasse ganharia ou quebraria se pudesse
   sobrescrevê-lo.

4. Declare um método novo em `MeioDePagamento` sem corpo `default`, anote
   quantos erros de compilação aparecem e onde; depois transforme-o em
   `default` e observe o que muda. Registre a regra que você tirou disso.

5. Modele com interface um segundo contrato do mercadinho: `Pesavel`, com um
   método que devolve o peso em gramas, implementado por `ProdutoPorPeso` e
   por uma nova classe `CestaBasica`. Escreva um método que receba um array
   de `Pesavel` e some o peso, sem `instanceof`.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| interface | conjunto de métodos que um tipo promete, sem implementação |
| `implements` | adesão de uma classe a uma interface; corpo obrigatório para cada método |
| contrato | a promessa observável de um tipo, separada do como |
| acoplamento | grau em que um trecho depende dos detalhes de outro |
| método default | método de interface com corpo padrão; permite evoluir contrato publicado |
| classe abstrata | classe não instanciável, feita para ser estendida; aceita campos e código |
| método abstrato | método sem corpo em classe abstrata; sobrescrita obrigatória |
