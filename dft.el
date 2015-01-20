;; lisp code for dft-book
;;
;; sets up org-mode and the custom links
;;
;; sets up the dft-book menu
;; adapted from http://ergoemacs.org/emacs/elisp_menu.html

;; [[incar:keyword]]
;; this makes nice links in org-mode to the online documentation and
;; renders useful links in output
(org-add-link-type "incar"
		   (lambda (keyword)
		     (browse-url
		      (format "http://cms.mpi.univie.ac.at/wiki/index.php/%s" keyword)))
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

(defun toggle-latex-images ()
  "toggle whether latex images or equations are shown. currently does not toggle, only shows"
  (interactive)
  (org-preview-latex-fragment 16))

;(defun dft-book-study (scope)
;  "Run org-drill on the scope"
;  (interactive)
;  (setq org-drill-scope scope)
;  (org-drill))

(defun dft-book-help ()
  (find-file "help.org"))

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
     (format "Type your note here, and press C-c C-c when you are done:

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

(defvar dft-book-mode nil "Mode variable for dft-book-minor-mode")
(make-variable-buffer-local 'dft-book-mode)

(defun dft-book-mode (&optional arg)
  "dft-book minor mode"
  (interactive "P")
  (setq dft-book-mode
        (if (null arg)
            (not dft-book-mode) ;set the value of dft-book-mode to the
                                ;opposite if its current value if no
                                ;arg is given
          (> (prefix-numeric-value arg) 0))) ;;if an arg was given, set it to t if arg > 0, otherwise set to nil
  (if dft-book-mode
      (easy-menu-define dft-book-menu global-map "DFT-BOOK-MENU"
        '("dft-book"
          ["Toggle equation images" (org-preview-latex-fragment 16) t]
          ;("Study"
          ; ["Molecules" (dft-book-study '("study-guides/molecules-drill.org")) t]
          ; ["Bulk"      (dft-book-study '("study-guides/bulk-drill.org")) t]
          ; ["Reset study data" org-drill-strip-all-data t])
          ;; these will be integrated with git
         ; ("Version Control"
          ; ["Commit your changes" (vc-next-action nil) t]
          ; ["Undo your changes" () nil]
          ; ["Get latest version" (vc-pull) t])
          ["Help" (find-file "help.org") t]
          ["VASP website" (browse-url "http://www.vasp.at/") t]
          ["VASP forum" (browse-url "http://cms.mpi.univie.ac.at/vasp-forum/forum.php") t]
          ["Email a bug/typo/question" email-bug-typo-question t]
          ["Get TODO agenda" (org-agenda "4" "t" "<") t]
          ["Exit" (progn (global-unset-key [menu-bar dft-book])
                         (kill-buffer "dft.org")) t]
          ))           ; code to turn on the mode
    (progn (global-unset-key [menu-bar dft-book])
                         (kill-buffer "dft.org"))))           ; code to turn off the mode

(dft-book-mode)

; some notes on what it might take to make EnableWrite/shell-escape globally true.
;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdflatex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\latex.ini

;C:\Users\jkitchin>initexmf --edit-config-file=miktex\config\pdftex.ini
