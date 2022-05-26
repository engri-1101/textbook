MAIN = branch_and_bound
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DEMO = $(MAIN)_demo
DATA = data/*
LAB_IMAGES = images-lab/*
DEMO_IMAGES = images-demo/*

all: lab demo bin-packing

lab: $(KEY).ipynb $(DATA) $(LAB_IMAGES)
	python ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(LAB_IMAGES)

demo: $(DEMO).ipynb $(DEMO_IMAGES)
	zip -r $(DEMO).zip $(DEMO).ipynb $(DEMO_IMAGES)

bin-packing: bin_packing_demo.ipynb data-bin_packing
	zip -r bin_packing_demo.zip bin_packing_demo.ipynb data-bin_packing

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

