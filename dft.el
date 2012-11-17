;; lisp code for dft-book
;;
;; sets up org-mode and the custom links
;;
;; sets up the dft-book menu
;; adapted from http://ergoemacs.org/emacs/elisp_menu.html

(require 'org-install)
(require 'org-list)
(require 'org-special-blocks)
(require 'org-drill)

(setq org-export-latex-default-packages-alist
      (quote
       (("AUTO" "inputenc" t)
        ("" "fixltx2e" nil)
        ("" "url")
        ("" "graphicx" t)
        ("" "minted" t)
        ("" "color" t)
        ("" "longtable" nil)
        ("" "float" nil)
        ("" "wrapfig" nil)
        ("" "soul" t)
        ("" "textcomp" t)
        ("" "amsmath" t)
        ("" "marvosym" t)
        ("" "wasysym" t)
        ("" "latexsym" t)
        ("" "amssymb" t)
        ("linktocpage,
          pdfstartview=FitH,
          colorlinks,
          linkcolor=blue,
          anchorcolor=blue,
          citecolor=blue,
          filecolor=blue,
          menucolor=blue,
           urlcolor=blue" "hyperref" t)
        ("" "attachfile" t)
        "\\tolerance=1000")))

(setq org-export-latex-listings 'minted)
(setq org-export-latex-minted-options
           '(("frame" "lines")
             ("fontsize" "\\scriptsize")
             ("linenos" "")))

(setq org-latex-to-pdf-process
      '("pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "bibtex %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"
        "pdflatex -shell-escape -interaction nonstopmode -output-directory %o %f"))

;;; new link formats for org-mode that I wrote
(require 'org)

; here is a way to get pydoc in a link: [[pydoc:numpy]]
(setq org-link-abbrev-alist
      '(("pydoc" . "shell:pydoc %s")))

;; -*- emacs-lisp -*-   [[incar:keyword]]
; this makes nice links in org-mode to the online documentation and
; renders useful links in output
(org-add-link-type
 "incar"
  (lambda (keyword)
    (shell-command (format "firefox http://cms.mpi.univie.ac.at/wiki/index.php/%s" keyword) nil))
  ; this function is for formatting
  (lambda (keyword link format)
   (cond
    ((eq format 'html)
     (format "<a href=http://cms.mpi.univie.ac.at/wiki/index.php/%s>%s</a>" keyword keyword))
    ((eq format 'latex)
     (format "\\href{http://cms.mpi.univie.ac.at/wiki/index.php/%s}{%s}"  keyword keyword)

))))

;; these allow me to write mod:numpy or func:numpy.dot to get
;; clickable links to documentation
(org-add-link-type
 "mod"
 (lambda (arg)
   (shell-command (format "pydoc %s" arg) nil))
 (lambda (path desc format)
   (cond
    ((eq format 'html)
     (format "%s" path))
    ((eq format 'latex)
     (format "\\texttt{%s}" path)))))

;; get python function documentation
(org-add-link-type
 "func"
 (lambda (arg)
   (shell-command (format "pydoc %s" arg) nil))
 (lambda (path desc format)
   (cond
    ((eq format 'html)
     (format "%s" path))
    ((eq format 'latex)
     (format "\\texttt{%s}" path)))))


;; add index link which creates an citation entry in latex and does nothing for html.
(org-add-link-type
 "index"
 (lambda (arg)
   ()) ; do nothing
 (lambda (keyword desc format)
   (cond
    ((eq format 'html)
     (format ""))
    ((eq format 'latex)
     (format "\\index{%s}" keyword)))))

;; Add a figure link so I can export images ina format appropriate for
;; the export. E.g. figure:test.svg will use test.pdf for a pdf file, and
;; test.png for html.  [[figure:path.svg][caption text]]

(org-add-link-type
 "figure"
 (lambda (arg)
   (find-file arg)) ; open file when clicked on
 (lambda (keyword desc format)
   (cond
    ((eq format 'html) ; table of image and caption
     (format "
<table class='image'>
<tr><td><img src='%s.png' alt='%s'/></td></tr>
<tr><td class='caption'>%s</td></tr>
</table>
" keyword desc desc))
    ((eq format 'latex) ; this is actually for pdflatex
     (if desc
         (format "
\\begin{figure}[H]
\\includegraphics[width=0.7\\textwidth]{%s}
\\caption{%s}
\\end{figure}
" (replace-in-string keyword ".svg" ".pdf") desc)
         (format "
\\begin{figure}[H]
\\includegraphics[width=0.7\\textwidth]{%s}
\\end{figure}
" (replace-in-string keyword ".svg" ".pdf"))
)))))



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Menu for dft-book



(define-key-after global-map [menu-bar dft-book]
  (cons "dft-book" (make-sparse-keymap "dft-book")) t)

(defun toggle-latex-images ()
  "toggle whether latex images or equations are shown. currently does not toggle, only shows"
  (interactive)
  (org-preview-latex-fragment 16))
  ;(save-excursion
  ;  (goto-char (point-max))
  ;  (org-preview-latex-fragment 16)))

;; (define-key global-map [(kbd "C-c, l, l")] 'toggle-latex-images)

(define-key global-map [menu-bar dft-book toggle-latex]
  '("Toggle latex equation images" . toggle-latex-images))

(defun dft-book-study () (interactive)
  (setq org-drill-scope '("study-guides/molecules-drill.org"))
  (org-drill))

(define-key global-map [menu-bar dft-book test]
  '("Study!" . dft-book-study))
