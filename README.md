# ssus_paper_template

The layout of an SSUS paper's repository: the data, the analysis, the
project's code as a package, the paper, and the talk, in one folder that
builds every copy of the paper from prose written once. The layout carries
no formatting of its own. The paper formats
([`ssus_papers`](https://github.com/ssus-lab/ssus_papers)), the slide format
([`ssus_slides`](https://github.com/ssus-lab/ssus_slides)), and Christopher
Kenny's [`wordcount`](https://github.com/christopherkenny/wordcount) filter
are dependencies, installed at pinned releases; so are the Python helpers
for tables and submission and [`qdiff`](https://github.com/knaaptime/qdiff)
for track-changes diffs. [Copier](https://copier.readthedocs.io) instantiates
the layout and [pixi](https://pixi.sh) runs everything after.

## Start a paper

```sh
pixi exec copier copy gh:ssus-lab/ssus_paper_template my-paper
cd my-paper
git init
pixi run init
```

Copier asks for the project's name, its Python package, and a one-line
description. `pixi run init` solves the environment, copies the paper
starter into `paper/` and the deck starter into `slides/`, and installs the
formats beside them. Then set the title, abstract, and authorship in
`paper/_quarto.yml` and write `paper/paper.qmd`.

Beyond pixi, a project needs a TeX distribution for the pdfs
(`quarto install tinytex` serves) and, for diffs,
[typst-diff](https://github.com/alexanderkoller/typst-diff):
`cargo install --locked --git https://github.com/alexanderkoller/typst-diff typst-diff`.

## The layout

```
my-paper/
├── pixi.toml          the environment, the pins, and every task
├── pyproject.toml     src/ as a package, installed editable
├── README.md          the build, for collaborators
├── AGENTS.md          the conventions, for coding agents
├── data/              the data (git-ignored)
├── notebooks/         exploratory work
├── src/<package>/     the project's code
├── analysis/          run scripts; each writes raw output to results/
│   └── tables/        formatters; each reads results/ and writes a table for the paper
├── results/           the raw outputs (CSV)
├── paper/             the manuscript, from ssus_papers' starter
└── slides/            the talk, from ssus_slides' starter
```

`paper/` and `slides/` are sibling Quarto projects, each with its own
`_quarto.yml` and `_extensions/`. The installed `_extensions/` are
committed, so a clone renders without a network.

## The tasks

| Task | Does |
|---|---|
| `init` | once: the paper and deck starters, with their formats, at the pinned tags |
| `render` | the working-paper pdf (`ssus-masthead-pdf`) |
| `html`, `preview` | the working-paper html; a live preview of it |
| `blind` | the blinded manuscript (`ssus-blind-pdf`, rendered with `--profile blind`) |
| `titlepage` | the separate title page (`ssus-titlepage-pdf`) |
| `submit` | `blind` and `titlepage`, then the journal bundle in `paper/submission/`: the upload files, the figures the manuscript includes, the blind-hygiene checklist, and a manifest (`ssus_papers.submit`) |
| `diff OLD [NEW]` | qdiff's track-changes pdf from OLD to NEW, each a git ref or a directory |
| `tables` | every formatter in `analysis/tables/`; the renders run it first |
| `slides` | the deck |
| `formats`, `versions` | reinstall every format at its pin; list the pins and the installed formats |

Every command is a pixi task, and shell runs only inside one. No task
stages, commits, or tags anything in git.

## The analysis and the tables

The analysis writes raw outputs and can be rerun at will. A formatter reads
them, formats the numbers, and writes the table with `ssus_papers.Table` as
a Quarto include (`paper/_tbl_<name>.md`), which the paper pulls in with an
`include` shortcode. Formatting touches presentation only, and no number is
typed into the manuscript by hand.

## The pins

Quarto keeps no manifest, so `pixi.toml` records every dependency's version:

- `[activation.env]` holds the source each format installs from:
  `SSUS_PAPERS` and `SSUS_SLIDES` as `org/repo@tag`, `WORDCOUNT` as a
  commit's archive, since `wordcount` has no release tags (a ref after `@`
  must be a tag or a branch; a commit sha does not resolve).
- `[pypi-dependencies]` holds `ssus-papers` (the formats' Python package,
  at the same tag as `SSUS_PAPERS`) and `qdiff`.
- `[dependencies]` holds Quarto itself, so `pixi.lock` records the Quarto
  every copy rendered with, and qdiff renders both sides of a diff with it.

To take a later release of a format, change its pin, run `pixi run formats`
(and `pixi install` for `ssus-papers`), and commit the installed folders
with the pin.

## Updating a project's layout

```sh
pixi exec copier update
```

takes this template's later changes (a new task, a corrected pin) into a
project and merges them with the project's own edits. The project's working
tree must be committed first; `.copier-answers.yml` records the template
release it last took.
