EMACS=emacs
BATCH_EMACS=$(EMACS) --batch -l ~/Dropbox/.emacs.d/init.el dft.org
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
	pdflatex -shell-escape dft
	bibtex dft
	pdflatex -shell-escape dft
	makeindex dft
	pdflatex -shell-escape dft

xhtml: $(PNGIMAGES)
	htlatex dft.tex "xhtml,mathml" " -cunihtf" "-cvalidate"

html: $(PNGIMAGES)
	$(BATCH_EMACS) -f org-export-as-html

mobi: html
	/home/jkitchin/kindlegen/kindlegen dft.html

all: pdf html mobi

clean:
	rm -f *.aux *.log *.dvi *.blg *.bbl *.toc *~ *.out *.idx *.ilg *.ind *.lof *.lot *.css *.idv *.lg *.tmp *.xref *.4ct *.4tc
