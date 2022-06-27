# Platform

This document serves to analyze potential platform options for the forthcoming
ENGRI 1101 textbook. In addition, it details a vision for the textbook, the
available formats, and the imagined student interaction.

## Vision

The textbook will exist in both a dynamic and interactive online setting
requiring a live coding platform as well as a static textbook version.
Currently, the textbook, handout, and lab materials exist largely independent
of one another. However, in the final vision, these will be much more cohesive.
Current labs consist of multiple parts that will be interspersed in the text of
the corresponding chapter. Larger and more complicated modules will find
themselves at the end of the chapter under the label of additional materials
or chapters. At a finer granularity, the textbook is made of the following
components.

- Static educational material (e.g. text, math, code & output, etc..)
- Dynamic educational material (static web-based visualizations)
- Static exercises (text-based Q&A)
- Dynamic exercises (code-based questions. E.g. "Make this change and run cell.")

The dynamic nature of the online setting allows for the full use of these
components. To compensate for the limitations of the static textbook, an
auxillary site will maintain the web-based visualizations. These can be reached
via a link in the textbook PDF or a navigated to by section if one is reading
the hard textbook. As for dynamic code-based exercises, these would exist in
Jupyter Notebooks that could be downloaded.

In the spirit of self-learning, an answer key section will be provided at the
end of the textbook with answers to all text and code based questions. In the
static textbook, this answer key could also include static output from
coding questions.

*"Given that some platforms such as Jupyter Notebooks will use Markdown for text,
I argue that the source of the textbook existing in Markdown and Jupyter Notebooks
allows for the most flexibility. Additionally, as Markdown is a more limited
format, it will reduce unforeseen errors in the translation of things such as
mathematical equations and tables."* - Henry (hwr26)

## Options

This section serves as an exploration of available platforms for the
interactive online setting of the textbook.

### [Codio][1]

This option is particularly pertinent as we are required to use it for the
Spring 2023 eCornell offering of the course. I (hwr26) am currently awaiting
access to an instructional account to test this platform myself. From available
demos, it appears to provide a powerful IDE that should handle our Jupyter
Notebooks and their embedded web-based visualizations. However, it is hard to
gauge without testing as both [Bokeh][4] and [Plotly][5] have the propensity to
work poorly with online IDEs.

### [D2L-Book][2]

Proposed by Sam Gutekunst (scg94), D2L-Book is a toolkit for producing a static
HTML website and PDF version of a textbook. It was developed for the [Dive into
Deep Learning][6] textbook. The source is written solely in Markdown files.
Additionally, the D2L-Book provides many special tags that are used to include
Python code and make references. To build the book, the Python code embedded in
these Markdown files is run to obtain the output and the specially tagged
Markdown files along with this output are combined into `.rst` files written in
a more expressive markup language called [reStructuredText][7] which is used by
a popular tool called [Sphinx][8] to build documentation. Essentially, D2L-Book
acts a wrapper for Sphinx to make the source less verbose.

As the web-based output offered by D2L-Book is static, this toolkit is not
suited for our final vision. However, I think the custom flavor of Markdown
they developed should serve as inspiration for our final product. I think this
will allow us to capture the features of LaTeX while migrating to Markdown as
the markup language for the source of the text-based textbook components.

### [Deepnote][3]

Proposed by David Williamson (dw36), Deepnote provides an online platform
for running Jupyter Notebooks. Based on the sample "workspace" David created,
the static visualizations appear to work properly. It seems this tool is most
aimed towards data scientists who want to collaboratively work on a Jupyter
Notebook. They have a new feature which allows for the publication of a
workspace although the "interactivity of published projects is still heavily
in development." While the user interface and notebooks are beautiful, it is
unlikely to suit our needs in producing an educational resource.

[1]: <https://www.codio.com> "Codio"
[2]: <https://book.d2l.ai> "D2L-Book"
[3]: <https://deepnote.com> "Deepnote"
[4]: <https://docs.bokeh.org/en/latest/> "Bokeh"
[5]: <https://plotly.com> "Plotly"
[6]: <https://d2l.ai> "Dive into Deep Learning"
[7]: <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html> "reStructuredText"
[8]: <https://www.sphinx-doc.org/en/master/index.html> "Sphinx"
