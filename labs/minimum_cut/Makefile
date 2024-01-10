MAIN = minimum_cut
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data-lab/*
IMAGES = images-lab/*
SRCS = max_flow.py social_network.py

all: lab

lab: $(KEY).ipynb $(DATA) $(IMAGES) $(SRCS)
	python3 ../distribute.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRCS)

jhub-labs: lab ../../../jhub-labs
	rm -rf ../../../jhub-labs/$(MAIN)
	mkdir ../../../jhub-labs/$(MAIN)
	unzip $(LAB).zip -d ../../../jhub-labs/$(MAIN)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all
