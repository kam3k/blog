import numpy as np
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt

#plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=8)

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5, 2)
plt.xlim([-1, 10])
x = np.linspace(-1, 10, 1000)
mu = range(0,10,2)
std = [0.1 + 0.1 * t for t in range(0,10,2)]
for m, s in zip(mu, std):
    ax.plot(x, norm.pdf(x, m, s), 'k-', lw=2, alpha=1.0, label='norm pdf')

plt.savefig("../images/kf_predict.png", dpi=300)
#plt.show()
