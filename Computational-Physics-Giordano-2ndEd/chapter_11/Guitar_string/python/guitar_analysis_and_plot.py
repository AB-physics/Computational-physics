import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.fft import fft, fftfreq
import matplotlib.animation as animation

def analyze_bridge_force(filename="bridge_f", beta=1/5, frequency=247):
    data = np.loadtxt(filename)
    force = data[:, 0]
    time = data[:, 1]

    # Normalize and rescale for time-domain plot (to match the book figure)
    force_norm = force / np.max(np.abs(force))
    force_norm *= 1.65
    force_norm += 0.1

    # Plot: Force on bridge vs time
    plt.figure()
    plt.plot(time * 1000, force_norm)
    plt.title("Force on Bridge vs Time")
    plt.xlabel("Time (ms)")
    plt.ylabel("Bridge Force (arb units)")
    plt.ylim(-1.1, 2.3)
    plt.grid()
    plt.savefig("bridge_force_time_scaled.png")
    plt.show()

    # Power Spectrum (normalized)
    n = len(force)
    dt = time[1] - time[0]
    freq = fftfreq(n, dt)
    fft_vals = np.abs(fft(force))**2
    fft_vals /= np.max(fft_vals)
    fft_vals *= 15  # scale max to 15 like the book

    if beta == 1/5:
        max_freq = 2000
        f_label = 5 * frequency
    elif beta == 1/20:
        max_freq = 6000
        f_label = 20 * frequency
    else:
        max_freq = 8000
        f_label = int(1 / beta) * frequency

    # Plot: Frequency Spectrum
    plt.figure()
    plt.plot(freq[:n // 2], fft_vals[:n // 2])
    plt.xlim(0, max_freq)
    plt.ylim(0, 15)
    plt.title(f"Guitar Spectrum – Pluck at 1/{int(1 / beta)}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Bridge Power (arb units)")
    plt.axvline(x=f_label, color='gray', linestyle='--')
    plt.text(f_label + 30, max(fft_vals) / 10, f"{int(1 / beta)} × f₁", rotation=90)
    plt.grid()
    plt.savefig("bridge_force_fft_clean.png")
    plt.show()

    print("✅ Figures saved: bridge_force_time_scaled.png and bridge_force_fft_clean.png")


def animate_string(pattern="y_string.*", save_as_mp4=True):
    files = sorted(glob.glob(pattern), key=lambda f: int(f.split('.')[-1]))
    data = [np.loadtxt(f) for f in files]

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_xlim(0, data[0][-1, 0])
    y_min = min([np.min(d[:, 1]) for d in data])
    y_max = max([np.max(d[:, 1]) for d in data])
    ax.set_ylim(y_min, y_max)
    ax.set_title("String Vibration Animation")
    ax.set_xlabel("Position Along String (m)")
    ax.set_ylabel("Displacement (m)")

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        x = data[frame][:, 0]
        y = data[frame][:, 1]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(fig, update, frames=len(data),
                                  init_func=init, blit=True, interval=50)

    if save_as_mp4:
        writer = animation.FFMpegWriter(fps=10, bitrate=1800)
        ani.save("string_vibration.mp4", writer=writer)
        print("🎞 Animation saved: string_vibration.mp4")

    plt.show()


def main():
    if os.path.exists("bridge_f"):
        analyze_bridge_force(beta=1/5)  # Or beta=1/20 for the second spectrum
    else:
        print("⛔ File 'bridge_f' not found.")

    if glob.glob("y_string.*"):
        animate_string()
    else:
        print("⛔ No 'y_string.*' files found.")


if __name__ == "__main__":
    main()
