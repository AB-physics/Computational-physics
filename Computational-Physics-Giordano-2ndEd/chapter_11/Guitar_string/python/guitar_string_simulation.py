import numpy as np

# Constants and simulation parameters
MAX = 3001
PI = 3.14159

# Global variables
y_new = np.zeros(MAX)
y = np.zeros(MAX)
y_old = np.zeros(MAX)

t = 0.0
dt = dx = r2 = 0.0
n_string = 1000  # Number of discrete points along the string

length = 0.65          # String length (m)
rho = 8000             # Density (kg/m³)
radius = 0.24 / 2.0    # String radius (m)
tension = 149          # Tension (N)
c = 0.0                # Wave speed
mu = 0.0               # Linear mass density (kg/m)

t_end = 0.02           # Total simulation time (20 ms)
frequency = 247        # Fundamental frequency (Hz)
beta = 1.0 / 5.0       # Plucking position ratio (1/5 or 1/20)
amplitude = 0.005      # Initial pluck amplitude (m)
n_pluck = 0            # Index of pluck location
n_smooth = 0           # Use > 0 for smoothed pluck (e.g., 3)

t_plot = 0.001         # Time between plot snapshots (1 ms)
y_string_file = "y_string."


def init():
    global t, dx, dt, c, mu, tension, n_pluck, t_plot, r2
    t = 0.0
    r2 = 1.0

    c = 2 * length * frequency
    mu = PI * radius**2 * rho
    tension = c**2 * mu

    dx = length / n_string
    dt = np.sqrt(r2 * dx**2 / c**2)
    n_pluck = int(beta * n_string)

    init_string()
    smooth_string()


def init_string():
    amp = amplitude
    slope = amp / (n_pluck * dx)
    for i in range(n_pluck + 1):
        y[i] = y_old[i] = i * dx * slope
    slope = amp / ((n_string - n_pluck) * dx)
    for i in range(n_pluck, n_string + 1):
        y[i] = y_old[i] = amp - (i - n_pluck) * dx * slope


def save_y(n):
    offset = amplitude * n / 10
    filename = f"{y_string_file}{n}"
    with open(filename, "w") as fp:
        for i in range(n_string + 1):
            fp.write(f"{i * dx:.6f}\t{y[i] - offset:.6f}\n")


def smooth_string():
    global y
    if n_smooth < 1:
        return
    y_smoothed = np.copy(y)
    for j in range(n_smooth, n_string - n_smooth):
        val = 0.0
        for i in range(-n_smooth, n_smooth + 1):
            val += y[j + i]
        y_smoothed[j] = val / (2 * n_smooth + 1)
    y = y_smoothed


def pluck():
    global t
    t_next_plot = t_plot
    i_plot = 1

    with open("bridge_f", "w") as fp_force:
        while t < t_end:
            for i in range(1, n_string):
                y_new[i] = 2 * y[i] - y_old[i] + r2 * (y[i + 1] + y[i - 1] - 2.0 * y[i])
            for i in range(n_string + 1):
                y_old[i] = y[i]
                y[i] = y_new[i]

            # Save bridge force (proportional to derivative at x = 0)
            fp_force.write(f"{tension * (y[1] - y[0]) / dx:.6f}\t{t:.6f}\n")

            t += dt
            t_next_plot -= dt
            if t_next_plot < 0.0:
                save_y(i_plot)
                i_plot += 1
                t_next_plot = t_plot


def main():
    init()
    save_y(0)
    pluck()


if __name__ == "__main__":
    main()
