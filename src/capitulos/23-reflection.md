# Annotations, reflection e proxies

O capítulo 15 deixou uma pergunta armada: nenhuma linha do mercadinho chama
`CaixaTest`, e os testes rodam. Alguém encontra as classes de teste,
descobre quais métodos carregam `@Test` e os executa, sem conhecer nenhum
deles de antemão. Este capítulo constrói esse alguém, com as vinte linhas
prometidas, e no caminho apresenta o mecanismo por trás das ferramentas que
examinam e executam código alheio: executores de teste, mapeadores,
containers.

## Anotação própria e retenção

Anotações existem no livro desde o `@Override`, sempre de prateleira.
Declarar uma é curto:

```java
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;

@Retention(RetentionPolicy.RUNTIME)
public @interface MeuTeste { }
```

O `@interface` declara a anotação, e o corpo vazio diz que ela é pura
marca, sem dados. Anotações também carregam dados, declarados como métodos
no corpo: um `String nome();` ali dentro permitiria `@MeuTeste(nome =
"desconto do dinheiro")`, e o leitor da anotação recupera o valor em
execução. O `@SuppressWarnings("unchecked")` usa essa forma com um atalho:
quando o único elemento se chama `value`, o nome pode ser omitido no uso;
com qualquer outro nome, como `nome`, ele é obrigatório, e `@MeuTeste("x")`
nem compila. A linha de cima é a decisão que importa aqui: a retenção define até
onde a anotação sobrevive. `SOURCE` vive só no fonte, para o compilador e
ferramentas de fonte, o destino do `@Override`; `CLASS` chega ao bytecode e
para lá; `RUNTIME` chega à execução, visível para o mecanismo da próxima
seção. Uma anotação que pretende ser lida por um executor, como `@Test` e
como a nossa, precisa de `RUNTIME` declarado.

## Reflexão

Reflexão é a capacidade de um programa examinar e manipular os próprios
tipos em execução: perguntar a uma classe quais métodos ela tem, que
anotações carrega, e invocá-los, tudo por objetos que representam essas
coisas. A porta de entrada é o `Class`, o objeto que representa um tipo,
obtido pelo literal de classe, `CaixaTest.class`, ou pelo
`getClass` de qualquer objeto. Dele saem os representantes dos membros:
`Method` para métodos, `Field` para campos e `Constructor` para
construtores, cada um sabendo o próprio nome, os tipos envolvidos e as
anotações que carrega; do `Class` também saem a superclasse e as interfaces
implementadas, a hierarquia inteira disponível como dado. É o
programa lendo a própria estrutura, e um encontro com isso o livro já teve
sem dizer o nome: o `Produto@6f2b958e` é o `getClass` por
trás do `toString` herdado, imprimindo o nome do tipo real.

O laboratório deste capítulo usa a moldura completa, cada classe em seu
próprio arquivo: em arquivo-fonte compacto as classes viram aninhadas, e o
executor adiante não as encontraria pelo caminho mostrado. O alvo é uma
`CaixaTest` sem JUnit nenhum, com a asserção escrita à mão para o
laboratório rodar com `java` puro, sem classpath de biblioteca:

```java
import java.math.BigDecimal;

public class CaixaTest {
    @MeuTeste
    public void somaDuasVendas() {
        BigDecimal total = new BigDecimal("19.90").add(new BigDecimal("19.90"));
        if (!total.equals(new BigDecimal("39.80"))) {
            throw new AssertionError("esperado: <39.80> mas foi: <" + total + ">");
        }
    }

    @MeuTeste
    public void descontoDoDinheiro() {
        BigDecimal recebido = new BigDecimal("100.00").multiply(new BigDecimal("0.95"));
        if (!recebido.equals(new BigDecimal("95.00"))) {
            throw new AssertionError("esperado: <95.00> mas foi: <" + recebido + ">");
        }
    }
}
```

O `if` com `throw new AssertionError(...)`, o erro que representa uma
asserção violada, faz à mão o papel do `assertEquals`, e o segundo teste
reencontra de propósito a escala do `BigDecimal`: `100.00` vezes `0.95` dá
`95.0000`, e `equals` distingue as escalas. O executor prometido cabe
inteiro numa tela:

```java
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class Executor {
    public static void main(String[] args) throws Exception {
        int passaram = 0;
        int falharam = 0;
        Class<?> tipo = CaixaTest.class;
        for (Method metodo : tipo.getDeclaredMethods()) {
            if (metodo.isAnnotationPresent(MeuTeste.class)) {
                Object instancia = tipo.getDeclaredConstructor().newInstance();
                try {
                    metodo.invoke(instancia);
                    IO.println("PASSOU  " + metodo.getName());
                    passaram++;
                } catch (InvocationTargetException erro) {
                    IO.println("FALHOU  " + metodo.getName() + ": " + erro.getCause().getMessage());
                    falharam++;
                }
            }
        }
        IO.println(passaram + " passaram, " + falharam + " falharam");
    }
}
```

```console
$ javac *.java
$ java Executor
PASSOU  somaDuasVendas
FALHOU  descontoDoDinheiro: esperado: <95.00> mas foi: <95.0000>
1 passaram, 1 falharam
```

A leitura, linha a linha do que é novo. `getDeclaredMethods` devolve os
métodos declarados na classe, em ordem não prometida, e
`isAnnotationPresent` filtra os marcados, recebendo o literal de classe da
anotação. `getDeclaredConstructor().newInstance()` cria a instância pelo
construtor sem argumentos, uma por teste, que é exatamente a fixture nova
do JUnit, agora explicada. O `invoke` chama o método sobre a
instância; quando o método lança, a exceção chega embrulhada numa
`InvocationTargetException`, e o `getCause` desembrulha a original, a
`AssertionError` do `if` da `CaixaTest`. Vinte linhas, e o `@Test`, o
placar e a fixture do JUnit deixaram de ser mágica: a ferramenta real tem
dez anos de recursos em volta, e este núcleo no centro.

O `Class<?>`, de passagem, usa o wildcard no lugar honesto:
um tipo desconhecido, porque o executor serve para qualquer classe.

Duas extensões do mesmo caminho aparecem em toda ferramenta dessa família.
A primeira lê os dados da anotação: `metodo.getAnnotation(MeuTeste.class)`
devolve o objeto da anotação encontrada, e cada elemento declarado nela
vira um método a chamar, de modo que um `@MeuTeste(nome = "desconto do
dinheiro")` se lê com `marca.nome()`. É assim que um executor de verdade
descobre o nome de exibição de um teste, o tempo limite e as demais opções,
e é o que o `@DisplayName` do capítulo 15 faz por dentro.

A segunda vai além dos métodos. `getDeclaredFields` devolve os campos
declarados, e cada `Field` sabe o próprio nome, o próprio tipo e o valor
que ele tem num objeto dado, com `campo.get(objeto)`;
`getDeclaredConstructors` faz o mesmo pelos construtores, com os tipos dos
parâmetros de cada um, que é justamente o que o capítulo 24 vai percorrer.
Um mapeador entre objeto e linha de tabela é esse laço e mais nada: para
cada campo, o nome vira coluna e o valor vira dado.

<div class="armadilha">

O executor pronto, a anotação declarada, e uma distração de uma linha:

```java
public @interface MeuTeste { }
```

```console
$ javac *.java
$ java Executor
0 passaram, 0 falharam
```

Os dois testes continuam no arquivo, compilando, marcados. Nenhum roda.

</div>

Sem `@Retention` declarada, a retenção padrão é `CLASS`: a anotação chega ao
bytecode e é invisível em execução, e `isAnnotationPresent` responde `false`
para todos, sem erro, sem aviso. O placar zerado é a única pista, e é por
isso que a armadilha do teste que não roda tem uma prima
aqui: ferramenta baseada em anotação falha em silêncio quando a retenção
está errada, e conferir o placar continua sendo a defesa.

A reflexão cobra dois preços que definem onde usá-la. O primeiro é o
contrato por texto: `getDeclaredConstructor()` e companhia procuram por
nomes e formas em execução, e o compilador não confere nada, de modo que
renomear um construtor ou mudar uma assinatura quebra o código reflexivo só
quando ele rodar, a categoria de erro que o livro inteiro empurra para a
compilação. O segundo é que ela atravessa muros: com `setAccessible`,
código reflexivo lê e escreve até membros `private`, e o encapsulamento
vale contra código comum, não contra ferramentas decididas. A
regra de uso sai dos dois preços: reflexão é técnica de ferramenta e de
infraestrutura, executores, mapeadores, injetores, e não de regra de
negócio; o estoque do mercadinho nunca precisa dela.

## Proxy dinâmico

A segunda metade do arsenal fabrica objetos. Um proxy dinâmico é um objeto
criado em execução que implementa interfaces escolhidas e entrega toda
chamada recebida a um único ponto, o `InvocationHandler`: uma interface
funcional cujo método recebe o proxy, o `Method` chamado e os argumentos, e
decide o que fazer. O mercadinho quer auditoria de tudo que passa pelo
pagamento, sem tocar nas classes de pagamento:

```java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Proxy;

MeioDePagamento dinheiro = compra -> compra.multiply(new BigDecimal("0.95"));

InvocationHandler auditoria = (proxy, metodo, argumentos) -> {
    IO.println("[auditoria] " + metodo.getName() + " com " + argumentos[0]);
    return metodo.invoke(dinheiro, argumentos);
};

MeioDePagamento vigiado = (MeioDePagamento) Proxy.newProxyInstance(
        MeioDePagamento.class.getClassLoader(),
        new Class<?>[] { MeioDePagamento.class },
        auditoria);

IO.println(vigiado.valorFinal(new BigDecimal("100.00")));
IO.println(vigiado.getClass().getName());
```

```console
[auditoria] valorFinal com 100.00
95.0000
$Proxy0
```

O `vigiado` é um `MeioDePagamento` legítimo: o caixa o aceita
sem saber de nada, o polimorfismo funciona, e cada chamada passa pela
auditoria antes de ser delegada ao objeto real pelo `invoke`. A última
linha mostra a certidão de nascimento: `$Proxy0`, uma classe que não existe
em arquivo nenhum, fabricada pela JVM na hora. O nome sai sem pacote porque
a interface do laboratório vive sem pacote; num projeto com pacotes, como o
da prática, a mesma linha imprime o nome qualificado, `jdk.proxy1.$Proxy0`. O padrão, interceptar
chamadas de uma interface sem alterar as implementações, é o mecanismo com
que frameworks, as bibliotecas que invertem o controle e chamam o código de
quem as usa, adicionam auditoria, medição de tempo e controle de acesso
em volta de código alheio; o capítulo 24 usa a ideia por um ângulo mais
simples, e quem encontrar um `$Proxy` num stack trace de framework agora
sabe o que está olhando. A dupla deste capítulo fecha um circuito que vale
enxergar de uma vez: anotação marca a intenção no código, reflexão encontra
a marca e age, e o proxy embrulha o resultado quando o agir é interceptar.
É a receita do executor deste capítulo, e a das ferramentas dessa família
que o leitor vai encontrar depois deste livro, e ela cabe numa tela de
cada vez.

<div class="aprofundamento">

**O custo.** Chamada reflexiva custa múltiplas vezes uma chamada direta,
entre validações e embrulhos, e proxy soma uma indireção a cada método. Para
executor de testes e montagem de sistema, irrelevante; para o método quente
de um laço, proibitivo. Ferramentas sérias geram bytecode ou usam variantes
otimizadas depois da primeira chamada, e a regra do usuário fica a mesma:
reflexão na borda do sistema, nunca no miolo do cálculo.

</div>

## Prática

1. Monte o executor completo num projeto Maven: a anotação, duas classes de
   teste com métodos que passam e falham, e o placar. Depois remova o
   `@Retention` e reproduza a armadilha.

2. Estenda o executor com `@AntesDeCada`: um método assim anotado roda antes
   de cada teste da classe, na mesma instância. Compare com o `@BeforeEach`
   do capítulo 15.

3. Escreva um método `descrever(Class<?> tipo)` que imprima os métodos
   públicos de qualquer classe com seus tipos de retorno, e aponte-o para
   `Produto` e para `String`. Anote o que a saída revela que você não
   sabia.

4. Crie um proxy de medição para `MeioDePagamento` que imprima a duração de
   cada chamada com `System.nanoTime`, empilhado por cima do proxy de
   auditoria. Descreva a ordem em que os dois interceptam.

5. Prove os dois preços da reflexão: renomeie um método de teste e mostre
   que nada quebra até a execução; use `setAccessible` para ler um campo
   `private` de `Produto` e escreva em um parágrafo por que isso não
   invalida o encapsulamento como prática.

## Ficha do capítulo

| Peça | O que faz |
| --- | --- |
| `@interface` | declara uma anotação própria |
| `@Retention(RetentionPolicy.RUNTIME)` | anotação visível em execução; exigida por executores |
| `Tipo.class` / `getClass()` | o objeto `Class` que representa o tipo |
| `getDeclaredMethods` / `isAnnotationPresent` | lista métodos; pergunta pela marca |
| `getAnnotation(Tipo.class)` | devolve a anotação encontrada, com os dados dela |
| `getDeclaredFields` / `campo.get(objeto)` | os campos declarados; o valor de um deles num objeto |
| `getDeclaredConstructor().newInstance()` | cria instância pelo construtor |
| `Method.invoke(instancia, args)` | chama o método representado |
| `Proxy.newProxyInstance(loader, interfaces, handler)` | fabrica o proxy dinâmico |

| Termo | Definição |
| --- | --- |
| anotação própria | anotação declarada com `@interface` |
| retenção | até onde a anotação sobrevive: fonte, bytecode ou execução |
| reflexão | examinar e manipular tipos e membros em execução |
| proxy dinâmico | objeto fabricado em execução que implementa interfaces e delega tudo |
| `InvocationHandler` | o ponto único que recebe cada chamada do proxy |
