MAIN = game_theory
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES = images/*
SRC = penaltykickgame/*

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRC)  

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

