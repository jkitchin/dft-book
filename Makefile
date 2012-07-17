EMACS=emacs
BATCH_EMACS=$(EMACS) --batch -l ~/Dropbox/.emacs.d/init.el dft.org
REQUIREMENTS=python

org:
	emacs dft.org &

all: pdf

tex: dft.org dft.bib
	$(BATCH_EMACS) -f org-export-as-latex

pdf: tex
	pdflatex -shell-escape dft
	bibtex dft
	makeindex dft
	pdflatex -shell-escape dft
	pdflatex -shell-escape dft

clean:
	rm -f *.aux *.log *.dvi *.blg *.bbl *.toc *.tex *~ *.out *.idx *.ilg *.ind
