;; lisp code for dft-book
;;
;; sets up org-mode and the custom links
;;
;; sets up the dft-book menu
;; adapted from http://ergoemacs.org/emacs/elisp_menu.html

;; [[incar:keyword]]
;; this makes nice links in org-mode to the online documentation and
;; renders useful links in output
(require 'org)

(org-add-link-type "incar"
		   (lambda (keyword)
		     (browse-url
		      (format "http://cms.mpi.univie.ac.at/wiki/index.php/%s"
			      keyword)))
					; this function is for formatting
		   (lambda (keyword link format)
		     (cond
		      ((eq format 'html)
		       (format "<a href=http://cms.mpi.univie.ac.at/wiki/index.php/%s>%s</a>"
			       keyword keyword))
		      ((eq format 'latex)
		       (format "\\href{http://cms.mpi.univie.ac.at/wiki/index.php/%s}{%s}"
			       keyword keyword)))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; Menu for dft-book

(defvar dft-book-mode-map
  (let ((map (make-sparse-keymap)))

    map)
  "Keymap for dft-book-mode.")

(easy-menu-define dft-book-menu dft-book-mode-map "DFT-BOOK-MENU"
    '("dft-book"
      ["VASP website" (browse-url "http://www.vasp.at/") t]
      ["VASP forum" (browse-url "http://cms.mpi.univie.ac.at/vasp-forum/forum.php") t]
      ["Get TODO agenda" (org-agenda "4" "t" "<") t]
      ["Exit" (progn (global-unset-key [menu-bar dft-book])
		     (kill-buffer "dft.org"))
       t]))


(define-minor-mode dft-book-mode
  "Minor mode for dft-book"
  :lighter "dft"
  :keymap dft-book-mode-map)


(dft-book-mode)

; some notes on what it might take to make EnableWrite/shell-escape globally true.
;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\latex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdftex.ini
