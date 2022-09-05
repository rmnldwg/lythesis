![social card](./github-social-card.png)

* _University:_ **University of Zurich (UZH)**
* _Department:_ **Department of Physics**
* _Supervisor:_ **Prof. Jan Unkelbach**
* _Time:_ **September 2019 - December 2022**

## Set up

This repository contains the source code for my PhD dissertation. It is set up to be - above all - modular and reproducible. Below follows a quick guide to this repository's layout.

### Subfiles

I make heavy use of LaTeX's [`subfiles`] package to make everything as modular as possible. The `main.tex` contains no content, except the thesis title, author and date. It only loads in other files and directories.

1. First, it loads the `preamble.tex`, where I define all the packages and set up the document. There I also load the `math_operators.tex` I defined for myself and an extensive `glossary.tex` of abbreviations.
2. Then - after defining title, author and date - it loads the `content/frontmatter.tex`, where one can find the abstract and acknowledgement along with the ToC.
3. Thirdly, all the content is pulled in from subdirectories within the folder `content`. It does, however, not include content files directly, but `content/<title>/_chapter.tex` files, that - like the `main.tex` - don't have much content in them. These chapter TeX files, too, use subfiles to include the sections within the respective chapter. This makes it super easy to in- or exclude entire sections and chapters.
4. In the end, like the `content/frontmatter.tex` a file `content/backmatter.tex` defines what follows after the main body. Like a table of figures and stuff like that.

Since it is set up such that every `.tex` file that has a `document` environment in it compiles into a working PDF, this repo should have `_build` directories on every level. I have configured VS Code such that it always puts intermediate files and compiled PDFs there. These folders can then just be ignored by git to keep the repo uncluttered.

### Data

In every chapter folder I placed `data` directories that hold data that will be plotted in some form or another. The data is imported and versioned using a tool called _Data Version Control_ ([DVC]).

I do not intend to put raw data here which then runs in an hours long inference process to produce a single figure in the end, but rather _outputs_ of such inference processes. In my case, the inference pipelines are stored in the repository [`lynference`].

### Figures

The root and every chapter folder also have `figures` directories in them. This is the place to store...

1. ...static images to be displayed in the thesis (straightforward)
2. ...scripts that produce plots of computed results (more intricate)

For the second point, I again rely heavily on [DVC]. This tool defines which files in the respective `data` folder to use with which script to produce exactly which version (using MD5 hashes) of a plot.



[`subfiles`]: https://www.ctan.org/pkg/subfiles
[`lynference`]: https://github.com/rmnldwg/lynference
[DVC]: https://dvc.org
