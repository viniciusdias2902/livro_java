# Herança, polimorfismo e composição

O mercadinho vende café em pacote fechado e queijo fatiado na hora: um tem
preço por unidade, o outro por quilo. Com o capítulo 7, a saída natural
seria uma segunda classe, `ProdutoPorPeso`, copiando de `Produto` o nome, as
validações e tudo o mais, e mudando só o cálculo do preço. A cópia funciona
no primeiro dia e começa a cobrar no segundo: cada correção em uma classe precisa
ser lembrada na outra, e a que for esquecida diverge em silêncio. A
linguagem tem um mecanismo para "é igual àquela, exceto em": a herança.

```java
class Produto {
    private final String nome;
    private final BigDecimal preco;

    Produto(String nome, BigDecimal preco) {
        // validações do capítulo 7
        this.nome = nome;
        this.preco = preco;
    }

    public String nome() {
        return nome;
    }

    public BigDecimal preco() {
        return preco;
    }

    public BigDecimal precoPara(int quantidade) {
        return preco.multiply(new BigDecimal(quantidade));
    }

    public String etiqueta() {
        return nome + ", R$ " + preco;
    }
}

class ProdutoPorPeso extends Produto {
    ProdutoPorPeso(String nome, BigDecimal precoPorQuilo) {
        super(nome, precoPorQuilo);
    }

    @Override
    public String etiqueta() {
        return super.etiqueta() + " o quilo";
    }
}
```

O estoque do capítulo 7 sai de cena nestes trechos, para cada exemplo
mostrar só o que muda; na classe do projeto ele continua onde estava, com
as validações.

## extends, superclasse e subclasse

Herança é o mecanismo em que uma classe estende outra, recebendo os campos e
os métodos dela e podendo acrescentar os seus ou redefinir os herdados. A
palavra `extends` declara a relação: `Produto` é a superclasse,
`ProdutoPorPeso` é a subclasse. Uma instância de `ProdutoPorPeso` é um
`Produto` no sentido pleno: carrega os campos da superclasse e responde a
todos os métodos dela.

O que se herda tem fronteiras precisas, e três delas evitam surpresa.
Primeira: construtores não são herdados. Cada classe declara os seus, e o
construtor da subclasse abre com `super(...)`, a chamada ao construtor da
superclasse, obrigatória antes de qualquer outra coisa; é por ela que as
validações do capítulo 7 continuam protegendo o nascimento, e um
`ProdutoPorPeso` de nome vazio é recusado pela mesma linha que recusa um
`Produto` de nome vazio. Segunda: campo `private` da superclasse existe
dentro do objeto da subclasse, mas continua invisível até para ela; quem o
acessa são os métodos da própria superclasse, e a subclasse os usa como
qualquer outro código usa. Terceira: a herança pode ser proibida. O
modificador `final`, aplicado a uma classe, veta o `extends`
(`String` é uma classe `final`, e é em parte por isso que a imutabilidade
dela é uma garantia, não um costume); aplicado a um método, veta a
sobrescrita daquele método, deixando o resto da classe aberto. Uma classe
que não foi desenhada para ser estendida declara isso com `final`, e o
compilador passa a defender a decisão.

## Sobrescrita e @Override

Redefinir na subclasse um método herdado chama-se sobrescrita, e é o que
`etiqueta()` fez: a versão de `ProdutoPorPeso` substitui a herdada, podendo
aproveitá-la por dentro com `super.etiqueta()`, a chamada da versão da
superclasse. A linha `@Override` em cima do método é uma anotação: uma marca
no código, lida pelo compilador e por ferramentas, que não muda o
comportamento. Essa anotação específica pede ao compilador que confira se o
método de fato sobrescreve algo, e a armadilha abaixo mostra o que acontece
sem essa conferência.

<div class="armadilha">

O queijo custa R$ 39,80 o quilo, e a subclasse calcula o preço por gramas:

```java
class ProdutoPorPeso extends Produto {
    // construtor como antes

    public BigDecimal precoPara(long gramas) {
        return preco().multiply(new BigDecimal(gramas))
                      .divide(new BigDecimal(1000));
    }
}

void main() {
    Produto queijo = new ProdutoPorPeso("Queijo minas", new BigDecimal("39.80"));
    IO.println(queijo.precoPara(250));
}
```

```
9950.00
```

Duzentos e cinquenta gramas de queijo saíram por nove mil, novecentos e
cinquenta reais: o programa cobrou 250 unidades de R$ 39,80.

</div>

O método novo recebe `long`; o herdado recebe `int`. Assinaturas diferentes
não sobrescrevem: convivem, como sobrecarga. Pela variável `queijo`, de tipo
`Produto`, a versão de `long` nem é visível, e a chamada vai direto à
herdada, que multiplica por unidade; mesmo por uma variável do subtipo, o
argumento `250`, um `int`, prefere a versão herdada de `int`, pela regra do
tipo mais estreito do capítulo 4. Nenhum caminho comum chega ao método
novo, nenhum erro aparece, e a diferença só existe na conta do cliente.
Com `@Override` escrito sobre o método, o compilador teria recusado na hora,
avisando que `precoPara(long)` não sobrescreve nada. Daí a regra, curta:
toda sobrescrita carrega `@Override`, sempre, porque a anotação transforma
esse engano silencioso em erro de compilação.

## Polimorfismo e despacho dinâmico

A herança paga o preço da hierarquia quando o código trata tudo pelo tipo da
superclasse:

<div class="previsao">

Um carrinho misto:

```java
void main() {
    Produto[] carrinho = {
        new Produto("Café 500g", new BigDecimal("19.90")),
        new ProdutoPorPeso("Queijo minas", new BigDecimal("39.80"))
    };
    for (Produto item : carrinho) {
        IO.println(item.etiqueta());
    }
}
```

A variável do laço tem tipo `Produto` nas duas voltas. Qual `etiqueta()`
roda para o queijo?

</div>

```
Café 500g, R$ 19.90
Queijo minas, R$ 39.80 o quilo
```

A do queijo, com "o quilo" no fim. Isso é polimorfismo: referências do tipo
da superclasse apontando para objetos de subtipos variados, com cada chamada
de método atendida pela versão do objeto real, não pela do tipo da variável.
A escolha acontece durante a execução, objeto a objeto, e tem nome: despacho
dinâmico. É o inverso da sobrecarga do capítulo 4: a sobrecarga é resolvida
pelo compilador, olhando o tipo escrito do argumento; a sobrescrita é
resolvida pela JVM, na hora, olhando o objeto real. Os dois mecanismos
convivem na mesma chamada, cada um decidindo a sua metade.

Para o mercadinho, a consequência prática vale ser dita por inteiro. O laço
do carrinho foi escrito conhecendo só `Produto`, e continua correto para
subtipos que ainda não existem: no dia em que o mercadinho passar a vender
produto com desconto de validade próxima, a classe nova entra, sobrescreve o
cálculo, e o caixa, o carrinho e os relatórios somam certo sem uma linha
editada. Código que ganha comportamento novo sem ser tocado é o que o
polimorfismo compra, e é a diferença entre acrescentar uma classe e caçar
todos os `if` do sistema.

## Object, casts e instanceof

Toda classe sem `extends` estende `Object`, a superclasse de todas:
`Produto` estende `Object` sem que ninguém tenha pedido, e a cadeia
completa do queijo é `Object`, depois `Produto`, depois `ProdutoPorPeso`. Duas consequências saem desse desenho. A
primeira: uma variável do tipo `Object` aceita referência para qualquer
objeto, o que dá à biblioteca padrão um jeito de escrever código que serve
para todos os tipos de uma vez; o custo e o conserto desse truque são o
assunto do capítulo 16. A segunda: `Object` declara métodos que toda classe
herda, entre eles o `equals` conhecido do capítulo 5, e o capítulo 10 é
inteiro sobre o que esses métodos prometem e como sobrescrevê-los bem.

Guardar um `ProdutoPorPeso` numa variável `Produto`, como o carrinho fez, é
um upcast: a conversão implícita para o tipo mais geral, sempre segura,
porque a subclasse responde a tudo que a superclasse promete. O caminho de
volta é o downcast, escrito como o casting do capítulo 3, e ele é uma
aposta:

```java
Produto item = carrinho[1];
ProdutoPorPeso porPeso = (ProdutoPorPeso) item;
```

Se o objeto real não for um `ProdutoPorPeso`, a linha derruba o programa com
um erro de execução chamado `ClassCastException`, na hora do cast. A
pergunta que evita a queda é o `instanceof`, que responde `true` quando o
objeto real é do tipo perguntado:

```java
if (item instanceof ProdutoPorPeso) {
    ProdutoPorPeso porPeso = (ProdutoPorPeso) item;
    // trato especial
}
```

Vale registrar o sinal de alerta: um código que enfileira `instanceof` para tratar
cada subtipo de um jeito está refazendo à mão o que o despacho dinâmico faz
sozinho, e cada subtipo novo exige lembrar de mais um `if`. Quando o
comportamento varia por tipo, o lugar dele é um método sobrescrito; o
capítulo 9 dá a essa ideia a forma definitiva.

## Composição e delegação

Nem toda relação entre classes é "é um". O carrinho de compras do mercadinho
tem produtos, e tem-um se modela guardando referências, o que se chama
composição:

```java
class Carrinho {
    private final Produto[] itens;
    private final int[] quantidades;
    // construtor e validações omitidos

    public BigDecimal total() {
        BigDecimal soma = BigDecimal.ZERO;
        for (int i = 0; i < itens.length; i++) {
            soma = soma.add(itens[i].precoPara(quantidades[i]));
        }
        return soma;
    }
}
```

`Carrinho` não estende coisa nenhuma: contém. E o `total()` não calcula
preço de produto; pede a cada item que calcule o seu, via `precoPara`, e
soma. Encaminhar trabalho para um objeto contido chama-se delegação, e o
polimorfismo continua valendo dentro dela: o item por peso responde com a
conta por peso. Os dois arrays lado a lado reabrem, de propósito, a dívida
da abertura do capítulo 7: aqui dentro, escondidos pelo encapsulamento e
mantidos por uma classe só, eles têm um dono; ainda assim são dívida, e o
capítulo 11 dá ao par produto-quantidade a forma definitiva. `BigDecimal.ZERO`, de passagem, é uma constante
`static final` da própria classe, irmã das constantes da seção de
`static`.

A escolha entre herança e composição tem uma regra que envelheceu bem:
herança só quando cada subclasse é um caso genuíno da superclasse, no
domínio, e o resto é composição. Herança amarra forte: tudo que a
superclasse muda, as subclasses sentem. Composição depende só do essencial:
o `Carrinho` conhece apenas as promessas públicas de `Produto`. Na dúvida entre as
duas, composição, e o arrependimento é menor.

<div class="aprofundamento">

**Como a JVM despacha.** Cada classe carregada tem uma tabela com o endereço
da versão de cada método que vale para ela; sobrescrever um método troca a
entrada na tabela da subclasse. Uma chamada polimórfica consulta a tabela do
objeto real, e é por isso que o despacho custa quase nada e não depende de
quantos subtipos existem.

</div>

## Prática

1. Implemente `Produto` e `ProdutoPorPeso` completos, com o preço por gramas
   correto na subclasse, `@Override` em toda sobrescrita e as validações do
   capítulo 7. Imprima a etiqueta e o preço de 250 gramas de um queijo de
   R$ 39,80 o quilo.

2. Reproduza a armadilha da sobrecarga acidental: remova o `@Override`,
   troque o tipo do parâmetro e documente a conta errada. Devolva o
   `@Override` e anote a mensagem exata do compilador.

3. Acrescente uma terceira subclasse, `ProdutoComDesconto`, que sobrescreva
   `precoPara` aplicando um percentual de desconto recebido no construtor,
   com validação do percentual. Ponha os três tipos num mesmo array e some o
   carrinho sem nenhum `instanceof`.

4. Escreva um trecho que provoque `ClassCastException` de propósito, depois
   o conserte com `instanceof`, e por fim explique por escrito por que a
   versão do exercício 3 é melhor que as duas.

5. Modele com composição um `Combo` de café da manhã: um nome próprio e um
   conjunto de produtos, com `total()` delegando o preço a cada um. Escreva
   em um parágrafo por que `Combo extends Produto` seria uma modelagem pior.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| herança (`extends`) | uma classe estende outra, herdando campos e métodos |
| superclasse / subclasse | a classe estendida / a classe que estende |
| `super` | chamada ao construtor ou ao método da superclasse |
| sobrescrita | redefinição, na subclasse, de um método herdado; mesma assinatura |
| anotação | marca no código lida por ferramentas; `@Override` confere a sobrescrita |
| polimorfismo | referências do tipo base atendidas pela versão do objeto real |
| despacho dinâmico | a escolha do método pelo objeto, em execução |
| `Object` | superclasse de todas as classes |
| upcast | conversão implícita para o tipo mais geral; sempre segura |
| downcast | cast para o subtipo; sujeito a `ClassCastException` |
| `instanceof` | pergunta se o objeto real é do tipo dado |
| `ClassCastException` | erro de execução de um downcast errado |
| composição | objeto que contém referências a outros ("tem-um") |
| delegação | encaminhar trabalho ao objeto contido |
