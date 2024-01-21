MAIN = python_intro
LAB = $(MAIN)_lab

all: lab

lab: $(LAB).ipynb campus_map.png
	zip -r $(LAB).zip $(LAB).ipynb campus_map.png

jhub-labs: lab ../../../jhub-labs
	rm -rf ../../../jhub-labs/$(MAIN)
	mkdir ../../../jhub-labs/$(MAIN)
	unzip $(LAB).zip -d ../../../jhub-labs/$(MAIN)

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all