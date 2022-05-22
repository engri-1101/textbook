MAIN = baseball_elimination
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
SRC = max_flow.py

all: $(MAIN)

$(MAIN): $(KEY).ipynb $(DATA)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(SRC)

clean:
	-rm -f $(LAB).{zip,ipynb}

.PHONY: clean all

