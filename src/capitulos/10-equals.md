# O contrato equals/hashCode/toString

O mercadinho recebe a segunda remessa de café da semana, e o sistema cria o
objeto do produto de novo, a partir da nota do fornecedor:

```java
void main() {
    Produto primeira = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    Produto segunda = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    IO.println(primeira.equals(segunda));
}
```

```
false
```

Mesmo código de barras, mesmo nome, mesmo preço, e `equals` responde
`false`. Para o estoque, isso significa café duplicado no relatório: a busca
que pergunta "esse produto já existe?" com `equals` nunca encontra o que
procura, porque cada remessa cria um objeto novo. O capítulo 5 avisou que
`equals` compara conteúdo, e a frase era verdadeira para `String`; para as
classes nossas, ainda não, e este capítulo explica o porquê e o conserto.

O `equals` que rodou ali é o herdado de `Object`, e a versão
de `Object` compara identidade, como o `==`: só responde `true` para o
mesmíssimo objeto. `String` responde por conteúdo porque a classe `String`
sobrescreve `equals`; `Produto` ainda não sobrescreveu, e igualdade por
conteúdo é uma decisão que cada classe toma por si. Tomá-la direito exige
conhecer as cláusulas.

## O contrato de equals

A documentação de `Object` define o que toda sobrescrita de `equals` deve
cumprir, e o conjunto se chama contrato de equals, contrato no sentido
exato do capítulo 9: promessas que quem chama pode assumir e quem
implementa deve honrar. São cinco cláusulas, três delas com nome de
propriedade matemática.

Reflexividade: todo objeto é igual a si mesmo, `x.equals(x)` responde
`true`. Simetria: a resposta não depende da ordem, `x.equals(y)` e
`y.equals(x)` respondem o mesmo. Transitividade: se `x` é igual a `y` e `y`
é igual a `z`, então `x` é igual a `z`. Consistência: enquanto os objetos
não mudam, a resposta não muda entre chamadas. E a quinta: comparação com
`null` responde `false`, sem derrubar o programa.

Nenhuma dessas cláusulas é conferida pelo compilador, e essa é a
característica que muda o jogo: o compilador confere a assinatura e mais
nada, e todo o resto do sistema, da busca do estoque às estruturas do
capítulo 17, assume as cláusulas como verdadeiras sem perguntar. Um `equals`
que viola o contrato não produz erro em lugar nenhum; produz comportamento
errado nos lugares que confiaram nele, que é a definição de bug difícil.

As cláusulas parecem óbvias até a primeira implementação torta violar uma. A
simetria, por exemplo, quebra quando `Produto` aceita se comparar com
`String` de código de barras: `produto.equals("7891...")` diria `true`, e
`"7891...".equals(produto)` diria `false`, porque `String` não conhece
`Produto`. Buscas que funcionam numa direção e falham na outra são o sintoma
clássico, e a raiz é sempre uma cláusula violada.

Para o mercadinho, a decisão de domínio vem antes do código: dois produtos
são o mesmo produto quando têm o mesmo código de barras. Nome e preço podem
divergir entre remessas, o código não. A implementação canônica:

```java
public class Produto {
    private final String codigoDeBarras;
    private final String nome;
    private final BigDecimal preco;

    // construtor com as validações de sempre

    @Override
    public boolean equals(Object outro) {
        if (this == outro) {
            return true;
        }
        if (!(outro instanceof Produto)) {
            return false;
        }
        Produto produto = (Produto) outro;
        return codigoDeBarras.equals(produto.codigoDeBarras);
    }
}
```

A primeira conferência resolve o caso comum, mesmo objeto, sem trabalho. O
`instanceof` cobre o `null` e qualquer tipo estranho de uma vez, porque
`null instanceof Produto` responde `false` sem erro. O downcast vem protegido pela pergunta anterior, e a última linha delega a comparação
ao `equals` de `String`, que já cumpre o contrato. Cada linha dessa forma
tem função, e a assinatura tem uma exigência que a armadilha abaixo torna
inesquecível: o parâmetro é `Object`, não `Produto`.

<div class="armadilha">

Uma versão que parece mais limpa, com o tipo certo no parâmetro:

```java
public boolean equals(Produto outro) {
    return codigoDeBarras.equals(outro.codigoDeBarras);
}

void main() {
    Produto primeira = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    Produto segunda = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"));
    Object registro = primeira;
    IO.println(primeira.equals(segunda));
    IO.println(registro.equals(segunda));
}
```

```
true
false
```

A chamada direta respondeu `true`; a mesma pergunta, feita através de uma
variável `Object`, respondeu `false`.

</div>

`equals(Produto)` não sobrescreve
`equals(Object)`: assinatura diferente é sobrecarga, o mesmo acidente do
capítulo 8, e as duas versões passam a conviver. A chamada através da
variável `Object` resolve para o `equals(Object)` herdado, o de identidade,
e responde `false`. O defeito é intermitente: nos testes diretos, com
variáveis `Produto`, tudo funciona; dentro das estruturas do capítulo 17,
que guardam tudo por referências genéricas, a igualdade some. `@Override`
pega o engano na hora, porque `equals(Produto)` não sobrescreve nada, e é
mais uma vez a diferença entre bug silencioso e erro de compilação.

## hashCode e o código de hash

`equals` obriga a sobrescrever um segundo método de `Object`. O código de hash
de um objeto é um `int` que o acompanha, devolvido pelo método `hashCode`:
as sobrescritas corretas o derivam dos mesmos campos que o `equals`
compara, e o herdado de `Object` deriva da identidade, não do conteúdo. A
cláusula que amarra os dois métodos é curta: objetos iguais segundo
`equals` devem ter o mesmo código de hash. O contrário não é exigido:
objetos diferentes podem partilhar um hash, o que se chama colisão de hash,
e colisões são inevitáveis, porque há mais conteúdos possíveis do que
valores de `int`.

O propósito do hash é velocidade de busca: estruturas que o capítulo 17
apresenta usam o código de hash para saltar direto à vizinhança do objeto,
em vez de comparar com todos, e só usam `equals` para o desempate final
entre vizinhos. Quem sobrescreve `equals` sem sobrescrever `hashCode` deixa
os dois em desacordo: os cafés iguais das duas remessas ficam com hashes
herdados diferentes, a estrutura procura cada um na vizinhança do próprio
hash, e o produto guardado nunca é encontrado, sem erro nenhum. O capítulo
17 reproduz esse desaparecimento ao vivo; aqui fica a regra que o evita:
sobrescreveu um, sobrescreve o outro, derivando o hash dos mesmos campos
que o `equals` compara.

```java
@Override
public int hashCode() {
    return codigoDeBarras.hashCode();
}
```

`String` já sabe calcular o próprio hash, e delegar a ele cumpre a cláusula:
mesmo código de barras, mesmo hash, sempre. Quando a igualdade olha mais de
um campo, o utilitário `Objects.hash(campo1, campo2)`, do pacote `java.util`, combina os hashes de
todos numa chamada, e a regra continua a mesma: os campos do `hashCode` são
exatamente os campos do `equals`. A mesma classe utilitária resolve o
outro lado: `Objects.equals(a, b)` compara dois valores que podem ser
nulos sem derrubar nada, respondendo `true` para dois nulos e `false`
quando só um dos lados é nulo. É a chamada que substitui
`a.equals(b)` dentro de um `equals` sempre que o campo comparado admite
`null`, e a que evita a ironia de um método de comparação derrubar o
programa com `NullPointerException`. Um hash também pode ser ruim sem estar
errado: devolver sempre `42` cumpre a cláusula à risca, porque iguais têm o
mesmo hash, e destrói a velocidade, porque tudo colide com tudo e a busca
degenera em comparar com todos. Correção é obrigação; espalhamento é
qualidade, e delegar aos hashes dos próprios campos costuma entregar os
dois.

## toString

O terceiro método de `Object` responde pela forma em texto do objeto:

```java
IO.println(new Produto("7891000100103", "Café 500g", new BigDecimal("19.90")));
```

```
Produto@6f2b958e
```

Sem sobrescrita, `toString` devolve o nome da classe, um arroba e um número
em hexadecimal derivado da identidade; o número muda de objeto para objeto
e de execução para execução, e a saída acima é a de uma execução, não a de
todas. No arquivo-fonte compacto ainda sai o nome qualificado pela classe
implícita do arquivo, como `Caixa$Produto@...`. Serve para distinguir
objetos e para nada mais. Sobrescrever muda a impressão inteira,
porque `IO.println` chama `toString` de qualquer objeto que recebe, e essa é
a resposta da promessa sobre o `StringBuilder` impresso direto no capítulo
5:

```java
@Override
public String toString() {
    return "Produto[" + codigoDeBarras + ", " + nome + ", R$ " + preco + "]";
}
```

O contrato de `toString` é mais frouxo que o de `equals`, e cabe numa
frase: devolver uma descrição do objeto em texto, concisa e legível para
quem lê. Nenhuma cláusula obriga formato, e é por isso que a regra de uso
importa tanto: `toString` existe para depuração e registro, para gente
lendo saída de programa, e não para dado que outro código interprete. Um
formato de verdade, recibo ou relatório, é método próprio com nome próprio;
o `toString` fica livre para mudar sem quebrar ninguém. O retorno do
investimento vem na primeira sessão de caça a defeito: a mensagem de uma
`IllegalArgumentException` que concatena o produto, ou um
`IO.println(produto)` jogado no meio do caixa para inspecionar, imprime
`Produto[7891000100103, Café 500g, R$ 19.90]` em vez de um arroba com
hexadecimal, e a diferença entre os dois é a diferença entre ler o problema
e caçá-lo. Vale sobrescrever `toString` em toda classe de domínio, mesmo
quando nenhum requisito pede.

## O resto de Object

Os três métodos deste capítulo são os que se sobrescrevem, e não são os
únicos que toda classe herda. A lista completa de `Object` é curta e vale
ser conhecida, porque todo objeto do programa responde a ela:

| Método | O que faz | Sobrescrever? |
| --- | --- | --- |
| `equals(Object)` | igualdade por conteúdo, quando sobrescrito | em todo tipo cujo valor é o conteúdo |
| `hashCode()` | o código de hash | sempre que `equals` for sobrescrito |
| `toString()` | a forma em texto | vale a pena em toda classe de domínio |
| `getClass()` | o objeto que representa o tipo real | impossível: é `final` |
| `clone()` | cópia rasa, sob um protocolo antigo e cheio de arestas | não; cópia se faz por construtor |
| `finalize()` | resto de um mecanismo de limpeza abandonado | não; o uso dele foi desativado |
| `wait()`, `notify()`, `notifyAll()` | coordenação entre execuções simultâneas | não; é assunto do capítulo 22 |

`getClass` devolve o tipo real do objeto em execução, o mesmo nome que
aparece no `Produto@6f2b958e` da seção anterior, e é a porta de entrada
das ferramentas do capítulo 23. As três últimas linhas da tabela
existem para serem reconhecidas e deixadas em paz: `clone` e `finalize`
são decisões antigas da linguagem que o código moderno não usa, e o trio
de espera pertence ao vocabulário de outro capítulo. Sobra o que este
capítulo tratou, e a razão de ele ter tratado: os três primeiros são os
únicos cuja versão herdada dá resposta errada para tipos do domínio.

## O caso BigDecimal

<div class="previsao">

O mesmo preço, escrito com e sem o zero final:

```java
BigDecimal a = new BigDecimal("2.50");
BigDecimal b = new BigDecimal("2.5");
IO.println(a.equals(b));
IO.println(a.compareTo(b));
```

Duas linhas de saída. Quais?

</div>

```
false
0
```

Para `equals`, os dois são diferentes; para `compareTo`, o método de
comparação do capítulo 7, valem o mesmo. `BigDecimal` guarda o valor e a
quantidade de casas, e o `equals` dele compara as duas coisas: 2.50 tem duas
casas, 2.5 tem uma, e a igualdade estrita recusa. É uma decisão documentada
da classe, não um defeito, e a consequência prática cabe numa regra:
igualdade de dinheiro se pergunta com `compareTo(...) == 0`, nunca com
`equals`. Levar essa regra para dentro de um `equals` nosso exige cuidado
com a cláusula do hash: um `equals` que iguala 2.5 a 2.50 precisa de um
`hashCode` que também os iguale, e o caminho seguro é normalizar a escala
do campo na entrada, fixando as casas com `setScale`, para `equals` e hash
enxergarem o mesmo valor. O sintoma de esquecer é o de sempre nesta família:
valores que são o mesmo preço na etiqueta e objetos que se dizem diferentes
no código.

<div class="aprofundamento">

**Hash e mutação.** O código de hash é calculado a partir dos campos; se um
campo que participa do hash mudar depois que o objeto entrou numa estrutura
de busca, o objeto fica arquivado na vizinhança do hash antigo e passa a ser
procurado na do novo, sumindo sem sair do lugar. É um dos motivos de os
campos de identidade, como o código de barras, serem `final`, e de os tipos
feitos para chave serem imutáveis por inteiro.

</div>

## Prática

1. Complete o `Produto` deste capítulo com `equals`, `hashCode` e `toString`
   sobrescritos, e reproduza a abertura obtendo `true` para as duas
   remessas.

2. Reproduza a armadilha da sobrecarga: mantenha `equals(Produto)`, mostre o
   par de saídas divergentes através de `Produto` e de `Object`, e depois
   anote a mensagem do compilador ao pôr `@Override` na versão errada.

3. Quebre a simetria de propósito: faça `Produto.equals` aceitar `String` de
   código de barras e demonstre `x.equals(y)` diferente de `y.equals(x)`.
   Desfaça e escreva em uma frase qual cláusula estava violada.

4. Sobrescreva `equals` sem `hashCode`, imprima os hashes das duas remessas
   iguais e explique por escrito qual cláusula do contrato ficou violada e
   onde isso vai doer no capítulo 17.

5. Escreva um método `mesmoPreco(Produto outro)` que compare os preços com
   `compareTo`, e demonstre um par de produtos com `equals` de preço `false`
   e `mesmoPreco` `true`.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| contrato de equals | as cláusulas que toda sobrescrita de `equals` deve cumprir |
| reflexividade | `x.equals(x)` é `true` |
| simetria | `x.equals(y)` e `y.equals(x)` respondem o mesmo |
| transitividade | iguais a um mesmo terceiro são iguais entre si |
| `hashCode` | devolve o código de hash; iguais por `equals` têm o mesmo hash |
| código de hash | `int` que acompanha o objeto; sobrescrito, deriva dos campos do `equals` |
| colisão de hash | objetos diferentes com o mesmo hash; permitida e inevitável |
| contrato de `toString` | descrição do objeto em texto, para gente ler; sem formato obrigatório |
| `Objects.equals(a, b)` | comparação que aceita `null` dos dois lados sem derrubar |
| `getClass()` | o tipo real do objeto em execução; herdado e `final` |

| Regra prática | |
| --- | --- |
| parâmetro do `equals` | sempre `Object`, com `@Override` |
| `equals` e `hashCode` | sobrescreve um, sobrescreve o outro, sobre os mesmos campos |
| dinheiro | igualdade com `compareTo(...) == 0`; campo `BigDecimal` em `equals` pede escala normalizada |
