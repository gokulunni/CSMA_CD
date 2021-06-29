from csma_cd import CSMA_CD
import matplotlib.pyplot as plt

D = 10
S = (2/3) * 3 * (10**8)
R =  1000000
L = 1500
T = 1000
nodes = [20, 40, 60, 80, 100]
arrival_rates = [7, 10, 20]
efficiency = [ [], [], [] ]
throughput = [ [], [], [] ]

for N in nodes:
    for i in range(len(arrival_rates)):
        A = arrival_rates[i]

        csma_cd_sim = CSMA_CD(N, A, R, L, D, S, T, False)
        csma_cd_sim.simulate()
        csma_cd_sim.print_results()
        
        efficiency[i].append(csma_cd_sim.efficiency)
        throughput[i].append(csma_cd_sim.throughput)

# Plot the efficiency and throughput graphs using the simulation data
for i in range(len(efficiency)):
    plt.figure(0)
    plt.plot(nodes, efficiency[i], label = str(arrival_rates[i]) + " packets/s")

    plt.figure(1)
    plt.plot(nodes, throughput[i], label = str(arrival_rates[i]) + " packets/s")

plt.figure(0)
plt.xlabel('Number of nodes')
plt.ylabel('Efficiency')
plt.title('Number of Nodes vs. Efficiency for Different Arrival Rates')
plt.legend()
plt.savefig('q2_efficiency.png')

plt.figure(1)
plt.xlabel('Number of nodes')
plt.ylabel('Throughput')
plt.title('Number of Nodes vs. Throughput for Different Arrival Rates')
plt.legend()
plt.savefig('q2_throughput.png')