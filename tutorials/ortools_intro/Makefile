MAIN = ortools_intro
FIGURES = images/*

all: $(MAIN)

$(MAIN): $(MAIN).tex $(FIGURES)
	pdflatex $(MAIN).tex

clean:
	-rm -f *.{log,aux,bcf,run.xml,blg,*.blg,bbl,*.bbl,out}

.PHONY: clean all
