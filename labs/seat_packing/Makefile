MAIN = seat_packing
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES = images-lab/*

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

