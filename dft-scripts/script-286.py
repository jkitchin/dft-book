(import [ase [Atom Atoms]])
(import [vasp [Vasp]])
(setv co (Atoms [(Atom "C" [0.0 0.0 0.0])
                 (Atom "O" [1.2 0.0 0.0])]
                :cell [6.0 6.0 6.0]))
(setv calc (Vasp "molecules/simple-co-hy"
                 :xc "pbe"
                 :nbands 6
                 :encut 350
                 :ismear 1
                 :sigma 0.01
                 :atoms co))
(print (.format "energy = {0} eV"
                (.get_potential_energy co)))
(print (. calc potential_energy))
; (print (.potential_energy calc)) ;; not ok
(print (.get_forces co))