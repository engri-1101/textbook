MAIN = bipartite_matching
LAB = $(MAIN)_lab
DEMO = $(MAIN)_demo
KEY = $(LAB)_key
DATA = data/*
IMAGES = images/*
SRC = bipartite_matching.py

all: lab demo

lab: $(KEY).ipynb $(DATA) $(SRC) $(IMAGES)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(SRC) $(IMAGES)

jhub-labs: lab ../../../jhub-labs
	rm -rf ../../../jhub-labs/$(MAIN)
	mkdir ../../../jhub-labs/$(MAIN)
	unzip $(LAB).zip -d ../../../jhub-labs/$(MAIN)

demo: $(DEMO).ipynb $(DATE) $(SRC)
	zip -r $(DEMO).zip $(DEMO).ipynb $(DATA) $(SRC)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

