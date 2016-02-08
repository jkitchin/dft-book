;; M-x eval-buffer to run this
;; Should be run on gilgamesh.


(load-file "dft.el")
(find-file "dft.org")
(require 'ox-publish)
(setq org-publish-project-alist
      '(
	("dft-book-content"
	 :base-directory "/home-research/jkitchin/dft/course/dft-book/"
	 :base-extension "org"
	 :publishing-directory "~/home-research/jkitchin/dft/course/dft-book/gh-pages/"
	 :exclude "gh-pages\\|test\\|archive\\|molecules\\|surfaces\\|bulk\\|study-guides\\|blog\\|topics\\|index\\|help\\|header"
	 :recursive t
	 :publishing-function org-html-publish-to-html
	 :headline-levels 4             ; Just the default for this project.
	 :auto-preamble t
	 )
	("dft-book-static"
	 :base-directory "/home-research/jkitchin/dft/course/dft-book/"
	 :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf\\|svg"
	 :publishing-directory "/home-research/jkitchin/dft/course/dft-book/gh-pages/"
	 :exclude  "gh-pages\\|test/\\|archive/\\|molecules/\\|surfaces/\\|bulk/\\|study-guides/"
	 :recursive t
	 :publishing-function org-publish-attachment
	 )
	;; ... all the components ...
	("dft-book" :components ( "dft-book-content" "dft-book-static"))
	))
(setq org-image-actual-width nil)
(org-publish "dft-book")
