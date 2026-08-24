# Concorrência: executors e virtual threads

O fechamento do mês do mercadinho lê trinta arquivos de vendas do capítulo
21, um por dia, e soma tudo. A leitura é sequencial e demora; a máquina tem
oito processadores e usa um. A tentação é óbvia, dividir o trabalho, e este
capítulo existe porque a tentação, executada sem as regras, produz
fechamento errado sem erro nenhum. Antes do desastre, a peça nova.

## Thread: a segunda linha de execução

Todo programa deste livro até aqui executou numa linha só: uma instrução
por vez, uma pilha de chamadas, do `main` ao fim. Uma thread é uma linha de
execução independente dentro do mesmo processo: tem a própria pilha de
chamadas e o próprio "onde estou", e compartilha com as outras o heap, os
objetos do capítulo 5. Criar uma segunda é pedir à JVM que execute um
trecho, um `Runnable`, a interface funcional de um método `run` sem
argumentos e sem retorno, em paralelo com quem pediu:

<div class="previsao">

O fechamento divide o mês em duas quinzenas, uma thread para cada, e o
`main` espera as duas com `join`:

```java
void main() throws InterruptedException {
    Thread primeira = new Thread(() -> {
        for (int i = 1; i <= 3; i++) {
            IO.println("quinzena 1, arquivo " + i);
        }
    });
    Thread segunda = new Thread(() -> {
        for (int i = 1; i <= 3; i++) {
            IO.println("quinzena 2, arquivo " + i);
        }
    });
    primeira.start();
    segunda.start();
    primeira.join();
    segunda.join();
    IO.println("fechado");
}
```

Em que ordem saem as seis linhas?

</div>

Em ordem nenhuma garantida, e essa é a resposta certa: numa execução as
seis podem sair intercaladas, noutra a quinzena 1 inteira antes da
quinzena 2, e duas execuções seguidas podem diferir. Quem decide qual
thread avança a cada momento é o escalonador do sistema, e o programa
correto sob concorrência é o que está certo em todas as intercalações
possíveis, não o que deu certo na intercalação de hoje. Só o "fechado" tem
posição prometida, porque `join` faz o `main` esperar a thread terminar;
`join` declara `InterruptedException`, a exceção checked da espera
interrompida, que os `main` de laboratório repassam com `throws`. `start`
dispara;
`run` chamado direto seria um método comum na mesma linha de execução, sem
paralelismo nenhum, um clássico de primeira semana.

Uma peça acompanha os experimentos deste capítulo: `Thread.sleep(500)` faz
a thread corrente parar pelo número de milissegundos dado e depois seguir.
Ela declara a mesma `InterruptedException` do `join`, pela mesma razão,
porque quem espera pode ser acordado antes da hora, e serve aqui para
simular trabalho demorado sem inventar cálculo. No código de verdade,
`sleep` aparece pouco: esperar por tempo fixo em vez de esperar pelo evento
é quase sempre sinal de coordenação mal desenhada.

## A condição de corrida

<div class="armadilha">

O fechamento conta os itens vendidos no mês num contador compartilhado:
duas tarefas, cada uma varrendo metade dos arquivos e registrando cem mil
itens:

```java
class Contador {
    int total = 0;

    void incrementar() {
        total++;
    }
}

void main() throws InterruptedException {
    Contador itens = new Contador();
    Runnable tarefa = () -> {
        for (int i = 0; i < 100_000; i++) {
            itens.incrementar();
        }
    };
    Thread primeiraMetade = new Thread(tarefa);
    Thread segundaMetade = new Thread(tarefa);
    primeiraMetade.start();
    segundaMetade.start();
    primeiraMetade.join();
    segundaMetade.join();
    IO.println(itens.total);
}
```

Duzentos mil itens registrados. Três execuções reais imprimiram:

```
127572
114925
120697
```

</div>

Nem duzentas mil, nem duas vezes o mesmo número. Isso é uma condição de
corrida: duas ou mais threads acessando o mesmo dado, com pelo menos uma
escrevendo, e o resultado dependendo da intercalação. A raiz é a
atomicidade, ou a falta dela: `total++` parece uma operação e são três,
ler o valor, somar um, gravar de volta. Quando as duas threads leem o mesmo
`total` antes de qualquer uma gravar, as duas gravam o mesmo resultado e um
incremento evapora; em cem mil voltas isso acontece dezenas de milhares de
vezes, ao acaso. Nenhuma exceção, nenhum aviso, um total diferente por
execução: é o bug silencioso levado à perfeição, e a versão dele com
dinheiro se chama fechamento que não bate.

## synchronized

A correção clássica torna a operação indivisível:

```java
class Contador {
    private int total = 0;

    synchronized void incrementar() {
        total++;
    }

    synchronized int total() {
        return total;
    }
}
```

O modificador `synchronized` pendura no método uma tranca: cada objeto tem
uma, só uma thread por vez a segura, e as demais esperam na porta. A mesma
tranca também se pede por bloco, `synchronized (objeto) { ... }`, quando o
trecho a proteger é menor que o método inteiro ou quando o objeto que
guarda a tranca não é o `this`. Com a
tranca, o ler-somar-gravar acontece inteiro antes de a próxima thread
entrar, e o programa imprime 200000 em toda execução. O preço está no
próprio desenho: dentro do trecho trancado, o paralelismo deixa de existir,
e trancar demais devolve o programa lento que motivou a divisão. A tranca
protege o dado; o desenho decide onde ela é inevitável.

## Impasse

A tranca resolve a corrida e traz um problema próprio. A caderneta de fiado
permite transferir saldo entre dois clientes, e a transferência tranca as
duas contas envolvidas:

```java
void transferir(Conta origem, Conta destino, BigDecimal valor) {
    synchronized (origem) {
        synchronized (destino) {
            origem.debitar(valor);
            destino.creditar(valor);
        }
    }
}
```

Duas threads, duas transferências simultâneas em sentidos opostos, de Ana
para Bruno e de Bruno para Ana. A primeira tranca Ana e fica esperando
Bruno; a segunda tranca Bruno e fica esperando Ana; nenhuma das duas solta
o que já tem. Isso é um impasse (*deadlock*): duas ou mais threads paradas
para sempre, cada uma esperando uma tranca que a outra segura. Não há
exceção, não há mensagem e não há fim: o programa simplesmente para de
responder, e no servidor o sintoma é o pedido que nunca volta.

A regra que evita a família inteira desse defeito é de disciplina e cabe
numa frase: quando duas trancas precisam ser tomadas juntas, tome-as
sempre na mesma ordem, em todo o código do sistema. Ordenar as contas por
um critério fixo, como o código do cliente, e trancar sempre a menor
primeiro faz as duas transferências pedirem as trancas na mesma sequência,
e o impasse deixa de ser possível. A alternativa melhor continua sendo a
deste capítulo inteiro: não trancar duas coisas, desenhando o trabalho para
não haver disputa.

## Visibilidade e volatile

A corrida não é o único fantasma. Cada processador guarda cópias locais do
que lê, e uma thread pode não enxergar o que outra escreveu:

```java
class Fechamento {
    boolean aberto = true;

    void rodar() {
        while (aberto) {
            // registra vendas
        }
        IO.println("caixa encerrado");
    }
}
```

Outra thread escreve `aberto = false` e o laço pode nunca parar: a thread do
laço, otimizada pela JVM, segue lendo a cópia velha do campo, e o
"encerrado" não sai nunca. Esse é o problema da visibilidade entre threads:
sem sinalização explícita, não há garantia de quando uma escrita feita por
uma thread aparece para as outras. O modificador `volatile` no campo,
`volatile boolean aberto`, é a sinalização mínima: toda leitura vê a última
escrita, e o laço para. O que o `volatile` não faz é tanto quanto o que
faz: ele garante visibilidade, não atomicidade, e um `volatile int total`
com `total++` continua perdendo incrementos na corrida da seção anterior. A
tabela mental: `synchronized` para operações compostas sobre dado
compartilhado; `volatile` para bandeiras simples que uma thread escreve e
outras leem.

Entre os dois existe um meio-termo que a biblioteca já resolveu. Os tipos
atômicos, do pacote `java.util.concurrent.atomic`, tornam a operação
composta indivisível sem tranca nenhuma: `AtomicInteger` tem
`incrementAndGet`, que lê, soma e grava numa operação só, garantida pelo
processador.

```java
AtomicInteger itens = new AtomicInteger();
Runnable tarefa = () -> {
    for (int i = 0; i < 100_000; i++) {
        itens.incrementAndGet();
    }
};
```

Duzentos mil em toda execução, sem `synchronized` e sem a fila na porta que
ele cria. A mesma prateleira traz `AtomicLong`, `AtomicBoolean` e
`AtomicReference`, e ao lado dela ficam as coleções concorrentes, com
`ConcurrentHashMap` à frente: é o mapa feito para escrita simultânea, e ele
substitui o `HashMap` compartilhado do capítulo 17 sempre que mais de uma
thread grava. A troca não é preciosismo. `HashMap` sob escrita simultânea
não perde apenas entradas: ele pode corromper a própria estrutura interna,
e o estrago aparece como entrada que some ou como laço que não termina,
longe da causa e sem erro nenhum.

## ExecutorService, Future e o desenho que evita tudo isso

Criar threads à mão espalha `new Thread` pelo sistema; o executor centraliza.
Um `ExecutorService` é um serviço que recebe tarefas e as executa num
conjunto de threads que ele administra, e um `Future` é o recibo de uma
tarefa entregue: a promessa de um resultado que ainda não existe, resgatada
com `get`, que espera se preciso. O fechamento do mês, na forma correta:

```java
try (ExecutorService executor = Executors.newFixedThreadPool(8)) {
    List<Future<BigDecimal>> recibos = new ArrayList<>();
    for (Path arquivo : arquivosDoMes) {
        recibos.add(executor.submit(() -> totalDoArquivo(arquivo)));
    }

    BigDecimal totalDoMes = BigDecimal.ZERO;
    for (Future<BigDecimal> recibo : recibos) {
        totalDoMes = totalDoMes.add(recibo.get());
    }
    IO.println("Fechamento: R$ " + totalDoMes);
}
```

O desenho importa mais que a ferramenta: cada tarefa lê o próprio arquivo e
devolve o próprio subtotal, sem tocar em nada compartilhado, e o `main`
combina os resultados sozinho, em sequência. Não há corrida porque não há
dado disputado: as threads trabalham em confinamento e se comunicam por
valores imutáveis de retorno, `BigDecimal` do capítulo 7, e essa é a
primeira regra do código concorrente que envelhece bem, não compartilhe;
combine. `synchronized` e `volatile` ficam para quando o compartilhamento é
inevitável. O executor entra num try-with-resources porque encerrar o
serviço é fechamento de recurso como os do capítulo 21: o `close` espera as
tarefas em andamento terminarem antes de liberar as threads. Quem não usa a
forma com recurso chama `shutdown`, que faz o mesmo pedido sem esperar, ou
`shutdownNow`, que tenta interromper o que estiver rodando; executor
esquecido sem fechamento nenhum mantém as threads vivas, e o programa não
termina, que é o tropeço de primeira semana com executores.

O `submit` aceita as duas formas de tarefa. O `Runnable` da primeira seção
não recebe nem devolve nada; `Callable<T>` é a irmã que devolve valor: uma
interface funcional de um método só, `call`, que produz um `T` e pode
lançar exceção checked, o que o `Runnable` não pode. É um `Callable` que o
fechamento acima entrega em cada `submit`, e é dele que o `Future` tira o
que devolver. Quando as tarefas já estão todas montadas, `invokeAll` recebe
a coleção inteira de uma vez e devolve a lista de `Future` na mesma ordem,
dispensando o laço de `submit`. O `get` do `Future` declara
duas exceções checked: a `InterruptedException` da espera e a
`ExecutionException`, que embrulha a falha da tarefa e a entrega a quem
resgatou o recibo.

## Virtual threads

A thread da seção anterior, dita de plataforma, é um recurso caro do
sistema operacional: milhares delas esgotam a máquina. A virtual thread é a
thread barata da JVM: milhões podem existir, porque quando uma bloqueia
esperando o mundo externo, a JVM a tira do processador e o empresta a
outra. O executor muda numa linha:

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    // uma tarefa por trabalho, sem contar quantas
}
```

A regra de escolha fecha o capítulo. Trabalho que espera, arquivos, rede,
banco de dados, é o habitat da virtual thread, uma por tarefa, sem pool e
sem contagem; trabalho que calcula sem esperar ganha pouco além do número
de processadores, e o pool fixo continua certo. É esta segunda peça que
explica onde a concorrência vive de verdade: um programa de terminal como o
do livro tem um usuário e paraleliza por dentro quando quer velocidade, mas
um servidor atende milhares de pedidos simultâneos, cada um numa thread, e
todo o vocabulário deste capítulo, corrida, visibilidade, confinamento, é o
idioma nativo de lá. O leitor que seguir para esse mundo vai reconhecer
cada palavra.

<div class="aprofundamento">

**O resto da caixa de ferramentas.** Além dos tipos atômicos e das
coleções concorrentes, `java.util.concurrent` traz peças para os padrões de
coordenação: `BlockingQueue` liga threads produtoras a consumidoras, com
quem consome esperando na fila vazia em vez de girar; `CountDownLatch` faz
um grupo esperar até um contador zerar; e `CompletableFuture` encadeia
tarefas assíncronas sem o `get` que bloqueia. A regra de quem sabe o básico
deste capítulo: antes de escrever `synchronized`, procurar a peça pronta que
já resolve o padrão.

</div>

## Prática

1. Reproduza a previsão da intercalação cinco vezes e cole duas saídas
   diferentes lado a lado. Depois remova os `join` e explique o que muda no
   "fechado".

2. Reproduza a corrida do contador dez vezes, anotando os totais. Conserte
   com `synchronized`, rode dez vezes de novo, e meça com `System.nanoTime`
   o preço da tranca nas duas versões.

3. Reproduza o laço que não enxerga a bandeira, conserte com `volatile`, e
   depois prove no contador que `volatile` não conserta corrida: troque
   `synchronized` por `volatile` e mostre os totais errados.

4. Implemente o fechamento do mês com `ExecutorService` sobre os arquivos do
   capítulo 21: gere trinta arquivos de vendas de teste, some em paralelo
   com confinamento e combine com `BigDecimal`. Confira contra a soma
   sequencial.

5. Troque o pool fixo por virtual threads no fechamento e descreva o que
   mudou e o que não mudou. Escreva em um parágrafo qual dos dois executores
   você usaria para: somar arquivos locais; consultar trezentos fornecedores
   pela rede.

6. Provoque um impasse de propósito: duas contas, duas threads, duas
   transferências em sentidos opostos, com um `Thread.sleep(100)` entre as
   duas trancas para tornar o encontro provável. Confirme que o programa
   trava sem erro, encerre-o à força, e conserte ordenando as trancas pelo
   código do cliente.

7. Refaça o contador da armadilha com `AtomicInteger` e confirme os duzentos
   mil em dez execuções. Meça o tempo das três versões, a com corrida, a
   com `synchronized` e a atômica, e escreva o que os números dizem.

8. Troque, num fechamento que escreve num mapa compartilhado, o `HashMap`
   por `ConcurrentHashMap`, e rode as duas versões com oito tarefas
   gravando ao mesmo tempo. Anote quantas entradas cada versão terminou
   com, em dez execuções.

## Ficha do capítulo

| Peça | O que faz |
| --- | --- |
| `new Thread(runnable)` / `start` / `join` | cria, dispara e espera uma thread |
| `synchronized` | tranca por objeto: um método trancado por vez |
| `volatile` | visibilidade da escrita; não dá atomicidade |
| `ExecutorService` / `submit` | serviço de execução; recebe tarefas |
| `Callable<T>` / `Runnable` | tarefa que devolve valor e pode lançar / tarefa sem retorno |
| `Future` / `get` | o recibo da tarefa; espera e devolve o resultado |
| `shutdown` / `close` | encerra o serviço; sem isso o programa não termina |
| `Thread.sleep(ms)` | para a thread corrente pelo tempo dado |
| `AtomicInteger.incrementAndGet` | soma indivisível, sem tranca |
| `ConcurrentHashMap` | o mapa para escrita simultânea; `HashMap` compartilhado corrompe |
| `Executors.newFixedThreadPool(n)` | pool de tamanho fixo, para trabalho de cálculo |
| `Executors.newVirtualThreadPerTaskExecutor()` | uma virtual thread por tarefa, para trabalho que espera |

| Termo | Definição |
| --- | --- |
| thread | linha de execução com pilha própria, partilhando o heap |
| condição de corrida | resultado dependente da intercalação de acessos, com escrita |
| atomicidade | operação indivisível; `total++` não é |
| visibilidade entre threads | garantia de que uma escrita apareça para as outras |
| virtual thread | thread barata da JVM; milhões, para tarefas que esperam |
| impasse | threads paradas para sempre, cada uma esperando a tranca da outra |

| Regra prática | |
| --- | --- |
| primeiro desenho | não compartilhe; confine e combine resultados imutáveis |
| compartilhou | `synchronized` para operação composta; `volatile` para bandeira |
| duas trancas | tomadas sempre na mesma ordem, em todo o sistema |
| antes de trancar à mão | procurar a peça pronta em `java.util.concurrent` |
