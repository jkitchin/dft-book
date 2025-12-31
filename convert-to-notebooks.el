;; Batch convert org files to Jupyter notebooks using ox-ipynb
;; Usage: emacs --batch -l convert-to-notebooks.el

;; Add elisp directory to load path
(add-to-list 'load-path (expand-file-name "elisp" (file-name-directory load-file-name)))

;; Load required packages
(require 'org)
(require 'ox)
(require 'ox-ipynb)

;; Add python to kernelspecs
(add-to-list 'ox-ipynb-kernelspecs
             '(python . (kernelspec . ((display_name . "Python 3")
                                       (language . "python")
                                       (name . "python3")))))

;; Add python to language-infos (required alongside kernelspec)
(add-to-list 'ox-ipynb-language-infos
             '(python . (language_info . ((codemirror_mode . ((name . ipython)
                                                              (version . 3)))
                                          (file_extension . ".py")
                                          (mimetype . "text/x-python")
                                          (name . "python")
                                          (nbconvert_exporter . "python")
                                          (pygments_lexer . "ipython3")
                                          (version . "3.9.0")))))

;; Add sh/bash
(add-to-list 'ox-ipynb-kernelspecs
             '(sh . (kernelspec . ((display_name . "Bash")
                                   (language . "bash")
                                   (name . "bash")))))
(add-to-list 'ox-ipynb-language-infos
             '(sh . (language_info . ((name . "bash")
                                      (file_extension . ".sh")))))

;; Don't execute code blocks during export
(setq org-export-use-babel nil)

;; Set up org-babel for python
(org-babel-do-load-languages
 'org-babel-load-languages
 '((python . t)
   (emacs-lisp . t)
   (shell . t)))

;; Don't ask for confirmation when executing code blocks
(setq org-confirm-babel-evaluate nil)

;; Output directory for notebooks
(defvar notebook-output-dir (expand-file-name "notebooks" (file-name-directory load-file-name)))

;; Create output directory if it doesn't exist
(unless (file-exists-p notebook-output-dir)
  (make-directory notebook-output-dir t))

;; List of chapter files to convert
(defvar chapter-files
  '("chapters/01-introduction-to-book.org"
    "chapters/02-introduction-to-dft.org"
    "chapters/03-molecules.org"
    "chapters/04-bulk-systems.org"
    "chapters/05-surfaces.org"
    "chapters/06-atomistic-thermodynamics.org"
    "chapters/07-advanced-electronic-structure.org"
    "chapters/08-databases.org"
    "chapters/09-acknowledgments.org"
    "chapters/10-appendices.org"
    "chapters/11-python.org"))

;; Convert each file
(dolist (file chapter-files)
  (let* ((full-path (expand-file-name file (file-name-directory load-file-name)))
         (base-name (file-name-base file))
         (output-file (expand-file-name (concat base-name ".ipynb") notebook-output-dir)))
    (message "Converting %s -> %s" file output-file)
    (condition-case err
        (with-current-buffer (find-file-noselect full-path)
          (let ((default-directory (file-name-directory full-path)))
            (ox-ipynb-export-to-ipynb-file))
          ;; Move the generated file to notebooks directory
          (let ((generated-file (concat (file-name-sans-extension full-path) ".ipynb")))
            (when (file-exists-p generated-file)
              (rename-file generated-file output-file t)
              (message "  -> Success: %s" output-file)))
          (kill-buffer))
      (error (message "  -> Error converting %s: %s" file (error-message-string err))))))

(message "\nConversion complete! Notebooks are in: %s" notebook-output-dir)
