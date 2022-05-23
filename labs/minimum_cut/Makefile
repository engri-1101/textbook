MAIN = minimum_cut
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data-lab/*
IMAGES = images-lab/*
SRCS = max_flow.py social_network.py

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES) $(SRCS)
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRCS)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all
