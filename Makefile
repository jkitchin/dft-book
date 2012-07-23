EMACS=emacs
BATCH_EMACS=$(EMACS) --batch -l ~/Dropbox/.emacs.d/init.el dft.org
REQUIREMENTS=python

org:
	emacs dft.org &

all: pdf html mobi

tex: dft.org dft.bib
	$(BATCH_EMACS) -f org-export-as-latex

pdf: tex
	pdflatex -shell-escape dft
	bibtex dft
	makeindex dft
	pdflatex -shell-escape dft
	pdflatex -shell-escape dft

html:
	$(BATCH_EMACS) -f org-export-as-html

xhtml:
	mk4ht htlatex dft.tex '-shell-escape,xhtml,charset=utf-8,pmathml' ' -cunihtf -utf8 -cvalidate'

mobi: html
	/home/jkitchin/kindlegen/kindlegen dft.html

clean:
	rm -f *.aux *.log *.dvi *.blg *.bbl *.toc *~ *.out *.idx *.ilg *.ind
