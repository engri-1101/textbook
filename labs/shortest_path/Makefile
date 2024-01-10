MAIN = shortest_path
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DEMO = $(MAIN)_demo
DATA = data/*
SRC = graph_tools.py

all: lab demo

lab: $(KEY).ipynb $(DATA) $(SRC)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(SRC)

jhub-labs: lab ../../../jhub-labs
	rm -rf ../../../jhub-labs/$(MAIN)
	mkdir ../../../jhub-labs/$(MAIN)
	unzip $(LAB).zip -d ../../../jhub-labs/$(MAIN)

demo: $(DEMO).ipynb $(DATA) $(SRC)
	zip -r $(DEMO).zip $(DEMO).ipynb $(DATA) $(SRC)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

