import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt('out.txt', unpack='False')

eta = data[0]
phi = data[1]
p = data[2]
flp = data[3]
localx = data[4]
localy = data[5]
pT = data[6]

print(eta)

print(phi)

print(flp)

#bins = np.linspace(0, 50, 100000)

plt.hist(eta, histtype='bar', rwidth=0.8)
plt.xlabel('eta')
plt.ylabel('Number of Particles')
plt.title('Distribution of eta')
plt.savefig("Histogram_eta.png")
plt.cla()




plt.hist(phi, histtype='bar', rwidth=0.8)
plt.xlabel('phi')
plt.ylabel('Number of Particles')
plt.title('Distribution of phi')
plt.savefig("Histogram_phi.png")
plt.cla()

plt.hist(p, histtype='bar', rwidth=0.8)
plt.xlabel('p')
plt.ylabel('Number of Particle')
plt.title('Distribution of p')
plt.savefig("Histogram_p.png")
plt.cla()



plt.hist(pT, histtype='bar', rwidth=0.8)
plt.xlabel('pT')
plt.ylabel('Number of Particle')
plt.title('Distribution of pT')
plt.savefig("Histogram_pT.png")

