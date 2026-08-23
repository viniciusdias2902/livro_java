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
casos, `assertTrue`, `assertFalse` e `assertNotNull` entre elas, todas na
ficha.

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

## Ficha do capítulo

| Anotação / chamada | O que faz |
| --- | --- |
| `@Test` | marca o método como teste, para o executor encontrar |
| `@BeforeEach` | roda antes de cada teste; monta a fixture |
| `assertEquals(esperado, obtido)` | falha se diferentes; esperado vem primeiro |
| `assertTrue` / `assertFalse` / `assertNotNull` | asserções sobre condição e presença |
| `fail(mensagem)` | derruba o teste ao ser alcançado |
| `mvn test` | compila e roda todos os testes de `src/test/java` |

| Termo | Definição |
| --- | --- |
| JUnit | ferramenta que descobre, executa e reporta testes |
| teste unitário | método que executa uma unidade do sistema e confere o resultado |
| asserção | afirmação verificável que derruba o teste quando falsa |
| `assertEquals` | asserção de igualdade, via `equals`; dinheiro pede `compareTo` |
| fixture | objetos de partida dos testes, recriados antes de cada um |
| teste de regressão | teste nascido de um defeito, para ele não voltar despercebido |
