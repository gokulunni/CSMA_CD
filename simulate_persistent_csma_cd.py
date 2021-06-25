from csma_cd import CSMA_CD

D = 10
S = (2/3) * (10**8)
R =  1000000
L = 1500
T = 1000

for N in [20, 40, 60, 80, 100]:
    for A in [7, 10, 20]:
        
        csma_cd_sim = CSMA_CD(N, A, R, L, D, S, T)
        csma_cd_sim.simulate()
        csma_cd_sim.print_results()