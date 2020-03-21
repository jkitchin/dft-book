from vasp import VAsp
calc = Vasp('bulk/Cu-cls-0')
calc.clone('bulk/Cu-cls-1')
calc.set(ibrion=None,
         isif=None,
         nsw=None,
         setups=[[0, 'Cu']],  # Create separate entry in POTCAR for atom index 0
         icorelevel=2,        # Perform core level shift calculation
         clnt=0,              # Excite atom index 0
         cln=2,               # 2p3/2 electron for Cu core level shift
         cll=1,
         clz=1)
calc.update()