# Prefácio

Este é um livro de Java para quem parte do zero. Ele não assume que o leitor
já programou em outra linguagem, não assume vocabulário prévio de computação e
não assume ferramenta nenhuma além de um computador com terminal. O ponto de
chegada é o núcleo da linguagem — o que se costuma chamar de Java core: a
linguagem em si, a orientação a objetos como o Java a pratica, a biblioteca
padrão nas partes que todo programa usa, testes, e a capacidade de ler e
escrever um programa de verdade. Quem termina o livro está preparado para o
passo seguinte da maior parte das carreiras Java, que são os frameworks de
aplicação como o Spring; o livro não os cobre, mas o penúltimo capítulo
constrói à mão o mecanismo central deles, exatamente para que, ao encontrá-los,
o leitor reconheça o que já viu por dentro.

São vinte e quatro capítulos e três apêndices. A ordem não é temática, é de
dependência: cada capítulo assume todos os anteriores, cada termo técnico é
definido uma única vez, no capítulo que o apresenta, e usado livremente dali
em diante. Por isso a leitura é sequencial — pular um capítulo cobra o preço
nos seguintes. Os apêndices, sobre a construção de interfaces gráficas com
JavaFX, são os únicos desviáveis: dependem do livro inteiro, mas nada no livro
depende deles.

## O mercadinho

Do capítulo 6 ao 24, todos os exemplos e exercícios constroem o mesmo sistema:
um mercadinho de bairro, com produtos e preços, estoque, lotes e validades,
vendas, a caderneta de fiado e relatórios.
Ele cresce peça a peça — cada capítulo acrescenta o que acabou de ensinar — e
termina, no capítulo 24, como um programa completo de terminal; nos apêndices,
ganha tela.

A escolha de um sistema contínuo, no lugar dos exemplos avulsos habituais, é a
decisão pedagógica mais deliberada do livro. Exemplos desconexos não acumulam
consequência: cada um nasce limpo e morre na mesma página, e o leitor nunca vê
o que acontece com uma decisão de projeto depois que ela envelhece. Em um
sistema contínuo acontece o que acontece em software real — uma escolha
apressada no capítulo 7 cobra seu preço no capítulo 15, e consertá-la exige
mexer em código que já existia. Aprender a conviver com isso é parte do que o
livro ensina.

O mercadinho aparece pela primeira vez bem antes do capítulo 6: no capítulo 2, o
primeiro programa do livro imprime uma única linha com o nome dele. Dos
capítulos 2 ao 5, enquanto a linguagem ainda não tem peças para construir um
sistema, os exemplos são pequenos e avulsos de propósito; o nome na tela é só
o lembrete de para onde eles levam.

## Como ler este livro

O livro fala com o leitor em três notações, e vale conhecê-las antes do
primeiro capítulo.

Blocos de código aparecem de dois tipos. Os de fonte Java mostram o conteúdo
de um arquivo, e são sempre completos ou têm a omissão marcada. Os de terminal
mostram uma sessão real: as linhas que começam com `$` são o que se digita
(sem o `$`), e as linhas sem `$` são a resposta da máquina, copiada sem
edição. Mensagens de erro, em particular, aparecem por extenso — aprender a
lê-las é conteúdo do livro, não ruído.

Além do texto corrido, quatro caixas aparecem ao longo dos capítulos, cada uma
com um rótulo fixo e um papel diferente:

**Preveja antes de continuar** mostra um trecho de código e faz uma pergunta —
em geral, o que será impresso — antes de revelar a resposta. Essa caixa só
funciona com participação: pare, decida a resposta de verdade, de preferência
por escrito, e só então continue. Acertar confirma o modelo mental; errar vale
mais ainda, porque expõe exatamente a peça que estava montada errado, no
momento em que corrigi-la ainda é barato. A resposta vem sempre logo depois da
caixa. Ler a pergunta e deslizar para a resposta desperdiça o instrumento.

**Armadilha — cai nos testes** marca comportamento da linguagem que parece uma
coisa e faz outra, produzindo defeito silencioso: o programa roda, não avisa,
e o resultado está errado. É o conteúdo mais importante do livro para a vida
prática, e por isso é cobrado nos exercícios.

**Aprofundamento — nunca cai nos testes** é contexto: explica um porquê, um
mecanismo interno, uma história. Muda o entendimento, não muda o que se
escreve. Pode ser pulado sem quebrar a sequência do livro e nenhum exercício
depende dele.

**Onde a analogia quebra** acompanha as raras comparações do livro com coisas
de fora da computação. Toda analogia mente a partir de algum ponto; essa caixa
declara o ponto. O livro prefere explicação direta a analogia, e quando abre
essa exceção, o limite vem junto.

Cada capítulo abre com um problema concreto e fecha com duas seções fixas. A
**Prática** traz exercícios sem resposta publicada — de propósito, porque o
critério de acerto (o programa compila? imprime o que a previsão dizia?) está
na máquina do leitor, e porque exercício com gabarito ao lado treina
conferência, não construção. A **Ficha** resume em tabelas os comandos e
termos do capítulo, para consulta rápida quando um capítulo posterior os
reutilizar.

## O que é preciso ter

Um computador com Windows, Linux ou macOS, um terminal, um editor de texto
qualquer e um JDK da versão 25 ou mais nova — o capítulo 1 explica o que é um
JDK, de onde baixar e como conferir a versão. Até o capítulo 13, nenhum outro
programa é necessário.

Um ambiente integrado de desenvolvimento — IDE, de *integrated development
environment*, os programas como IntelliJ IDEA e Eclipse que reúnem editor,
compilador e depurador — vai ser útil mais adiante, mas os primeiros capítulos
são feitos deliberadamente no terminal. A IDE esconde exatamente os comandos
que esses capítulos ensinam, e quem aprende primeiro o que a ferramenta
esconde depois usa a ferramenta entendendo o que ela faz — o contrário não
acontece.

O livro usa Java 25 porque é a versão de suporte longo mais recente na
escrita, e porque um recurso dela — explicado no capítulo 2 — deixa os
primeiros programas do tamanho que programas de primeiro capítulo deveriam ter
tido desde sempre.
