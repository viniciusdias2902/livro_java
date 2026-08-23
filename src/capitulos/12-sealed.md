# Sealed types, enums e pattern matching

A categoria de cada produto do mercadinho decide o corredor da prateleira e
o relatório em que a venda entra, e a primeira versão a guarda como texto:

```java
Produto cafe = new Produto("7891000100103", "Café 500g", new BigDecimal("19.90"), "mercearia");

if (cafe.categoria().equals("Mercearia")) {
    IO.println("Corredor 3");
}
```

O `if` nunca acha o corredor, porque a categoria foi gravada com minúscula e
comparada com maiúscula. `String` aceita qualquer conteúdo: "mercearia",
"Mercearia", "merceária" e um erro de digitação são quatro valores
diferentes e todos válidos, e o compilador não tem como saber que o domínio
só reconhece meia dúzia de categorias. O problema é de tipo: categoria não é
texto livre, é uma escolha numa lista fechada, e a linguagem tem uma
declaração exatamente para isso.

## enum: a lista fechada de valores

```java
public enum Categoria {
    MERCEARIA, HORTIFRUTI, LIMPEZA, BEBIDAS;
}
```

Um enum é um tipo cujos valores possíveis são declarados um a um, na própria
definição, e acabou: não existe quinto valor de `Categoria`, nem errado de
digitação, nem fora da lista. Cada nome declarado é uma constante de enum,
um objeto único daquele tipo, criado pela JVM; `Categoria.MERCEARIA` é o
mesmo objeto em qualquer ponto do programa, e por isso enum se compara com
`==` sem o risco do capítulo 5: identidade e conteúdo coincidem quando cada
valor existe uma vez só. O campo do produto vira
`private final Categoria categoria`, o construtor recebe o tipo em vez de
texto, e o erro da abertura morre na compilação: `new Produto(...,
"mercearia")` nem compila, porque `String` não é `Categoria`.

O pagamento prometido no capítulo 4 vem no switch. Com um `int` na entrada,
o `default` era obrigatório, porque o compilador não conhecia os valores
possíveis; com um enum, ele conhece todos:

```java
public int corredor(Categoria categoria) {
    return switch (categoria) {
        case MERCEARIA -> 3;
        case HORTIFRUTI -> 1;
        case LIMPEZA -> 4;
        case BEBIDAS -> 2;
    };
}
```

Sem `default`, e compila. Essa é a exaustividade: a garantia, conferida pelo
compilador, de que o switch cobre todos os casos possíveis do valor. Ela
parece detalhe até a lista crescer, e a armadilha abaixo mostra os dois
lados.

<div class="armadilha">

Um switch de enum escrito com `default`, por hábito:

```java
public int corredor(Categoria categoria) {
    return switch (categoria) {
        case MERCEARIA -> 3;
        case HORTIFRUTI -> 1;
        default -> 4;
    };
}
```

Meses depois, o mercadinho ganha padaria, e `PADARIA` entra no enum. O
programa inteiro recompila sem um aviso. Onde o pão vai parar?

</div>

No corredor 4, junto com a limpeza. O `default` engoliu o caso novo: para o
compilador, `PADARIA` está coberta, e a exaustividade que ele conferiria foi
desligada por quem escreveu `default`. Sem o `default`, a recompilação
falharia em cada switch que esqueceu a padaria, com a lista exata dos
lugares a atualizar, que é o comportamento desejável quando o domínio
cresce. A regra que sai daí: switch sobre enum não leva `default`; cobrir
todos os casos por extenso é o que mantém o compilador de guarda.

Constantes de enum aceitam dados e comportamento próprios, porque enum é uma
classe com nascimento controlado. O corredor pertence mais à categoria do
que ao método solto acima:

```java
public enum Categoria {
    MERCEARIA(3), HORTIFRUTI(1), LIMPEZA(4), BEBIDAS(2);

    private final int corredor;

    Categoria(int corredor) {
        this.corredor = corredor;
    }

    public int corredor() {
        return corredor;
    }
}
```

O construtor de enum roda uma vez por constante, na carga do tipo, e não é
chamável com `new`: as constantes só nascem na lista do topo. Campos e métodos
seguem as regras normais dos capítulos 7 em diante.

## sealed: hierarquia fechada

O enum fecha uma lista de valores; falta fechar uma lista de tipos. O caixa
do capítulo 9 devolve o resultado de um pagamento, e resultado não é um
valor único: aprovado carrega o valor cobrado, recusado carrega um motivo.
São tipos diferentes com dados diferentes, e a hierarquia aberta do capítulo
8 deixaria qualquer um criar um resultado novo que o resto do sistema não
trata. A palavra `sealed` fecha a hierarquia:

```java
public sealed interface Resultado permits Aprovado, Recusado { }

public record Aprovado(BigDecimal valorCobrado) implements Resultado { }

public record Recusado(String motivo) implements Resultado { }
```

Uma interface ou classe `sealed` declara em `permits` a lista completa de
quem pode implementá-la ou estendê-la; qualquer tipo fora da lista é erro de
compilação. Cada tipo permitido declara o próprio destino: records e classes `final`
encerram o ramo; um tipo permitido pode seguir fechado, declarando-se
`sealed` com a própria lista; e `non-sealed` reabre o ramo para herança
livre, o que é raro e deliberado. O casamento com o capítulo 11 é
natural: os ramos de uma hierarquia selada costumam ser records, dados
imutáveis com o contrato pronto, e o conjunto descreve "um resultado é isto
ou aquilo, com estes dados em cada caso".

## Pattern matching

Falta consumir o resultado, e é aqui que entra o recurso que amarra o
capítulo. Pattern matching (casamento de padrões) é comparar um valor contra
um padrão que, ao casar, já extrai as partes. A forma mais simples é o
padrão de tipo, que aposenta o par instanceof-e-cast do capítulo 8:

```java
if (resultado instanceof Recusado recusado) {
    IO.println("Recusado: " + recusado.motivo());
}
```

O `instanceof` com uma variável ao lado pergunta e converte num passo só:
casando, `recusado` nasce já com o tipo certo, no escopo do `if`, e o
downcast manual desaparece junto com o risco de `ClassCastException`. Sobre
uma hierarquia selada, o switch com padrões de tipo ganha a exaustividade do
enum:

```java
public String linhaDoRecibo(Resultado resultado) {
    return switch (resultado) {
        case Aprovado aprovado -> "Pago: R$ " + aprovado.valorCobrado();
        case Recusado recusado -> "Recusado: " + recusado.motivo();
    };
}
```

Sem `default`, porque `permits` disse ao compilador que a lista acabou; a
mesma regra da armadilha do enum vale inteira aqui. E quando o ramo é um
record, o padrão de registro (*record pattern*) desestrutura os componentes
na própria cláusula:

```java
return switch (resultado) {
    case Aprovado(BigDecimal valor) -> "Pago: R$ " + valor;
    case Recusado(String motivo) -> "Recusado: " + motivo;
};
```

`Aprovado(BigDecimal valor)` casa com um `Aprovado` e já entrega o
componente na variável `valor`, sem acessor e sem variável intermediária: é
a resposta à promessa deixada no capítulo 11.

<div class="previsao">

O mercadinho passa a aceitar estorno, e `Estornado` entra na hierarquia:

```java
public sealed interface Resultado permits Aprovado, Recusado, Estornado { }

public record Estornado(BigDecimal valorDevolvido) implements Resultado { }
```

Nenhum switch do sistema foi tocado. O que acontece na recompilação?

</div>

Cada switch sobre `Resultado` sem o caso novo vira um erro de compilação,
com a mensagem `the switch expression does not cover all possible input
values`; quem aponta os lugares a atualizar é a lista dos próprios erros,
cada um com arquivo e linha. É a mesma mecânica
da armadilha do enum, agora a favor: o compilador entrega a lista completa
dos pontos do sistema que precisam aprender o que fazer com um estorno, e
nada compila até todos decidirem. A dupla sealed e switch exaustivo
transforma "esquecemos de tratar um caso", o defeito silencioso clássico das
cascatas do capítulo 9, em tarefa listada pelo compilador.

<div class="aprofundamento">

**Tipos de soma.** A dupla "hierarquia fechada de records" mais "switch
exaustivo com desestruturação" reproduz em Java o que outras linguagens
chamam de tipos de soma ou uniões etiquetadas: o dado é um entre poucos
formatos conhecidos, e o consumo é obrigado a tratar todos. Enum é o caso
degenerado, soma de valores sem dados; sealed com records é a forma geral.

</div>

## Prática

1. Converta a categoria do `Produto` para o enum com corredor e refaça a
   abertura do capítulo: mostre o erro de compilação ao tentar passar texto
   e o corredor certo saindo de `categoria().corredor()`.

2. Reproduza a armadilha: switch de enum com `default`, categoria nova, pão
   no corredor errado. Depois remova o `default` e anote a mensagem exata do
   compilador para cada switch desatualizado.

3. Implemente `Resultado` com os três ramos, faça o `Caixa` do capítulo 9
   devolver `Resultado` em vez de valor cru (recusando pagamento acima de um
   limite, por exemplo) e escreva `linhaDoRecibo` com padrões de registro.

4. Acrescente um quarto ramo, `EmAnalise`, sem dados. Decida entre record
   vazio e outra forma, siga os erros de compilação até o sistema inteiro
   tratá-lo, e conte quantos lugares o compilador listou por você.

5. Volte ao exercício 3 do capítulo 8 e reescreva o trecho que usava
   `instanceof` com cast para a forma com padrão de tipo, comparando as duas
   versões por escrito.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| enum | tipo com a lista fechada e nomeada de valores possíveis |
| constante de enum | cada valor declarado; objeto único, comparável com `==` |
| exaustividade | garantia do compilador de que o switch cobre todos os casos |
| `sealed` / `permits` | hierarquia fechada, com a lista completa de subtipos declarada |
| `non-sealed` | reabre um ramo de hierarquia selada para herança livre |
| pattern matching | comparar contra um padrão que, casando, extrai as partes |
| padrão de tipo | `instanceof Tipo nome`: pergunta e converte num passo |
| padrão de registro | `case Tipo(componentes)`: casa e desestrutura o record |

| Regra prática | |
| --- | --- |
| switch sobre enum ou sealed | sem `default`, para o compilador cobrar os casos novos |
| ramos de hierarquia selada | de preferência records, imutáveis e com contrato pronto |
