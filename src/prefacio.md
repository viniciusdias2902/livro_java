<div class="capa">

![Java 25](capa.png)

</div>

# Prefácio

Este é um livro de Java para quem parte do zero. Ele não assume que o leitor
já programou em outra linguagem, não assume vocabulário prévio de computação e
não assume ferramenta nenhuma além de um computador com terminal. O ponto de
chegada é o núcleo da linguagem, o que se costuma chamar de Java core: a
linguagem em si, a orientação a objetos como o Java a pratica, a biblioteca
padrão nas partes que todo programa usa, testes, e a capacidade de ler e
escrever um programa de verdade. O livro é uma experiência completa em si:
termina com um sistema real, construído do zero e funcionando no terminal, e
nada nele depende de um passo seguinte. Quem quiser seguir adiante encontra o
caminho preparado, porque os frameworks de aplicação, como o Spring, são o
rumo mais comum das carreiras Java, e o penúltimo capítulo constrói à mão o
mecanismo central deles. Quem não quiser não perde nada: esse mesmo capítulo
vale por si, como técnica de organizar programas grandes.

São vinte e cinco capítulos e quatro apêndices. A ordem não é temática, é de
dependência: cada capítulo assume todos os anteriores, cada termo técnico é
definido uma única vez, no capítulo que o apresenta, e usado livremente dali
em diante. Por isso a leitura é sequencial, e pular um capítulo cobra o preço
nos seguintes. Os apêndices são os únicos desviáveis: dependem do livro
inteiro, mas nada no livro depende deles. O primeiro leva o projeto do livro
para um banco de dados com JDBC, e é o único ponto em que o livro assume
conhecimento de fora, a saber, SQL e um banco configurado; ele declara isso na
própria abertura, junto com material de referência para quem precisar. Os
outros três constroem interfaces gráficas com JavaFX.

## O mercadinho

Do capítulo 7 ao 25, todos os exemplos e exercícios constroem o mesmo sistema:
um mercadinho de bairro, com produtos e preços, estoque, lotes e validades,
vendas, a caderneta de fiado e relatórios. Ele cresce peça a peça, cada
capítulo acrescentando o que acabou de ensinar, e termina, no capítulo 25,
como um programa completo de terminal; nos apêndices, ganha tela.

A escolha de um sistema contínuo, no lugar dos exemplos avulsos habituais, é
uma decisão pedagógica deliberada. Exemplos desconexos não acumulam
consequência: cada um nasce limpo e morre na mesma página, e o leitor nunca vê
o que acontece com uma decisão de projeto depois que ela envelhece. Em um
sistema contínuo acontece o que acontece em software real: uma escolha
apressada no capítulo 7 cobra seu preço no capítulo 15, e consertá-la exige
mexer em código que já existia. Aprender a conviver com isso é parte do que o
livro ensina.

O mercadinho aparece pela primeira vez bem antes do capítulo 7: no capítulo 2,
o primeiro programa do livro imprime uma única linha com o nome dele. Dos
capítulos 2 ao 6, enquanto a linguagem ainda não tem peças para construir um
sistema, os exemplos são pequenos e avulsos de propósito; o nome na tela é só
o lembrete de para onde eles levam.

## Como ler este livro

O livro fala com o leitor em três notações, e vale conhecê-las antes do
primeiro capítulo.

Blocos de código aparecem de dois tipos. Os de fonte Java mostram o conteúdo
de um arquivo, e são sempre completos ou têm a omissão marcada. Os de terminal
mostram uma sessão real: as linhas que começam com `$` são o que se digita
(sem o `$`), e as linhas sem `$` são a resposta da máquina, copiada sem
edição. Mensagens de erro, em particular, aparecem por extenso, porque
aprender a lê-las é conteúdo do livro, não ruído.

Além do texto corrido, quatro caixas aparecem ao longo dos capítulos. Cada uma
se apresenta abaixo com a mesma aparência que terá lá dentro:

<div class="previsao">

Esta caixa mostra um trecho de código e faz uma pergunta, em geral sobre o que
será impresso, antes de revelar a resposta. Ela só funciona com participação:
pare, decida a resposta de verdade, de preferência por escrito, e só então
continue. Acertar confirma o modelo mental; errar vale mais ainda, porque
expõe exatamente a peça que estava montada errado, no momento em que
corrigi-la ainda é barato. A resposta vem sempre logo depois da caixa. Ler a
pergunta e deslizar para a resposta desperdiça o instrumento.

</div>

<div class="armadilha">

Esta caixa marca comportamento da linguagem que parece uma coisa e faz outra,
produzindo defeito silencioso: o programa roda, não avisa, e o resultado está
errado. Na vida prática, é dessa família que saem os defeitos que atravessam
testes e chegam a quem usa o programa, e por isso a caixa é cobrada nos
exercícios.

</div>

<div class="aprofundamento">

Esta caixa é contexto: explica um porquê, um mecanismo interno, uma história.
Muda o entendimento, não muda o que se escreve. Pode ser pulada sem quebrar a
sequência do livro e nenhum exercício depende dela.

</div>

<div class="analogia">

Esta caixa acompanha as raras comparações do livro com coisas de fora da
computação. Toda analogia mente a partir de algum ponto; a caixa declara o
ponto. O livro prefere explicação direta a analogia, e quando abre essa
exceção, o limite vem junto.

</div>

Cada capítulo abre com um problema concreto e fecha com duas seções fixas. A
**Prática** traz exercícios sem resposta publicada, de propósito: o critério
de acerto (o programa compila? imprime o que a previsão dizia?) está na
máquina do leitor, e exercício com gabarito ao lado treina conferência, não
construção. A **Ficha** resume em tabelas os comandos e termos do capítulo,
para consulta rápida quando um capítulo posterior os reutilizar.

## O que é preciso ter

Um computador com Windows, Linux ou macOS, um terminal, um editor de texto
qualquer e um JDK da versão 25 ou mais nova; o capítulo 1 explica o que é um
JDK, de onde baixar e como conferir a versão. Até o capítulo 14, nenhum outro
programa é necessário.

Um ambiente integrado de desenvolvimento vai ser útil mais adiante, mas os
primeiros capítulos são feitos deliberadamente no terminal. IDE, de
*integrated development environment*, é o nome desses programas que reúnem
editor, compilador e depurador, como o IntelliJ IDEA e o Eclipse. A IDE
esconde exatamente os comandos que os primeiros capítulos ensinam, e quem
aprende primeiro o que a ferramenta esconde depois a usa entendendo o que ela
faz; o contrário não acontece.

O livro usa Java 25 porque é a versão de suporte longo mais recente na
escrita, e porque um recurso dela, explicado no capítulo 2, deixa os primeiros
programas do tamanho que programas de primeiro capítulo deveriam ter tido
desde sempre.

## Sobre esta edição

A versão 1.0 deste livro foi inteiramente gerada por inteligência artificial,
sob direção humana. A geração não foi livre: o texto foi produzido sob um
contrato de estilo explícito, com verificação mecânica a cada capítulo, e
todos os capítulos passaram por extensa revisão humana, que definiu o escopo,
a ordem, o domínio dos exemplos e corrigiu o que a máquina errou. O registro
fica aqui por honestidade com quem lê: nenhuma parte do texto finge uma origem
que não tem.
