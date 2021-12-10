# Target plot histogram of review length
import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Hi reader,
# I could not generate norm in a specific scale
# so I truncate it from [-1, 1] then map it to
# configured range.
#
# A bit tricky but accepting it ok :P

# Configure variable
num_sample = 1000
start_pos = 0
end_pos = 1000

# data generate
v_range = end_pos - start_pos
generator = stats.truncnorm(-1, 1, loc=0, scale=1)
observes = generator.rvs(num_sample)
obs_values = [(observes[i] + 1) * (v_range / 2) + start_pos
              for i in range(num_sample)]

# histogram by lib :P
plt.hist(obs_values, bins=int(num_sample / 5))  # bins is number of intervals
plt.savefig("./02.review.length.png")

# statistic calculation
# u is mean and stand is standard deviation
u = sum([obs_values[i] for i in range(num_sample)]) / num_sample
stand = math.sqrt(
    sum([(obs_values[i] - u)**2 for i in range(num_sample)]) / num_sample)
print("mean: ", u)
print("sv  : ", stand)
x_axis = np.linspace(start_pos, end_pos, num_sample)

# norm pdf
plt.clf()
plt.plot(x_axis, stats.norm.pdf(x_axis, loc=u, scale=stand))
plt.savefig("./02.review.length.estimated.png")
