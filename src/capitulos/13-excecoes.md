# Exceções

O caixa do mercadinho pergunta a quantidade e o operador, com pressa, digita
o nome do número:

```java
void main() {
    String resposta = IO.readln("Quantidade: ");
    int quantidade = Integer.parseInt(resposta);
    IO.println("Registrado: " + quantidade);
}
```

```console
$ java Caixa.java
Quantidade: duas
Exception in thread "main" java.lang.NumberFormatException: For input string: "duas"
	at java.base/java.lang.NumberFormatException.forInputString(NumberFormatException.java:64)
	at java.base/java.lang.Integer.parseInt(Integer.java:565)
	at java.base/java.lang.Integer.parseInt(Integer.java:662)
	at Caixa.main(Caixa.java:3)
```

O programa caiu, e um caixa que cai por erro de digitação não serve para o
balcão. O capítulo 5 prometeu que sobreviver a isso era assunto para este
capítulo, e a promessa vence agora. Desde o capítulo 2 o livro provoca erros
de execução e lê as mensagens deles; o que faltava era o mecanismo por trás,
e ele muda a pergunta: não "como evitar toda queda", mas "quem decide o que
acontece quando algo dá errado".

## A exceção é um objeto

Tudo que este livro chamou de erro de execução tem um nome próprio na
linguagem: exceção. Uma exceção é um objeto, dos comuns, criado no instante
do problema: carrega uma mensagem, o tipo que classifica o problema
(`NumberFormatException`, `NullPointerException` e as demais conhecidas) e
um retrato da pilha de chamadas do momento. O `throw` é quem
lança esse objeto, e a biblioteca faz o mesmo por dentro: o
`parseInt` da abertura executa um `throw new NumberFormatException(...)`
quando o texto não é número.

Lançada, a exceção interrompe o fluxo normal no ato: a linha seguinte não
roda. Ela então sobe pela pilha de chamadas, encerrando cada
método no caminho, à procura de alguém disposto a tratá-la; essa subida
chama-se propagação. Quando ninguém trata e a propagação passa do `main`, a
JVM encerra o programa e imprime o que a abertura mostrou. Toda queda que o
livro provocou até aqui foi exatamente isto: uma exceção que propagou até o
fim sem encontrar tratador.

A transcrição da queda tem nome, stack trace: o retrato da pilha, impresso
de cima para baixo do ponto do problema até o `main`. Lê-se assim: a
primeira linha dá o tipo e a mensagem; cada linha `at` é um método que
estava em andamento, com arquivo e linha; as de `java.base` são o interior
da biblioteca, com números de linha que variam de uma versão de JDK para
outra, e a primeira linha com um arquivo nosso, `Caixa.java:3`,
aponta onde o nosso código entrou na história. Em stack traces longos, achar
a linha do próprio programa é o primeiro gesto da leitura.

## try e catch

Tratar é declarar-se disposto a receber a exceção:

```java
void main() {
    int quantidade = -1;
    while (quantidade < 0) {
        String resposta = IO.readln("Quantidade: ");
        try {
            quantidade = Integer.parseInt(resposta);
        } catch (NumberFormatException erro) {
            IO.println("Não entendi \"" + resposta + "\". Digite um número.");
        }
    }
    IO.println("Registrado: " + quantidade);
}
```

```console
$ java Caixa.java
Quantidade: duas
Não entendi "duas". Digite um número.
Quantidade: 2
Registrado: 2
```

O bloco `try` delimita o trecho vigiado; o `catch` declara o tipo de exceção
que aceita e recebe o objeto numa variável, como um parâmetro. Dando tudo
certo, o `catch` é ignorado; lançada uma exceção do tipo declarado dentro do
`try`, a execução salta o resto do bloco e entra no `catch`, e o programa
segue vivo depois dele. O laço em volta transforma o tratamento em política:
pergunta de novo até vir número. Um `try` aceita vários `catch`, um por
tipo, avaliados na ordem, e o polimorfismo vale aqui: `catch (Exception erro)`
apanha qualquer exceção do livro, porque todas descendem de `Exception`.
A ordem entre eles é conferida pelo compilador: um `catch` de tipo geral
escrito antes de um mais específico deixa o segundo inalcançável, e a
compilação falha. Quando dois tipos diferentes pedem o mesmo tratamento,
o multi-catch os junta num bloco só, com barra vertical entre eles:

```java
try {
    registrar(linha);
} catch (NumberFormatException | ArrayIndexOutOfBoundsException erro) {
    IO.println("Linha malformada, ignorada: " + linha);
}
```

A variável de um multi-catch é `final` sem que se escreva, e o tipo dela é
o ancestral comum dos tipos listados, de modo que só os métodos desse
ancestral estão disponíveis dentro do bloco. Os tipos listados também não
podem ter parentesco entre si: com um sendo subclasse do outro, o mais
geral já cobriria o caso, e a lista seria redundante.
Existe uma família irmã, `Error`, das falhas da própria JVM, como o
`StackOverflowError` do capítulo 4; ela fica fora dessa rede, e é melhor
assim, porque não há tratamento sensato para a pilha estourada. A armadilha
adiante mostra por que mesmo a rede das exceções costuma ser larga demais.

<div class="previsao">

A propagação atravessando dois métodos:

```java
int converter(String texto) {
    IO.println("antes do parse");
    int valor = Integer.parseInt(texto);
    IO.println("depois do parse");
    return valor;
}

void main() {
    try {
        IO.println("vou converter");
        int quantidade = converter("duas");
        IO.println("converti: " + quantidade);
    } catch (NumberFormatException erro) {
        IO.println("não deu: " + erro.getMessage());
    }
    IO.println("caixa segue aberto");
}
```

Cinco `IO.println` no fonte. Quais rodam, e em que ordem?

</div>

```
vou converter
antes do parse
não deu: For input string: "duas"
caixa segue aberto
```

O "depois do parse" e o "converti" nunca rodam: a exceção nasceu dentro de
`parseInt`, encerrou `converter` no meio e continuou subindo até o `catch`
do `main`, pulando tudo que estava entre o ponto do lançamento e o
tratador. Depois do `catch`, o fluxo normal volta. A propagação atravessa
quantos métodos houver, e é isso que permite tratar o erro longe de onde ele
nasce, no nível que tem contexto para decidir; o método `getMessage`, usado
no tratador, devolve a mensagem que o criador da exceção escreveu.

<div class="armadilha">

Um tratamento escrito para "não deixar o caixa cair de jeito nenhum":

```java
BigDecimal total = BigDecimal.ZERO;
for (ItemDeVenda item : itens) {
    try {
        total = total.add(item.subtotal());
    } catch (Exception erro) {
    }
}
IO.println("Total do dia: " + total);
```

O caixa nunca cai. O fechamento do dia bate com o dinheiro na gaveta?

</div>

Não há como saber, e esse é o dano. O `catch` vazio engole qualquer exceção
sem registrar nada: um item com produto nulo, um subtotal que estourou uma
validação, qualquer defeito vira uma venda silenciosamente ausente do
total, e a primeira notícia é a diferença no caixa, dias depois, sem pista.
Engolir exceção é o bug silencioso em estado puro, e a rede
`catch (Exception ...)` agrava, porque apanha até os erros de programação
que deveriam derrubar e ser corrigidos. As duas regras que evitam o buraco:
captura-se o tipo mais específico que se sabe tratar, e todo `catch` faz
alguma coisa, nem que seja registrar e relançar. O registro mínimo, num
programa sem biblioteca de registro configurável, é
`erro.printStackTrace()`, que imprime o mesmo retrato da queda sem
derrubar o programa; sistemas maiores trocam a chamada por um registrador
que decide destino e nível, e o que não muda é a exigência de o erro
deixar rastro em algum lugar. Cair com stack trace é
melhor do que errar em silêncio: a queda tem endereço, o silêncio não.

## Checked, unchecked e throws

Nem toda exceção é igual perante o compilador, e é a divisão que decide o
que ele exige de quem chama. As exceções unchecked são `RuntimeException` e tudo
que descende dela, a família inteira das conhecidas deste livro:
`NullPointerException`, `ArrayIndexOutOfBoundsException`,
`NumberFormatException`, `IllegalArgumentException`, `ArithmeticException`,
`ClassCastException`. O compilador não exige nada sobre elas, porque em
geral denunciam erro de programação, e a correção é consertar o código, não
tratar. Para a violação mais comum dessa família a biblioteca traz a
guarda pronta: `Objects.requireNonNull(valor, "produto é obrigatório")`
devolve o valor quando ele existe e lança `NullPointerException` com a
mensagem quando é nulo. Escrita na primeira linha de um construtor, ela
transforma um `null` que entraria calado no objeto numa queda imediata, no
ponto de entrada e com a mensagem de quem escreveu a regra, e é a forma
consagrada de dizer "este argumento é obrigatório". As checked são as demais descendentes de `Exception`: o compilador
obriga cada método em que elas podem nascer ou passar a escolher entre
tratar com `catch` ou declarar com `throws` que as deixa propagar:

```java
public class LimiteDeFiadoException extends Exception {
    public LimiteDeFiadoException(String mensagem) {
        super(mensagem);
    }
}

public void vender(ItemDeVenda item) throws LimiteDeFiadoException {
    if (devendo.add(item.subtotal()).compareTo(limite) > 0) {
        throw new LimiteDeFiadoException("Fiado estouraria o limite de R$ " + limite);
    }
    devendo = devendo.add(item.subtotal());
}
```

Criar exceção própria é estender `Exception`, para checked, ou
`RuntimeException`, para unchecked, repassando a mensagem com o `super`. A caderneta de fiado acima escolheu checked de propósito:
estourar o limite não é bug, é uma resposta possível do domínio, e quem
chama `vender` é obrigado pelo compilador a decidir na hora o que o
mercadinho faz, recusa a venda, oferece outro pagamento, chama o dono. O
`throws` na assinatura é o aviso público dessa obrigação, parte do contrato
do método no sentido do capítulo 9.

A régua deste livro, num assunto que divide opiniões há décadas: unchecked para violação de regra que o chamador tinha como
respeitar (argumento inválido, estado impossível), checked para condição
esperável do domínio que o chamador precisa decidir, e com parcimônia,
porque cada `throws` se espalha pelas assinaturas acima. Grande parte do
código moderno usa quase só unchecked; o encontro inevitável com as checked
da biblioteca acontece no capítulo 21, quando o programa tocar arquivos.

## A causa

Um método que trata uma exceção e lança outra no lugar dela apaga o rastro
do problema original, a não ser que o leve junto. Toda exceção pode
carregar uma causa: a exceção que a provocou, entregue no construtor.

```java
try {
    return Integer.parseInt(coluna);
} catch (NumberFormatException erro) {
    throw new EstoqueCorrompidoException("Quantidade inválida na linha " + numero, erro);
}
```

O segundo argumento é a causa, e ela sobrevive à troca. O stack trace
impresso na queda mostra a exceção nova e, abaixo dela, uma seção aberta
por `Caused by:` com o tipo, a mensagem e a pilha da original, e assim por
diante enquanto houver causa encadeada. É a diferença entre saber que o
estoque está corrompido e saber que ele está corrompido porque o
`parseInt` recusou o texto " cristal 5kg" na linha 42 do arquivo. Quem
trata recupera o objeto da causa com `getCause`, e o capítulo 23 encontra
essa mecânica outra vez, quando uma chamada indireta embrulha o que o
método chamado lançou.

Para uma exceção própria aceitar causa, o construtor precisa recebê-la e
repassá-la:

```java
public class EstoqueCorrompidoException extends RuntimeException {
    public EstoqueCorrompidoException(String mensagem, Throwable causa) {
        super(mensagem, causa);
    }
}
```

`Throwable` é o topo dessa família inteira, superclasse comum de
`Exception` e de `Error`, e é o tipo que aparece nas assinaturas que
aceitam qualquer exceção, esta inclusive. A regra que fecha a seção:
quem troca uma exceção por outra passa a causa adiante, sempre. Exceção
que perde a causa muda o problema de endereço sem levar a informação
junto, e quem investiga recomeça do zero.

## finally

O bloco `finally`, acoplado ao `try`, roda sempre: com sucesso, com exceção
tratada, com exceção propagando.

```java
try {
    IO.println(Integer.parseInt(resposta));
} catch (NumberFormatException erro) {
    IO.println("entrada inválida");
} finally {
    IO.println("tentativa encerrada");
}
```

O uso legítimo é limpeza do que precisa acontecer aconteça o que acontecer,
tipicamente devolver um recurso ao sistema. Para o caso mais comum dessa
limpeza, fechar o que foi aberto, a linguagem tem uma escrita dedicada que o
capítulo 21 apresenta junto com os arquivos, e é ela que o código atual usa;
o `finally` fica para as limpezas que não são fechamento e para ler o código
dos outros.

<div class="aprofundamento">

**O preço de lançar.** Criar uma exceção custa ordens de grandeza mais que
um `if`, porque o retrato da pilha é capturado no `new`. É um dos motivos de exceção
não servir como desvio de fluxo comum: `if` decide caminho esperado, exceção
sinaliza o excepcional. A regra de bolso: se o chamador vai tratar em todo
uso normal, provavelmente era um retorno, não uma exceção.

</div>

## Prática

1. Blinde o caixa interativo por completo: quantidade não numérica pergunta
   de novo, quantidade zero ou negativa idem, com mensagens distintas, e o
   registro só sai com valor válido. Decida onde cada validação mora e por
   quê.

2. Reproduza a previsão com três métodos aninhados em vez de dois, prevendo
   a saída antes de rodar. Depois remova o `catch` e compare o stack trace
   impresso com a sua previsão da propagação.

3. Reproduza a armadilha do `catch` vazio com um item defeituoso no meio de
   três, mostre o total errado, e conserte duas vezes: registrando o erro e
   seguindo, e deixando propagar. Escreva quando cada política é a certa
   para um caixa de verdade.

4. Implemente a caderneta de fiado com `LimiteDeFiadoException` e um `main`
   que venda até estourar o limite, tratando a exceção com uma mensagem ao
   operador. Depois converta a exceção para unchecked, observe o que o
   compilador deixa de exigir, e escreva qual das duas versões você
   defenderia na revisão de código do mercadinho.

5. Escreva um método que provoque, de propósito, três exceções unchecked
   diferentes deste livro, conforme o argumento recebido, e um `main` com
   três `catch` específicos que identifique cada uma. Acrescente um quarto
   caso que nenhum `catch` cubra e descreva o que acontece. Depois junte
   dois dos três num multi-catch, e tente também escrever
   `catch (Exception erro)` antes dos específicos, anotando a recusa do
   compilador.

6. Escreva `EstoqueCorrompidoException` com construtor de mensagem e causa,
   e um método de leitura de linha que embrulhe nela a
   `NumberFormatException` do preço. Derrube o programa de propósito e cole
   o stack trace inteiro, apontando onde termina a exceção nova e onde
   começa o `Caused by:`. Depois remova a causa do construtor e compare os
   dois rastros.

7. Ponha `Objects.requireNonNull` nos argumentos obrigatórios do construtor
   de `Produto` e escreva o teste que prova a recusa. Compare a mensagem
   com a da versão que lançava `IllegalArgumentException` à mão, e decida
   por escrito qual das duas você prefere encontrar num relatório de erro
   de madrugada.

## Ficha do capítulo

| Termo | Definição |
| --- | --- |
| exceção | objeto que descreve um problema; lançado, interrompe o fluxo |
| propagação | a subida da exceção pela pilha, encerrando métodos, até um tratador |
| stack trace | o retrato da pilha no momento do lançamento, impresso na queda |
| `try` / `catch` | trecho vigiado e tratador por tipo de exceção |
| `finally` | bloco que roda sempre, com ou sem exceção |
| `throws` | declara que o método deixa a exceção checked propagar |
| checked | o compilador obriga a tratar ou declarar; condição esperável do domínio |
| unchecked | `RuntimeException` e descendentes; em geral, erro de programação |
| `RuntimeException` | a raiz da família unchecked |
| `Throwable` | o topo da família: superclasse de `Exception` e de `Error` |
| multi-catch | `catch (A \| B erro)`: um bloco para tipos sem parentesco entre si |
| encadeamento de exceções | a causa entregue no construtor e impressa em `Caused by:` |
| `getCause` | devolve a exceção que provocou esta |
| `printStackTrace` | imprime o retrato da queda sem derrubar o programa |
| `Objects.requireNonNull` | devolve o valor ou lança na hora, com mensagem |

| Regra prática | |
| --- | --- |
| captura | o tipo mais específico que se sabe tratar |
| `catch` vazio | nunca; registrar, reagir ou relançar |
| exceção própria | estende `Exception` (checked) ou `RuntimeException` (unchecked) |
