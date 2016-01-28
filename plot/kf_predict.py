import numpy as np
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt

##plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=8)

fig, ax = plt.subplots(1, 1)
fig.set_size_inches(5, 2)
plt.xlim([-1, 10])
x = np.linspace(-1, 10, 1000)

mu = 3.5
std = 0.3
ax.plot(x, norm.pdf(x, mu, std), 'k--', dashes=(5,2), lw=1, alpha=1.0, label='norm pdf')

mu = 4.5
std = 0.5
ax.plot(x, norm.pdf(x, mu, std), 'k-', lw=1, alpha=1.0, label='norm pdf')

plt.savefig("../images/kf_predict_temp.png", dpi=300)
#plt.show()
