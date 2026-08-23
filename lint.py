#!/usr/bin/env python3
"""Verificador do livro. Executa as conferências que a skill manda fazer a olho.

Uso:  python3 lint.py [--esqueleto]

--esqueleto : verifica só o manifesto (ordem e adiamentos). Rode ANTES de
              escrever prosa: pega erro de dependência quando corrigi-lo
              ainda custa mover uma linha de JSON.

Sem a flag, verifica também os arquivos .md (termos, registro, ambientes).
Saída: lista de violações e código 1 se houver alguma.
"""
import json, re, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).parent
SRC = RAIZ / "src"

# Construções proibidas pelo contrato de registro (references/capitulo.md).
PROIBIDAS = [
    (r"\bé só isso\b", "interjeição"),
    (r"\bnão pensa nisso\b", "interjeição"),
    (r"\brepare que\b", "comentário sobre o texto"),
    (r"\bveja bem\b", "comentário sobre o texto"),
    (r"\bguarde\b.{0,20}\b(dor|isso)\b", "comentário sobre o texto"),
    (r"\bacredite\b", "interjeição"),
    (r"\bvocê (vai )?(adora|ama|quer construir|quer fazer)", "desejo atribuído ao leitor"),
    (r"\bcerimônia obrigatória\b", "adiamento sem prazo"),
    (r"\bpor ora,? aceite\b", "adiamento sem prazo"),
    (r"\bnão se preocupe com isso agora\b", "adiamento sem prazo"),
    (r"\bcusta caro\b", "dramatização sem consequência concreta"),
    (r"\ba coisa mais importante\b", "superlativo"),
    (r"\bmais importante\b", "superlativo"),
    (r"\bmais \w+ d[oa] livro\b", "superlativo (ranking interno)"),
    (r"\bextremamente\b", "superlativo"),
    (r"\bincr[íi]vel(mente)?\b", "superlativo"),
    (r"\bfant[áa]stic\w*", "superlativo"),
    (r"\bespetacular\w*", "superlativo"),
    (r"\babsurdamente\b", "superlativo"),
]

AMBIENTES = {"armadilha", "aprofundamento", "analogia", "previsao"}


def carregar():
    man = json.loads((RAIZ / "manifesto.json").read_text(encoding="utf-8"))
    return man, {c["id"]: c for c in man}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn").strip()


def caminho(cap):
    sub = "apendice" if cap["apendice"] else "capitulos"
    return SRC / sub / f"{cap['id']}.md"


def pos(man):
    """Posição de leitura. Apêndice vem depois de tudo."""
    return {c["id"]: (i if not c["apendice"] else 10_000 + i) for i, c in enumerate(man)}


def checar_esqueleto(man, por_id, ordem, erros):
    introduz = {}          # termo normalizado -> id do capítulo
    for cap in man:
        for t in cap["termos_introduzidos"]:
            k = norm(t)
            if k in introduz:
                erros.append(f"[{cap['id']}] termo '{t}' já introduzido em {introduz[k]}")
            else:
                introduz[k] = cap["id"]

    for cap in man:
        for termo, destino in cap["termos_adiados"].items():
            if destino not in por_id:
                erros.append(f"[{cap['id']}] adia '{termo}' para '{destino}', que não existe")
                continue
            if norm(termo) not in {norm(t) for t in por_id[destino]["termos_introduzidos"]}:
                erros.append(
                    f"[{cap['id']}] adia '{termo}' para {destino}, mas {destino} não o declara "
                    f"em termos_introduzidos"
                )
            elif ordem[destino] <= ordem[cap["id"]]:
                erros.append(
                    f"[{cap['id']}] adia '{termo}' para {destino}, que vem ANTES ou é ele mesmo"
                )
    return introduz


def checar_prosa(man, ordem, introduz, erros):
    for cap in man:
        p = caminho(cap)
        if not p.exists():
            erros.append(f"[{cap['id']}] arquivo ausente: {p}")
            continue
        txt = p.read_text(encoding="utf-8")
        if "<!-- TODO -->" in txt:
            continue  # ainda não escrito
        prosa = re.sub(r"```.*?```", "", txt, flags=re.S)      # fora dos blocos de código
        baixo = norm(prosa)

        # 1. registro
        for padrao, rotulo in PROIBIDAS:
            for m in re.finditer(padrao, prosa, flags=re.I):
                erros.append(f"[{cap['id']}] registro ({rotulo}): '{m.group(0)}'")

        # 2a. saturação de travessão: aparte se resolve com vírgula, parêntese
        #     ou frase própria; travessão é recurso raro
        n_trav = prosa.count("—")
        n_palavras = len(prosa.split())
        if n_palavras and n_trav > max(3, n_palavras // 250):
            erros.append(
                f"[{cap['id']}] {n_trav} travessões em {n_palavras} palavras "
                f"(limite: 1 a cada 250)"
            )

        # 2. saturação de segunda pessoa
        frases = [f for f in re.split(r"[.!?]\s", prosa) if f.strip()]
        com_voce = sum(1 for f in frases if re.search(r"\bvoc[êe]\b", f, re.I))
        if frases and com_voce / len(frases) > 0.34:
            erros.append(
                f"[{cap['id']}] segunda pessoa em {com_voce}/{len(frases)} frases "
                f"(limite: 1 em 3)"
            )

        # 3. termo usado antes de introduzido
        # hífen conta como parte da palavra: "long-term" não é o termo "long"
        for termo, dono in introduz.items():
            padrao_termo = rf"(?<![\w-]){re.escape(termo)}(?![\w-])"
            if ordem[dono] > ordem[cap["id"]] and re.search(padrao_termo, baixo):
                erros.append(
                    f"[{cap['id']}] usa '{termo}', que só é introduzido em {dono} "
                    f"(adie explicitamente em termos_adiados ou reordene)"
                )

        # 4. ambientes com classe válida
        for m in re.finditer(r'<div class="([^"]+)"', prosa):
            if m.group(1) not in AMBIENTES:
                erros.append(f"[{cap['id']}] ambiente desconhecido: '{m.group(1)}'")

        # 5. capítulo sem prática nem ficha
        if not re.search(r"^##.*(prática|exercícios)", prosa, re.I | re.M):
            erros.append(f"[{cap['id']}] sem seção de prática")
        if not re.search(r"^##.*ficha", prosa, re.I | re.M):
            erros.append(f"[{cap['id']}] sem ficha de referência")

        # 6. conceito de carga precisa aparecer
        for c in cap["conceitos_de_carga"]:
            if norm(c) not in baixo:
                erros.append(f"[{cap['id']}] conceito de carga não aparece no texto: '{c}'")


def main():
    so_esqueleto = "--esqueleto" in sys.argv
    man, por_id = carregar()
    ordem = pos(man)
    erros = []
    introduz = checar_esqueleto(man, por_id, ordem, erros)
    if not so_esqueleto:
        checar_prosa(man, ordem, introduz, erros)

    if erros:
        print(f"{len(erros)} violação(ões):\n")
        for e in erros:
            print("  " + e)
        return 1
    print("esqueleto ok" if so_esqueleto else "livro ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
