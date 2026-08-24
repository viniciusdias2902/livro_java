# Maven e Gradle

O mercadinho já soma uma dúzia de classes, e o ritual de colocá-lo de pé
cresceu junto:

```console
$ javac -d saida *.java
$ java -cp saida Loja
```

Funciona, e três incômodos moram aí. O curinga `*.java` alcança uma pasta
só: no momento em que os fontes se organizarem em subpastas, os pacotes do
capítulo 7, o comando deixa arquivos para trás. O classpath, digitado desde
o capítulo 2, precisa ser combinado entre todos que rodam o projeto, em
toda máquina. E o terceiro incômodo é o maior:
nenhum código de fora entra. A ferramenta de testes do capítulo 15, ou
qualquer outra peça pronta do ecossistema, chegaria como um arquivo a
baixar, guardar em algum lugar e acrescentar ao classpath, à mão, para cada
projeto e cada máquina. Sistemas reais não vivem assim; eles usam uma
ferramenta de construção, e este capítulo instala a do resto do livro.

## O que uma ferramenta de construção faz

Uma ferramenta de construção é o programa que transforma o código-fonte,
junto do código de fora de que ele depende, num pacote pronto para
distribuir, sempre do mesmo jeito, em qualquer máquina. Ela descobre os fontes sozinha, baixa o código de fora que o
projeto declarar, monta o classpath, compila na ordem certa, roda
verificações e empacota o resultado. O que era uma sequência de comandos
combinada entre pessoas vira um arquivo guardado junto do projeto, e
"funciona na minha máquina" deixa de ser mistério: a construção é a mesma
em todas.

As duas ferramentas dominantes no mundo Java são Maven e Gradle. Este livro
apresenta as duas e adota o Maven do próximo capítulo em diante; os motivos
fecham o capítulo, junto com o mapa para ler projetos Gradle. A instalação
segue o caminho do capítulo 1:

```console
$ sdk install maven
$ mvn -version
Apache Maven 3.9.11
...
```

A primeira linha da resposta confirma a instalação; as seguintes, omitidas
acima, mostram qual JDK a ferramenta enxerga, que precisa ser o 25 do
livro.

## Maven: convenção e pom.xml

O Maven não pergunta onde estão os fontes: ele decide, e essa é a primeira
ideia da ferramenta. A convenção de diretórios é o leiaute fixo de pastas
que o Maven espera:

```
mercadinho/
├── pom.xml
└── src/
    ├── main/
    │   └── java/        ← código do sistema
    └── test/
        └── java/        ← código de teste, a partir do capítulo 15
```

Tudo que a ferramenta produz vai para `target/`, uma pasta descartável que
nunca se edita nem se versiona. A convenção vale por contrato social:
qualquer pessoa que já viu um projeto Maven sabe onde está cada coisa neste,
sem ler documentação nenhuma.

O único arquivo a escrever é o `pom.xml`, a descrição do projeto:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
    <modelVersion>4.0.0</modelVersion>

    <groupId>br.com.mercadinho</groupId>
    <artifactId>mercadinho</artifactId>
    <version>1.0</version>

    <properties>
        <maven.compiler.release>25</maven.compiler.release>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>
</project>
```

A escrita entre `<` e `>` é XML, um formato de texto para dados
aninhados, e o essencial dela se lê no exemplo: cada `<coisa>` abre e
`</coisa>` fecha, e o conteúdo vai no meio. As três linhas do meio
identificam o projeto: `groupId` é o dono, escrito como um domínio de internet de trás para a
frente, `br.com.mercadinho` para quem controla `mercadinho.com.br`,
convenção que garante nome único no mundo sem cadastro central, porque só o
dono do domínio o usaria; `artifactId` é o nome; `version` é a versão. As `properties`
travam a versão do Java, a 25 exigida desde o capítulo 1, e a codificação
dos fontes. Com isso e os fontes movidos para `src/main/java`, a construção
inteira vira:

```console
$ mvn package
[INFO] BUILD SUCCESS
$ java -cp target/classes Loja
```

`mvn compile` compila tudo para `target/classes`; `mvn package` compila e
ainda empacota. O pacote gerado, `target/mercadinho-1.0.jar`, é um jar: o
formato de distribuição do Java, um arquivo único que embrulha o bytecode e
metadados, feito para entrar no classpath de outros projetos. O nome sai da
coordenada do `pom.xml`, e o capítulo 21 mostra a variante executável
com um único comando.

<div class="previsao">

A armadilha do capítulo 2, revisitada com ferramenta. O projeto foi
empacotado, o preço do café mudou no fonte, e o operador roda:

```console
$ mvn package
[INFO] BUILD SUCCESS
$ # o preço muda em Produto.java, no editor
$ java -cp target/classes Loja
```

A saída mostra o preço novo ou o antigo?

</div>

O antigo. O Maven automatiza a construção, não a adivinha: `target/classes`
guarda o bytecode do último `mvn package`, e editar fonte não recompila
nada, exatamente como no capítulo 2. A diferença é que o hábito protetor
ficou barato: um único comando reconstrói o projeto inteiro, sempre, e
"editou, rodou `mvn`, executou" vira o ciclo padrão de trabalho.

## As fases da construção

`mvn compile` e `mvn package` não são dois comandos avulsos: são duas
fases de uma sequência fixa. O ciclo de vida da construção é a sequência
ordenada de fases que o Maven conhece, com a regra de que pedir uma fase
executa antes todas as anteriores:

| Fase | O que acontece |
| --- | --- |
| `validate` | confere se o projeto está completo e o `pom.xml` é legível |
| `compile` | compila `src/main/java` para `target/classes` |
| `test` | compila e roda o que estiver em `src/test/java` |
| `package` | monta o jar em `target/` |
| `verify` | roda as verificações adicionais que o projeto configurar |
| `install` | copia o artefato para o repositório local, em `~/.m2/repository` |
| `deploy` | publica o artefato num repositório remoto |

Da regra da sequência sai uma consequência que evita confusão: `mvn
package` roda as verificações da fase `test`, sempre, porque `test` vem
antes na lista, e uma delas falhando interrompe a construção sem gerar jar
nenhum. `mvn install` é o comando de quem tem dois projetos na mesma
máquina, um usando o outro: instalado no repositório local, o mercadinho
vira uma coordenada que o outro projeto declara como dependência, do mesmo
jeito que declara as de fora.

O `clean` fica fora dessa sequência, num ciclo próprio, e apaga a pasta
`target/` inteira. É por isso que se escreve `mvn clean package`, os dois
na mesma linha: apagar o que foi produzido antes e reconstruir do zero. A
construção do dia a dia dispensa o `clean`, porque o Maven refaz o que
mudou; a construção que precisa ser confiável, antes de publicar ou no
meio de uma investigação de comportamento estranho, começa por ele, e o
custo é só o tempo de compilar tudo de novo.

## Dependências

O ganho que justifica a cerimônia é declarar código de fora:

```xml
<dependencies>
    <dependency>
        <groupId>com.google.code.gson</groupId>
        <artifactId>gson</artifactId>
        <version>2.11.0</version>
    </dependency>
</dependencies>
```

O trio grupo, artefato e versão é a coordenada: o endereço único de um
artefato publicado, onde artefato é qualquer pacote construído e distribuído,
tipicamente um jar. Declarada a coordenada, o `mvn package` baixa o artefato
do repositório, o servidor público que hospeda artefatos publicados, sendo o
Maven Central o repositório padrão do ecossistema, guarda uma cópia local e
o coloca no classpath de compilação e de execução. O exemplo acima traz uma
biblioteca de conversão de dados apenas para mostrar a forma; a primeira
dependência que o mercadinho vai realmente usar chega no capítulo 15, com a
ferramenta de testes.

Toda dependência tem ainda um escopo, e omiti-lo escolhe `compile`, o
padrão. O escopo de dependência responde a duas perguntas: em que momentos
o artefato entra no classpath, e se ele acompanha o projeto quando outro
projeto depender dele.

| Escopo | Onde o artefato entra |
| --- | --- |
| `compile` | compilação, verificação e execução; acompanha quem depender do projeto |
| `test` | apenas na compilação e na execução das verificações; não entra no jar |
| `provided` | compilação e verificação; na execução, quem fornece é o ambiente |
| `runtime` | verificação e execução, não na compilação |

O `test` é o escopo que o capítulo 15 declara, para a ferramenta de
verificação não viajar dentro do jar do mercadinho, que não a executa.
`provided` é o escopo do que o servidor ou a plataforma de destino já
traz. E `runtime` é o do artefato que o código nunca menciona por nome e
que precisa existir quando o programa roda, como o tradutor de banco de
dados que o primeiro apêndice usa. Números de versão repetidos em mais de uma
dependência saem para uma propriedade, declarada uma vez e usada com
`${...}`, a substituição do Maven que já aparecia no
`maven.compiler.release`:

```xml
<properties>
    <gson.version>2.11.0</gson.version>
</properties>
```

```xml
<version>${gson.version}</version>
```

Junto da dependência declarada vêm as dela: se o artefato pedido depende de
outros, o Maven os baixa também, e esses são as dependências transitivas. É
o que torna o ecossistema utilizável, ninguém declara a árvore inteira à
mão, e é também uma porta de surpresas: duas dependências que pedem versões
diferentes do mesmo artefato obrigam a ferramenta a escolher uma, e o
comando `mvn dependency:tree` imprime a árvore completa quando a escolha
precisar de auditoria. A regra prática: declarar o que o código importa
diretamente, deixar o transitivo para a ferramenta, e olhar a árvore quando
algo cheirar a versão trocada.

<div class="armadilha">

Uma classe nova, `Promocao.java`, criada por engano na raiz do projeto, ao
lado do `pom.xml`, em vez de dentro de `src/main/java`:

```console
$ mvn package
[INFO] BUILD SUCCESS
```

A construção passa limpa. Onde está a classe?

</div>

Em lugar nenhum: fora da convenção, o arquivo é invisível para o Maven, que
compilou o resto e declarou sucesso, porque dele nada foi pedido sobre um
arquivo que ele não enxerga. O sintoma aparece depois, como
`cannot find symbol` em quem usar `Promocao`, ou como um jar sem a classe. A
convenção de diretórios não é sugestão: é o contrato de descoberta dos
fontes, e arquivo fora dela simplesmente não existe para a construção. O
mesmo vale para os testes, na pasta deles.

## Gradle, e a escolha do livro

O Gradle constrói sobre os mesmos conceitos, convenção de diretórios
idêntica, coordenadas idênticas, os mesmos repositórios, trocando o XML por
um script de configuração:

```
plugins {
    java
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("com.google.code.gson:gson:2.11.0")
}
```

O arquivo é mais curto, o modelo de execução é mais flexível, e projetos
grandes o adotam por desempenho de construção; o preço é um script
programável onde o Maven tem um documento fixo, e mais de um jeito de fazer
cada coisa. Este livro adota o Maven daqui em diante por três motivos
práticos: é o formato que o leitor mais vai encontrar em projetos e em
respostas na internet, o `pom.xml` se lê sem conhecer linguagem de script
nenhuma, e tudo que o livro ensinar sobre ele se traduz para Gradle trocando
a grafia, porque os conceitos deste capítulo são os mesmos nas duas
ferramentas. Quem cair num projeto Gradle lê o `build.gradle.kts` com o
vocabulário daqui: coordenada, repositório, dependência, convenção.

<div class="aprofundamento">

**O repositório local.** Tudo que o Maven baixa fica em `~/.m2/repository`,
organizado por coordenada, e cada artefato é baixado uma vez por máquina,
não por projeto. A primeira construção de um projeto novo é lenta e as
seguintes são rápidas por causa desse cache; apagar a pasta é seguro e
custa só o novo download.

</div>

## Prática

1. Converta o mercadinho para a estrutura Maven: crie o `pom.xml` deste
   capítulo, mova os fontes para `src/main/java`, rode `mvn package` e
   execute com `java -cp target/classes`. Guarde o `pom.xml` junto do
   código, e confirme que `target/` é descartável apagando-o e
   reconstruindo.

2. Reproduza a previsão: mude um preço, execute sem reconstruir, veja o
   valor antigo, reconstrua e veja o novo. Escreva a regra de trabalho em
   uma frase.

3. Reproduza a armadilha da classe fora da convenção e a conserte. Depois
   liste, com `ls target/classes`, o que a construção produziu, e confira o
   conteúdo do jar com `jar tf target/mercadinho-1.0.jar`.

4. Declare a dependência de exemplo do capítulo, rode `mvn package` e
   depois `mvn dependency:tree`. Identifique na árvore o que você declarou
   e o que veio por transitividade, e localize os arquivos correspondentes
   em `~/.m2/repository`.

5. Troque o `maven.compiler.release` para 21 e reconstrua. Anote o erro,
   explique-o com o capítulo 2, e desfaça.

6. Rode `mvn compile`, depois `mvn package`, e observe na saída quais fases
   cada um executou. Apague `target/` com `mvn clean`, confirme com `ls`, e
   reconstrua. Escreva em duas frases quando vale a pena escrever
   `mvn clean package` em vez de `mvn package`.

7. Declare a dependência de exemplo com `<scope>test</scope>`, tente usá-la
   numa classe de `src/main/java` e anote o erro de compilação. Depois mova
   a versão para uma propriedade e confirme que a construção continua
   igual. Por fim, rode `mvn install` e localize o mercadinho dentro de
   `~/.m2/repository`.

## Ficha do capítulo

| Comando | O que faz |
| --- | --- |
| `mvn compile` | compila os fontes de `src/main/java` para `target/classes` |
| `mvn package` | passa por todas as fases anteriores e empacota o jar em `target/` |
| `mvn clean` | apaga a pasta `target/` inteira; combina-se como `mvn clean package` |
| `mvn install` | põe o artefato no repositório local, para outros projetos da máquina |
| `mvn dependency:tree` | imprime a árvore de dependências, transitivas incluídas |
| `jar tf arquivo.jar` | lista o conteúdo de um jar |

| Termo | Definição |
| --- | --- |
| Maven | ferramenta de construção adotada pelo livro; descrita pelo `pom.xml` |
| Gradle | ferramenta equivalente com script de configuração; mesmos conceitos |
| convenção de diretórios | leiaute fixo (`src/main/java`, `src/test/java`, `target/`) que a ferramenta espera |
| artefato | pacote construído e distribuído; tipicamente um jar |
| coordenada | endereço único de um artefato: grupo, nome e versão |
| repositório | servidor que hospeda artefatos; o central é o padrão do ecossistema |
| dependência transitiva | dependência trazida por outra dependência |
| ciclo de vida da construção | a sequência de fases; pedir uma executa todas as anteriores |
| escopo de dependência | em que momentos o artefato entra no classpath; `compile` é o padrão |
| jar | arquivo único com bytecode e metadados, pronto para o classpath |
