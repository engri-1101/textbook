MAIN = diet
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DEMO = $(MAIN)_demo
DATA = data/*
SRC = graph_tools.py

all: lab demo

lab: $(KEY).ipynb $(DATA) $(SRC)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(SRC)

demo: $(DEMO).ipynb $(DATA) $(SRC)
	zip -r $(DEMO).zip $(DEMO).ipynb $(DATA) $(SRC)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

