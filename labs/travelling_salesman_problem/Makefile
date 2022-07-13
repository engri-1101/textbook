MAIN = travelling_salesman_problem
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DEMO = radio_telescope_demo
DATA = data/*
DEMO_DATA = data-demo/*
IMAGES = images/*
SRC = tsp.py

all: lab demo

lab: $(KEY).ipynb $(DATA) $(IMAGES) $(SRC)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRC)

demo: $(DEMO).ipynb $(DEMO_DATA)
	zip -r $(DEMO).zip $(DEMO).ipynb $(DEMO_DATA)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

