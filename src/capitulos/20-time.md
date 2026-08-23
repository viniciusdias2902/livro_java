# java.time: datas sem armadilha

O queijo do mercadinho tem validade, e a pergunta do balcão é diária: quantos
dias faltam? Datas são o território clássico do bug bobo, ano bissexto, mês
de trinta dias, virada de ano, e a biblioteca `java.time` existe para que
nenhuma dessas contas seja feita à mão:

```java
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

LocalDate hoje = LocalDate.of(2026, 8, 23);
LocalDate validade = LocalDate.of(2026, 9, 30);
long diasRestantes = ChronoUnit.DAYS.between(hoje, validade);
IO.println(diasRestantes);
```

```
38
```

## LocalDate: a data civil

`LocalDate` representa uma data de calendário, dia, mês e ano, sem hora e
sem lugar: a data da etiqueta de validade, do feriado, do vencimento.
Nasce de `LocalDate.of(ano, mes, dia)`, que valida na entrada e recusa 31 de
fevereiro com a `DateTimeException` da família do capítulo 13, ou de
`LocalDate.now()`, a data corrente do relógio da máquina. A aritmética vem
por métodos, `plusDays`, `plusMonths`, `minusWeeks`, e as comparações por
`isBefore`, `isAfter` e o `compareTo` de `Comparable`, que o tipo implementa;
produto vencido é `validade.isBefore(hoje)`, sem conta manual nenhuma.

Todo tipo deste capítulo é imutável, na tradição do `String` e do
`BigDecimal`: cada `plus` devolve um objeto novo e o original permanece. A
consequência já tem cicatriz conhecida no livro, e aqui ela reaparece com
fantasia de data:

```java
LocalDate vencimento = LocalDate.of(2026, 8, 23);
vencimento.plusDays(30);
IO.println(vencimento);
```

```
2026-08-23
```

A segunda linha calculou um vencimento novo e o jogou fora, como o
`toUpperCase` ignorado do capítulo 5: o fiado continua vencendo hoje, sem
erro nenhum. A forma certa guarda o retorno, `vencimento =
vencimento.plusDays(30)`, e a imutabilidade paga o preço da distração com o
mesmo troco de sempre: nenhum outro trecho do sistema vê a data mudar por
baixo dele.

<div class="previsao">

A promoção de aniversário do mercadinho, marcada para "um mês depois" do dia
31 de janeiro:

```java
LocalDate inicio = LocalDate.of(2026, 1, 31);
IO.println(inicio.plusMonths(1));
```

Fevereiro de 2026 tem 28 dias. O que imprime, e o que a linha nem tenta
fazer?

</div>

```
2026-02-28
```

`plusMonths` avança o mês e, quando o dia não existe no destino, recua para
o último dia válido, sem lançar erro e sem inventar 3 de março. É uma
decisão documentada da biblioteca, boa para vencimentos e mensalidades, e o
que a linha nem tenta fazer é adivinhar intenção: quem precisa de outra
política, como "primeiro dia do mês seguinte", escreve a política. A lição
transferível: aritmética de calendário tem casos de borda por natureza, e a
biblioteca os resolve com regras declaradas, não com aproximações.

## Period, Duration e as duas perguntas de distância

Entre duas datas existem duas perguntas diferentes. "Quanto tempo civil?"
responde-se com `Period`, o intervalo em anos, meses e dias:

```java
Period prazo = Period.between(hoje, validade);
IO.println(prazo);
```

```
P1M7D
```

Um mês e sete dias, na notação compacta que o `toString` de `Period` usa: o
`P` abre o período, e cada número carrega sua unidade. "Quantos dias
corridos?" responde-se com `ChronoUnit.DAYS.between`, como na abertura, que
devolve o total na unidade pedida, 38, sem decompor. Os dois discordam de
propósito, porque medem coisas diferentes, e relatório que mistura os dois
mistura unidades. Para distâncias com relógio, horas, minutos, segundos, o
tipo é `Duration`, com a mesma notação: `Duration.ofMinutes(90)` imprime
`PT1H30M`, uma hora e meia depois do `T` que separa a parte de tempo.
`LocalDateTime`, data e hora juntas, é o carimbo dos registros do dia a
dia, a venda das `2026-08-23T14:32`, com a mesma aritmética imutável.

## Instant, ZoneId e o fuso horário

Nenhum tipo acima diz onde. `LocalDateTime` é anotação de calendário sem
localização: "23 de agosto, 14:32" acontece em momentos físicos diferentes
em São Paulo e em Tóquio, e para dinheiro, auditoria e sincronização isso
importa. O tipo do momento físico é o `Instant`: o ponto na linha do tempo
global, único para o planeta inteiro, sem calendário e sem opinião sobre
como humanos o chamam. `Instant.now()` é o agora, o mesmo agora em qualquer
máquina do mundo.

A tradução entre o momento físico e o calendário humano depende do fuso
horário: a regra regional que diz que horas são em cada lugar, representada
por `ZoneId`:

```java
import java.time.Instant;
import java.time.ZoneId;

Instant momentoDaVenda = Instant.now();
ZoneId saoPaulo = ZoneId.of("America/Sao_Paulo");
IO.println(momentoDaVenda.atZone(saoPaulo).toLocalDateTime());
```

O `atZone` aplica o fuso e revela o calendário local daquele instante. A
regra de arquitetura que essa distinção sustenta é curta e cai em
entrevista: registra-se o momento como `Instant`, e converte-se para data e
hora locais só na hora de mostrar a alguém, com o fuso de quem olha. Um
sistema que grava `LocalDateTime` sem anotar o fuso grava um registro
ambíguo, e a ambiguidade cobra quando o servidor muda de país, quando dois
sistemas se integram, ou na próxima mudança de regra de horário, que
governos fazem quando querem.

## DateTimeFormatter: mostrar e ler

O `toString` dos tipos usa o formato internacional, ano-mês-dia, ótimo para
registro e ordenável como texto. O balcão fala outra língua, e o
`DateTimeFormatter` traduz nas duas direções:

```java
import java.time.format.DateTimeFormatter;

DateTimeFormatter brasileiro = DateTimeFormatter.ofPattern("dd/MM/yyyy");
IO.println(validade.format(brasileiro));
LocalDate lida = LocalDate.parse("30/09/2026", brasileiro);
```

O padrão usa letras com papel fixo: `dd` dia, `MM` mês, `yyyy` ano. A caixa
das letras importa, e a dupla `MM` maiúsculo mês contra `mm` minúsculo
minuto é a confusão mais famosa; a segunda mais famosa é pior, porque passa
meses sem sintoma:

<div class="armadilha">

Um cupom com a data formatada por quem lembrou do padrão "quase certo":

```java
DateTimeFormatter doCupom = DateTimeFormatter.ofPattern("dd/MM/YYYY");
IO.println(LocalDate.of(2025, 12, 31).format(doCupom));
```

```
31/12/2026
```

A data é de 2025, e o cupom imprime 2026.

</div>

`YYYY` maiúsculo não é o ano do calendário: é o ano da semana, uma convenção
em que os últimos dias de dezembro podem pertencer à primeira semana do ano
seguinte, e 31 de dezembro de 2025 pertence. O formato funciona idêntico ao
`yyyy` o ano inteiro e erra exatamente na virada, quando ninguém está
olhando e todo cupom importa. A regra: ano de calendário é `yyyy`
minúsculo, e `YYYY` só existe para quem trabalha deliberadamente com
semanas. É o tipo de defeito que o teste de regressão do capítulo 15 fixa
para sempre com uma data de dezembro.

<div class="aprofundamento">

**O relógio injetável.** `LocalDate.now()` dentro de uma regra de negócio é
o `Random` sem semente do capítulo 6: cada execução, um valor, e o teste do
"produto vence em três dias" passa hoje e falha na semana que vem. A
biblioteca prevê a saída: as versões de `now` aceitam um `Clock`, um relógio
substituível, e o teste entrega um relógio congelado num dia escolhido. O
capítulo 24 dá o nome geral dessa manobra.

</div>

## Prática

1. Acrescente validade ao produto perecível do mercadinho: `LocalDate` no
   construtor, um método `vencido(LocalDate hoje)` e um
   `diasParaVencer(LocalDate hoje)`. Recuse validade nula com a exceção de
   sempre.

2. Escreva o relatório "vence em até sete dias" com um pipeline do capítulo
   19: filtrar por proximidade da validade, ordenar pela data, mapear para
   nome e dias restantes.

3. Reproduza a previsão do 31 de janeiro para os doze meses de 2026 num
   laço, imprimindo cada resultado, e marque quais meses recuaram o dia.

4. Reproduza a armadilha do `YYYY` com cinco datas de dezembro e janeiro,
   identifique exatamente quais erram, e escreva o teste de regressão que
   trava o formato certo.

5. Registre uma venda com `Instant.now()`, mostre-a no fuso de São Paulo e
   no de Tóquio com o mesmo formatador de data e hora, e explique por
   escrito por que o `Instant` gravado é um só.

6. Calcule o vencimento do fiado: trinta dias corridos após a compra, e
   também "mesmo dia do mês seguinte", comparando as duas políticas para uma
   compra feita em 31 de janeiro.

## Ficha do capítulo

| Tipo | Representa | Nasce de |
| --- | --- | --- |
| `LocalDate` | data civil, sem hora e sem lugar | `of(ano, mes, dia)`, `now()`, `parse` |
| `LocalDateTime` | data e hora, sem lugar | `of(...)`, `now()` |
| `Instant` | o momento físico global | `Instant.now()` |
| `Period` | distância em anos, meses e dias | `Period.between(a, b)` |
| `Duration` | distância com relógio | `Duration.ofMinutes(90)` |
| `ZoneId` | o fuso horário | `ZoneId.of("America/Sao_Paulo")` |

| Termo | Definição |
| --- | --- |
| fuso horário | a regra regional que traduz momento físico em hora local |
| `ChronoUnit` | distância total numa unidade só: `DAYS.between(a, b)` |
| `DateTimeFormatter` | formata e interpreta datas: `ofPattern("dd/MM/yyyy")` |
| imutabilidade | todo cálculo devolve objeto novo; guardar o retorno é obrigatório |

| Regra prática | |
| --- | --- |
| registrar momento | `Instant`; converter para local só na exibição |
| ano no formato | `yyyy` minúsculo; `YYYY` é ano de semana e erra na virada |
| `now()` em regra de negócio | pede relógio injetável para o teste mandar no tempo |
