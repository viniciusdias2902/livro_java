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
fevereiro com `DateTimeException`, uma exceção unchecked, ou de
`LocalDate.now()`, a data corrente do relógio da máquina. A aritmética vem
por métodos, `plusDays`, `plusMonths`, `minusWeeks`, e as comparações por
`isBefore`, `isAfter` e o `compareTo` de `Comparable`, que o tipo implementa;
produto vencido é `validade.isBefore(hoje)`, sem conta manual nenhuma.

Além de somar e subtrair, `LocalDate` responde sobre si mesma.
`getDayOfWeek` devolve um `DayOfWeek` e `getMonth` devolve um `Month`, e os
dois são enums da biblioteca, com as constantes `SUNDAY`, `FEBRUARY` e as
demais, o que põe o switch exaustivo do capítulo 12 à disposição de quem
decide por dia da semana. `lengthOfMonth` responde quantos dias tem o mês
daquela data, `isLeapYear` diz se o ano é bissexto, e `getDayOfYear` dá a
posição no ano. A família `with` troca uma parte e mantém o resto,
`withDayOfMonth(1)` levando ao primeiro dia do mês. E para os ajustes que
não cabem numa troca simples existe `TemporalAdjusters`, a classe
utilitária dos ajustes de data:

```java
LocalDate hoje = LocalDate.of(2026, 8, 23);
IO.println(hoje.getDayOfWeek());
IO.println(hoje.with(TemporalAdjusters.lastDayOfMonth()));
IO.println(hoje.with(TemporalAdjusters.next(DayOfWeek.FRIDAY)));
```

```
SUNDAY
2026-08-31
2026-08-28
```

`lastDayOfMonth`, `firstDayOfNextMonth` e `next(diaDaSemana)` cobrem a
maior parte das políticas de vencimento e de fechamento sem nenhuma conta
de calendário escrita à mão, que é a razão de a biblioteca existir.

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

Fevereiro de 2026 tem 28 dias. O que imprime?

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

## LocalTime, LocalDateTime e ZonedDateTime

A data civil é uma peça de um conjunto pequeno, e as outras se leem por
combinação. `LocalTime` é a hora do dia sem data e sem lugar: o horário de
abertura do mercadinho, `LocalTime.of(8, 0)`, ou a hora corrente,
`LocalTime.now()`. Guarda até nanossegundos, tem a mesma aritmética
imutável, `plusHours`, `minusMinutes`, `isBefore`, e é o tipo do
expediente, do horário de entrega e da faixa de promoção do fim da tarde.

`LocalDateTime` é a soma dos dois, data e hora sem lugar, e é o carimbo dos
registros do dia a dia: a venda das `2026-08-23T14:32`. Monta-se com
`LocalDateTime.of(data, hora)` ou a partir de uma das partes, com
`data.atTime(14, 32)` e `hora.atDate(data)`, e se decompõe de volta com
`toLocalDate()` e `toLocalTime()`.

`ZonedDateTime` acrescenta a terceira dimensão, o lugar: data, hora e fuso
juntos, o tipo do compromisso marcado num ponto do mundo, que sabe
responder que horas são ali e a que momento físico aquilo corresponde. A
próxima seção mostra por que registrar não é o trabalho dele.

E `YearMonth` representa o mês inteiro, sem dia: é o tipo da competência de
um relatório e da validade impressa num cartão. `YearMonth.of(2026, 2)`
responde 28 a `lengthOfMonth()`, e `atEndOfMonth()` devolve o último dia
como `LocalDate`.

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
As duas famílias não se misturam: `Period` mede em unidades de calendário e
`Duration` em segundos e nanossegundos, e é por isso que a distância entre
dois `LocalDate` não se pede em horas.

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

O `atZone` aplica o fuso e devolve o `ZonedDateTime` da seção anterior, o
momento físico já vestido de calendário local; o `toLocalDateTime` no fim
tira a roupa do fuso para a exibição. A
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

O padrão usa letras com papel fixo: `dd` dia, `MM` mês, `yyyy` ano, `HH`
hora de 0 a 23 e `mm` minuto. Texto que não casa com o padrão lança
`DateTimeParseException`, unchecked, com a posição exata do caractere que
desmentiu o formato; é a irmã da `NumberFormatException` do capítulo 5, e o
tratamento é o do capítulo 13. A caixa
das letras importa, e a dupla `MM` maiúsculo mês contra `mm` minúsculo
minuto é a confusão frequente; a do `YYYY`, logo adiante, é pior, porque
passa meses sem sintoma:

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
`yyyy` o ano inteiro e erra exatamente na virada do ano. A regra: ano de calendário é `yyyy`
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
   compra feita em 31 de janeiro. Acrescente uma terceira política, "último
   dia do mês seguinte", com `TemporalAdjusters`.

7. Modele o expediente do mercadinho com `LocalTime`: abertura às 8h,
   fechamento às 20h, e um método que responda se um `LocalDateTime` de
   venda caiu dentro do expediente. Trate o domingo à parte, decidindo com
   `getDayOfWeek` num switch sem `default`.

8. Escreva o relatório mensal a partir de um `YearMonth`: quantos dias o mês
   tem, qual o primeiro e o último dia, e quantos deles são sábados ou
   domingos. Depois interprete "02/2026" com um `DateTimeFormatter` e trate
   a `DateTimeParseException` de um texto malformado.

## Ficha do capítulo

| Tipo | Representa | Nasce de |
| --- | --- | --- |
| `LocalDate` | data civil, sem hora e sem lugar | `of(ano, mes, dia)`, `now()`, `parse` |
| `LocalTime` | a hora do dia, sem data e sem lugar | `of(8, 0)`, `now()` |
| `LocalDateTime` | data e hora, sem lugar | `of(data, hora)`, `data.atTime(...)` |
| `ZonedDateTime` | data, hora e fuso juntos | `instante.atZone(fuso)` |
| `YearMonth` | o mês inteiro, sem dia | `YearMonth.of(2026, 2)` |
| `Instant` | o momento físico global | `Instant.now()` |
| `Period` | distância em anos, meses e dias | `Period.between(a, b)` |
| `Duration` | distância com relógio | `Duration.ofMinutes(90)` |
| `ZoneId` | o fuso horário | `ZoneId.of("America/Sao_Paulo")` |

| Termo | Definição |
| --- | --- |
| fuso horário | a regra regional que traduz momento físico em hora local |
| `ChronoUnit` | distância total numa unidade só: `DAYS.between(a, b)` |
| `DateTimeFormatter` | formata e interpreta datas: `ofPattern("dd/MM/yyyy")` |
| `DateTimeParseException` | texto que não casa com o padrão; unchecked |
| `DayOfWeek` / `Month` | enums do calendário; servem a switch exaustivo |
| `TemporalAdjusters` | ajustes prontos: último dia do mês, próxima sexta |
| `with` | troca uma parte da data e mantém o resto |
| imutabilidade | todo cálculo devolve objeto novo; guardar o retorno é obrigatório |

| Regra prática | |
| --- | --- |
| registrar momento | `Instant`; converter para local só na exibição |
| ano no formato | `yyyy` minúsculo; `YYYY` é ano de semana e erra na virada |
| `now()` em regra de negócio | pede relógio injetável para o teste mandar no tempo |
