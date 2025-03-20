import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta, norm
from scipy.stats.sampling import TransformedDensityRejection
from math import exp

class CoinPosterior:
    def pdf(self, p: float) -> float:
        # note that the normalization constant isn't required
        return p**16 * (1 - p)**4
    def dpdf(self, p: float) -> float:
        return 16*p**15 * (1 - p)**4 - p**16 *4* (1 - p)**3

dist = CoinPosterior()
urng = np.random.default_rng()
rng = TransformedDensityRejection(dist, domain=(0,1), random_state=urng)
rvs = rng.rvs(size=1000)

x = np.linspace(0, 1, num=1000)
fx = beta.pdf(x,17,5)

plt.plot(x, fx, 'r-', lw=2, label='true coin posterior')
plt.hist(rvs, bins=30, density=True, alpha=0.8, label='random sample from the posterior')
plt.xlabel('p')
plt.ylabel('PDF(p)')
plt.title('Transformed Density Rejection Samples')
plt.legend()
plt.show()
#plt.savefig('eg_sampling.png')
