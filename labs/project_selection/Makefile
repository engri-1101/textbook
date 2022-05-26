MAIN = project_selection
LAB = $(MAIN)_lab
KEY = $(LAB)_key
IMAGES = images-lab/*

all: lab

lab: $(KEY).ipynb $(IMAGES)
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all
