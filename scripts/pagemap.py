#!/usr/bin/env python3
"""Construit la carte ligne -> page imprimee d'un texte extrait par pdftotext.

Usage:  python scripts/pagemap.py cache/<slug>/raw.txt > cache/<slug>/pagemap.tsv
        python scripts/pagemap.py cache/<slug>/raw.txt 6331      # page d'une ligne

Le decoupage se fait sur les sauts de page (\f) inseres par pdftotext ; le numero
imprime est le premier nombre isole trouve dans le bloc (en-tete ou pied de page).
Les blocs sans numero heritent du dernier numero connu.
"""
import re
import sys

NUM = re.compile(r"^\s*(\d{1,4})\s*$")


def build(path):
    """Retourne une liste de tuples (premiere_ligne, page_imprimee)."""
    blocks, current, page = [], 1, None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            if "\f" in line:
                blocks.append((current, page))
                current, page = lineno, None
            if page is None:
                hit = NUM.match(line.replace("\f", ""))
                if hit:
                    page = int(hit.group(1))
    blocks.append((current, page))

    out, last = [], 0
    for start, page in blocks:
        if page is None:
            page = last
        last = page
        out.append((start, page))
    return out


def main():
    path = sys.argv[1]
    blocks = build(path)
    if len(sys.argv) > 2:  # interrogation d'une ligne precise
        target = int(sys.argv[2])
        page = next((p for s, p in reversed(blocks) if s <= target), 0)
        print(page)
        return
    for start, page in blocks:
        print(f"{start}\t{page}")


if __name__ == "__main__":
    main()
