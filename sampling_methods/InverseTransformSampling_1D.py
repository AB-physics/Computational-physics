# can you made a python animation code for demonstrating inverse transfrom sampling in 1 dimensions and two dimensions?
# please modify the codes such that another plot is added to show the distribution of the sampled points in comparison with the true pdf sampled from

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the inverse CDF of the exponential distribution
def inverse_cdf_exp(u, lambd=1.0):
    return -np.log(1 - u) / lambd

# Define the PDF of the exponential distribution
def pdf_exp(x, lambd=1.0):
    return lambd * np.exp(-lambd * x)

# Generate uniform random numbers
np.random.seed(42)
u = np.random.uniform(0, 1, 1000)

# Apply inverse transform sampling
samples = inverse_cdf_exp(u)

# Create the animation
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.set_xlim(0, 5)
ax1.set_ylim(0, 1)
ax1.set_xlabel('x')
ax1.set_ylabel('CDF')
ax1.set_title('1D Inverse Transform Sampling')

# Plot the theoretical CDF
x = np.linspace(0, 5, 1000)
cdf = 1 - np.exp(-x)
ax1.plot(x, cdf, 'r-', label='Theoretical CDF')

# Initialize the scatter plot for samples
scatter = ax1.scatter([], [], c='b', alpha=0.5, label='Samples')

# Set up the second plot for PDF comparison
ax2.set_xlim(0, 5)
ax2.set_ylim(0, 1)
ax2.set_xlabel('x')
ax2.set_ylabel('PDF')
ax2.set_title('PDF Comparison')

# Plot the theoretical PDF
ax2.plot(x, pdf_exp(x), 'r-', label='Theoretical PDF')

# Initialize the histogram for sampled points
hist, = ax2.plot([], [], 'b-', label='Sampled PDF')

def update(frame):
    # Update the scatter plot
    scatter.set_offsets(np.c_[samples[:frame], u[:frame]])
    
    # Update the histogram for sampled points
    if frame > 0:
        hist_data, bin_edges = np.histogram(samples[:frame], bins=30, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        hist.set_data(bin_centers, hist_data)
    
    return scatter, hist,

ani = FuncAnimation(fig, update, frames=len(u), interval=50, blit=True)
ax1.legend()
ax2.legend()
plt.tight_layout()
plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # Define the inverse CDF of the exponential distribution
# def inverse_cdf_exp(u, lambd=1.0):
#     return -np.log(1 - u) / lambd

# # Generate uniform random numbers
# np.random.seed(42)
# u = np.random.uniform(0, 1, 1000)

# # Apply inverse transform sampling
# samples = inverse_cdf_exp(u)

# # Create the animation
# fig, ax = plt.subplots()
# ax.set_xlim(0, 5)
# ax.set_ylim(0, 1)
# ax.set_xlabel('x')
# ax.set_ylabel('CDF')
# ax.set_title('1D Inverse Transform Sampling')

# # Plot the theoretical CDF
# x = np.linspace(0, 5, 1000)
# cdf = 1 - np.exp(-x)
# ax.plot(x, cdf, 'r-', label='Theoretical CDF')

# # Initialize the scatter plot for samples
# scatter = ax.scatter([], [], c='b', alpha=0.5, label='Samples')

# def update(frame):
#     scatter.set_offsets(np.c_[samples[:frame], u[:frame]])
#     return scatter,

# ani = FuncAnimation(fig, update, frames=len(u), interval=50, blit=True)
# plt.legend()
# plt.show()
