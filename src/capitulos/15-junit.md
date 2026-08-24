# JUnit 5 e o hábito de testar

Toda correção do mercadinho, até aqui, foi conferida do mesmo jeito: rodar o
programa e olhar a saída. O método funciona para um arquivo e morre de
cansaço num sistema: a cada mudança no `Caixa`, alguém precisaria reexecutar
à mão a venda em dinheiro, a venda no cartão, o fiado no limite, o desconto,
o troco, e ninguém reexecuta tudo, então as quebras passam. A conferência manual
deixa de acontecer conforme o sistema cresce; a saída é escrever programas
que conferem programas.

Um teste unitário é um método que executa um pedaço pequeno do sistema, uma
unidade, e confere o resultado contra o esperado, falhando sozinho quando
eles divergem. O JUnit é a ferramenta que descobre esses métodos, roda todos
e imprime o placar, e é a primeira dependência de verdade do `pom.xml`,
exatamente como o capítulo 14 prometeu:

```xml
<dependencies>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.11.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
        </plugin>
    </plugins>
</build>
```

Duas novidades no XML. O `<scope>test</scope>` diz que a dependência existe
só para os testes: o JUnit não entra no jar do mercadinho, porque o cliente
do sistema não roda testes. E o bloco do `surefire` fixa a versão do
executor de testes do Maven. A trava protege contra máquinas e projetos
presos a Maven antigo, cujo executor padrão ignora testes de JUnit 5 em
silêncio, exibindo `BUILD SUCCESS` sem rodar teste nenhum; o Maven do
capítulo 14 já traz executor moderno, e fixar a versão mantém a construção
igual em toda máquina.

## O primeiro teste

Teste é código, e mora na pasta que a convenção de diretórios reservou:
`src/test/java`. A classe de teste espelha a classe testada, com `Test` no
nome:

```java
import java.math.BigDecimal;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

class ProdutoTest {

    @Test
    void calculaPrecoParaTresUnidades() {
        Produto cafe = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
        BigDecimal total = cafe.precoPara(3);
        assertEquals(new BigDecimal("59.70"), total);
    }
}
```

```console
$ mvn test
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] BUILD SUCCESS
```

A anotação `@Test`, no espírito do `@Override`, marca o método
para o executor encontrar; o nome do método é a descrição do caso, e vale
uma frase inteira, porque é ele que aparece no placar quando falha. O corpo
segue um ritmo em três tempos que praticamente todo teste do mundo repete:
preparar os objetos, executar a operação, conferir o resultado.

A conferência é a asserção: uma afirmação verificável sobre o resultado, que
derruba o teste quando é falsa. `assertEquals(esperado, obtido)` é a
asserção central, e a ordem dos argumentos importa: o valor esperado vem
primeiro, e trocá-los não quebra nada hoje, mas inverte a mensagem de erro
de todas as falhas futuras, apontando o certo como errado. O `import static`
da abertura é a novidade de sintaxe: importa o método, em vez do tipo, para
`assertEquals` dispensar prefixo. Existem asserções irmãs para os demais
casos, `assertTrue`, `assertFalse` e `assertNotNull` entre elas, e a
terceira seção deste capítulo reúne o repertório inteiro.

Quando a asserção falha, o teste conta exatamente o quê e onde:

```console
$ mvn test
[ERROR] CaixaTest.aplicaDescontoDeCincoPorCento:18
org.opentest4j.AssertionFailedError: expected: <57.00> but was: <57.0000>
[INFO] Tests run: 2, Failures: 1, Errors: 0, Skipped: 0
[INFO] BUILD FAILURE
```

<div class="previsao">

A falha acima nasce de um teste sobre o método que aplica o desconto de 5%
do dinheiro:

```java
@Test
void aplicaDescontoDeCincoPorCento() {
    BigDecimal resultado = caixa.comDesconto(new BigDecimal("60.00"));
    assertEquals(new BigDecimal("57.00"), resultado);
}
```

Sessenta reais menos 5% são exatamente cinquenta e sete, e o método
multiplica por `0.95` sem errar a conta. Por que o teste falha mesmo assim?

</div>

Porque `assertEquals` usa o `equals`, e o `equals` de `BigDecimal` é o
estrito por escala: `57.00` e `57.0000` são o mesmo número, o `compareTo`
daria zero, e ainda assim não são iguais para o `equals`, porque a
multiplicação somou as casas dos dois lados. O teste está protegendo o
sistema de um jeito que a etiqueta não mostra: ou o método fixa a escala
com `setScale(2)`, e todo valor de dinheiro do sistema circula com duas
casas, ou cada desconto acumula casas fantasmas que vão aparecer em alguma
comparação futura. Teste bom falha por motivo verdadeiro, e este é o
primeiro serviço do placar: a conversa sobre escala aconteceu no capítulo
do teste, e não numa diferença de caixa.

## Fixture e o ciclo de cada teste

Testes da mesma classe repetem preparação, e a repetição tem lugar próprio.
A fixture é o conjunto de objetos que os testes de uma classe usam como
ponto de partida, e o método anotado com `@BeforeEach` a monta de novo antes
de cada teste:

Os imports já vistos ficam omitidos dos próximos trechos.

```java
import org.junit.jupiter.api.BeforeEach;

class CaixaTest {

    private Caixa caixa;
    private Produto cafe;

    @BeforeEach
    void prepara() {
        caixa = new Caixa();
        cafe = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    }

    @Test
    void somaUmaVendaAoTotal() {
        caixa.registrar(cafe, 2);
        assertEquals(0, new BigDecimal("39.80").compareTo(caixa.totalDoDia()));
    }

    @Test
    void comecaComTotalZerado() {
        assertEquals(0, BigDecimal.ZERO.compareTo(caixa.totalDoDia()));
    }
}
```

Três parentes completam o ciclo. `@AfterEach` roda depois de cada teste, e
serve à limpeza do que o teste deixou fora da memória, um arquivo, uma
pasta. `@BeforeAll` e `@AfterAll` rodam uma vez por classe, antes do
primeiro teste e depois do último, e por isso são declarados `static`:
existem antes de haver instância. O que cabe neles é o preparo caro e
compartilhado que nenhum teste altera; estado alterável ali dentro
reintroduz exatamente a dependência entre testes que o `@BeforeEach` existe
para eliminar.

| Anotação | Quando roda |
| --- | --- |
| `@BeforeAll` | uma vez, antes do primeiro teste da classe; método `static` |
| `@BeforeEach` | antes de cada teste |
| `@AfterEach` | depois de cada teste |
| `@AfterAll` | uma vez, depois do último teste da classe; método `static` |

O "de novo antes de cada" é a parte que importa: cada teste recebe uma
fixture recém-criada, e a ordem em que os testes rodam deixa de ter
importância, porque nenhum herda o estado sujo do anterior. Um teste que só
passa depois de outro é um teste que mente, e a fixture por teste é o que
evita a mentira. A comparação via `compareTo`, nas duas asserções, é a regra de dinheiro
aplicada a testes.

Falta testar o que deve dar errado: o construtor de `Produto` precisa
recusar estoque negativo, e isso também é comportamento com contrato. Sem as
peças do capítulo 18, a forma disponível usa `try` e `catch`:

```java
@Test
void recusaEstoqueNegativo() {
    try {
        new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"), -8);
        fail("Deveria ter recusado estoque negativo.");
    } catch (IllegalArgumentException erro) {
        assertTrue(erro.getMessage().contains("-8"));
    }
}
```

`fail` derruba o teste ao ser alcançado: se o construtor aceitar o valor
inválido, a linha roda e o placar acusa. Se recusar, o `catch` confirma que
a mensagem carrega o valor, e o teste passa. O capítulo 18 apresenta a forma
moderna e mais curta de escrever exatamente isso.

<div class="armadilha">

Um teste novo entra em `CaixaTest`, e o placar da classe segue limpo:

```java
void recusaQuantidadeZero() {
    try {
        new ItemDeVenda(cafe, 0);
        fail("Deveria ter recusado quantidade zero.");
    } catch (IllegalArgumentException erro) {
    }
}
```

```console
$ mvn test
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0 -- in CaixaTest
[INFO] BUILD SUCCESS
```

A validação de quantidade zero nunca foi escrita em `ItemDeVenda`. Por que
nada falhou?

</div>

Porque o teste nunca rodou: faltou o `@Test`, o método é invisível para o
executor, e o placar conta só os dois testes antigos. Nenhum erro, nenhum
aviso, e uma proteção que todo mundo acredita existir não existe. A defesa é
dupla: conferir o número do placar quando se acrescenta teste, esperando vê-lo
subir, e desconfiar de teste que nasce passando. Um teste novo deve falhar
pelo menos uma vez, na frente de quem o escreveu, antes de valer alguma
coisa; teste que nunca falhou não provou que sabe falhar.

## O nome no placar e as asserções que faltavam

O placar é lido por gente, e o que aparece nele é o nome do método. Quando
a frase que descreve o caso não cabe num nome de método,
`@DisplayName` escreve a descrição em português corrido, com espaço e
acento, e é ela que o executor imprime:

```java
@Test
@DisplayName("venda em dinheiro aplica 5% de desconto")
void aplicaDescontoDoDinheiro() {
```

`@Disabled` desliga um teste, com o motivo no argumento, e o placar passa a
contá-lo na coluna `Skipped`, que é a coluna que ninguém lê: teste
desligado sem data para voltar é proteção perdida com aparência de
proteção mantida.

Ao lado do `assertEquals`, o repertório que o dia a dia usa:

| Asserção | Falha quando |
| --- | --- |
| `assertEquals(esperado, obtido)` | os dois diferem, pelo `equals` |
| `assertNotEquals(inesperado, obtido)` | os dois são iguais |
| `assertTrue(condição)` / `assertFalse(condição)` | a condição não é o que se afirmou |
| `assertNull(valor)` / `assertNotNull(valor)` | há objeto onde se esperava nada, ou o contrário |
| `assertSame(esperado, obtido)` / `assertNotSame(...)` | não são, ou são, o mesmo objeto |
| `assertArrayEquals(esperado, obtido)` | os arrays diferem no tamanho ou em alguma posição |
| `fail(mensagem)` | sempre, ao ser alcançada |

Toda asserção aceita uma mensagem como último argumento, e ela paga a
digitação quando a falha sozinha não diz o bastante:
`assertTrue(produto.estoque() > 0, "estoque deveria ter sobrado depois da
venda")` explica o que se esperava, enquanto o `assertTrue` pelado falha
informando apenas que `false` não é `true`. `assertSame` é a pergunta de
identidade do capítulo 5, e serve quando o assunto do teste é justamente o
compartilhamento de referência: dois pedidos ao mesmo repositório devolvem
o mesmo objeto ou dois iguais?

## Um teste, muitos casos

Cinco testes iguais que só mudam o valor de entrada são cinco cópias para
manter. O teste parametrizado é o teste que roda uma vez por conjunto de
argumentos, declarado com `@ParameterizedTest` no lugar de `@Test` e
acompanhado da fonte dos valores:

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

@ParameterizedTest
@CsvSource({
    "1,  19.90",
    "2,  39.80",
    "10, 199.00"
})
void calculaOPrecoPorQuantidade(int quantidade, BigDecimal esperado) {
    Produto cafe = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    assertEquals(0, esperado.compareTo(cafe.precoPara(quantidade)));
}
```

```console
$ mvn test
[INFO] Tests run: 3, Failures: 0, Errors: 0, Skipped: 0
```

Três testes no placar, um por linha da tabela, cada um com os próprios
argumentos no nome; um caso novo passa a custar uma linha, e não um método.
`@CsvSource` entrega uma linha de valores separados por vírgula a cada
execução, convertendo cada coluna para o tipo do parâmetro
correspondente, inclusive para `BigDecimal`. `@ValueSource` é a forma curta
para um parâmetro só, como `@ValueSource(ints = { 1, 2, 10 })`, e
`@EnumSource` roda uma vez por constante de um enum, que é a versão
executável do percurso por `values()` do capítulo 12.

A régua de uso: parametrizar quando os casos são o mesmo comportamento com
dados diferentes, e escrever testes separados quando cada caso existe por
uma razão própria. A tabela de preços acima é o primeiro caso; "recusa nome
vazio" e "recusa estoque negativo" são o segundo, porque falham por motivos
diferentes e merecem nomes diferentes no placar.

## Regressão: o bug vira teste

O uso mais valioso do JUnit num sistema vivo tem nome. Um teste de regressão
é o teste escrito a partir de um defeito encontrado: antes de corrigir,
escreve-se o teste que reproduz o erro e falha; corrige-se; o teste passa e
fica. O defeito do dado viciado do capítulo 6 nunca mais volta sem ser
notado, porque a semente fixa daquele capítulo torna o sorteio testável:

```java
@Test
void sorteioComSementeFixaFicaNaFaixaDoDado() {
    Random dado = new Random(42);
    for (int volta = 0; volta < 1000; volta++) {
        int face = dado.nextInt(1, 7);
        assertTrue(face >= 1 && face <= 6);
    }
}
```

É a promessa de reprodutibilidade paga: com a semente fixa, o
teste confere as mesmas mil jogadas em qualquer máquina, para sempre. E o
conjunto de testes acumulado muda a economia do sistema inteiro: refatorar o
`Caixa`, trocar o cálculo do desconto ou acelerar um método deixa de ser um
salto no escuro, porque o placar diz na hora o que quebrou. O contrato do
capítulo 9 dizia o que cada tipo promete; o teste é a versão executável da
promessa, conferida a cada `mvn test`.

<div class="aprofundamento">

**De onde o JUnit conhece os testes.** Nenhuma linha do mercadinho chama
`ProdutoTest`. O executor abre as classes de teste compiladas e pergunta a
cada uma quais métodos carregam `@Test`, usando um mecanismo da linguagem
para examinar tipos em execução; o capítulo 23 constrói um executor desses
do zero, em vinte linhas.

</div>

## Prática

1. Adote o `pom.xml` deste capítulo no mercadinho e escreva `ProdutoTest`
   completo: preço para quantidade, recusa de nome vazio, recusa de estoque
   negativo, com o padrão try-fail-catch para as recusas.

2. Escreva `CaixaTest` com fixture: total zerado no início, uma venda, três
   vendas somadas, e o desconto do dinheiro com a escala decidida por
   `setScale`. Faça cada teste falhar uma vez de propósito, alterando o
   código testado, e desfaça.

3. Reproduza a armadilha do teste sem `@Test` e descreva em uma frase qual
   número do placar teria denunciado o problema.

4. Escreva um teste de regressão para a armadilha do `equals` sobrecarregado
   do capítulo 10: dois produtos de mesmo código comparados através de
   `Object` devem ser iguais. Rode-o contra a versão errada e contra a
   certa.

5. Escreva um teste que documente o comportamento do `LimiteDeFiadoException`
   do capítulo 13: vender dentro do limite passa, estourar o limite lança, e
   a mensagem carrega o limite. Decida na fixture qual limite usar.

6. Acrescente a `CaixaTest` um `@BeforeAll` que imprima uma linha e um
   `@AfterEach` que imprima outra, rode a classe e cole a saída, mostrando
   a ordem exata em que os quatro momentos do ciclo aconteceram. Tente
   declarar o `@BeforeAll` sem `static` e anote o que o executor diz.

7. Converta os cinco casos de preço por quantidade de `ProdutoTest` num
   único teste parametrizado com `@CsvSource`, dê a ele um `@DisplayName`
   em português e rode com `mvn test -Dtest=ProdutoTest`. Confira que o
   número no placar subiu de um para cinco.

8. Escreva um teste com `assertSame` que prove que duas buscas do mesmo
   código no seu estoque em memória devolvem o mesmo objeto, e outro com
   `assertNotSame` que prove o contrário para duas leituras de arquivo.
   Acrescente mensagem a cada asserção e provoque a falha das duas para ler
   o que o placar imprime.

## Ficha do capítulo

| Anotação / chamada | O que faz |
| --- | --- |
| `@Test` | marca o método como teste, para o executor encontrar |
| `@BeforeEach` | roda antes de cada teste; monta a fixture |
| `assertEquals(esperado, obtido)` | falha se diferentes; esperado vem primeiro |
| `assertTrue` / `assertFalse` / `assertNotNull` | asserções sobre condição e presença |
| `fail(mensagem)` | derruba o teste ao ser alcançado |
| `@AfterEach` / `@BeforeAll` / `@AfterAll` | depois de cada teste / uma vez antes / uma vez depois |
| `@DisplayName("...")` | a descrição que aparece no placar |
| `@Disabled("motivo")` | desliga o teste; conta como `Skipped` |
| `assertNull` / `assertSame` / `assertArrayEquals` | ausência, identidade e conteúdo de array |
| `@ParameterizedTest` + `@CsvSource` / `@ValueSource` / `@EnumSource` | um teste por conjunto de argumentos |
| `mvn test` | compila e roda todos os testes de `src/test/java` |
| `mvn test -Dtest=ProdutoTest` | roda só a classe de teste indicada |

| Termo | Definição |
| --- | --- |
| JUnit | ferramenta que descobre, executa e reporta testes |
| teste unitário | método que executa uma unidade do sistema e confere o resultado |
| asserção | afirmação verificável que derruba o teste quando falsa |
| `assertEquals` | asserção de igualdade, via `equals`; dinheiro pede `compareTo` |
| fixture | objetos de partida dos testes, recriados antes de cada um |
| teste de regressão | teste nascido de um defeito, para ele não voltar despercebido |
| teste parametrizado | um método de teste executado uma vez por conjunto de argumentos |
