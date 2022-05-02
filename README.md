# PhD thesis

This repository contains my PhD thesis about modeling the lymphatic progression in head and neck cancer. The work was done in Prof. Jan Unkelbach's group from September 2019 to the end of 2022.

## Layout

So far, I am using the `hepthesis` document class, because it looks nice. But maybe at some point, I will subclass that or use another one all together.

## Directory structure

The files and folders in this repo should mostly be self-explanatory, but here's a quick explanation anyways:

* `ms.tex` is the main manuscript file. All files are combined in this one.
* `preamble.tex` contains the various `\usepackage{}` directives and basically defines how LaTeX works and looks.
* `frontmatter.tex` defines all the content that comes _before_ the actual content and page numbering starts. This includes acknowledgment, abstract, declarations and so on.
* `backmatter.tex`, same as the front matter, but for stuff like list of tables/figures/acronyms, bibliography and so on.
* `glossary.tex` is where I define all the acronyms and special vocabulary for reuse.
* `math_operators.tex` holds mathematical operators and terms I have defined for easier use and less typing.
* `references.bib` is a file of BibTeX items that was generated from my Zotero catalog of references. So, if I want to add another citation that isn't in there, I should add it to Zotero first and then re-sync it with Overleaf.

### Chapters

The individual chapters (and potentially subchapters) are in the `chapters` directory and should be semantically named. They are included in the main `ms.tex` file at the root of the repo using the `subfiles` package. This enables me to quickly recompile only one chapter.

### Appendices

Same as for the chapters, but for the `appendices`.

### Figures & Plots

Figures, images and plots are placed inside a `figures` folder.