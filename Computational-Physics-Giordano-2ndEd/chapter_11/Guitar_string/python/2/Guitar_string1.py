import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
import matplotlib.animation as animation

# ------------------------
# Helper: ordinal suffix (1st, 2nd, 3rd, etc.)
# ------------------------

def ordinal_suffix(n):
    if 10 <= n % 100 <= 20:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


# ------------------------
# 1. Analyze bridge_force file
# ------------------------

def analyze_bridge_force(filename="bridge_force"):
    data = np.loadtxt(filename)
    force = data[:, 0]
    time = data[:, 1]

    # Force vs Time plot
    plt.figure()
    plt.plot(time, force)
    plt.title("Bridge Force Over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Force (N)")
    plt.grid()
    plt.savefig("bridge_force_time.png")
    plt.show()

    # Frequency analysis (FFT)
    n = len(force)
    dt = time[1] - time[0]
    freq = fftfreq(n, dt)
    fft_vals = np.abs(fft(force))

    # Find peaks in FFT
    peaks, _ = find_peaks(fft_vals[:n // 2], height=1e3)
    peak_freqs = freq[peaks]
    peak_amps = fft_vals[peaks]

    # Get top N peaks
    N = 5
    top_indices = np.argsort(peak_amps)[-N:][::-1]
    top_freqs = peak_freqs[top_indices]

    # Plot FFT and highlight harmonics
    plt.figure()
    plt.plot(freq[:n // 2], fft_vals[:n // 2])
    plt.title("Frequency Spectrum of Bridge Force")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.xlim(0, 5000)

    for i, f in enumerate(top_freqs):
        plt.axvline(x=f, color='red', linestyle='--')
        label = f"{i+1}{ordinal_suffix(i+1)} Harmonic\n{f:.2f} Hz"
        plt.text(f, max(fft_vals) * 0.6, label, rotation=90,
                 color='red', ha='right', va='bottom', fontsize=8)

    plt.savefig("bridge_force_fft.png")
    plt.show()

    print("✅ Plots saved: bridge_force_time.png and bridge_force_fft.png")


# ------------------------
# 2. Animate y_string.* files
# ------------------------

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
    ax.set_xlabel("Position along string (m)")
    ax.set_ylabel("Displacement (m)")

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        x = data[frame][:, 0]
        y = data[frame][:, 1]
        line.set_data(x, y)
        return line,

    ani = animation.FuncAnimation(
        fig, update, frames=len(data),
        init_func=init, blit=True, interval=50
    )

    if save_as_mp4:
        writer = animation.FFMpegWriter(fps=10, bitrate=1800)
        ani.save("string_vibration.mp4", writer=writer)
        print("🎞 Animation saved: string_vibration.mp4")

    plt.show()


# ------------------------
# Run all analyses
# ------------------------

def main():
    if os.path.exists("bridge_force"):
        analyze_bridge_force()
    else:
        print("⛔ File 'bridge_force' not found.")

    if glob.glob("y_string.*"):
        animate_string()
    else:
        print("⛔ No 'y_string.*' files found.")


if __name__ == "__main__":
    main()
