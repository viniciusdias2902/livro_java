<div align="center">

<img src="src/capa.png" alt="Capa do livro Java 25" width="340">

# Java 25

**Java do zero ao núcleo da linguagem, construindo um sistema completo de terminal.**

*Livro didático em português brasileiro · Por Vinícius Dias*

</div>

---

## O livro

Um livro para quem parte do zero em programação e quer chegar ao domínio do Java moderno: Java 25, com arquivos-fonte compactos, records, sealed types, pattern matching, streams, virtual threads e Maven. A partir do capítulo 7, um fio condutor único, um mercadinho de bairro, cresce capítulo a capítulo até culminar no projeto integrador: um sistema de terminal com arquitetura em camadas e MVC, testado e empacotado de ponta a ponta.

O texto segue algumas convenções fixas, explicadas no prefácio:

- **Previsão** — o código aparece antes da explicação, com a pergunta "o que este trecho imprime?" antes da resposta;
- **Armadilha** — comportamento contraintuitivo que produz bug silencioso, sempre demonstrado com saída real;
- **Aprofundamento** — contexto opcional, nunca cobrado adiante;
- **Ficha do capítulo** — as definições e chamadas essenciais, recolhidas no fim de cada capítulo.

Toda saída de programa mostrada no livro foi reproduzida em execução real num JDK 25.

## Sumário em uma olhada

| Parte | Capítulos |
| --- | --- |
| Fundamentos | 1–6 · linguagem e plataforma, execução, valores, fluxo de controle, referências, Math e Random |
| Orientação a objetos | 7–13 · classes, herança, interfaces, equals/hashCode, records, sealed types, exceções |
| Ferramentas e biblioteca padrão | 14–22 · Maven, JUnit 5, generics, coleções, lambdas, streams, java.time, I/O, concorrência |
| Ecossistema e projeto | 23–25 · reflection, injeção de dependência, projeto integrador com MVC |
| Apêndices | JDBC, interface gráfica com JavaFX (três apêndices) e leitura de código legado |

## Como compilar o livro

O HTML é gerado com [mdBook](https://rust-lang.github.io/mdBook/) e o preprocessador [mdbook-mermaid](https://github.com/badboy/mdbook-mermaid):

```bash
cargo install mdbook mdbook-mermaid
mdbook serve --open
```

`mdbook build` gera a versão estática na pasta `book/`.

## Estrutura do repositório

| Caminho | Conteúdo |
| --- | --- |
| `src/capitulos/` | os 25 capítulos, em Markdown |
| `src/apendice/` | os apêndices |
| `src/titulo.md` / `src/prefacio.md` | página de rosto e prefácio |
| `theme/` | tema visual do livro (modus-vivendi) |
| `lint.py` | verificador de registro, estilo e dependências entre capítulos |
| `manifesto.json` | o mapa do livro: termos introduzidos e adiados por capítulo |
| `REVISAO.md` | o protocolo de revisão em duas passadas de cada capítulo |

## Sobre esta edição

A versão 1.0 deste livro foi integralmente gerada por inteligência artificial, com extensa revisão humana de todos os capítulos. Com as contribuições da comunidade e escrita própria, a versão 2.0 virá mais humanizada e revisada; a 1.0 veio ao mundo porque fez falta um livro de Java atualizado, em português, com uma abordagem que atendesse a todas as necessidades de quem o escreveu, e que bem podem ser as suas.

## Contribuições

Correções, sugestões didáticas e melhorias de texto são bem-vindas por issue ou pull request. Antes de propor mudança em capítulo, vale ler o `REVISAO.md` e rodar `python3 lint.py`, que verificam o registro e as regras de dependência que o livro segue.

Boa sorte a todos que vão aprender usando este livro.
