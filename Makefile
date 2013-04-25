EMACS=emacs
BATCH_EMACS=$(EMACS) --batch -l ~/Dropbox/.emacs.d/init.el -l dft.el dft.org
REQUIREMENTS=python
PDFLATEX=pdflatex -shell-escape
LATEX=latex -shell-escape

IMAGES = $(wildcard images/*.svg)

PNGIMAGES = $(IMAGES:.svg=.png)
PDFIMAGES = $(IMAGES:.svg=.pdf)

%.png: %.svg
	inkscape -f $< -e $@

%.pdf: %.svg
	inkscape -f $< -A $@

org:
	emacs dft.org &

tex: dft.org dft.bib
	$(BATCH_EMACS) -f org-export-as-latex

pdf: tex $(PDFIMAGES)
	# note I do not use the org-export-as-pdf function here. I do not
	# remember why. Maybe to avoid the problem with enabling
	# -shell-escape globally?
	pdflatex -shell-escape dft
	bibtex dft
	pdflatex -shell-escape dft
	makeindex dft
	pdflatex -shell-escape dft

xhtml: $(PNGIMAGES)
	htlatex dft.tex "xhtml,mathml" " -cunihtf" "-cvalidate"

html: $(PNGIMAGES)
	cp dftbook.sty /tmp
	$(BATCH_EMACS) -f org-export-as-html

mobi: html
	/home/jkitchin/kindlegen/kindlegen dft.html

all: pdf html

clean:
	rm -f *.aux *.log *.dvi *.blg *.bbl *.toc *~ *.out *.idx *.ilg *.ind *.lof *.lot *.css *.idv *.lg *.tmp *.xref *.4ct *.4tc
