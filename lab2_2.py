from math import cos, sin, pi, sqrt, atan2
import numpy as np
import matplotlib.pyplot as plt
import json


def calculate_coefficients(signal):
    N = len(signal)
    coefficients = []
    A0 = 1/N * sum(signal[i] for i in range(N))
    B0 = 0
    coefficients.append((A0, B0))
    for k in range(1, N//2 + 1):
        A = 1/N * sum(signal[i]*cos(2*pi*k*i/N) for i in range(N))
        B = 1/N * sum(signal[i]*sin(2*pi*k*i/N) for i in range(N))
        coefficients.append((A, B))
    return coefficients


def calculate_phases_and_amplitudes(coefficients):
    amplitudes = []
    phases = []

    for A, B in coefficients:
        C = sqrt(A**2 + B**2)
        phi = atan2(B, A)

        amplitudes.append(C)
        phases.append(phi)

    return amplitudes, phases


def plot_amplitudes_and_phases(amplitudes, phases):
    plt.figure(figsize=(10, 6))
    plt.stem(range(len(amplitudes)), amplitudes, "b", markerfmt="bo",
             basefmt=" ", label="|C_k|")
    plt.title("Спектр амплітуд")
    plt.xlabel("k")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.stem(range(len(phases)), phases, "b", markerfmt="bo",
             basefmt=" ", label="arg(C_k)")
    plt.title("Спектр фаз")
    plt.xlabel("k")
    plt.ylabel("Фаза")
    plt.grid(True)
    plt.legend()
    plt.show()


def s(t, amplitudes, phases, Tc):
    extend_amplitudes = []
    extend_phases = []

    for i in range(len(amplitudes) - 2, 0, -1):
        a = amplitudes[i]
        p = phases[i]
        extend_amplitudes.append(a)
        extend_phases.append(-p)
    new_amplitudes = amplitudes.copy()
    new_phases = phases.copy()
    new_amplitudes.extend(extend_amplitudes)
    new_phases.extend(extend_phases)

    s = 0
    for i in range(len(new_amplitudes)):
        s += new_amplitudes[i]*cos(2*pi*i*t - new_phases[i])
    return s


def plot_signal(amplitudes, phases, Tc):
    t_values = np.linspace(0, Tc, 500)

    s_values = [s(t, amplitudes, phases, Tc) for t in t_values]

    plt.figure(figsize=(10, 6))
    plt.plot(t_values, s_values, label="s(t)")
    plt.title("Plot of the function s(t)")
    plt.xlabel("Time t")
    plt.ylabel("s(t)")
    plt.grid(True)
    plt.legend()
    plt.show()


def print_table_and_formula(amplitudes, phases, Tc):
    t_values = np.linspace(0, Tc, 9)
    s_values = [s(t, amplitudes, phases, Tc) for t in t_values]

    for i in t_values:
        print(f"{i:.5f} | ", end="")
    print()
    for i in range(len(t_values)*10 - 1):
        print("-", end="")
    print()
    for i in s_values:
        print(f"{i:.5f} | ", end="")
    print()

    print(f"s(t) = {amplitudes[0]}", end="")
    for i in range(1, len(amplitudes) - 1):
        print(f" + 2*{amplitudes[i]:.4f}*cos({2 *
              i}*pi*t/Tc + {phases[i]:.4f})", end="")
    print(f" + {amplitudes[-1]}*cos({2 *
          (len(amplitudes) - 1)}*pi*t/Tc + {phases[-1]:.4f})")


def save_coefficients(coefficients, filename):
    data = {
        "coefficients": [{"A": A, "B": B} for A, B in coefficients]
    }

    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def main():
    Tc = 1
    n = 5
    N = 96 + n
    signal = list(bin(N)[2:])
    signal.insert(0, "1")
    for i in range(len(signal)):
        signal[i] = int(signal[i])

    print(f"Signal : {signal}")
    coefficients = calculate_coefficients(signal)
    for i, (A, B) in enumerate(coefficients):
        print(f"C{i} = {A} + i*{B}")
    amplitudes, phases = calculate_phases_and_amplitudes(coefficients)
    print_table_and_formula(amplitudes, phases, Tc)
    plot_amplitudes_and_phases(amplitudes, phases)
    plot_signal(amplitudes, phases, Tc)
    save_coefficients(coefficients, "coefficients.json")


if __name__ == "__main__":
    main()
