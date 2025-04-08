import numpy as np

# Constants and simulation parameters
MAX = 3001
PI = 3.14159

# Global arrays for string displacement
y_new = np.zeros(MAX)
y = np.zeros(MAX)
y_old = np.zeros(MAX)

# Time and space parameters
t = 0.0
dt = dx = r2 = 0.0
num_points = 300

# Physical properties of the string
length = 0.65            # string length (meters)
density = 8000           # material density (kg/m^3)
radius = 0.24 / 2.0      # string radius (meters)
tension = 149            # string tension (Newtons)
wave_speed = 0.0         # wave propagation speed
mass_per_length = 0.0    # linear mass density (kg/m)

# Simulation timing
t_end = 0.0
frequency = 247          # vibration frequency (Hz)
pluck_position_ratio = 0.2
amplitude = 0.002        # initial pluck amplitude (meters)
pluck_index = 0
smoothing_level = 0

t_plot = 0.0
output_file_prefix = "y_string."


def initialize():
    global t, dx, dt, wave_speed, mass_per_length, tension
    global pluck_index, t_plot, t_end, r2

    t = 0.0
    r2 = 0.9

    wave_speed = 2 * length * frequency
    mass_per_length = PI * radius * radius * density
    tension = wave_speed * wave_speed * mass_per_length

    dx = length / num_points
    dt = np.sqrt(r2 * dx * dx / (wave_speed * wave_speed))
    period = 1.0 / frequency
    pluck_index = int(pluck_position_ratio * num_points)

    t_plot = 0.05 / frequency
    t_end = 10 * period

    initialize_string_shape()


def initialize_string_shape():
    amp = amplitude
    # Rising slope
    slope = amp / (pluck_index * dx)
    for i in range(pluck_index + 1):
        y[i] = y_old[i] = i * dx * slope
    # Falling slope
    slope = amp / ((num_points - pluck_index) * dx)
    for i in range(pluck_index, num_points + 1):
        y[i] = y_old[i] = amp - (i - pluck_index) * dx * slope


def save_displacement(n):
    offset = amplitude * n / 10
    filename = f"{output_file_prefix}{n}"
    with open(filename, "w") as file:
        for i in range(num_points + 1):
            file.write(f"{i * dx:.6f}\t{y[i] - offset:.6f}\n")


def smooth_string():
    global y
    if smoothing_level < 1:
        return
    y_smoothed = np.copy(y)
    for j in range(smoothing_level, num_points - smoothing_level):
        value = 0.0
        for i in range(-smoothing_level, smoothing_level + 1):
            value += y[j + i]
        y_smoothed[j] = value / (2 * smoothing_level + 1)
    y = y_smoothed


def simulate_pluck():
    global t
    t_next_plot = t_plot
    plot_index = 1

    with open("bridge_force", "w") as force_file:
        while t < t_end:
            for i in range(1, num_points):
                y_new[i] = (
                    2 * y[i]
                    - y_old[i]
                    + r2 * (y[i + 1] + y[i - 1] - 2.0 * y[i])
                )
            for i in range(num_points + 1):
                y_old[i] = y[i]
                y[i] = y_new[i]
            force_file.write(f"{tension * (y[1] - y[0]):.6f}\t{t:.6f}\n")

            t += dt
            t_next_plot -= dt
            if t_next_plot < 0.0:
                save_displacement(plot_index)
                plot_index += 1
                t_next_plot = t_plot


def main():
    initialize()
    save_displacement(0)
    simulate_pluck()


if __name__ == "__main__":
    main()
