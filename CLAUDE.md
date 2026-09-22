# BOOK_REVIEW — Lecture de livres et construction de résumés

Projet personnel de lecture assistée : à partir d'un livre (PDF, EPUB, papier, transcription
audio ou simple référence bibliographique), produire un ensemble de **notes Markdown
portables vers un vault Obsidian**.

Corpus visé : **ouvrages techniques et professionnels** (informatique, finance, trading,
méthodes de travail). L'objectif n'est pas la culture générale mais l'**extraction de
méthodes, règles, formules et checklists actionnables**.

---

## 1. Arborescence

```
BOOK_REVIEW/
├── CLAUDE.md
├── inbox/          Fichiers sources déposés, non encore traités
├── notes/          ← DESTINÉ AU VAULT OBSIDIAN
│   ├── <Titre>.md      une note par livre (tous les niveaux de lecture)
│   └── concepts/       notes atomiques de concepts, mutualisées entre livres
├── attachments/    ← DESTINÉ AU VAULT (PDF, EPUB, transcriptions, images)
├── cache/          Texte extrait, découpage en chapitres — jetable, non versionné
└── scripts/        Utilitaires d'extraction ajoutés au fil des besoins
```

`notes/` et `attachments/` sont conçus pour être **copiés tels quels dans le vault
Obsidian**, sans rien réécrire. Tout le reste est de la machinerie locale.

### Destination dans le vault

Vault cible : `C:\myDrive\Personnel\Obsidian\myNotes` (structure PARA).

| Source | Destination |
|---|---|
| `notes/<Titre>.md` | `3_Ressources/Livres/<thème>/` — à côté de son PDF |
| `attachments/<Titre>.pdf` | `3_Ressources/Livres/<thème>/` — même nom de base que la note |
| `notes/concepts/*.md` | `2_Connaissances/<domaine>/Concepts/` |

Le résumé vit avec sa source : un livre = un endroit, et les deux fichiers portant le même
nom s'affichent côte à côte dans l'explorateur. Les `<thème>` existants sont
`1_Certifications`, `2_Trading et marches`, `3_Portefeuille et risque`,
`4_Finance d'entreprise et MA`, `5_Economie et macro`, `6_Data science et ML`,
`7_Developpement logiciel`, `8_Mindset et developpement perso`, `9_Divers`.

Les notes de concepts vont ailleurs, et c'est délibéré : un concept est transversal
(`[[Kelly Criterion]]` sera nourri par plusieurs livres), il n'appartient donc à aucun
dossier de livre. `<domaine>` suit le découpage existant de `2_Connaissances` :
`Personnelles`, `Professionnelles`, `Techniques`, `Trading`.

L'index `3_Ressources/Livres/Résumés.md` recense les résumés via Dataview (`WHERE auteur`,
seuls les résumés ont ce champ) — rien à maintenir à la main.

### Avant de copier : vérifier les doublons

La bibliothèque contient 189 PDF, souvent nommés par leur source d'origine
(`Titre -- Auteur -- éditeur -- <md5> -- Anna's Archive.pdf`). **Toujours vérifier que
l'ouvrage n'y est pas déjà** avant de copier une pièce jointe, en comparant le MD5 plutôt
que le nom :

```bash
find "$VAULT/3_Ressources/Livres" -iname "*<mot du titre>*"
md5sum "attachments/<Titre>.pdf"   # le md5 figure dans les noms Anna's Archive
```

### Règle de portabilité (impérative)

- Liens internes : **wikilinks courts sans chemin** — `[[Kelly Criterion]]`, jamais
  `[[concepts/Kelly Criterion]]` ni `[[../notes/...]]`. Obsidian résout par nom dans tout
  le vault, donc les liens survivent à n'importe quel déplacement de dossier.
- Pièces jointes : même règle — `![[Thinking in Bets.pdf]]`.
- Aucun chemin absolu, aucun lien Markdown `[x](./y.md)` vers une note.
- Le dossier `BOOK_REVIEW/` peut être ouvert directement comme vault Obsidian pour relire
  et vérifier les liens avant migration.

---

## 2. Nommage

- Note de livre : **titre simple**, tel qu'il se cite — `Thinking in Bets.md`.
  Sous-titre omis. Pas de préfixe, pas d'auteur dans le nom.
- Note de concept : nom du concept au singulier — `concepts/Expected Value.md`.
- Pièce jointe : même titre que la note — `attachments/Thinking in Bets.pdf`.
- En cas d'homonymie seulement, désambiguïser par l'auteur : `Antifragile (Taleb).md`.

**Les noms de fichiers d'origine sont systématiquement raccourcis.** Un PDF déposé sous
son nom de source (`Titre -- Auteur -- éditeur -- <md5> -- Anna's Archive.pdf`, ~215
caractères) est renommé au titre court dès son passage dans `attachments/`. Deux raisons :
les wikilinks deviennent illisibles, et surtout `LongPathsEnabled` vaut `0` sur cette
machine — un tel nom dans `3_Ressources/Livres/<thème>/` produit un chemin de ~294
caractères, au-delà de la limite Windows de 260, que ni `git`, ni l'Explorateur, ni la
plupart des scripts ne savent manipuler sans le préfixe `\\?\`.

---

## 3. Langue

- **Par défaut : la langue du livre.** Un ouvrage anglais donne des notes en anglais,
  au plus près du vocabulaire technique de l'auteur.
- Sur demande (`--lang=fr`) : rédaction en français, **termes techniques conservés en
  anglais** entre parenthèses au premier emploi — « dimensionnement de position
  (position sizing) ». Les citations restent toujours en VO, traduction en dessous si utile.
- Le frontmatter (`langue:`) indique la langue **du livre**, pas celle des notes.

---

## 4. Chaîne d'extraction

Trois voies, à choisir dans cet ordre de préférence :

1. **Extraction outillée (défaut)** — le texte est extrait une fois vers `cache/<slug>/`
   puis lu depuis là.
   - PDF : `pdftotext -layout "attachments/X.pdf" "cache/<slug>/raw.txt"`
   - EPUB : `pandoc -t plain "attachments/X.epub" -o "cache/<slug>/raw.txt"`
   - Découpage en chapitres vers `cache/<slug>/NN-titre.txt` quand le livre est volumineux.
   - Outils disponibles sur la machine : Python 3.11 (Anaconda), pandoc, pdftotext,
     ffmpeg, node, git. Tout script récurrent va dans `scripts/`.
2. **Lecture directe** — si l'extraction échoue (PDF scanné, mise en page complexe),
   lecture du PDF avec l'outil natif, par plages de pages.
3. **Sans texte source** — livre papier, ou simple référence bibliographique : les notes
   sont construites à partir de mes notes manuelles et/ou de la connaissance + recherche web.

⚠️ Dans le cas 3 sans texte source, la note **doit** porter `source: web` en frontmatter et
un encart en tête : résumé de seconde main, non vérifié sur le texte original, pagination
absente. On ne fabrique **jamais** de numéro de page ni de citation verbatim dans ce cas.

Sources audio/vidéo : je fournis moi-même la transcription (`.txt` / `.srt`) dans `inbox/`.
Aucune transcription automatique n'est faite par le projet.

---

## 5. Déroulé du traitement d'un livre

Déclencheur type : « traite le livre X » / « résume le PDF déposé dans inbox ».
Le traitement se fait **d'une traite, sans point de validation intermédiaire** ; je relis à la fin.

1. Identifier l'ouvrage (titre, auteur, année, éditeur, ISBN, langue, pagination) — recherche
   web si les métadonnées ne sont pas dans le fichier.
2. Déplacer la source de `inbox/` vers `attachments/` en la renommant d'après le titre.
3. Extraire le texte vers `cache/<slug>/` (§4).
4. Reconstituer le plan réel de l'ouvrage (parties, chapitres) depuis la table des matières.
5. Rédiger `notes/<Titre>.md` en entier (§6).
6. Créer ou enrichir les notes de concepts dans `notes/concepts/` (§7).
7. Rapport final : chemin des notes créées, concepts ajoutés ou complétés, passages qui ont
   résisté à l'extraction, points où j'ai dû combler un trou.

---

## 6. Gabarit de la note de livre

Trois niveaux de lecture dans un seul fichier, du plus court au plus long.

```markdown
---
titre: Thinking in Bets
sous_titre: Making Smarter Decisions When You Don't Have All the Facts
auteur: Annie Duke
annee: 2018
editeur: Portfolio
isbn: 978-0735216358
langue: en
nb_pages: 288
type: technique
source: pdf
tags: [livre/technique/decision]
domaines: [prise de décision, probabilités]
concepts_cles: ["[[Resulting]]", "[[Expected Value]]"]
livres_lies: ["[[Fooled by Randomness]]"]
---
```

Puis, dans cet ordre :

- `# <Titre>` — titre complet, auteur, année en une ligne.
- **Pitch** — 3 lignes maximum, en callout `> [!abstract]`. La thèse centrale, rien d'autre.
- **Synthèse** — environ une page. Ce que défend l'auteur, comment il l'argumente, ce que
  le livre apporte concrètement. Se lit seule, sans le reste.
- **Plan d'action** — la partie la plus importante pour un livre technique. Les méthodes
  du livre converties en étapes applicables, règles chiffrées, checklists. Format liste à
  cocher. Chaque élément renvoie au chapitre d'origine.
- **Résumé détaillé** — une sous-section `### Ch.N — Titre` par chapitre :
  idée directrice (1-2 phrases), points clés (puces), formules/méthodes s'il y en a,
  citations marquantes avec pagination.
- **Citations** — extraits verbatim regroupés, typographiquement distincts de toute
  paraphrase : `> « ... » (p. 42)`. Une citation sans page vérifiable n'est pas une citation :
  elle est reformulée en paraphrase.
- **Esprit critique** — section obligatoire, jamais complaisante : limites de la thèse,
  biais et angles morts de l'auteur, affirmations non étayées, ce qui a vieilli, ce qu'il
  faut vérifier ailleurs. Si le livre est solide, le dire et expliquer pourquoi.
- **Liens** — livres du corpus en accord ou en contradiction, avec une ligne d'explication
  par lien. Pas de liste de wikilinks nus.

### Fidélité

- Distinguer systématiquement ce que **dit l'auteur** de ce que **j'en conclus** : la voix
  personnelle vit dans « Plan d'action », « Esprit critique » et « Liens », pas dans le
  résumé détaillé.
- Ne jamais inventer une donnée, une étude ou un chiffre absent du texte. Un chiffre cité
  par l'auteur reste attribué à l'auteur.
- Pagination systématique dès qu'on dispose du texte source.

---

## 7. Notes de concepts

Un concept devient une note atomique dans `notes/concepts/` dès qu'il est **réutilisable
hors du livre** (une méthode, un biais, une formule, un modèle mental) — pas pour chaque
idée du livre.

- Court : définition, mécanisme, quand l'appliquer, quand il échoue.
- Frontmatter minimal : `type: concept`, `tags`, `livres: ["[[Titre]]"]`.
- Si la note existe déjà, on **l'enrichit** avec l'apport du nouveau livre plutôt que d'en
  créer une seconde : ajouter une section `## Selon [[Titre]]` et compléter `livres:`.
- Quand deux livres se contredisent sur un concept, la contradiction est exposée dans la
  note de concept, sans trancher arbitrairement.

Pas de note d'index ni de MOC à maintenir : le graphe et la recherche Obsidian s'en chargent.

---

## 8. Conventions de frontmatter

Le vault `myNotes` a sa propre convention, qui prime : **clé `title:` en tête**, `aliases:`
juste après, et **toute valeur multiple en liste YAML**, jamais en tableau sur une ligne.

```yaml
---
title: Systematic Trading
aliases:
  - Carver - Systematic Trading
auteur: Robert Carver
tags:
  - livre/technique/trading
---
```

Champs suivis : **bibliographiques** (`title`, `aliases`, `sous_titre`, `auteur`, `annee`,
`editeur`, `isbn`, `langue`, `nb_pages`, `type`, `source`) et **classement Obsidian**
(`tags`, `domaines`, `concepts_cles`, `livres_lies`).

`auteur` sert de marqueur : c'est le champ sur lequel l'index `Résumés.md` distingue un
résumé d'un PDF. Ne jamais l'omettre.

Pas de suivi de lecture (statut, dates, progression) ni de note d'évaluation : volontairement
hors périmètre.

Tags hiérarchisés, en minuscules, sans accent : `livre/technique/finance`,
`concept/probabilites`.

---

## 9. Git

Dépôt local + remote GitHub **privé** (notes personnelles, sources sous droits d'auteur).

- Versionné : `CLAUDE.md`, `notes/`, `scripts/`.
- Ignoré : `cache/`, `inbox/`, et les binaires de `attachments/` (PDF, EPUB, audio) — trop
  lourds pour GitHub et sous copyright. Les transcriptions `.txt` / `.md` d'`attachments/`
  sont versionnées.
- Commits en français, un commit par livre traité : `notes: <Titre> (<Auteur>)`.
- `gh` n'est pas installé sur cette machine : la création du remote se fait à la main ou
  après installation de GitHub CLI.
