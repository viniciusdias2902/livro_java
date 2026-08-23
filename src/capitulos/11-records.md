# Records e semântica de valor

O código de barras merece deixar de ser um `String` solto: como texto, ele
aceita qualquer conteúdo, e a validação de treze dígitos fica espalhada por
quem lembrar dela. A ferramenta dos capítulos 7 e 10 resolve, ao preço de um
ritual completo:

```java
public class CodigoDeBarras {
    private final String digitos;

    public CodigoDeBarras(String digitos) {
        if (digitos == null || !digitos.matches("\\d{13}")) {
            throw new IllegalArgumentException("Código de barras inválido: " + digitos);
        }
        this.digitos = digitos;
    }

    public String digitos() {
        return digitos;
    }

    @Override
    public boolean equals(Object outro) {
        if (this == outro) {
            return true;
        }
        if (!(outro instanceof CodigoDeBarras)) {
            return false;
        }
        CodigoDeBarras codigo = (CodigoDeBarras) outro;
        return digitos.equals(codigo.digitos);
    }

    @Override
    public int hashCode() {
        return digitos.hashCode();
    }

    @Override
    public String toString() {
        return "CodigoDeBarras[" + digitos + "]";
    }
}
```

Trinta e seis linhas, todas corretas, todas já justificadas por este livro, e
todas dizendo uma única ideia: um código de barras é treze dígitos, e dois
códigos com os mesmos dígitos são o mesmo código. O mercadinho vai precisar
do mesmo ritual para item de venda, para valor em dinheiro, para endereço de
entrega, e cada repetição manual é uma chance nova de errar como a
armadilha da sobrecarga mostrou: um parâmetro `Produto` onde devia ser `Object`, um
campo esquecido no `hashCode`, um `toString` desatualizado depois que um
campo entrou. Ritual previsível que se repete e dá margem a erro é trabalho
de compilador, e a linguagem o absorveu. O
`matches`, novidade pontual, pergunta se o texto casa com um padrão; o
`\\d{13}` descreve "treze dígitos", e a notação completa desses padrões fica
fora deste livro, com o essencial registrado na ficha.

## record

```java
public record CodigoDeBarras(String digitos) { }
```

Uma linha. A palavra `record` declara um tipo cuja definição é a lista entre
parênteses, os componentes do record, e o compilador gera o resto do ritual:
um campo `private final` por componente; o construtor canônico, que recebe
todos os componentes na ordem declarada; um método de acesso por componente,
com o mesmo nome dele, `digitos()`; e `equals`, `hashCode` e `toString`
sobre todos os componentes, este último no formato `Nome[componente=valor]`,
cumprindo o contrato de equals por inteiro. Um
record é imutável por construção: não existe forma de alterar um componente
depois do `new`, e a imutabilidade deixa de ser disciplina
para ser garantia.

O ganho de leitura vale tanto quanto o de digitação. A declaração de um
record é a forma dos dados, inteira, numa linha: quem abre o arquivo sabe
que não há estado escondido, que não há mutação possível, que a igualdade é
por conteúdo e cobre todos os componentes. Numa classe comum, cada uma
dessas propriedades exige ler a classe inteira para confirmar; no record,
elas são consequência da palavra-chave, e a leitura do tipo se resume à
leitura da lista.

<div class="previsao">

A abertura do capítulo 10, refeita com records:

```java
void main() {
    CodigoDeBarras primeira = new CodigoDeBarras("7891000100103");
    CodigoDeBarras segunda = new CodigoDeBarras("7891000100103");
    IO.println(primeira.equals(segunda));
    IO.println(primeira);
}
```

O que imprimem as duas linhas, sem nenhum método escrito à mão?

</div>

```
true
CodigoDeBarras[digitos=7891000100103]
```

Igualdade por conteúdo e impressão legível, de fábrica, porque o compilador
gerou as sobrescritas que antes se escreviam à mão. Saber escrevê-las
à mão continua sendo o que separa usar o record de entendê-lo: o record
não muda as regras do contrato, muda quem digita.

## Construtor compacto

A linha única perdeu a validação dos treze dígitos, e recuperá-la não exige
voltar ao ritual. O construtor compacto é um corpo de construtor escrito sem
repetir a lista de parâmetros, que roda antes de os componentes serem
atribuídos:

```java
public record CodigoDeBarras(String digitos) {
    public CodigoDeBarras {
        if (digitos == null || !digitos.matches("\\d{13}")) {
            throw new IllegalArgumentException("Código de barras inválido: " + digitos);
        }
    }
}
```

Sem parênteses depois do nome: essa é a grafia do compacto. Dentro dele, os
nomes dos componentes são os parâmetros recebidos, e o que o corpo pode
fazer é validar, como acima, ou normalizar, reatribuindo ao parâmetro
(`digitos = digitos.strip()`, com `strip` removendo espaços das pontas)
antes de a atribuição automática acontecer. As invariantes do capítulo 7
voltam inteiras, com uma linha de cerimônia a menos, e valem para todo
caminho de criação, porque todo caminho passa pelo canônico.

Um record também aceita construtores adicionais, com outras assinaturas,
desde que cada um comece delegando ao canônico com `this(...)`. É a porta
para conveniências como aceitar o código de barras com espaços de nota
fiscal, ou um item de venda com quantidade implícita de um:

```java
public ItemDeVenda(Produto produto) {
    this(produto, 1);
}
```

A delegação obrigatória garante que a validação do compacto rode sempre,
venha o objeto do caminho que vier; não existe caminho de criação que
contorne a validação do canônico.

## Semântica de valor

O nome do que o record materializa é semântica de valor: um tipo tem
semântica de valor quando seus exemplares valem pelo conteúdo, e dois
exemplares de mesmo conteúdo são intercambiáveis em qualquer uso. É o regime
dos primitivos, o `7` de uma conta é o `7` de outra, e o oposto do regime
de identidade, em que cada objeto é ele mesmo. O ritual da abertura constrói
semântica de valor à mão, sobrescrevendo o contrato; o record a declara de
nascença.

A régua para o mercadinho separa os tipos em duas famílias. Têm semântica de
valor os que descrevem: código de barras, um item de venda com produto e
quantidade, um valor em dinheiro. Têm identidade os que vivem: o `Produto`
com estoque que sobe e desce continua classe, porque duas remessas do mesmo
café são o mesmo produto com histórias diferentes, e estado mutável não cabe
em record. A regra prática: dado imutável que vale pelo conteúdo vira
record; entidade com ciclo de vida vira classe. Na dúvida, a pergunta é "faz
sentido trocar um pelo outro de mesmo conteúdo?", e a resposta sim aponta o
record. No código profissional, os records se concentraram exatamente
nesses papéis: retratos de dados que atravessam fronteiras, a linha de um
relatório, o resultado de uma consulta, a resposta que um sistema envia a
outro, todos dados que nascem prontos, viajam e não mudam no caminho. O capítulo
12 apresenta a forma de abrir um record em padrões, componente a
componente.

Records participam do resto da linguagem sem regalias: aceitam métodos
próprios, membros `static` e `implements` de interface; o que não aceitam é
`extends`, nem para estender nem para serem estendidos, porque herança de
estado e valor imutável não se misturam bem, e campos de instância fora da
lista de componentes também não existem. Um item de venda mostra o formato
típico, componente mais método derivado:

```java
public record ItemDeVenda(Produto produto, int quantidade) {
    public ItemDeVenda {
        if (quantidade <= 0) {
            throw new IllegalArgumentException("Quantidade inválida: " + quantidade);
        }
    }

    public BigDecimal subtotal() {
        return produto.precoPara(quantidade);
    }
}
```

<div class="armadilha">

Um record para as pesagens do dia da balança do queijo:

```java
public record PesagensDoDia(int[] gramas) { }

void main() {
    PesagensDoDia manha = new PesagensDoDia(new int[] { 250, 400 });
    PesagensDoDia copia = new PesagensDoDia(new int[] { 250, 400 });
    IO.println(manha.equals(copia));
    IO.println(manha);
}
```

```
false
PesagensDoDia[gramas=[I@76ed5528]
```

O mesmo conteúdo deu `false`, e a impressão saiu ilegível.

</div>

O `equals` gerado compara cada componente com o `equals` do componente, e o
`equals` de array é o herdado de `Object`, identidade, pelo capítulo 5: dois
arrays de mesmo conteúdo são objetos diferentes. O `toString` do array é o
herdado também, daí o `[I@` com hexadecimal. E há um furo pior: o array é
mutável, e alguém com a referência pode alterar as pesagens por fora,
minando a promessa de valor imutável. A regra que fecha as três frestas de
uma vez: componente de record deve ser imutável e ter igualdade por
conteúdo, como `String`, `BigDecimal`, primitivos e outros records. Sequência
de valores dentro de record espera o tipo certo de recipiente, que o
capítulo 17 apresenta.

Duas notas fecham a regra do componente. `ItemDeVenda` carrega um `Produto`,
entidade mutável, sem violar o que importa: a igualdade de `Produto` se
apoia no código de barras `final`, e o `equals` e o hash do item não se
movem quando o estoque muda. Componente pode ser entidade cuja igualdade é
estável; o que não pode é igualdade instável ou por identidade. E componente
`BigDecimal` herda a igualdade estrita de escala do capítulo 10: dois
records com 95.0 e 95.00 no mesmo componente não se igualam. Dinheiro que
participa da igualdade de um record pede escala fixada na entrada, no
construtor compacto, com `setScale(2)`, o método de `BigDecimal` que fixa a
quantidade de casas.

<div class="aprofundamento">

**Acessor sem `get`.** O record consolidou a grafia `digitos()` para leitura
de componente, mas quase todo código anterior a ele segue a convenção
`getDigitos()`, dos tempos em que ferramentas descobriam propriedades pelo
prefixo. As duas grafias convivem no mundo real e dizem a mesma coisa; o
apêndice de legado volta ao assunto.

</div>

## Prática

1. Escreva o record `CodigoDeBarras` com validação e normalização no
   construtor compacto, e prove com impressões: igualdade por conteúdo,
   recusa de código curto, espaços removidos das pontas.

2. Converta `Produto` para carregar um `CodigoDeBarras` em vez de `String`,
   delegando `equals` e `hashCode` ao record, e refaça a abertura do
   capítulo 10 com a versão nova.

3. Escreva `ItemDeVenda` completo e um `main` que monte três itens, imprima
   cada um e some os subtotais com `BigDecimal`. Compare a legibilidade da
   impressão gerada com a que você escreveria à mão.

4. Reproduza a armadilha do componente array e conserte da forma primitiva
   disponível: guarde as pesagens como `String` no formato "250;400" e
   converta ao ler. Anote o que essa gambiarra custa e o que o capítulo 17
   promete no lugar dela.

5. Decida, para cada tipo do mercadinho até aqui, record ou classe:
   `Produto`, `CodigoDeBarras`, `ItemDeVenda`, `Carrinho`, `Caixa`,
   `MeioDePagamento` e implementações. Justifique cada decisão em uma linha,
   pela régua da semântica de valor.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| record | tipo declarado pela lista de componentes; imutável, com o ritual gerado |
| componente de record | cada item da lista; vira campo `final`, acessor e parte do `equals` |
| construtor canônico | o construtor com todos os componentes, na ordem declarada |
| construtor compacto | corpo sem lista de parâmetros, para validar e normalizar antes da atribuição |
| semântica de valor | exemplares valem pelo conteúdo; iguais são intercambiáveis |

| Regra prática | |
| --- | --- |
| record × classe | dado imutável que vale pelo conteúdo × entidade com ciclo de vida |
| componente | imutável e com igualdade por conteúdo; array não |
| `\d{13}` em `matches` | padrão de texto "treze dígitos"; a notação completa fica fora do livro |
