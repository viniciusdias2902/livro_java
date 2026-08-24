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
classe pode implementar quantas interfaces fizerem sentido: duas promessas
de mesma assinatura pedem a mesma coisa, e a ressalva dos métodos com corpo
aparece na seção do default. Cada interface é um papel, e
um mesmo tipo pode exercer vários: o `ProdutoPorPeso` do capítulo 8 pode
implementar um contrato `Pesavel` sem deixar de ser um `Produto`, e cada
trecho do sistema o enxerga pelo papel que lhe interessa.

Uma interface também é um tipo, com tudo que isso implica desde o capítulo
3: existe variável do tipo `MeioDePagamento`, parâmetro, retorno e array
desse tipo, e guardar um `Dinheiro` numa variável assim é um upcast,
sempre seguro. A única coisa que não existe é
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
concretamente quebrando o contrato, e derrubaria o caixa com um
`NullPointerException` longe da causa. Contrato bem escrito
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

O parâmetro é do tipo da interface, e o polimorfismo vale igual para ela: a chamada `meio.valorFinal(compra)` é despachada para a
classe do objeto real. O `Caixa` compila sem conhecer `Dinheiro` nem
`Cartao`, e é essa ignorância deliberada que tem nome: acoplamento é o grau
em que um trecho de código depende dos detalhes de outro, e programar contra
a interface deixa o acoplamento no mínimo necessário. Quando o mercadinho
adotar Pix, a classe nova implementa `MeioDePagamento` e o `Caixa` a atende
sem uma linha editada, no mesmo espírito do carrinho de compras.

O caminho oposto é o sinal de alerta registrado no capítulo 8, e vale ver
o custo dele por extenso:

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
lição do polimorfismo, agora sem exigir parentesco de classe nenhum. O
fiado, terceiro meio da abertura, é o cumpridor mais simples do contrato,
devolvendo a própria compra, e o registro na caderneta, com o limite dele,
é assunto que o capítulo 13 retoma:

```java
class Fiado implements MeioDePagamento {
    @Override
    public BigDecimal valorFinal(BigDecimal compra) {
        return compra;
    }
}
```

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
mudança. Com corpo na interface, o conflito volta a ser possível: uma classe que
implemente duas interfaces com o mesmo método default é obrigada pelo
compilador a sobrescrever e decidir. O método default existe para evolução
de contrato publicado, e não para virar depósito de lógica: interface que acumula corpos está
fazendo o trabalho da construção da próxima seção.

## O que mais cabe numa interface

Além do método abstrato e do default, uma interface aceita mais três
espécies de membro, e todas as três aparecem na biblioteca padrão.

A primeira é a constante de interface. Todo campo declarado numa interface
é `public static final`, escrevam-se as três palavras ou não:

```java
public interface MeioDePagamento {
    BigDecimal LIMITE_SEM_SENHA = new BigDecimal("50.00");

    BigDecimal valorFinal(BigDecimal compra);
}
```

`MeioDePagamento.LIMITE_SEM_SENHA` fica disponível a quem implementa e a
quem chama, com a grafia de constante do capítulo 7. O que não existe é
campo de instância: uma interface não guarda estado, e é essa a fronteira
que a separa da classe abstrata da próxima seção. A constante serve ao
valor que pertence ao contrato e não a uma implementação, como um limite
regulamentar; valor que muda com a configuração do sistema não é constante
e não mora aqui.

A segunda é o método estático de interface: um método com corpo, chamado
pelo nome da interface, que não é herdado por quem implementa e não faz
parte do contrato.

```java
public interface MeioDePagamento {
    BigDecimal valorFinal(BigDecimal compra);

    static MeioDePagamento doCaixaRapido() {
        return new Dinheiro();
    }
}
```

`MeioDePagamento.doCaixaRapido()` entrega um exemplar pronto sem que quem
chama precise saber qual classe atendeu, e esse é o uso típico da forma: a
fábrica, o método que cria por baixo do contrato, e a conveniência que
acompanha a promessa em vez de morar numa classe utilitária à parte. É
assim que boa parte das fábricas da biblioteca padrão é declarada, incluindo
as que os capítulos 17 e 18 usam.

A terceira é o método `private` de interface, que só existe para os
defaults. Quando dois métodos default repetem um pedaço de lógica, ele sai
para um método privado da própria interface, invisível de fora, com o
mesmo papel do auxiliar privado de uma classe. É o membro menos usado dos
quatro, e existe para o default não ter que escolher entre duplicar código
e publicar um método que ninguém deveria chamar.

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
   compra pelos três meios, exibindo nome do recibo e valor final. A impressão sai com casas de sobra,
   porque `multiply` soma as casas dos dois lados; registre o fato e siga,
   que o conserto, `setScale`, aparece no capítulo 11.

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

6. Acrescente a `MeioDePagamento` uma constante com o limite de compra sem
   senha e um método estático que devolva o meio padrão do caixa rápido.
   Tente declarar um campo de instância na interface e anote a recusa do
   compilador. Depois escreva dois métodos default que repitam uma conta e
   extraia a repetição para um método `private` da interface.

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
| constante de interface | campo de interface; `public static final` por definição |
| método estático de interface | método com corpo chamado pelo nome da interface; fábrica típica |
| método `private` de interface | auxiliar dos defaults, invisível de fora |
