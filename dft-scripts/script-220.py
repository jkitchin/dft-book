from jasp import *
with jasp('bulk/CuPd-cls-0') as calc:
    calc.clone('bulk/CuPd-cls-1')
with jasp('bulk/CuPd-cls-1') as calc:
    calc.set(ibrion=None,
             isif=None,
             nsw=None,
             setups={'0': 'Cu'},  # Create separate entry in POTCAR for atom index 0
             icorelevel=2,        # Perform core level shift calculation
             clnt=0,              # Excite atom index 0
             cln=2,               # 2p3/2 electron for Cu core level shift
             cll=1,
             clz=1)
    print(calc.get_atoms().get_potential_energy())