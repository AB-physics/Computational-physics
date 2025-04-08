#include <math.h>
#include <stdio.h>

#define MAX 3001
#define PI 3.14159
#define ON 0
#define OFF 1

// «⁄·«‰  «»⁄ùÂ«
void init();
void pluck();
void init_string();
void save_y(int n);
void smooth_string();

double y_new[MAX], y[MAX], y_old[MAX];
double t, dt, dx;
double r2; // r2 = c^2 dt^2 / dx^2
int n_string;
double length, c, tension, density, radius;
double rho, mu;

double t_end;
double frequency;
double beta;
int n_pluck, n_smooth;
double amplitude;

double t_plot;
char y_string_file[100];

// »—‰«„Â «’·Ì
int main()
{
    init();
    save_y(0);
    pluck();
    return 0;
}

void pluck()
{
    int i;
    double t_next_plot;
    int i_plot;
    FILE *fp_force;

    fp_force = fopen("bridge_f", "w");

    t_next_plot = t_plot;
    i_plot = 1;

    while (t < t_end)
    {
        // propagate string
        for (i = 1; i < n_string; i++)
        {
            y_new[i] = 2 * y[i] - y_old[i] +
                       r2 * (y[i + 1] + y[i - 1] - 2.0 * y[i]);
        }

        // update profiles
        for (i = 0; i <= n_string; i++)
        {
            y_old[i] = y[i];
            y[i] = y_new[i];
        }

        // –ŒÌ—Â ‰Ì—ÊÌ Å· (” Ê‰ «Ê·: ‰Ì—Ê° ” Ê‰ œÊ„: “„«‰)
        fprintf(fp_force, "%g\t%g\n", tension * (y[1] - y[0]), t);

        t += dt;
        t_next_plot -= dt;
        if (t_next_plot < 0.0)
        {
            save_y(i_plot);
            ++i_plot;
            t_next_plot = t_plot;
        }
    }

    fclose(fp_force);
}

void init()
{
    double period;

    t = 0.0;
    n_string = 100;

    length = 0.65;
    rho = 8000;
    radius = 0.24 / 2.0;
    tension = 149;
    r2 = 1.0;
    frequency = 247;
    beta = 1.0 / 5.0;
    amplitude = 0.005;

    c = 2 * length * frequency;
    mu = PI * radius * radius * rho;
    tension = c * c * mu;

    sprintf(y_string_file, "y_string.");

    dx = length / n_string;
    dt = sqrt(r2 * dx * dx / (c * c));
    period = 1.0 / frequency;
    n_pluck = beta * n_string;

    t_plot = 0.05 / frequency;
    t_end = 1 * period;

    init_string();
}

void init_string()
{
    int i;
    double amp;
    double slope;

    amp = amplitude;

    slope = amp / (n_pluck * dx);
    for (i = 0; i <= n_pluck; i++)
    {
        y[i] = y_old[i] = i * dx * slope;
    }

    slope = amp / ((n_string - n_pluck) * dx);
    for (i = n_pluck; i <= n_string; i++)
    {
        y[i] = y_old[i] = amp - (i - n_pluck) * dx * slope;
    }
}

void save_y(int n)
{
    FILE *fp;
    char name[100];
    int i;
    double offset;

    offset = amplitude * n / 10;

    sprintf(name, "%s%d", y_string_file, n);
    fp = fopen(name, "w");
    for (i = 0; i <= n_string; i++)
    {
        fprintf(fp, "%g\t%g\n", i * dx, y[i] - offset);
    }
    fclose(fp);
}

void smooth_string()
{
    int i, j, n;
    double val;

    for (j = n_smooth; j < n_string - n_smooth; j++)
    {
        val = 0.0;
        n = 0;
        for (i = -n_smooth; i <= n_smooth; i++)
        {
            val += y[j + i];
            ++n;
        }
        y[j] = val / n;
    }
}

