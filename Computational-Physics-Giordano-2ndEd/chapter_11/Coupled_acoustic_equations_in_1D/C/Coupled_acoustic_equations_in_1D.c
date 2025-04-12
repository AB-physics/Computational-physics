/*
 *  sound.c
 *  Ahmad Biglar    April 12, 2025
 *
 *  Solve the coupled acoustic equations for velocity (v) and pressure (p) in a 1D geometry.
 *
 *  Drive one end as a piston and use a real acoustic impedance Z = p/v at the other end.
 *
 *  Use staggered grids in space and time (see book for details).
 *
 *  Spatial grid:
 *  0   1/2   1   3/2   .....    N-1   N-1/2   N
 *  p    v    p    v                      p     v      p
 *  wall                                            wall
 *
 *  For the arrays containing v: v[1] = v[1/2], etc.
 *
 *  Time stepping:
 *  Update first p, then v, then p, etc.
 *
 *  Functions:
 *  - init(): Initialize variables (c = speed of sound, rho = density of air, length = length of pipe,
 *            n_wall = number of spatial units along pipe, Z = acoustic impedance of wall).
 *  - v_speaker(): Define the velocity at the speaker wall (piston).
 *  - propagate(): Solve the acoustic equations and output pressure at the wall and velocity at a specific point.
 *
 *  The program is currently configured to perform a calculation at a single frequency and record the pressure
 *  at the wall and the air velocity as a function of time.
 *
 *  It also contains (commented) routines to scan the frequency and look at resonant behavior when the frequency
 *  passes through the resonant frequency of the pipe.
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>  // Added for srand

#define MAX 3001
#define PI  3.14159

// Function declarations
double v_speaker(double t);  // Velocity at the speaker wall
double propagate();          // Main propagation function
void init();                 // Initialization function (added declaration)

double v[MAX], v_old[MAX];   // Arrays for velocity and its previous values
double p[MAX], p_old[MAX];   // Arrays for pressure and its previous values

double length, dx, dt;       // Length of pipe, spatial step, time step
int n_wall;                  // Number of spatial units along pipe
double rho, c;               // Density of air, speed of sound
double Z;                    // Acoustic impedance of wall

double t_end;                // End time of simulation
double t_start_meas;         // Time to start measuring

double f_start, f_end, df;   // Frequency range for scanning (start, end, step)
double f_current;            // Current frequency

double v_0, frequency;       // Amplitude and frequency of the piston
double t_speaker_off;        // Time to turn off the speaker
double rand_max;             // Maximum value for random number generation

int main()  // Changed to int main() for standard compliance
{
    double pressure;
    FILE *fp_v_max;

    init();      // Initialize variables
    propagate(); // Run the simulation

    /*
    fp_v_max = fopen("v_2_freq", "w");
    f_current = f_start;
    while (f_current <= f_end) {
        pressure = propagate();
        fprintf(fp_v_max, "%g\t%g\n", f_current, pressure);
        f_current += df;
    }
    fclose(fp_v_max);
    */

    return 0;  // Added return statement for main
}

void init()  // Changed to void since it doesn't return anything
{
    int i;

    length = 1.0;                    // Length of the pipe (m)
    rho = 1.3;                       // Density of air (kg/m^3)
    c = 330;                         // Speed of sound (m/s)
    n_wall = 100;                    // Number of spatial grid points
    dx = length / n_wall;            // Spatial step size
    dt = dx / c;                     // Time step size (satisfies Courant condition)

    Z = 100;                         // Acoustic impedance (initially set to 100, but changed to 6e3)
    Z = 6e3;                         // Final impedance value
    v_0 = 1e-3;                      // Amplitude of piston velocity
    frequency = c / length;          // Fundamental resonant frequency of the pipe
    rand_max = pow(2.0, 31.0) - 1.0;// Max value for random number generation

    t_end = 200 / frequency;         // Total simulation time
    t_start_meas = t_end / 2;        // Start measuring after half the simulation time
    t_speaker_off = t_end;           // Time to turn off the speaker

    // Initialize pressure and velocity arrays to zero
    for (i = 0; i <= n_wall; i++) {
        p[i] = p_old[i] = 0.0;
        v[i] = v_old[i] = 0.0;
    }

    f_start = frequency / 4;         // Start frequency for scanning
    f_end = 1.8 * frequency;         // End frequency for scanning
    df = (f_end - f_start) / 60;     // Frequency step

    f_current = frequency / 4;       // Initial frequency for simulation

    srand(32);                       // Seed for random number generation
}

double v_speaker(double t)
{
    double val;

    if (t < t_speaker_off) {
        val = v_0 * sin(2 * PI * f_current * t); // Sinusoidal velocity of the piston

        /* Want to add a white noise generator eventually */
        /* val = v_0 * (0.5 - rand() / rand_max); */
    }
    else {
        val = 0.0;  // Turn off the speaker after t_speaker_off
    }

    return val;
}

double propagate()
{
    int i, n_v;
    double t, p_tmp, v_tmp, a1, a2;
    FILE *fp_p_wall, *fp_v;
    double p_max, v_max_2, tmp;

    fp_p_wall = fopen("p_wall", "w");  // File to record pressure at the far wall
    fp_v = fopen("v_signal", "w");     // File to record velocity at a specific point
    n_v = n_wall / 2.5;                // Position to record velocity

    a1 = 1.0 - Z * dt / (rho * dx);    // Coefficients for impedance boundary condition
    a2 = 1.0 + Z * dt / (rho * dx);
    p_tmp = rho * c * c * dt / dx;     // Coefficient for pressure update
    v_tmp = dt / (rho * dx);           // Coefficient for velocity update
    t = 0;

    p_max = v_max_2 = 0.0;
    while (t < t_end) {
        fprintf(fp_p_wall, "%g\t%g\n", t, p[n_wall-1]); // Write pressure at the wall
        fprintf(fp_v, "%g\t%g\n", t, v[n_v]);          // Write velocity at position n_v

        if (p[n_wall-1] > p_max) p_max = p[n_wall-1];  // Track maximum pressure

        // Update pressure (interior points only)
        for (i = 1; i < n_wall; i++) {
            p[i] += -p_tmp * (v[i] - v[i-1]);
        }

        // Update velocity (interior points)
        for (i = 1; i < n_wall - 1; i++) {
            v[i] += -v_tmp * (p[i+1] - p[i]);
        }
        v[0] = v_speaker(t);  // Boundary condition at the piston
        v[n_wall-1] += (a1 / a2) * v[n_wall-1] + p[n_wall-1] * 2 * dt / (rho * dx * a2); // Impedance boundary

        // Measure velocity magnitude after t_start_meas
        if (t > t_start_meas) {
            tmp = 0.0;
            for (i = 1; i < n_wall - 1; i++) {
                tmp += v[i] * v[i];
            }
            if (tmp > v_max_2) v_max_2 = tmp;
        }

        t += dt;  // Increment time
    }

    fclose(fp_p_wall);
    fclose(fp_v);

    return v_max_2;  // Return the maximum velocity squared
}  // Added closing brace
