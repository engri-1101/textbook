MAIN = maximum_flow
LAB = $(MAIN)_lab
KEY = $(LAB)_key
IMAGES = images-lab/*
SRC = max_flow.py

all: lab

lab: $(KEY).ipynb $(IMAGES) $(SRC)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES) $(SRC)

jhub-labs: lab ../../../jhub-labs
	rm -rf ../../../jhub-labs/$(MAIN)
	mkdir ../../../jhub-labs/$(MAIN)
	unzip $(LAB).zip -d ../../../jhub-labs/$(MAIN)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

