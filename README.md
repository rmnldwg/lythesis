![social card](./github-social-card.png)

* _University:_ **University of Zurich ([UZH])**
* _Department:_ **Department of Physics**
* _Supervisor:_ **Prof. Jan Unkelbach**
* _Time:_ **September 2019 - December 2022**

This repository contains the source code for my PhD dissertation. It is set up to be - above all - modular and reproducible. Below follows a quick guide to this repository's layout.


## Requirements

To compile this thesis, one needs a TeX distribution. Ideally TeX Live 2022, I have noticed some errors with TeXt Live 2019.

All figures in the thesis are compiled using scripts that are contained in this repository. This means, given the correct data, one can recreate all plots. This is not necessary for compiling the thesis, because the figures are also contained in the repository, but if anyone wants to check if I have done everything correctly, feel free to do so.

To recreate all figures, in addition to a TeX Live distribution, one needs...
1. Python 3.8 or later installed. Ideally one has also created a virtual environment.
2. an installation of [Inkscape] to convert `.svg` plots into a `.pdf` and a `.pdf_tex` file each.

The section below lays out the steps for recreating the figures.


## Reproduce

If you want to reproduce the thesis, i.e. recompile it and recreate all the figures, do the following (ideally inside a virtual environment, like [`venv`]):

First, install the dependencies:

```
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Then, update all the data sources. You could go through all `data` folders inside every chapter's directory and execute `dvc update -R .` but there is a faster way. At the root of the repository, call

```
find -iname "*.dvc" -exec dvc update {} \;
```

Next, the plots can be reproduced by telling the tool [DVC] to rerun the pipelines that were defined with its help. Again, this could be done chapter by chapter, but the shorthand command is

```
find -iname "dvc.yaml" -exec dvc repro {} \;
```

And after this, you can build the entire document by running

```
latexmk -synctex=1 -interaction=nonstopmode -file-line-error -pdf -outdir=_build main
```

Now your `_build` directory at the root of the repo should contain a beautifully rendered `main.pdf` :+1:

## Repository Structure

### Subfiles

I make heavy use of LaTeX's [`subfiles`] package to make everything as modular as possible. The `main.tex` contains no content, except the thesis title, author and date. It only loads in other files and directories.

1. First, it loads the `preamble.tex`, where I define all the packages and set up the document. There I also load the `math_operators.tex` I defined for myself and an extensive `glossary.tex` of abbreviations.
2. Then - after defining title, author and date - it loads the `content/frontmatter.tex`, where one can find the abstract and acknowledgement along with the ToC.
3. Thirdly, all the content is pulled in from subdirectories within the folder `content`. It does, however, not include content files directly, but `content/<title>/_chapter.tex` files, that - like the `main.tex` - don't have much content in them. These chapter TeX files, too, use subfiles to include the sections within the respective chapter. This makes it super easy to in- or exclude entire sections and chapters.
4. In the end, like the `content/frontmatter.tex` a file `content/backmatter.tex` defines what follows after the main body. Like a table of figures and stuff like that.

Since it is set up such that every `.tex` file that has a `document` environment in it compiles into a working PDF, this repo should have `_build` directories on every level. I have configured VS Code such that it always puts intermediate files and compiled PDFs there. These folders can then just be ignored by git to keep the repo uncluttered.

### Data

In every chapter folder I placed `data` directories that hold data that will be plotted in some form or another. The data is imported and versioned using [DVC].

I do not intend to put raw data here which then runs in an hours long inference process to produce a single figure in the end, but rather _outputs_ of such inference processes. In my case, the inference pipelines are stored in the repository [`lynference`].

### Figures

The root and every chapter folder also have `figures` directories in them. This is the place to store...

1. static images to be displayed in the thesis
2. scripts that produce plots of computed results

For the second point, I again rely heavily on [DVC]. This tool defines which files in the respective `data` folder to use with which (Python) script to produce exactly which version (using MD5 hashes) of a plot.

## Make this _YOUR_ thesis

In order to use this thesis as a template, first delete the content of all `_build` folders. Then, delete all the directories inside the `content` folder and replace them with your chapters.

You also need to adapt some stuff in the `frontmatter.tex`, `backmatter.tex` and of course the title, author and date in the `main.tex`.

Finally, replace the `references.bib` with your list of references and adapt/extend the `math_operators.tex` and `glossary.tex` to what you need.

### Troubleshooting with figures

I often stumbled over the `graphicspath` setting and how it interacts with the `subfiles` package. If the build fails because some figure has not been found, this is likely the issue.

In that case, make sure that in the `preamble.tex` the path to all `figures` directories is listed (each in their own `{}` bracket pair and **not** separated by commas). Also make sure each `_chapter.tex` lists `\subfix{./figures/}` in their `graphicspath` setting. And the same goes for the other section files in each chapter's directory.

That _should_ fix all errors regarding LaTeX not being able to find figures.


[UZH]: https://www.uzh.ch/en.html
[TeX Live]: https://tug.org/texlive/
[DVC]: https://dvc.org
[Inkscape]: https://inkscape.org/
[`subfiles`]: https://www.ctan.org/pkg/subfiles
[`lynference`]: https://github.com/rmnldwg/lynference
[`venv`]: https://docs.python.org/3/library/venv.html
