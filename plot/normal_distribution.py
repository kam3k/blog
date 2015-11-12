import numpy as np
from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('font', size=8)

fig, ax = plt.subplots(1, 1)
x = np.linspace(norm.ppf(0.00001), norm.ppf(0.99999), 100)
ax.plot(x, norm.pdf(x), 'k-', lw=2, alpha=1.0, label='norm pdf')
plt.xlim([-3.5, 3.5])
plt.ylim([0, 0.45])
fig.set_size_inches(5, 2)

plt.savefig("../images/normal_pdf.png", dpi=300)
