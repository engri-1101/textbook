MAIN = lp_formulation
LAB = $(MAIN)_lab
KEY = $(LAB)_key

all: lab

lab: $(KEY).ipynb
	python ../make_student_version.py $(KEY).ipynb
	zip -r $(LAB).zip $(LAB).ipynb

clean:
	rm -rf {*.zip,$(LAB).ipynb}

.PHONY: clean all

