MAIN = shortest_path_problem
LAB = $(MAIN)_lab
KEY = $(LAB)_key
IMAGES = images/*
PAGES = intro,model,algorithm,verify,modeling_with

all: web key lab

web:
	python ../make_web.py --list $(PAGES)

key:
	python ../make_key.py --list $(PAGES) --name $(KEY).ipynb

lab: $(KEY).ipynb $(IMAGES)
	python ../make_lab.py --key $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb $(IMAGES)

# lab for Windows
lab_win: $(KEY).ipynb $(IMAGES)
	python ../make_lab.py --key $(KEY).ipynb
	tar.exe -a -c -f $(LAB).zip $(LAB).ipynb $(IMAGES)

clean:
	rm -rf *.zip $(LAB).ipynb $(KEY).ipynb *_web.ipynb

# clean for Windows
clean_win:
	del *.zip, $(LAB).ipynb, $(KEY).ipynb, *_web.ipynb

.PHONY: clean all
