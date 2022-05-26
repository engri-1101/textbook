MAIN = simplex
LAB = $(MAIN)_lab
KEY = $(LAB)_key

all: lab

lab: $(KEY).ipynb
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

