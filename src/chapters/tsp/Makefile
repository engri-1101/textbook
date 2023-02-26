MAIN = traveling_salesman_problem
LAB = $(MAIN)_lab
KEY = $(LAB)_key
DATA = data/*
IMAGES = images/*
SRC = tsp.py
PAGES = intro,model,algorithms,tsp_modeling,vlsi

all: web key lab

web:
	python ../make_web.py --list $(PAGES)

key:
	python ../make_key.py --list $(PAGES) --name $(KEY).ipynb

lab: $(KEY).ipynb $(DATA) $(IMAGES) $(SRC)
	python ../make_lab.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRC)

# lab for Windows
lab_win: $(KEY).ipynb $(DATA) $(IMAGES) $(SRC)
	python ../make_lab.py --key $(KEY).ipynb
	tar.exe -a -c -f $(LAB).zip $(LAB).ipynb $(DATA) $(IMAGES) $(SRC)

clean:
	rm -rf *.zip $(LAB).ipynb $(KEY).ipynb *_web.ipynb

# clean for Windows
clean_win:
	del *.zip, $(LAB).ipynb, $(KEY).ipynb, *_web.ipynb

.PHONY: clean all
