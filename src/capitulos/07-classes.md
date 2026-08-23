# Classes, construtores e encapsulamento

O mercadinho prometido no prefácio abre as portas neste capítulo, e a
primeira tentativa de registrar o estoque dele usa o que o livro tem até
aqui:

```java
void main() {
    String[] nomes = { "Arroz 5kg", "Café 500g", "Sabão em pó" };
    int[] estoques = { 40, 25, 12 };
    IO.println(nomes[1] + ": " + estoques[1] + " unidades");
}
```

```console
$ java Estoque.java
Café 500g: 25 unidades
```

Funciona, e é uma armadilha armada. Os dados de um produto estão espalhados
em dois arrays que só se correspondem pela posição: o café é o nome de
índice 1 e o estoque de índice 1, e nada além de disciplina mantém esse
acordo. Basta remover um produto de um array e esquecer o outro, ou ordenar
os nomes sem ordenar os estoques, para o café passar a exibir o estoque do
sabão, sem erro de compilação e sem erro de execução. A raiz do problema é
que "produto" não existe no programa; existem pedaços de produto em lugares
que o compilador não sabe que se relacionam. Este capítulo cria tipos
próprios, e com eles o mercadinho começa a virar sistema.

## Um tipo novo: a palavra-chave class

A palavra-chave `class` declara uma classe: a definição de um tipo de
objeto, com os dados que cada objeto carrega e os métodos que operam sobre
esses dados. Os dados declarados na classe chamam-se campos:

```java
class Produto {
    String nome;
    int estoque;
}

void main() {
    Produto cafe = new Produto();
    cafe.nome = "Café 500g";
    cafe.estoque = 25;
    IO.println(cafe.nome + ": " + cafe.estoque + " unidades");
}
```

O capítulo 5 apresentou objetos prontos, como `String` e `StringBuilder`;
aqui, pela primeira vez, o tipo é nosso. Cada `new Produto()` cria uma
instância: um objeto independente desse tipo, com os próprios valores nos
campos. Duas instâncias de `Produto` são dois objetos no heap, cada um com
seu `nome` e seu `estoque`, e a variável `cafe` guarda a referência de um
deles. Nome, estoque e o que mais o produto
tiver agora viajam juntos, e o desalinhamento dos arrays paralelos deixa de
ser possível: não há mais duas listas para dessincronizar.

## Construtor e this

Criar o objeto vazio e preencher campo a campo, como acima, deixa um intervalo
perigoso: entre o `new` e a última atribuição existe um produto pela
metade, visível a qualquer código que rode no meio. O construtor fecha esse
intervalo. Construtor é o método especial que roda no
`new`, tem o mesmo nome da classe, não declara tipo de retorno e recebe o
necessário para o objeto nascer completo:

<div class="previsao">

Um construtor escrito às pressas:

```java
class Produto {
    String nome;
    int estoque;

    Produto(String nome, int estoque) {
        nome = nome;
        estoque = estoque;
    }
}

void main() {
    Produto cafe = new Produto("Café 500g", 25);
    IO.println(cafe.nome);
}
```

O programa compila. O que a impressão mostra?

</div>

```
null
```

Dentro do construtor existem dois `nome`: o parâmetro e o campo. Quando
dois escopos sobrepostos declaram o mesmo nome, o mais interno vence, uma
regra nova deste capítulo chamada sombreamento, e `nome = nome` fala do
parâmetro duas vezes, atribuindo-o a ele mesmo. O campo nunca é tocado e
fica com o valor padrão: campo de objeto nasce valendo zero, `false` ou
`null`, conforme o tipo, ao contrário da variável local, que o compilador
recusa usar sem valor. Nenhum aviso, porque a linha é válida. A palavra
`this` resolve: ela é a referência da própria instância em construção, e
`this.nome` aponta sem ambiguidade para o campo:

```java
Produto(String nome, int estoque) {
    this.nome = nome;
    this.estoque = estoque;
}
```

## Invariantes e a recusa no nascimento

Um produto de estoque negativo não descreve coisa nenhuma do mercadinho; se
um objeto assim circular pelo sistema, cada relatório que o somar sai
errado. A condição que todo objeto válido de um tipo sustenta, do nascimento
em diante, chama-se invariante, e o construtor é o lugar de defendê-la:

```java
Produto(String nome, int estoque) {
    if (nome == null || nome.isBlank()) {
        throw new IllegalArgumentException("Produto precisa de nome.");
    }
    if (estoque < 0) {
        throw new IllegalArgumentException("Estoque não pode ser negativo: " + estoque);
    }
    this.nome = nome;
    this.estoque = estoque;
}
```

A palavra `throw` dispara um erro de execução no ponto do problema, e
`IllegalArgumentException` é o erro padrão da biblioteca para argumento que
viola as regras de quem recebe; a mensagem entre parênteses aparece na tela
com a linha do disparo. O ganho é de localização: sem a defesa, o estoque
negativo entra sem aviso e o efeito aparece longe, num relatório qualquer;
com ela, o
programa cai no instante e na linha em que o valor ruim tentou entrar, com o
valor impresso. O mecanismo completo por trás do `throw`, incluindo como um
programa reage a ele em vez de cair, é o capítulo 13; `isBlank`, usado ali,
apenas pergunta se o texto está vazio ou só com espaços.

## Encapsulamento

A defesa do construtor tem um furo: qualquer código pode escrever
`cafe.estoque = -8` depois do nascimento, por engano ou por atalho. A
solução é controlar o acesso. Os modificadores de acesso definem quem
enxerga cada membro da classe, o nome coletivo de campos, métodos e
construtores: `private` restringe à própria classe,
`public` libera para todo o programa. Campo fica `private`; o que o resto do
programa pode fazer vira método `public`, e passa pela regra:

```java
class Produto {
    private final String nome;
    private int estoque;

    Produto(String nome, int estoque) {
        // validações do construtor, como antes
        this.nome = nome;
        this.estoque = estoque;
    }

    public String nome() {
        return nome;
    }

    public int estoque() {
        return estoque;
    }

    public void baixar(int quantidade) {
        if (quantidade <= 0 || quantidade > estoque) {
            throw new IllegalArgumentException("Baixa inválida: " + quantidade);
        }
        estoque -= quantidade;
    }
}
```

Isso é encapsulamento: esconder a representação interna de um objeto e
expor apenas operações que mantêm as invariantes. O estoque continua
existindo, mas o único caminho até ele agora valida cada baixa; o
`cafe.estoque = -8` passa a ser recusado pelo compilador em qualquer classe
de arquivo próprio, porque o campo é invisível fora de `Produto`. Uma
ressalva de laboratório: no arquivo-fonte compacto, em que tudo divide um
arquivo, as classes dali de dentro se enxergam por inteiro, `private`
incluído, e a recusa só vale com cada classe no seu arquivo, que é o
formato da última seção e de todo o livro daqui em diante. O `final` no campo `nome` acrescenta outra trava, do próprio
compilador: o modificador `final` marca o que recebe valor uma vez e nunca
mais, e produto que muda de nome não existe neste domínio. A regra prática
do capítulo: campo `private` sempre; `public` é decisão, tomada método a
método, e cada método `public` é uma promessa de comportamento que o resto
do sistema vai usar.

## Dinheiro entra no mercadinho

Falta o preço, e o capítulo 3 deixou dito que `double` não serve: centavos
aproximados espalham diferenças que ninguém rastreia. Existem duas soluções
honestas. A primeira é guardar centavos em inteiros: `int precoEmCentavos`,
com 1990 valendo R$ 19,90. É exata, rápida, muito usada em sistemas de
pagamento, e o nome do campo carrega a unidade para ninguém somar centavos
com reais. A segunda é o `BigDecimal`, o tipo da biblioteca padrão para
números decimais exatos, e é a escolha deste livro, por dois motivos: os
valores aparecem no código como aparecem na etiqueta, e o tipo é um objeto
imutável de método em método, o que exercita exatamente o que este capítulo
ensina.

```java
BigDecimal preco = new BigDecimal("19.90");
BigDecimal total = preco.multiply(new BigDecimal(3));
IO.println(total);
```

```
59.70
```

`BigDecimal` nasce de `new`, como qualquer objeto, e o argumento do
construtor é um `String` com o valor exato. As contas são métodos: `add`
soma, `subtract` subtrai, `multiply` multiplica, e todos devolvem um
`BigDecimal` novo, porque o tipo é imutável como o `String`;
comparações de ordem usam o método `compareTo`, que devolve negativo, zero
ou positivo. No arquivo compacto, `BigDecimal` resolve sem linha extra; o
`import` que a moldura exige aparece na última seção.

<div class="armadilha">

O construtor de `BigDecimal` também aceita um `double`:

```java
BigDecimal errado = new BigDecimal(0.1);
BigDecimal certo = new BigDecimal("0.1");
IO.println(errado);
IO.println(certo);
```

```
0.1000000000000000055511151231257827021181583404541015625
0.1
```

</div>

O `new BigDecimal(0.1)` não criou o valor um décimo: criou o retrato exato
da aproximação binária do `double`, com todas as casas. O
`double` já chega contaminado, e o `BigDecimal` apenas fotografa. Em código
de dinheiro, `BigDecimal` nasce de `String` ou de inteiros, nunca de
`double`; essa regra é curta e a violação passa em qualquer teste que não
imprima as casas todas.

## static: o membro que pertence ao tipo

Dois capítulos deixaram uma diferença sem explicação: `Random` exige
`new Random()`, e `Math.max` se chama direto pelo nome. A resposta é o
modificador `static`. Um membro estático pertence à classe, não a cada
instância: existe uma única cópia, acessada pelo nome do tipo, sem `new`.
`Math` é uma classe cujos métodos são todos estáticos, porque `max` e `abs`
não dependem de nenhum estado guardado; `Random` precisa de instância porque
cada gerador carrega o próprio estado, a semente em andamento. `IO.println`
e `Integer.parseInt` seguem o mesmo desenho de `Math`. Em `Produto`, o uso
típico de `static` é a constante compartilhada por todas as instâncias:

```java
static final int ESTOQUE_MAXIMO = 10_000;
```

`static final` com nome em maiúsculas é a grafia consagrada de constante. A
regra prática: método estático para cálculo que não depende de instância;
todo o resto, membro de instância. Estado mutável em campo estático é uma
única variável compartilhada pelo programa inteiro, e os defeitos disso
aparecem no capítulo 22.

## A moldura, enfim

O capítulo 2 prometeu explicar as linhas que o arquivo-fonte compacto
dispensa. Todas as palavras delas agora têm dono:

```java
import java.math.BigDecimal;

public class Loja {
    public static void main(String[] args) {
        Produto cafe = new Produto("Café 500g", 25);
        IO.println(cafe.nome());
    }
}
```

`public class Loja` declara a classe visível a todo o programa, no arquivo
`Loja.java`, com o nome do arquivo amarrado ao da classe pública; é dessa
declaração que a extensão `.class` do bytecode tira o nome. O `main` com `public static` é a forma
tradicional, esperada por décadas de ferramentas e presente em praticamente
todo projeto existente: `static` dispensa instância para a partida, e
`public` o expõe ao lançador. O Java 25 flexibilizou esse protocolo junto
com o arquivo compacto, e formas mais enxutas de `main` também valem; o
livro escreve a tradicional na moldura, porque é a que o leitor vai
encontrar. O `import` declara de
onde vem um tipo de fora do arquivo: `BigDecimal` mora no pacote
`java.math`, e pacote é o espaço de nomes que agrupa classes relacionadas,
declarado com `package` na primeira linha de um arquivo e refletido em
pastas homônimas no disco. Os capítulos até o 13 mantêm as classes sem
declaração de pacote, para `javac *.java` e `java Loja` continuarem diretos;
a organização completa em pastas chega com a ferramenta do capítulo 14.

<div class="aprofundamento">

**A moldura que o compilador escrevia.** No arquivo-fonte compacto, o
compilador gera uma classe implícita em volta dos métodos soltos e importa
de uma vez os tipos principais da biblioteca padrão; é por isso que
`IO.println` e `Random` sempre funcionaram sem `import`. A moldura escrita
não acrescenta poder nenhum: torna explícito o que era fornecido, e passa a
ser necessária quando o programa tem mais de uma classe pública em arquivos
próprios.

</div>

## Prática

1. Escreva a classe `Produto` completa deste capítulo, com nome, estoque e
   preço em `BigDecimal`, invariantes no construtor e campos `private`.
   Monte na estrutura da última seção, cada classe em seu arquivo, tente
   violar cada invariante a partir do `main` e anote o que o compilador
   recusa e o que o construtor recusa.

2. Acrescente a `Produto` um método `repor(int quantidade)` com a validação
   que ele merece, e um método `valorEmEstoque()` que devolva o preço
   multiplicado pelo estoque, em `BigDecimal`.

3. Reproduza a armadilha do `new BigDecimal(0.1)` e conserte. Depois some
   `0.10` dez vezes com `BigDecimal` e imprima, comparando com a soma de
   `0.1` dez vezes em `double` do capítulo 3.

4. Escreva uma classe `Caixa` com um campo `private BigDecimal` para o total
   do dia e um método `registrar(Produto produto, int quantidade)` que baixa
   o estoque e acumula o valor da venda. Imprima o total após três vendas.

5. Refaça o programa de abertura, com os arrays paralelos substituídos por
   um array de `Produto`, e escreva em um parágrafo qual classe de erro
   ficou impossível na nova versão.

6. Converta o jogo de adivinhação do capítulo 6 para a moldura completa:
   uma classe pública com `main`, em arquivo próprio, compilada com `javac`
   e executada com `java`.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| classe (`class`) | declaração de um tipo de objeto: os campos e os métodos dele |
| campo | dado declarado na classe, presente em cada objeto |
| instância | um objeto de uma classe, criado por `new` |
| construtor | método de nome igual ao da classe, executado pelo `new`; sem tipo de retorno |
| `this` | a referência da própria instância |
| invariante | condição que todo objeto válido do tipo sustenta sempre |
| `throw` | dispara um erro de execução no ponto do problema |
| `IllegalArgumentException` | erro padrão para argumento que viola as regras de quem recebe |
| modificador de acesso | `public` (visível a todos) e `private` (só a própria classe) |
| encapsulamento | esconder a representação e expor operações que mantêm as invariantes |
| modificador `final` | campo que recebe valor uma vez e nunca mais |
| `static` / membro estático | membro que pertence à classe, único, acessado pelo nome do tipo |
| representação de dinheiro | centavos em inteiros, ou `BigDecimal`; nunca `double` |
| `BigDecimal` | decimal exato e imutável; nasce de `String`, opera por métodos |
| pacote | espaço de nomes que agrupa classes; declarado com `package` |
| `import` | declara de onde vem um tipo usado no arquivo |
