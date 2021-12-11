# Target plot histogram of review length
import math
import json

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Hi reader,
# I could not generate norm in a specific scale
# so I truncate it from [-1, 1] then map it to
# configured range.
#
# A bit tricky but accepting it ok :P

# Load data
documents = []
with open("./yelp_academic_500-head-sample.json", "r") as f:
    for text in f:
        jsonText = json.loads(text)
        realText = jsonText['text']
        documents.append(realText)

# data generate
num_sample = len(documents)
obs_values = [len(doc) for doc in documents]
start_pos = min(obs_values)
end_pos = max(obs_values)

# plot preparation
fig, ax_left = plt.subplots()
ax_right = ax_left.twinx()

# histogram by lib :P
n, x, _ = ax_right.hist(obs_values,
                   bins=int(num_sample / 5))  # bins is number of intervals
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
ax_left.plot(x_axis, stats.norm.pdf(x_axis, loc=u, scale=stand))
plt.savefig("./02.review.length.estimated.png")
