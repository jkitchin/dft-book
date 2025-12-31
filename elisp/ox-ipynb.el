;;; ox-ipynb.el --- Convert an org-file to an ipynb.  -*- lexical-binding: t; -*-

;; Copyright(C) 2017-2025 John Kitchin

;; Author: John Kitchin <jkitchin@andrew.cmu.edu>
;; URL: https://github.com/jkitchin/ox-ipynb/ox-ipynb.el
;; Version: 0.1
;; Keywords: org-mode
;; Package-Requires: ((emacs "30") (org "9.7"))

;; This file is not currently part of GNU Emacs.

;; This program is free software; you can redistribute it and/or
;; modify it under the terms of the GNU General Public License as
;; published by the Free Software Foundation; either version 2, or (at
;; your option) any later version.

;; This program is distributed in the hope that it will be useful, but
;; WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
;; General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program ; see the file COPYING.  If not, write to
;; the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
;; Boston, MA 02111-1307, USA.

;;; Commentary:
;;
;; The export language is determined by the first cell. If the first cell is not
;; the notebook language, e.g. because you use a shell block for some reason,
;; you can specify the language with a keyword like this:
;;
;; #+OX-IPYNB-LANGUAGE: jupyter-python
;;
;; It is possible to set metadata at the notebook level using
;; #+ox-ipynb-keyword-metadata: key1 key2
;; This will use store key:value pairs in
;; the notebook metadata section, in an org section.
;;
;; You can also add custom notebook-level metadata (e.g. for RISE slideshows) using:
;; #+OX-IPYNB-NOTEBOOK-METADATA: (rise . ((autolaunch . t) (scroll . t)))
;; This adds arbitrary metadata at the top level of the notebook's metadata section.
;; Multiple lines are supported and will be merged.
;;
;; It is also possible to set cell metadata on src-block cells. You use an
;; attribute like #+ATTR_IPYNB: :key1 val1 :key2 val2 to set the cell metadata.
;; You can also do this on paragraphs. Only one attr_ipynb line is supported, so
;; all metadata needs to go in that line.
;;
;; You can force a new cell to be created with the org-directive #+ipynb-newcell
;;
;; This exporter supports ipython and R Juypter notebooks. Other languages could
;; be supported, but you need to add a kernelspec to `ox-ipynb-kernelspecs' and
;; the language info to `ox-ipynb-language-infos'.
;;
;; The org-file is parsed into a list of cells. Each cell is either a markdown
;; cell or a code cell (with results). Headlines are parsed to their own cells
;; to enable collapsible headings to work nicely.
;;
;; You can export an org-file to a buffer, file or file and open.
;;
;; `ox-ipynb' supports the following features for making notebooks that don't
;; include all the org-source. You can label regions of a code cell with ###
;; BEGIN SOLUTION...### END SOLUTION, and if you export with
;; `ox-ipynb-export-to-participant-notebook' those regions will be stripped out
;; in the notebook. You can also label a region as hidden with ### BEGIN
;; HIDDEN...### END HIDDEN.
;;
;; Finally any cell with
;; #+attr_ipynb: :remove t
;; on it will be removed in the export with `ox-ipynb-export-to-participant-notebook'.
;;
;; You can export a notebook with all the results stripped out with
;; `ox-ipynb-export-to-ipynb-no-results-file-and-open'.



;;; Code:
(require 'cl-lib)
(require 'ox-md)
(require 'ox-org)
(require 'json)

(unless (string-match "^9\\.[2-9][\\.0-9]*" (org-version))
  (warn "org 9.2+ is required for `ox-ipynb'. Earlier versions do not currently work."))

;; Helper functions to replace s.el functionality
(defun ox-ipynb--index-of (needle haystack &optional start)
  "Find the index of NEEDLE in HAYSTACK starting at START (default 0).
Returns nil if not found."
  (let ((pos (string-match (regexp-quote needle) haystack start)))
    pos))

(defun ox-ipynb--count-matches (regexp s)
  "Count occurrences of REGEXP in string S."
  (let ((count 0)
        (pos 0))
    (while (string-match regexp s pos)
      (setq count (1+ count)
            pos (match-end 0)))
    count))

(defun ox-ipynb--slice-at (regexp s)
  "Split string S at each match of REGEXP, keeping delimiters with following parts."
  (let ((parts '())
        (start 0)
        (pos 0))
    (while (string-match regexp s pos)
      (when (> (match-beginning 0) start)
        (push (substring s start (match-beginning 0)) parts))
      (setq start (match-beginning 0)
            pos (match-end 0)))
    (when (< start (length s))
      (push (substring s start) parts))
    (nreverse parts)))

(defun ox-ipynb--format (template replacer-fn)
  "Replace ${VAR} placeholders in TEMPLATE using REPLACER-FN.
REPLACER-FN is called with the variable name (without ${}) and should return the replacement string."
  (replace-regexp-in-string
   "\\${\\([^}]+\\)}"
   (lambda (match)
     (funcall replacer-fn (match-string 1 match)))
   template))

(defcustom ox-ipynb-preprocess-hook '()
  "Hook variable to apply to a copy of the buffer before exporting."
  :type 'hook
  :group 'ox-ipynb)


(defvar ox-ipynb-kernelspecs '((ipython . (kernelspec . ((display_name . "Python 3")
                                                         (language . "python")
                                                         (name . "python3"))))
                               (R . (kernelspec . ((display_name . "R")
                                                   (language . "R")
                                                   (name . "ir"))))
			       (jupyter-R . (kernelspec . ((display_name . "R")
							   (language . "R")
							   (name . "ir"))))
                               (julia . (kernelspec . ((display_name . "Julia 0.6.0")
                                                       (language . "julia")
                                                       (name . "julia-0.6"))))
			       (jupyter-julia . (kernelspec . ((display_name . "Julia 0.6.0")
							       (language . "julia")
							       (name . "julia-0.6"))))
                               (jupyter-python . (kernelspec . ((display_name . "Python 3")
                                                                (language . "python")
                                                                (name . "python3"))))
			       (clojure . (kernelspec . ((display_name . "Clojure")
							 (language . "clojure")
							 (name . "clojupyter"))))
			       (jupyter-clojure . (kernelspec . ((display_name . "Clojure")
								 (language . "clojure")
								 (name . "clojupyter")))))
  "Kernelspec metadata for different kernels.")


(defvar ox-ipynb-language-infos
  '((ipython . (language_info . ((codemirror_mode . ((name . ipython)
                                                     (version . 3)))
                                 (file_extension . ".py")
                                 (mimetype . "text/x-python")
                                 (name . "python")
                                 (nbconvert_exporter . "python")
                                 (pygments_lexer . "ipython3")
                                 (version . "3.5.2"))))

    (jupyter-python . (language_info . ((codemirror_mode . ((name . ipython)
                                                            (version . 3)))
                                        (file_extension . ".py")
                                        (mimetype . "text/x-python")
                                        (name . "python")
                                        (nbconvert_exporter . "python")
                                        (pygments_lexer . "ipython3")
                                        (version . "3.5.2"))))

    (jupyter-julia . (language_info . ((codemirror_mode . "julia")
				       (file_extension . ".jl")
				       (mimetype . "text/x-julia")
				       (name . "julia")
				       (pygments_lexer . "julia")
				       (version . "0.6.0"))))
    (julia . (language_info . ((codemirror_mode . "julia")
                               (file_extension . ".jl")
                               (mimetype . "text/x-julia")
                               (name . "julia")
                               (pygments_lexer . "julia")
                               (version . "0.6.0"))))

    (R . (language_info . ((codemirror_mode . "r")
                           (file_extension . ".r")
                           (mimetype . "text/x-r-source")
                           (name . "R")
                           (pygments_lexer . "r")
                           (version . "3.3.2"))))
    (jupyter-R . (language_info . ((codemirror_mode . "r")
				   (file_extension . ".r")
				   (mimetype . "text/x-r-source")
				   (name . "R")
				   (pygments_lexer . "r")
				   (version . "3.3.2"))))

    (clojure . (language_info . ((codemirror_mode . "clojure")
				 (file_extension . ".clj")
				 (mimetype . "text/x-clojure")
				 (name . "clojure")
				 (pygments_lexer . "clojure")
				 (version . "1.11"))))
    (jupyter-clojure . (language_info . ((codemirror_mode . "clojure")
					 (file_extension . ".clj")
					 (mimetype . "text/x-clojure")
					 (name . "clojure")
					 (pygments_lexer . "clojure")
					 (version . "1.11")))))
  "These get injected into notebook metadata.
They are reverse-engineered from existing notebooks.")


(defun ox-ipynb-insert-slide (type)
  "Insert the attribute line for a slide TYPE."
  (interactive (list (completing-read "Type: " '(slide subslide fragment notes skip))))
  (goto-char (line-beginning-position))
  (insert (format "#+attr_ipynb: (slideshow . ((slide_type . %s)))" type))
  (when (not (looking-at "$")) (insert "\n")))


(defun ox-ipynb-export-code-cell (src-result)
  "Return a code cell for the org-element in the car of SRC-RESULT.
The cdr of SRC-RESULT is the end position of the results."
  (let* ((src-block (car src-result))
         (results-end (cdr src-result))
         (results (org-no-properties (car results-end)))
         (output-cells '())
         img-path img-data
         (start 0)
         end
	 (src-metadata (or (when-let* ((smd (plist-get  (cadr src-block) :attr_ipynb)))
			     (read (format "(%s)" (string-join smd " "))))
			   (make-hash-table)))
         block-start block-end
         html
         latex
	 md)

    ;; Handle inline images first This is a clunky solution, using pattern
    ;; matching. Another option might be parsing the string and map over the
    ;; file links? It looks like I used to rely on these being file links, but
    ;; new versions of jupyter-emacs don't use file (or I patched that myself).
    (while (string-match org-any-link-re (or results ""))
      ;; while (string-match "\\[\\[\\(?:file:\\)?\\(.*?\\)\\]\\]" (or results "") start)
      (setq start (match-end 0))
      (setq img-path (match-string 2 results)
	    ;; org-any-link-re returns e.g. "file:./foo.png"; normalize so
	    ;; file predicates operate on actual paths instead of URIs.
	    img-path (if (and img-path (string-prefix-p "file:" img-path))
			 (substring img-path 5)
		   img-path)
	    ;; We delete the thing we found if it is an image
	    results (when (image-supported-file-p img-path)
		      (replace-match "" nil nil results))
            img-data (base64-encode-string
                      (encode-coding-string
		       (if (file-exists-p img-path)
			   (with-temp-buffer
                             (insert-file-contents  img-path)
                             (buffer-string))
			 "")
                       'binary)
                      t))

      (setq output-cells
	    (append output-cells
		    `(((data . ((image/png . ,img-data)
				("text/plain" . "<matplotlib.figure.Figure>")))
		       (metadata . ,(make-hash-table))
		       (output_type . "display_data"))))))

    ;; Check for HTML cells. I think there can only be one I don't know what the
    ;; problem is, but I can't get the match-end functions to work correctly
    ;; here. Its like the match-data is not getting updated.
    (when (string-match "#\\+BEGIN_EXPORT HTML" (or results ""))
      (setq block-start (ox-ipynb--index-of "#+BEGIN_EXPORT HTML" results)
            start (+ block-start (length "#+BEGIN_EXPORT HTML\n")))

      ;; Now, get the end of the block.
      (setq end (ox-ipynb--index-of "#+END_EXPORT" results)
            block-end (+ end (length "#+END_EXPORT")))

      (setq html (substring results start end))

      ;; remove the old output.
      (setq results (concat (substring results 0 block-start)
                            (substring results block-end)))
      (message "html: %s\nresults: %s" html results)
      (setq output-cells (append
			  output-cells `((data . ((text/html . ,html)
						  ("text/plain" . "HTML object")))
					 (metadata . ,(make-hash-table))
					 (output_type . "display_data")))))

    ;; Handle latex cells
    (when (string-match "#\\+BEGIN_EXPORT latex" (or results ""))
      (setq block-start (ox-ipynb--index-of "#+BEGIN_EXPORT latex" results)
            start (+ block-start (length "#+BEGIN_EXPORT latex\n")))

      ;; Now, get the end of the block.
      (setq end (ox-ipynb--index-of "#+END_EXPORT" results)
            block-end (+ end (length "#+END_EXPORT")))

      (setq latex (substring results start end))

      ;; remove the old output.
      (setq results (concat (substring results 0 block-start)
                            (substring results block-end)))

      (setq output-cells (append
			  output-cells
			  `((data . ((text/latex . ,latex)
				     ("text/plain" . "Latex object")))
			    (metadata . ,(make-hash-table))
			    (output_type . "display_data")))))

    ;; output cells
    (unless (or (string= "" results) (null results))
      (setq output-cells (append `(((name . "stdout")
				    (output_type . "stream")
				    (text . ,results)))
                                 output-cells)))


    `((cell_type . "code")
      (execution_count . 1)
      (id . ,(org-id-uuid))
      ;; the hashtable trick converts to {} in json. jupyter can't take a null here.
      (metadata . ,src-metadata)
      (outputs . ,(if (null output-cells)
                      ;; (vector) json-encodes to  [], not null which
                      ;; jupyter does not like.
                      (vector)
                    (vconcat output-cells)))
      (source . ,(vconcat
                  (list (string-trim (car (org-export-unravel-code src-block)))))))))


(defun ox-ipynb-filter-latex-fragment (text _ _)
  "Export org latex fragments in TEXT for ipynb markdown.
Latex fragments come from org as \(fragment\) for inline math or
\[fragment\] for displayed math. Convert to $fragment$
or $$fragment$$ for ipynb."
  ;; \\[frag\\] or \\(frag\\) are also accepted by ipynb markdown (need double backslash)
  (setq text (replace-regexp-in-string
              "\\\\\\[" "$$"
              (replace-regexp-in-string "\\\\\\]" "$$" text)))
  (replace-regexp-in-string "\\\\(\\|\\\\)" "$" text))


(defun ox-ipynb-filter-link (text _ _)
  "Make a link in TEXT into markdown.
For some reason I was getting angle brackets in them I wanted to remove.
This only fixes file links with no description I think.

[2019-08-11 Sun] added a small additional condition to not change
text starting with <sup. These are citations, and the previous
version was incorrectly modifying them."
  (if (and (string-prefix-p "<" text) (not (string-prefix-p "<sup" text)))
      (let ((path (substring text 1 -1)))
	(format "[%s](%s)" path path))
    text))


(defvar ox-ipynb-images '()
  "alist of paths and b64 encoded data for inline images.")

(defvar ox-ipynb--toc-content nil
  "Cached Table of Contents text for deduplication during export.")

(defvar ox-ipynb--attr-metadata nil
  "Cached attr_ipynb metadata for elements, preserved across intermediate export.
This is an alist of (ELEMENT-ID . ATTR-STRING) pairs.")

(defvar ox-ipynb--broken-links nil
  "Broken links handling mode for export (nil, 'mark, or 'ignore).
Captured from buffer settings or org-export-with-broken-links variable.")

;; This is an org-link to get inlined images from the file system. This makes
;; the notebook bigger, but more portable.
(org-link-set-parameters "image"
			 :export (lambda (path desc backend)
				   (cond
				    ((eq 'md backend)
				     (let* ((fname (file-name-nondirectory path))
					    (img-data (base64-encode-string
						       (encode-coding-string
							(with-temp-buffer
							  (insert-file-contents path)
							  (buffer-string))
							'binary)
						       t)))
				       ;; save data for constructing cells
				       ;; later. Obviously this is going to be a
				       ;; problem if you have images with
				       ;; different paths and the same name.
				       ;; That seems to also be a problem in the
				       ;; notebook though.
				       (push (cons fname img-data) ox-ipynb-images)
				       ;; (format "![%s](attachment:%s)" (or desc fname) fname)
				       (format "![%s](data:image/png;base64,%s)" (or desc fname) img-data)))))

			 ;; This puts overlays on top of the links. You can remove the overlays with C-c C-x C-v
			 :activate-func (lambda (start end path bracketp)
					  (when (and (file-exists-p path))
					    (let ((img (create-image (expand-file-name path)
								     'imagemagick nil :width 300))
						  (ov (make-overlay start end)))
					      (overlay-put ov 'display img)
					      (overlay-put ov 'org-image-overlay t)
					      (overlay-put ov 'modification-hooks (list 'org-display-inline-remove-overlay))
					      (push ov org-inline-image-overlays)))))


(defun ox-ipynb-export-markdown-cell (s)
  "Return the markdown cell for the string S."
  ;; Filter out redundant TOC cells. We drop the empty ones that
  ;; occasionally show up, and any copy that matches the generated TOC
  ;; block we inject later.
  (when (and (string-match "Table of Contents" s))
    (let ((trimmed-s (string-trim s)))
      (cond
       ((and ox-ipynb--toc-content
             (string= trimmed-s ox-ipynb--toc-content))
        (setq s ""))
       ((not (string-match "\\[.*\\](#.*)" s))
        (setq s "")))))

  (let* ((org-export-filter-latex-fragment-functions '(ox-ipynb-filter-latex-fragment))
         (org-export-filter-link-functions '(ox-ipynb-filter-link))
         ;; I overwrite the org function here because it does not give the right
         ;; levels otherwise. This one outputs exactly the level that is listed.
	 ;; Also, I modify the table exporters here to get a markdown table for
	 ncolumns
	 (org-html-text-markup-alist '((bold . "<b>%s</b>")
				       (code . "<code>%s</code>")
				       (italic . "<i>%s</i>")
				       (strike-through . "<del>%s</del>")
				       (underline . "<u>%s</u>")
				       (verbatim . "<code>%s</code>")))	; we overwrite the underline

	 ;; In here we temporarily define many export functions to fine-tune the markdown we get.
         (md (cl-letf (((symbol-function 'org-md-headline)
			(lambda (HEADLINE CONTENTS INFO)
			  "changed to get the right number of # for the heading level."
			  (concat
			   (cl-loop for i to (org-element-property :level HEADLINE)
				    concat "#")
			   " "
			   (org-export-string-as
			    (org-element-property :raw-value HEADLINE)
			    'md t `(:with-toc nil :with-tags nil :with-broken-links ,ox-ipynb--broken-links)))))
		       ((symbol-function 'org-export-get-relative-level)
                        (lambda (headline info)
			  "changed to get the level number of a headline. We need the absolute level."
			  (org-element-property :level headline)))
		       ;; Tables are kind of special. I want a markdown rendering, not html.
		       ((symbol-function 'org-html-table-cell)
			(lambda (table-cell contents info)
			  (concat  (org-trim (or contents "")) "|")))
		       ((symbol-function 'org-html-table-row) 'ox-ipynb--export-table-row)
		       ((symbol-function 'org-html-table)
			(lambda (_ contents info)
			  "We need to adapt the contents to remove leading and trailing rule lines.
Also removes extra horizontal rules - markdown tables only support one rule after the header."

			  ;; There are leading and trailing \n. strip off for the next step.
			  (setq contents (string-trim contents))

			  (let ((lines (split-string contents "\n"))
				(found-first-rule nil))
			    ;; Remove leading rule
			    (when (string-prefix-p "|-" (nth 0 lines))
			      (setq lines (cdr lines)))

			    ;; Remove trailing rule
			    (when (string-prefix-p "|-" (car (last lines)))
			      (setq lines (butlast lines)))

			    ;; Keep only the first rule line, remove all subsequent ones
			    (setq lines
				  (cl-loop for line in lines
					   unless (and (string-prefix-p "|---" line)
						       found-first-rule)
					   ;; Keep non-rule lines and the first rule
					   collect line
					   when (string-prefix-p "|---" line)
					   ;; Mark that we've seen a rule
					   do (setq found-first-rule t)))

			    ;; Now add back the blank lines
			    (setq contents (string-join (append '("") lines '(""))  "\n")))

			  ;; finally, it looks like there are double line returns we
			  ;; replace here.
         (replace-regexp-in-string "\n\n" "\n" (or contents "")))))
               (org-export-string-as
                s
                'md t `(:with-toc nil :with-tags nil :with-broken-links ,ox-ipynb--broken-links))))
 	 (pos -1)
	 (attachments '())
	 metadata)

    (when (and (string-match "Table of Contents" md))
      (let ((trimmed-md (string-trim md)))
        (cond
         ((and ox-ipynb--toc-content
               (string= trimmed-md ox-ipynb--toc-content))
          (setq md ""))
         ((not (string-match "\\[.*\\](#.*)" md))
          (setq md "")))))

    ;; we need to do some work to make images inlined for portability.
    (while (setq pos (string-match "(attachment:\\(.*\\))" md (+ 1 pos)))
      (push  (list (match-string 1 md)
 		   (list "image/png" (cdr (assoc (match-string 1 md) ox-ipynb-images))))
 	     attachments))

    ;; metadata handling, work on the original string since the attr line is
    ;; gone from the export
    ;; Match only at beginning of line (after newline or at string start) to avoid
    ;; matching text like "The =#+attr_ipynb:= directive"
    (when (string-match "\\(?:^\\|\n\\)#\\+attr_ipynb: *\\(.*\\)" s)
      (setq metadata (read (format "(%s)" (match-string 1 s)))))

    ;; check headline metadata
    (when (string-match ":metadata: *\\(.*\\)" s)
      (setq metadata (read (format "(%s)" (match-string 1 s)))))

    (if (not (string= "" (string-trim md)))
	(if attachments
	    `((attachments . ,attachments)
	      (cell_type . "markdown")
	      (id . ,(org-id-uuid))
	      (metadata . ,(or metadata (make-hash-table)))
	      (source . ,(vconcat
			  (list md))))
	  `((cell_type . "markdown")
	    (id . ,(org-id-uuid))
	    (metadata . ,(or metadata (make-hash-table)))
	    (source . ,(vconcat
			(list md)))))
      nil)))


(defun ox-ipynb--export-table-row  (table-row contents info)
  "Custom function to create a markdown string from a TABLE-ROW.
Note, this works a row at a time in a table, and does not store
information about how many horizontal rules there are. In simple
markdown, which we use here, you can only have one rule in the
header. If you wanted a fancier table, you should export it as
html I think. That is not currently supported.
"
  (let (ncolumns
	(contents (org-no-properties contents)))
    (cond
     ((eq (org-element-property :type table-row) 'standard)
      ;; for a regular row, it seems the opening | is not included in contents
      (concat "| " contents))

     ;; A rule in org looks like |---+---| we count the number of columns
     ;; assuming it looks like this
     ((eq (org-element-property :type table-row) 'rule)
      (setq contents (buffer-substring (org-element-property :begin table-row)
				       (org-element-property :end table-row)))
      (setq ncolumns (+ (ox-ipynb--count-matches "+" contents) 1))
      (if (= 1 ncolumns)
	  "|---|"
	(concat "|---" (cl-loop for i to (- ncolumns 2) concat "|---") "|"))))))


(defun ox-ipynb-export-keyword-cell ()
  "Make a markdown cell containing org-file keywords and values."
  (let* ((all-keywords (org-element-map (org-element-parse-buffer)
                           'keyword
                         (lambda (key)
                           (cons (org-element-property :key key)
                                 (org-element-property :value key)))))
         (ipynb-keywords (cdr (assoc "OX-IPYNB-KEYWORD-METADATA" all-keywords)))
         (include-keywords (mapcar 'upcase (split-string (or ipynb-keywords ""))))
         (keywords (cl-loop for key in include-keywords
                            if (assoc key all-keywords)
                            collect (cons key (or (cdr (assoc key all-keywords)) "")))))

    (setq keywords
          (cl-loop for (key . value) in keywords
                   collect
                   (format "- %s: %s\n"
                           key
                           (replace-regexp-in-string
                            "<\\|>" ""
                            (or value "")))))
    (when keywords
      `((cell_type . "markdown")
	(id . ,(org-id-uuid))
        (metadata . ,(make-hash-table))
        (source . ,(vconcat keywords))))))


(defun ox-ipynb--jupyter-anchor (title)
  "Generate anchor ID  for TITLE."
  (let ((s title))
    ;; First replace spaces with hyphens
    (setq s (replace-regexp-in-string " " "-" s))
    ;; Then remove all non-alphanumeric except hyphens and dots
    (replace-regexp-in-string "[^a-z0-9.-]" "" s)))


(defun ox-ipynb--build-toc (info &optional n)
  "Build a table of contents for ipynb export.
INFO is a plist used as a communication channel.
Optional argument N, when non-nil, is an integer specifying the depth of the table."
  (let ((headlines (org-export-collect-headlines info n)))
    (when headlines
      (concat
       "## Table of Contents\n\n"
       (mapconcat
        (lambda (headline)
          (let* ((level (org-export-get-relative-level headline info))
                 (indentation (make-string (* 4 (1- level)) ?\s))
                 (title (org-export-data-with-backend
                         (org-export-get-alt-title headline info)
                         (org-export-toc-entry-backend 'md)
                         info))
                 ;; Use CUSTOM_ID if set, otherwise generate Jupyter-style anchor
                 (anchor (or (org-element-property :CUSTOM_ID headline)
                             (ox-ipynb--jupyter-anchor
                              (org-element-property :raw-value headline)))))
            (format "%s- [%s](#%s)" indentation title anchor)))
        headlines
        "\n")
       "\n"))))


(defun ox-ipynb-get-language ()
  "Get the language for the exporter.
If you set OX-IPYNB-LANGUAGE it will be used, otherwise we assume
the first code-block contains the language you want. If none of
those exist, default to ipython.

Displays a warning if the detected language is not defined in
`ox-ipynb-kernelspecs'."
  (let ((lang (intern (or
		       (cdr (assoc "OX-IPYNB-LANGUAGE" (org-element-map (org-element-parse-buffer)
							   'keyword
							 (lambda (key)
							   (cons (org-element-property :key key)
								 (org-element-property :value key))))))
		       (org-element-map (org-element-parse-buffer)
			   'src-block
			 (lambda (src)
			   (unless (string= "none"
					    (cdr (assq :exports
						       (org-babel-parse-header-arguments
							(org-element-property :parameters src)))))
			     (org-element-property :language src)))
			 nil t)
		       "ipython"))))
    (unless (assq lang ox-ipynb-kernelspecs)
      (display-warning
       'ox-ipynb
       (format "Language \"%s\" not defined in ox-ipynb-kernelspecs. Add it with (add-to-list 'ox-ipynb-kernelspecs '(%s . (kernelspec . ...)))"
	       lang lang)
       :warning))
    lang))


(defun ox-ipynb-split-text (s)
  "Given a string S, split it into substrings.
Each heading is its own string. Also, split on #+ipynb-newcell and #+attr_ipynb.
Empty strings are eliminated."
  (let* ((s1 (ox-ipynb--slice-at org-heading-regexp s))
         ;; split headers out
         (s2 (cl-loop for string in s1
                   append
                   (if (string-match org-heading-regexp string)
                       (let ((si (split-string string "\n"))
			     heading content)
			 ;; The first one is definitely the heading. We may also
			 ;; need properties.
			 (setq heading (pop si))
			 (when (and si (string-match-p ":PROPERTIES:" (car si)))
			   (setq heading (concat "\n" heading (pop si) "\n"))
			   (while (not (string-match-p ":END:" (car si)))
			     (setq heading (concat heading (pop si) "\n")))
			   (setq heading (concat heading (pop si) "\n")))
                         (list heading
			       (mapconcat 'identity si "\n")))
                     (list string))))
         (s3 (cl-loop for string in s2
                   append
                   (split-string string "#\\+ipynb-newcell")))
	 ;; check for paragraph metadata and split on that, but keep the attribute.
	 (s4 (cl-loop for string in s3
                   append
		   ;; Note I specifically leave off the b: in this pattern so I
		   ;; can use it in the next section
                   (split-string string "^#\\+attr_ipyn")))
	 (s5 (cl-loop for string in s4 collect
		   (if (string-prefix-p "b: " string t)
		       (concat "#+attr_ipyn" string)
		     string))))

    s5))


(defun ox-ipynb-export-to-buffer-data ()
  ;; This is a hack to remove empty Results. I think this is a bug in org-mode,
  ;; that it exports empty results to have a nil in them without a \n, which
  ;; causes this exporter to fail to find them.
  (save-excursion
    (goto-char (point-min))
    (while (re-search-forward "#\\+RESULTS:\s+
:RESULTS:
nil:END:"  nil t)
      (replace-match "")))

  ;; this is a temporary hack to fix a bug in org-mode that puts a nil at the
  ;; end of exported dynamic blocks. <2017-05-19 Fri>
  (save-excursion
    (goto-char (point-min))
    (while (re-search-forward "\\(#\\+BEGIN:.*\\)nil"  nil t)
      (replace-match "\\1")))

  ;; expand any include files
  (org-export-expand-include-keyword)

  ;; preprocess some org-elements that need to be exported to strings prior to
  ;; the rest. This is not complete. Do these in reverse so the buffer positions
  ;; don't get changed in the parse tree.
  ;; ** footnotes
  (mapc (lambda (elm)
	  (cl--set-buffer-substring (org-element-property :begin elm)
				    (org-element-property :end elm)
				    (format "<a href=\"#%s\">[%s]</a>"
					    (org-element-property :label elm)
					    (org-element-property :label elm))))
	(reverse (org-element-map (org-element-parse-buffer) 'footnote-reference 'identity)))

  (mapc (lambda (elm)
	  (cl--set-buffer-substring (org-element-property :begin elm)
				    (org-element-property :end elm)
				    (format "<p id=\"%s\">[%s] %s"
					    (org-element-property :label elm)
					    (org-element-property :label elm)
					    (buffer-substring (org-element-property :contents-begin elm)
							      (org-element-property :contents-end elm)))))
	(reverse (org-element-map (org-element-parse-buffer) 'footnote-definition 'identity)))

  ;; ** quote blocks
  (mapc (lambda (elm)
          (cl--set-buffer-substring (org-element-property :begin elm)
				    (org-element-property :end elm)
				    (org-md-quote-block elm
							(buffer-substring
							 (org-element-property :contents-begin elm)
							 (org-element-property :contents-end elm))
							nil)))
        (reverse (org-element-map (org-element-parse-buffer) 'quote-block 'identity)))

  (mapc (lambda (elm)
          (cl--set-buffer-substring (org-element-property :begin elm)
				    (org-element-property :end elm)
				    (org-md-export-block elm
							 (buffer-substring
							  (org-element-property :contents-begin elm)
							  (org-element-property :contents-end elm))
							 nil)))
        (reverse (org-element-map (org-element-parse-buffer) 'dynamic-block 'identity)))



  ;; Now we parse the buffer.
  (let* ((ox-ipynb--toc-content nil)
         (cells '())
         (ox-ipynb-language (ox-ipynb-get-language))
         (metadata `(metadata . ((org . ,(let* ((all-keywords (org-element-map (org-element-parse-buffer)
                                                                  'keyword
                                                                (lambda (key)
                                                                  (cons (org-element-property :key key)
                                                                        (org-element-property :value key)))))
                                                (ipynb-keywords (cdr (assoc "OX-IPYNB-KEYWORD-METADATA" all-keywords)))
                                                (include-keywords (mapcar 'upcase (split-string (or ipynb-keywords ""))))
                                                (keywords (cl-loop for key in include-keywords
                                                                   collect (assoc key all-keywords))))
                                           keywords))
                                 ,(cdr (assoc ox-ipynb-language ox-ipynb-kernelspecs))
                                 ,(cdr (assoc ox-ipynb-language ox-ipynb-language-infos))
                                 ;; Add custom notebook metadata from OX-IPYNB-NOTEBOOK-METADATA
                                 ,@(let* ((all-keywords (org-element-map (org-element-parse-buffer)
                                                          'keyword
                                                        (lambda (key)
                                                          (cons (org-element-property :key key)
                                                                (org-element-property :value key)))))
                                          (notebook-metadata-strings (cl-loop for kw in all-keywords
                                                                             when (string= (car kw) "OX-IPYNB-NOTEBOOK-METADATA")
                                                                             collect (cdr kw)))
                                          (all-metadata (cl-loop for meta-string in notebook-metadata-strings
                                                                append (condition-case err
                                                                           (read (format "(%s)" meta-string))
                                                                         (error
                                                                          (message "Error parsing OX-IPYNB-NOTEBOOK-METADATA: %s" err)
                                                                          nil)))))
                                     all-metadata))))
         (ipynb (ox-ipynb-notebook-filename))
         src-blocks
         src-results
         current-src
         result
         result-end
         end
         data)

    ;; Do we need a title cell?
    (let* ((keywords (org-element-map (org-element-parse-buffer)
			 'keyword
		       (lambda (key)
			 (cons (org-element-property :key key)
			       (org-element-property :value key)))))
	   (title (cdr (assoc "TITLE" keywords)))
	   (author (cdr (assoc "AUTHOR" keywords)))
	   (date (cdr (assoc "DATE" keywords)))
	   title-string
	   cell)
      (when title
	(setq title_string (format "%s\n%s\n\n" title (make-string (length title) ?=)))
	(when author
	  (setq title_string (format "%s**Author:** %s\n\n" title_string author)))
	(when date
	  (setq title_string (format "%s**Date:** %s\n\n" title_string date)))

	(push `((cell_type . "markdown")
		(id . ,(org-id-uuid))
		(metadata . ,(make-hash-table))
		(source . ,title_string))
	      cells)))

    ;; Next keyword cells
    (let ((kws (ox-ipynb-export-keyword-cell)))
      (when kws (push kws cells)))

    ;; Add table of contents if requested
    (let* ((export-options (org-export--get-inbuffer-options))
           (with-toc (plist-get export-options :with-toc)))
      (when with-toc
        (let* ((tree (org-element-parse-buffer))
               (info (org-combine-plists
                      export-options
                      (org-export-get-environment 'md)
                      (list :parse-tree tree)))
               (toc-depth (if (wholenump with-toc) with-toc nil))
               (toc-content (ox-ipynb--build-toc info toc-depth)))
          (when toc-content
            (setq ox-ipynb--toc-content (string-trim toc-content))
            (push `((cell_type . "markdown")
                    (id . ,(org-id-uuid))
                    (metadata . ,(make-hash-table))
                    (source . ,toc-content))
                  cells)))))

    (setq src-blocks (org-element-map (org-element-parse-buffer) 'src-block
                       (lambda (src)
                         (when (string= (symbol-name ox-ipynb-language)
                                        (org-element-property :language src))
                           src))))

    ;; Get a list of (src . results). These are only source blocks and
    ;; corresponding results. We assume that before, between and after src
    ;; blocks there are markdown cells.
    (setq src-results
          (cl-loop for src in src-blocks
                   with result=nil
                   do
                   (setq result
			 (save-excursion
                           (goto-char (org-element-property :begin src))
                           (let ((location (org-babel-where-is-src-block-result nil nil))
				 start end
				 result-content)
                             (when location
                               (save-excursion
				 (goto-char location)
				 (when (looking-at
					(concat org-babel-result-regexp ".*$"))
                                   (setq start (1- (match-beginning 0))
					 end (progn (forward-line 1) (org-babel-result-end))
					 result-content (buffer-substring-no-properties
							 start end))
                                   ;; clean up the results a little. This gets rid
                                   ;; of the RESULTS markers for output and drawers
                                   (cl-loop for pat in '("#\\+RESULTS:"
							 "^: " "^:RESULTS:\\|^:END:")
					    do
					    (setq result-content (replace-regexp-in-string
								  pat
								  ""
								  result-content)))
                                   ;; the results and the end of the results.
                                   ;; we use the end later to move point.
                                   (cons (string-trim result-content) end)))))))
                   collect
                   (cons src result)))

    (setq current-source (pop src-results))

    ;; First block before a src is markdown, unless it happens to be empty.
    (if (car current-source)
        (unless (string= "" (string-trim
                             (buffer-substring-no-properties
                              (point-min)
                              (org-element-property :begin (car current-source)))))
          (let ((text (buffer-substring-no-properties
                       (point-min)
                       (org-element-property :begin (car current-source)))))
            (cl-loop for s in (ox-ipynb-split-text text)
                     unless (string= "" (string-trim s))
                     do
                     (when-let* ((md (ox-ipynb-export-markdown-cell s)))
                       (push md cells)))))
      ;; this is a special case where there are no source blocks, and the whole
      ;; document is a markdown cell.
      (let ((text (buffer-substring-no-properties (point-min) (point-max))))
        (cl-loop for s in (ox-ipynb-split-text text)
		 unless (string= "" (string-trim s))
		 do
		 (when-let* ((md (ox-ipynb-export-markdown-cell s)))
                   (push md cells)))))

    (while current-source
      ;; add the src cell
      (push (ox-ipynb-export-code-cell current-source) cells)
      (setq result-end (cdr current-source)
            result (car result-end)
            result-end (cdr result-end))

      (setq end (max
                 (or result-end 0)
                 (org-element-property :end (car current-source))))

      (setq current-source (pop src-results))

      (if current-source
          (when (not (string= "" (string-trim (buffer-substring
                                          end
                                          (org-element-property
                                           :begin
                                           (car current-source))))))
            (let ((text (buffer-substring-no-properties
                         end (org-element-property :begin
                                                   (car current-source)))))
              (cl-loop for s in (ox-ipynb-split-text text)
                       unless (string= "" s)
                       do
                       (when-let* ((md (ox-ipynb-export-markdown-cell (string-trim s))))
			 (push md cells)))))
        ;; on last block so add rest of document
        (let ((text (buffer-substring-no-properties end (point-max))))
          (cl-loop for s in (ox-ipynb-split-text text)
                   unless (string= "" s)
                   do
                   (when-let* ((md (ox-ipynb-export-markdown-cell (string-trim s))))
                     (push md cells))))))

    (setq data (append
                `((cells . ,(reverse cells)))
                (list metadata)
                '((nbformat . 4)
                  (nbformat_minor . 5))))

    data))



(defun ox-ipynb-notebook-filename ()
  "Get filename for export."
  (or (and (boundp 'export-file-name) export-file-name)
      ;; subtree
      (org-entry-get (point) "EXPORT_FILE_NAME")
      ;; file level
      (org-element-map (org-element-parse-buffer 'element) 'keyword
	(lambda (k)
	  (when (string= "EXPORT_FILE_NAME" (org-element-property :key k))
	    (org-element-property :value k)))
	nil t)
      ;; last case - preserve directory of source file
      (let ((source-file (buffer-file-name)))
	(if source-file
	    (concat (file-name-sans-extension source-file) ".ipynb")
	  "Untitled.ipynb"))))


(defun ox-ipynb-preprocess-ignore ()
  "Process the ignore headlines similar to
  `org-export-ignore-headlines'."
  (goto-char (point-min))
  (while (re-search-forward org-heading-regexp nil 'mv)
    (when (member "ignore" (org-get-tags))
      (save-restriction
	(org-narrow-to-subtree)
	;; first remove headline and properties.
	(beginning-of-line)
	(cl--set-buffer-substring (point)
				  (progn (org-end-of-meta-data)
					 (point))
				  "")
	;; now, promote any remaining headlines in this section
	(while (re-search-forward org-heading-regexp nil 'mv)
	  (org-promote))))))


(defun ox-ipynb-preprocess-babel-calls ()
  "Process babel calls to remove them.
They don't work well in the export."
  (goto-char (point-min))
  (cl-loop for bc in (reverse (org-element-map (org-element-parse-buffer) 'babel-call 'identity))
	   do
	   (delete-region (org-element-property :begin bc)
			  (org-element-property :end bc))))


(defun ox-ipynb-export-to-buffer ()
  "Export the current buffer to ipynb format in a buffer.
Only ipython source blocks are exported as code cells. Everything
else is exported as a markdown cell. The output is in *ox-ipynb*."
  (interactive)
  (org-export-with-buffer-copy
   ;; First, let's delete any headings in :exclude-tags
   (let ((exclude-tags (or (plist-get (org-export--get-inbuffer-options) :exclude-tags)
			   org-export-exclude-tags)))
     (cl-loop for hl in
	      (reverse
	       (org-element-map (org-element-parse-buffer) 'headline
		 (lambda (hl)
		   (when (cl-intersection (org-get-tags
					   (org-element-property :begin hl) t)
					  exclude-tags)
		     hl))))
	      do
	      (cl--set-buffer-substring (org-element-property :begin hl)
					(org-element-property :end hl)
					"")))

   ;; Now delete anything not in select_tags, but only if there is some headline
   ;; with one of the tags.
   (let* ((select-tags (or (plist-get (org-export--get-inbuffer-options) :select-tags)
			   org-export-select-tags))
	  (found nil)
	  (hls (reverse
		(org-element-map (org-element-parse-buffer) 'headline
		  (lambda (hl)
		    (when (cl-intersection (org-get-tags
					    (org-element-property :begin hl))
					   select-tags)
		      (setq found t))
		    (unless (cl-intersection (org-get-tags
					      (org-element-property :begin hl) t)
					     select-tags)
		      hl))))))
     (when found
       (cl-loop for hl in hls
		do
		(cl--set-buffer-substring (org-element-property :begin hl)
					  (org-element-property :end hl)
					  ""))))

   ;; Now we should remove any src blocks with :exports none in them
   (cl-loop for src in
	    (reverse
	     (org-element-map (org-element-parse-buffer)
		 'src-block
	       (lambda (src)
		 (when (string= "none"
				(cdr (assq :exports
				           (org-babel-parse-header-arguments
					    (org-element-property :parameters src)))))
		   src))))
	    do
	    (goto-char (org-element-property :begin src))
	    (org-babel-remove-result)
	    (cl--set-buffer-substring (org-element-property :begin src)
				      (org-element-property :end src)
				      ""))

   ;; And finally run any additional hooks
   (cl-loop for func in ox-ipynb-preprocess-hook do (funcall func))

   ;; Now get the data and put the json into a buffer
   ;; Disable org-element caching to ensure we see modifications from hooks
   (let ((org-element-use-cache nil))
   (let ((data (ox-ipynb-export-to-buffer-data))
	 (ipynb (ox-ipynb-notebook-filename)))
     (with-current-buffer (get-buffer-create "*ox-ipynb*")
       (erase-buffer)
       (insert (json-encode data)))

     (switch-to-buffer "*ox-ipynb*")
     (setq-local export-file-name ipynb)
     (get-buffer "*ox-ipynb*")))))


(defun ox-ipynb-nbopen (fname)
  "Open FNAME in jupyter notebook."
  (interactive  (list (read-file-name "Notebook: ")))
  (shell-command (format "nbopen \"%s\" &" fname)))


(defun ox-ipynb-remove-solution ()
  "Delete all SOLUTION regions.
This is usually run as a function in `ox-ipynb-preprocess-hook'."
  (goto-char (point-max))
  (while (re-search-backward "### BEGIN SOLUTION\\(.\\|\n\\)*?### END SOLUTION" nil t)
    (cl--set-buffer-substring (match-beginning 0) (match-end 0) "")))


(defun ox-ipynb-remove-hidden ()
  "Delete all HIDDEN regions.
This is usually run as a function in `ox-ipynb-preprocess-hook'."
  (goto-char (point-max))
  (while (re-search-backward "### BEGIN HIDDEN\\(.\\|\n\\)*?### END HIDDEN" nil t)
    (cl--set-buffer-substring (match-beginning 0) (match-end 0) "")))


(defun ox-ipynb-remove-remove ()
  "Delete all elements with :remove t in #+attr_ipynb metadata.
Works on src-blocks, paragraphs, plain-lists, and other elements.
This is usually run as a function in `ox-ipynb-preprocess-hook'."
  (let* ((parse-tree (org-element-parse-buffer))
         (elements-to-remove '()))
    ;; Collect all elements with :remove attribute
    ;; Helper to add element to removal list
    (cl-flet ((maybe-remove (elem)
                (when (plist-get (org-export-read-attribute :attr_ipynb elem) :remove)
                  (push (cons (org-element-property :begin elem)
                             (org-element-property :end elem))
                        elements-to-remove))))
      ;; Check src-blocks
      (org-element-map parse-tree 'src-block #'maybe-remove)
      ;; Check paragraphs
      (org-element-map parse-tree 'paragraph #'maybe-remove)
      ;; Check plain-lists
      (org-element-map parse-tree 'plain-list #'maybe-remove))
    ;; Remove elements in reverse order (from end to beginning) to preserve positions
    (dolist (bounds (sort elements-to-remove (lambda (a b) (> (car a) (car b)))))
      (cl--set-buffer-substring (car bounds) (cdr bounds) ""))))


(defvar ox-ipynb--results-blocks nil
  "Alist storing results blocks indexed by source code.
Used to preserve results through intermediate org export.")

(defun ox-ipynb--collect-results ()
  "Collect all #+RESULTS blocks from current buffer before intermediate export.
Stores results indexed by normalized source code in `ox-ipynb--results-blocks'."
  (setq ox-ipynb--results-blocks nil)
  (org-babel-map-src-blocks nil
    (let* ((src-code-raw (nth 1 (org-babel-get-src-block-info)))
           (src-code (ox-ipynb--normalize-code src-code-raw))
           (result-pos (org-babel-where-is-src-block-result))
           result-text)
      (when result-pos
        (save-excursion
          (goto-char result-pos)
          (when (looking-at (concat org-babel-result-regexp ".*$"))
            (let ((start (match-beginning 0))
                  (end (progn (forward-line 1) (org-babel-result-end))))
              (setq result-text (buffer-substring-no-properties start end))
              (push (cons src-code result-text) ox-ipynb--results-blocks))))))))

(defun ox-ipynb--restore-results ()
  "Restore #+RESULTS blocks that were stripped during intermediate export.
Uses results stored in `ox-ipynb--results-blocks'."
  (when ox-ipynb--results-blocks
    (let ((parse-tree (org-element-parse-buffer))
          (insertions '()))
      ;; Collect all src blocks and their matching results
      (org-element-map parse-tree 'src-block
        (lambda (src)
          (let* ((src-code-raw (car (org-export-unravel-code src)))
                 (src-code (ox-ipynb--normalize-code src-code-raw))
                 (result-text (cdr (assoc src-code ox-ipynb--results-blocks))))
            (when result-text
              ;; Store position to insert after src block
              (push (cons (org-element-property :end src) result-text) insertions)))))
      ;; Insert results in reverse order to preserve positions
      (dolist (insertion (sort insertions (lambda (a b) (> (car a) (car b)))))
        (save-excursion
          (goto-char (car insertion))
          ;; Insert a blank line then the results
          (insert "\n" (cdr insertion)))))))

(defun ox-ipynb--normalize-code (code)
  "Normalize CODE by removing leading/trailing whitespace from each line.
This handles indentation differences between original and intermediate export."
  (let ((lines (split-string code "\n")))
    (string-join (mapcar #'string-trim lines) "\n")))

(defun ox-ipynb--collect-attr-metadata ()
  "Collect all #+attr_ipynb: metadata from current buffer before intermediate export.
Stores metadata in `ox-ipynb--attr-metadata' indexed by element source code."
  (setq ox-ipynb--attr-metadata nil)
  (let ((parse-tree (org-element-parse-buffer)))
    ;; Collect from src blocks
    (org-element-map parse-tree 'src-block
      (lambda (src)
        (let ((attr (plist-get (cadr src) :attr_ipynb)))
          (when attr
            (let* ((src-code-raw (car (org-export-unravel-code src)))
                   (src-code (ox-ipynb--normalize-code src-code-raw))
                   (attr-string (string-join attr " ")))
              (push (cons src-code attr-string) ox-ipynb--attr-metadata))))))
    ;; Collect from paragraphs and other elements
    (org-element-map parse-tree 'paragraph
      (lambda (para)
        (let ((attr (plist-get (cadr para) :attr_ipynb)))
          (when attr
            (let* ((para-text (string-trim (buffer-substring-no-properties
                                            (org-element-property :contents-begin para)
                                            (org-element-property :contents-end para))))
                   (attr-string (string-join attr " ")))
              (push (cons para-text attr-string) ox-ipynb--attr-metadata))))))))

(defun ox-ipynb--restore-attr-metadata ()
  "Restore #+attr_ipynb: metadata to elements in current buffer after intermediate export.
Uses metadata stored in `ox-ipynb--attr-metadata'."
  (when ox-ipynb--attr-metadata
    (let ((parse-tree (org-element-parse-buffer))
          (insertions '()))
      ;; Collect all insertions for src blocks (with positions)
      (org-element-map parse-tree 'src-block
        (lambda (src)
          (let* ((src-code-raw (car (org-export-unravel-code src)))
                 (src-code (ox-ipynb--normalize-code src-code-raw))
                 (metadata (cdr (assoc src-code ox-ipynb--attr-metadata))))
            (when metadata
              (push (list 'src (org-element-property :begin src) metadata) insertions)))))
      ;; Collect insertions for paragraphs
      (org-element-map parse-tree 'paragraph
        (lambda (para)
          (let* ((para-text (when (and (org-element-property :contents-begin para)
                                       (org-element-property :contents-end para))
                             (string-trim (buffer-substring-no-properties
                                          (org-element-property :contents-begin para)
                                          (org-element-property :contents-end para)))))
                 (metadata (when para-text
                            (or
                             ;; Try exact match first
                             (cdr (assoc para-text ox-ipynb--attr-metadata))
                             ;; Try prefix match (for paragraphs that gained content like image links)
                             (cl-some (lambda (entry)
                                       (when (string-prefix-p (car entry) para-text)
                                         (cdr entry)))
                                     ox-ipynb--attr-metadata)))))
            (when metadata
              (push (list 'para (org-element-property :begin para) metadata) insertions)))))
      ;; Perform all insertions in reverse order (so positions don't shift)
      (dolist (insertion (sort insertions (lambda (a b) (> (cadr a) (cadr b)))))
        (let ((type (car insertion))
              (pos (cadr insertion))
              (metadata (caddr insertion)))
          (save-excursion
            (goto-char pos)
            (if (eq type 'para)
                ;; Paragraph: insert before
                (insert "#+attr_ipynb: " metadata "\n")
              ;; Src block: go back a line and insert
              (forward-line -1)
              (end-of-line)
              (insert "\n#+attr_ipynb: " metadata))))))))

;; * export menu


(defun ox-ipynb-export-to-ipynb-buffer (&optional async subtreep visible-only
                                                  body-only info)
  "Export the current buffer to an ipynb in a new buffer.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (let ((ox-ipynb-preprocess-hook ox-ipynb-preprocess-hook)
	(ipynb (ox-ipynb-notebook-filename))
	(content (buffer-string))
	;; Collect bibliography files early while we have access to the original buffer
	;; Use expand-file-name to get absolute paths
	(bib-files (condition-case nil
		       (progn (require 'oc)
			      (mapcar #'expand-file-name (org-cite-list-bibliography-files)))
		     (error nil)))
	;; Capture broken-links setting from buffer or variable
	;; Default to 'mark to allow citation links and other special links to pass through
	(ox-ipynb--broken-links (or (plist-get (org-export-get-environment) :with-broken-links)
				    org-export-with-broken-links
				    'mark))
        buf)

    (add-hook 'ox-ipynb-preprocess-hook 'ox-ipynb-preprocess-ignore)
    (add-hook 'ox-ipynb-preprocess-hook 'ox-ipynb-preprocess-babel-calls)

    ;; Collect #+attr_ipynb: metadata before intermediate export (they get stripped)
    (ox-ipynb--collect-attr-metadata)

    ;; Collect #+RESULTS: blocks before intermediate export (they get stripped)
    (ox-ipynb--collect-results)

    ;; Remove cite_export keyword to avoid requiring citeproc during intermediate export
    ;; We'll handle bibliography rendering ourselves later
    (save-excursion
      (goto-char (point-min))
      (while (re-search-forward "^#\\+cite_export:.*$" nil t)
	(replace-match "")))

    ;; now is the time for a final conversion
    ;; Disable TOC in the intermediate org export (we handle it ourselves)
    ;; Enable properties export to preserve PROPERTIES drawers (needed for slideshow metadata)
    ;; Get export environment to preserve buffer settings (like broken-links handling)
    ;; Always mark broken links during intermediate export (citations, fuzzy links will be handled later)
    ;; IMPORTANT: Disable cite processors to prevent org-cite from formatting citations
    ;; We'll handle citation formatting ourselves later
    (let ((info (org-combine-plists
                 (or info (org-export-get-environment))
                 '(:with-toc nil :with-properties t :with-broken-links mark :with-cite-processors nil))))
      (org-org-export-as-org async subtreep visible-only body-only info))
    (with-current-buffer "*Org ORG Export*"
      (setq content (buffer-string)))
    (kill-buffer "*Org ORG Export*")

    (with-temp-buffer
      (insert content)
      (org-mode)
      (setq-local export-file-name ipynb)

      ;; Restore #+attr_ipynb: metadata that was stripped during intermediate export
      (ox-ipynb--restore-attr-metadata)

      ;; Restore #+RESULTS: blocks that were stripped during intermediate export
      (ox-ipynb--restore-results)

      ;; Resolve fuzzy links before markdown conversion
      ;; We need to resolve them here because org-md exports cells in isolation
      ;; and can't resolve links that reference other parts of the document
      (let* ((parsed (org-element-parse-buffer))
             (info (org-combine-plists
                    (org-export-get-environment)
                    (list :with-broken-links ox-ipynb--broken-links
                          :parse-tree parsed)))
             (fuzzy-links (cl-loop for link in (org-element-map parsed 'link 'identity)
                                   if (string= "fuzzy" (org-element-property :type link))
                                   collect link))
             (custom-id-links (cl-loop for link in (org-element-map parsed 'link 'identity)
                                       if (string= "custom-id" (org-element-property :type link))
                                       collect link)))

        ;; Resolve fuzzy links
        (cl-loop for link in (reverse fuzzy-links)
                 do
                 (let* ((path (org-element-property :path link))
                        ;; Skip cite: style links (they're handled by org-ref preprocessing)
                        (is-cite-link (string-prefix-p "cite:" path))
                        (target (unless is-cite-link
                                  (condition-case nil
                                      (org-export-resolve-fuzzy-link link info)
                                    (error nil)))))
                   (when target
                     ;; Link resolved! Replace with markdown link to the target
                     ;; Generate markdown-style slug from heading text (not org's auto ID)
                     (let* ((target-text (cond
                                          ((eq (org-element-type target) 'headline)
                                           (org-element-property :raw-value target))
                                          ((eq (org-element-type target) 'target)
                                           (org-element-property :value target))
                                          (t path)))
                            ;; Slugify: replace spaces with hyphens, remove special chars, preserve case
                            ;; This matches GitHub-flavored markdown and Jupyter anchor style
                            (target-slug (replace-regexp-in-string
                                          "[^A-Za-z0-9-]" ""
                                          (replace-regexp-in-string
                                           " +" "-"
                                           target-text)))
                            (contents-begin (org-element-property :contents-begin link))
                            (contents-end (org-element-property :contents-end link))
                            (desc (when (and contents-begin contents-end)
                                    (buffer-substring-no-properties contents-begin contents-end)))
                            ;; For links like [[*Heading]], strip the leading * from the path when using as description
                            (link-text (or desc
                                          (if (string-prefix-p "*" path)
                                              (substring path 1) ; Remove leading *
                                            path)))
                            ;; Preserve any trailing whitespace that org-element includes in :end
                            (link-end (org-element-property :end link))
                            (trailing-space (when (and (< link-end (point-max))
                                                      (= (char-after (1- link-end)) ?\s))
                                             " "))
                            (markdown-link (concat (format "[%s](#%s)" link-text target-slug)
                                                  trailing-space)))
                       (cl--set-buffer-substring (org-element-property :begin link)
                                                 (org-element-property :end link)
                                                 markdown-link)))))

        ;; Handle custom-id links (org-ref style)
        (cl-loop for link in (reverse custom-id-links)
                 do
                 (cl--set-buffer-substring (org-element-property :begin link)
                                           (org-element-property :end link)
                                           (format "[%s]" (org-element-property :path link)))))

      ;; Format inline citations for org-cite
      ;; Build a map of citation keys to formatted short citations
      (when bib-files
	(let ((citation-map (make-hash-table :test 'equal)))
	  ;; Load all citations from bib files
	  (with-temp-buffer
	    (dolist (bibfile bib-files)
	      (when (file-exists-p bibfile)
		(insert-file-contents bibfile)))
	    (bibtex-mode)
	    ;; Parse each entry and create short citation
	    (goto-char (point-min))
	    (while (re-search-forward "@[a-zA-Z]+{" nil t)
	      (beginning-of-line)
	      (let ((entry (bibtex-parse-entry)))
		(when entry
		  (let* ((key (cdr (assoc "=key=" entry)))
			 ;; Clean and normalize author field (remove braces, newlines, extra spaces)
			 (author-raw (or (cdr (assoc "author" entry)) ""))
			 (author (string-trim
				  (replace-regexp-in-string
				   " +" " "
				   (replace-regexp-in-string
				    "[\n\r]+" " "
				    (replace-regexp-in-string "[{}]" "" author-raw)))))
			 (year (replace-regexp-in-string "[{}]" "" (or (cdr (assoc "year" entry)) "")))
			 ;; Extract first author's last name
			 (first-author (if (string-match "\\([A-Za-z-]+\\)," author)
					   (match-string 1 author)
					 "Unknown"))
			 ;; Check if multiple authors (contains "and")
			 (multiple-authors (string-match-p " and " author))
			 (short-cite (format "(%s%s %s)"
					     first-author
					     (if multiple-authors " et al." "")
					     year)))
		    (puthash key short-cite citation-map))))
	      (forward-line 1)))

	  ;; Collect all citations and citation keys BEFORE replacement
	  (let ((citations (org-element-map (org-element-parse-buffer) 'citation 'identity))
		(all-citation-keys (org-element-map (org-element-parse-buffer) 'citation-reference
				     (lambda (ref) (org-element-property :key ref)))))

	    ;; Replace all citation references in the buffer
	    (cl-loop for citation in (reverse citations)
		     do
		     (let* ((refs (org-element-map citation 'citation-reference
				    (lambda (ref) (org-element-property :key ref))))
			    (formatted-cite (mapconcat
					     (lambda (key)
					       (or (gethash key citation-map)
						   (format "(%s, ????)" key)))
					     refs
					     "; ")))
		       (cl--set-buffer-substring (org-element-property :begin citation)
						 (org-element-property :end citation)
						 formatted-cite)))

	    ;; Now process bibliography with access to all-citation-keys
	    ;; IMPORTANT: Re-parse the buffer AFTER citation replacements to get correct positions
	    (let* ((bib-entries (cl-loop for hl in (org-element-map
						     (org-element-parse-buffer) 'headline 'identity)
				       if (org-element-property :=KEY= hl)
				       collect hl))
		 (print-bib-keyword (org-element-map (org-element-parse-buffer) 'keyword
				      (lambda (kw)
					(when (string-match-p "PRINT_BIBLIOGRAPHY"
							     (upcase (org-element-property :key kw)))
					  kw))
				      nil t))
		 (formatted-entries nil))

	      ;; Format entries from org-bibtex headings if they exist
	      (when bib-entries
		(setq formatted-entries
		      (mapconcat
		       (lambda (hl)
			 (ox-ipynb--format "[${=KEY=}] ${AUTHOR}. ${TITLE}. https://dx.doi.org/${DOI}\n\n"
					   (lambda (arg &optional extra)
					     (let ((entry (org-element-property (intern-soft (concat ":"arg)) hl)))
					       (substring
						entry
						(if (string-prefix-p "{" entry) 1 0)
						(if (string-suffix-p "}" entry) -1 nil))))))
		       bib-entries
		       "")))

	      ;; If no org-bibtex entries found, try org-cite (read .bib files directly)
	      ;; Use the citation keys we collected earlier (before replacing citations)
	      (when (and (not bib-entries) print-bib-keyword all-citation-keys)
		(setq formatted-entries
		      (with-temp-buffer
			(dolist (bibfile bib-files)
			  (when (file-exists-p bibfile)
			    (insert-file-contents bibfile)))
			(bibtex-mode)
			(mapconcat
			 (lambda (key)
			   (goto-char (point-min))
			   (if (bibtex-search-entry key)
			       (let* ((entry (bibtex-parse-entry))
				      ;; Helper to clean bibtex field: remove braces and normalize whitespace
				      (clean-field (lambda (field)
						     (let ((value (or (cdr (assoc field entry)) "")))
						       ;; Remove braces
						       (setq value (replace-regexp-in-string "[{}]" "" value))
						       ;; Normalize whitespace: replace newlines and multiple spaces with single space
						       (setq value (replace-regexp-in-string "[\n\r]+" " " value))
						       (setq value (replace-regexp-in-string " +" " " value))
						       ;; Trim leading/trailing whitespace
						       (string-trim value))))
				      (author (funcall clean-field "author"))
				      (title (funcall clean-field "title"))
				      (year (funcall clean-field "year"))
				      (doi (funcall clean-field "doi"))
				      (url (funcall clean-field "url")))
				 (format "[%s] %s. %s. %s%s\n\n"
					 key
					 (if (string= author "") "Unknown" author)
					 (if (string= title "") "Untitled" title)
					 year
					 (if (and doi (not (string= doi "")))
					     (format " https://dx.doi.org/%s" doi)
					   (if (and url (not (string= url "")))
					       (format " %s" url)
					     ""))))
			     ""))
			 all-citation-keys
			 ""))))

	      ;; If we found a PRINT_BIBLIOGRAPHY keyword, replace it with the formatted entries
	      (when (and print-bib-keyword formatted-entries (not (string= formatted-entries "")))
		(cl--set-buffer-substring (org-element-property :begin print-bib-keyword)
					  (org-element-property :end print-bib-keyword)
					  formatted-entries))

	      ;; Remove the original bibliography entry headings (org-ref style)
	      (cl-loop for hl in (reverse bib-entries)
		       do
		       (cl--set-buffer-substring (org-element-property :begin hl)
						 (org-element-property :end hl)
						 ""))))))  ; Close cl-loop, let* (bib), let (citations), let (citation-map), when (bib-files)

      (let ((buf (ox-ipynb-export-to-buffer)))
	(with-current-buffer buf
	  (setq-local export-file-name ipynb))
	buf))))  ; Close let+with-temp-buffer


(defun ox-ipynb-export-to-ipynb-file (&optional async subtreep visible-only body-only info)
  "Export current buffer to a file.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (with-current-buffer (ox-ipynb-export-to-ipynb-buffer async subtreep visible-only body-only info)
    (let* ((efn export-file-name)
           (buf (find-file-noselect efn) ))
      (write-file efn)
      (with-current-buffer buf
        (setq-local export-file-name efn))
      (kill-buffer buf)
      efn)))


(defun ox-ipynb-export-to-ipynb-file-and-open (&optional async subtreep visible-only body-only info)
  "Export current buffer to a file and open it.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (let* ((async-shell-command-buffer 'confirm-kill-buffer)
         (fname (expand-file-name
                 (ox-ipynb-export-to-ipynb-file async subtreep visible-only body-only info))))
    ;; close the .ipynb buffer.
    (kill-buffer (find-file-noselect fname))
    (async-shell-command
     (format "jupyter notebook \"%s\"" fname))))


(defun ox-ipynb-export-to-ipynb-slides-and-open (&optional async subtreep visible-only body-only info)
  "Export current buffer to a slide show and open it.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (let* ((async-shell-command-buffer 'confirm-kill-buffer)
         (fname (expand-file-name
                 (ox-ipynb-export-to-ipynb-file async subtreep visible-only body-only info))))
    ;; close the .ipynb buffer.
    (kill-buffer (find-file-noselect fname))
    (async-shell-command
     (format "jupyter nbconvert \"%s\" --to slides --post serve" fname))))


(defun ox-ipynb-export-to-ipynb-no-results-file-and-open (&optional async subtreep visible-only body-only info)
  "Export current buffer to a file and open it. Strip results first.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (let ((ox-ipynb-preprocess-hook  ox-ipynb-preprocess-hook ))
    (add-hook 'ox-ipynb-preprocess-hook
              (lambda ()
                (org-babel-map-src-blocks nil
                  (org-babel-remove-result))
                ;; Clean up any stray RESULTS drawers left behind
                (save-excursion
                  ;; Remove full RESULTS drawers (handling nested drawers properly)
                  (goto-char (point-min))
                  (while (re-search-forward "^:RESULTS:\\s-*$" nil t)
                    (let ((start (match-beginning 0))
                          (depth 1))
                      ;; Move forward counting drawer depth
                      (forward-line)
                      (while (and (> depth 0) (not (eobp)))
                        (cond
                         ((looking-at "^:RESULTS:\\s-*$")
                          (setq depth (1+ depth)))
                         ((looking-at "^:END:\\s-*$")
                          (setq depth (1- depth))))
                        (forward-line))
                      ;; Remove the entire drawer
                      (delete-region start (point))))
                  ;; Clean up any remaining standalone :END: lines (not in property drawers)
                  (goto-char (point-min))
                  (while (re-search-forward "^\\s-*:END:\\s-*$" nil t)
                    (unless (save-excursion
                              (forward-line -1)
                              (looking-at "^:PROPERTIES:"))
                      (replace-match ""))))))

    (ox-ipynb-export-to-ipynb-file-and-open)))


(defun ox-ipynb-export-org-file-to-ipynb-file (file)
  "Export FILE  with `ox-ipynb-export-to-ipynb-file'.
Works interactively: M-x ox-ipynb-export-org-file-to-ipynb-file RET
Works non-interactively: (ox-ipynb-export-org-file-to-ipynb-file \"test.org\")
Works in Dired+ by marking some *.org files and pressing \"@\" ox-ipynb-export-org-file-to-ipynb-file RET
Based on the `org-babel-tangle-file' function that is to be
found in the ob-tangle.el file."
  (interactive "fOrg file to export as ipynb: ")
  (let ((visited-p (find-buffer-visiting (expand-file-name file)))
	to-be-removed)
    (prog1
	(save-window-excursion
	  (find-file file)
	  (setq to-be-removed (current-buffer))
          (ox-ipynb-export-to-ipynb-file) )
      (unless visited-p
	(kill-buffer to-be-removed)))))


(defun ox-ipynb-export-to-participant-notebook (&optional async subtreep visible-only body-only info)
  "Export current buffer to a participant file and open it.
Removes SOLUTION and HIDDEN regions.
Optional argument ASYNC to asynchronously export.
Optional argument SUBTREEP to export current subtree.
Optional argument VISIBLE-ONLY to only export visible content.
Optional argument BODY-ONLY export only the body.
Optional argument INFO is a plist of options."
  (let ((ox-ipynb-preprocess-hook (append ox-ipynb-preprocess-hook '(ox-ipynb-remove-hidden
								     ox-ipynb-remove-solution
								     ox-ipynb-remove-remove))))
    (ox-ipynb-export-to-ipynb-file-and-open)))


(org-export-define-derived-backend 'jupyter-notebook 'org
  :menu-entry
  '(?n "Export to jupyter notebook"
       ((?b "to buffer" ox-ipynb-export-to-ipynb-buffer)
        (?n "to notebook" ox-ipynb-export-to-ipynb-file)
	(?o "to notebook and open" ox-ipynb-export-to-ipynb-file-and-open)
	(?p "to participant nb & open" ox-ipynb-export-to-participant-notebook)
        (?r "to nb (no results) and open" ox-ipynb-export-to-ipynb-no-results-file-and-open)
	(?s "to slides and open" ox-ipynb-export-to-ipynb-slides-and-open))))


(defun ox-ipynb-publish-to-notebook (plist filename pub-dir)
  "Publish an org-file to a Jupyter notebook."
  (with-current-buffer (find-file-noselect filename)
    (let ((output (ox-ipynb-export-to-ipynb-file)))
      (org-publish-attachment plist (expand-file-name output)  pub-dir)
      output)))

(provide 'ox-ipynb)

;;; ox-ipynb.el ends here
