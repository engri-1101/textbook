MAIN = maximum_flow
LAB = $(MAIN)_lab
KEY = $(LAB)_key
IMAGES = images/*
IMAGES_LAB = images_lab/*
IMAGES_KEY = images_key/*
SRC = max_flow.py
PAGES = intro,model,verify,towards_algorithm,algorithms,algorithms_python

all: web key lab

web:
	python ../make_web.py --list $(PAGES)

key:
	python ../make_key.py --list $(PAGES) --name $(KEY).ipynb

lab: $(KEY).ipynb $(IMAGES) $(IMAGES_LAB) $(SRC)
	python ../make_lab.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES) $(IMAGES_LAB) $(SRC)

# lab for Windows
lab_win: $(KEY).ipynb $(IMAGES) $(IMAGES_LAB) $(SRC)
	python ../make_lab.py --key $(KEY).ipynb
	tar.exe -a -c -f $(LAB).zip $(LAB).ipynb $(IMAGES) $(IMAGES_LAB) $(SRC)

clean:
	rm -rf *.zip $(LAB).ipynb $(KEY).ipynb *_web.ipynb

# clean for Windows
clean_win:
	del *.zip, $(LAB).ipynb, $(KEY).ipynb, *_web.ipynb

.PHONY: clean all
