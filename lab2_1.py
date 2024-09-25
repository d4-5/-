import random
from math import cos, sin, pi, sqrt, atan
import matplotlib.pyplot as plt
import time
from datetime import datetime

N = 10 + 5


def generate_signal():
    random.seed(datetime.now().timestamp())
    signal = []
    for _ in range(N):
        signal.append(random.random())

    return signal


def calculate_coefficients(k, i, fi):
    return fi*cos(2*pi*k*i/N), fi*sin(2*pi*k*i/N)


def calculate_series(k, signal):
    A = 0
    B = 0
    for i in range(N):
        a, b = calculate_coefficients(k, i, signal[i])
        A += a
        B += b
    A = 1/N * A
    B = 1/N * B
    return A, B, 2*(4*N + N + 1)


def plot_graphs(amplitudes, phases):
    plt.figure(figsize=(10, 6))
    plt.stem(range(N), amplitudes, "b", markerfmt="bo",
             basefmt=" ", label="|C_k|")
    plt.title("Спектр амплітуд")
    plt.xlabel("k")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.stem(range(N), phases, "b", markerfmt="bo",
             basefmt=" ", label="arg(C_k)")
    plt.title("Спектр фаз")
    plt.xlabel("k")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    signal = generate_signal()
    results = []
    start = time.time()

    for k in range(N):
        results.append(calculate_series(k, signal))

    end = time.time()
    print(f"Час обчислення: {end - start}")

    amplitudes = []
    phases = []
    operations = 0

    for A, B, op in results:
        operations += op
        C = sqrt(A**2 + B**2)/2
        phi = atan(B/A)
        amplitudes.append(C)
        phases.append(phi)

    print(f"Кількість операцій множення і додавання: {operations}")
    plot_graphs(amplitudes, phases)


if __name__ == "__main__":
    main()
