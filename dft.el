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
(require 'org)

;; setup the latex export packages
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

;; code for syntax highlighting
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

; here is a way to get pydoc in a link: [[pydoc:numpy]]
(setq org-link-abbrev-alist
      '(("pydoc" . "shell:pydoc %s")))


;; [[lof:lof][List of Figures]]
;; the keyword is totally arbitrary
(org-add-link-type "lof"
  ; function executed when clicked on
  (lambda (keyword)
    (message "One day this will generate a list of clickable figure captions"))
  ; export functions
  (lambda (keyword link format)
   (cond
    ((eq format 'html)
     ("")) ; nothing for html. one day maybe get a list of captions
    ((eq format 'latex)
     ("\\listoffigures")))))

;; [[lot:lot][List of Tables]]
;; the keyword is totally arbitrary
(org-add-link-type "lot"
  ; function executed when clicked on
  (lambda (keyword)
    (message "One day this will generate a list of clickable table captions"))
  ; export functions
  (lambda (keyword link format)
   (cond
    ((eq format 'html)
     ("")) ; nothing for html. one day maybe get a list of captions
    ((eq format 'latex)
     ("\\listoftables")))))

;; [[printindex:ind][Print index]]
;; the keyword is totally arbitrary
(org-add-link-type "printindex"
  ; function executed when clicked on
  (lambda (keyword)
    (message "One day this will generate a clickable index"))
  ; export functions
  (lambda (keyword link format)
   (cond
    ((eq format 'html)
     ("")) ; nothing for html. one day maybe make an html indiex
    ((eq format 'latex)
     ("\\printindex")))))

;; add index link which creates an citation entry in latex and does nothing for html.
(org-add-link-type  "index"
 (lambda (arg)
   ()) ; do nothing when clicked on.
 (lambda (keyword desc format)
   (cond
    ((eq format 'html)
     (format ""))
    ((eq format 'latex)
     (format "\\index{%s}" keyword)))))

;; [[incar:keyword]]
;; this makes nice links in org-mode to the online documentation and
;; renders useful links in output
(org-add-link-type  "incar"
   (lambda (keyword)
     browse-url
    (format "http://cms.mpi.univie.ac.at/wiki/index.php/%s" keyword))
  ; this function is for formatting
  (lambda (keyword link format)
   (cond
    ((eq format 'html)
     (format "<a href=http://cms.mpi.univie.ac.at/wiki/index.php/%s>%s</a>" keyword keyword))
    ((eq format 'latex)
     (format "\\href{http://cms.mpi.univie.ac.at/wiki/index.php/%s}{%s}"  keyword keyword)

))))

;; these allow me to write mod:numpy or func:numpy.dot to get
;; clickable links to documentation. I made separate ones to
;; distinguish between a module and function.
(org-add-link-type
 "mod"
 (lambda (arg)
   (shell-command (format "pydoc %s" arg) nil))
 (lambda (path desc format)
   (cond
    ((eq format 'html)
     ; no formatting for html
     (format "<TT>%s</TT>" path))
    ((eq format 'latex)
     (format "\\texttt{%s}" path)))))

;; get python function documentation
(org-add-link-type
 "func"
 (lambda (arg)
   (shell-command (format "pydoc %s" arg) nil))
;; format as typewriter font in html and latex
 (lambda (path desc format)
   (cond
    ((eq format 'html)
     (format "<TT>%s</TT>" path))
    ((eq format 'latex)
     (format "\\texttt{%s}" path)))))


;; Add a figure link so I can export images in a format appropriate for
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

(defun toggle-latex-images ()
  "toggle whether latex images or equations are shown. currently does not toggle, only shows"
  (interactive)
  (org-preview-latex-fragment 16))

(defun dft-book-study (scope)
  "Run org-drill on the scope"
  (interactive)
  (setq org-drill-scope scope)
  (org-drill))

(defun dft-book-help ()
  (find-file "help.org"))

;; Create the book menu
(easy-menu-define dft-book-menu global-map "DFT-BOOK-MENU"
		      '("dft-book"
                ["Toggle equation images" (org-preview-latex-fragment 16) t]
                ("Study"
                 ["Molecules" (dft-book-study '("study-guides/molecules-drill.org")) t]
                 ["Bulk"      (dft-book-study '("study-guides/bulk-drill.org")) t]
                 ["Reset study data" org-drill-strip-all-data t])
                ;; these will be integrated with git
                ("Version Control"
                 ["Commit your changes" (vc-next-action nil) t]
                 ["Undo your changes" () t]
                 ["Get latest version" (vc-pull) t])
                ["Help" (find-file "help.org") t]
                ["VASP website" (browse-url "http://www.vasp.at/") t]
                ["VASP forum" (browse-url "http://cms.mpi.univie.ac.at/vasp-forum/forum.php") t]
                ["Email a bug/typo/question" email-bug-typo-question t]
                ["Get TODO agenda" (org-agenda "4" "t" "<") t]
                )
              )

(global-set-key "\C-cm" '(lambda ()
   (interactive)
   (popup-menu 'dft-book)))

(defun email-bug-typo-question ()
  "Construct and send an email about a bug/typo/question in the book.

The email body will contain
1. an optional message from the user.
2. the current line text
3. the git revision number
4. Some lisp code to make it trivial to open the file up to exactly the point."
  (interactive)

  ; create the lisp code that will open the file at the point
  (setq lisp-code (format "(progn (find-file \"%s\") (goto-char %d))" "dft.org" (point)))

  ; now create the body of the email
    (setq email-body
     (format "Type your note here:

======================================================
Line where point was:
%s: %s
======================================================
git rev-pars HEAD: %s
======================================================
Lisp code that opens dft-book at point
%s
======================================================"
          (what-line)
          (thing-at-point 'line)
          (shell-command-to-string "git rev-parse HEAD")
          lisp-code))
    (compose-mail-other-frame)
    (message-goto-to)
    (insert "jkitchin@andrew.cmu.edu")
    (message-goto-subject)
    (insert "Bug/typo/question report for dft-book")
    (message-goto-body)
    (insert email-body)
    (message-goto-body) ; go back to beginning of email body
    (next-line)         ; and down one line
    (message "Type C-c C-c to send message"))


(defun dft-book () (find-file "dft.org"))

(dft-book)



; some notes on what it might take to make EnableWrite/shell-escape globally true.
;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\latex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdftex.ini
