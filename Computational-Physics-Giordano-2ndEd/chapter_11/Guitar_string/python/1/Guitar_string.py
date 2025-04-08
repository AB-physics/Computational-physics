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
n_string = 100

length = 0.65
rho = 8000
radius = 0.24 / 2.0
tension = 149
c = 0.0
mu = 0.0

t_end = 0.0
frequency = 247
beta = 1.0 / 5.0
amplitude = 0.005
n_pluck = 0
n_smooth = 0

t_plot = 0.0
y_string_file = "y_string."


def init():
    global t, dx, dt, c, mu, tension, n_pluck, t_plot, t_end, r2
    t = 0.0
    r2 = 1.0

    c = 2 * length * frequency
    mu = PI * radius * radius * rho
    tension = c * c * mu

    dx = length / n_string
    dt = np.sqrt(r2 * dx * dx / (c * c))
    period = 1.0 / frequency
    n_pluck = int(beta * n_string)

    t_plot = 0.05 / frequency
    t_end = 1 * period

    init_string()


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
    name = f"{y_string_file}{n}"
    with open(name, "w") as fp:
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
            fp_force.write(f"{tension * (y[1] - y[0]):.6f}\t{t:.6f}\n")

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
