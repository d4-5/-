from math import sin, cos, pi
import matplotlib.pyplot as plt
import numpy as np


def f(x):
    y = 5*sin(pi*5*x)
    return y


def get_coefficients(n):
    a = -10*(2*n*sin(5*pi**2)*sin(2*pi*n) + 5*pi*cos(5*pi**2)
             * cos(2*pi*n) - 5*pi)/(25*pi**3 - 4*pi*n**2)
    if n == 0:
        return a

    b = 5*(sin(pi*(5*pi-2*n))/(5*pi - 2*n) -
           sin(pi*(2*n + 5*pi))/(2*n + 5*pi))/pi

    return a, b


def fourier(x, n):
    a_0 = get_coefficients(0)
    f = a_0/2

    for i in range(1, n + 1):
        a_n, b_n = get_coefficients(i)
        f += a_n*cos(2*i*x) + b_n*sin(2*i*x)

    return f


def relative_error(n):
    x = np.linspace(0.1, 0.15, 1000)
    return sum(abs(f(val) - fourier(val, n)) / (abs(f(val))) for val in x) / 1000


def absolute_error(n):
    x = np.linspace(0, pi, 1000)
    return sum(abs(f(val) - fourier(val, n)) for val in x) / 1000


def save_to_file(n):
    with open("save.txt", "w") as file:
        file.write(f"Порядок n: {n}\n")
        file.write("Коефіцієнти:\n")
        a_0 = get_coefficients(0)
        file.write(f"a_0 = {a_0:.6f}\n")
        for k in range(1, n + 1):
            a_n, b_n = get_coefficients(k)
            file.write(f"a_{k} = {a_n:.6f}, b_{k} = {b_n:.6f}\n")
        r_error = relative_error(n)
        a_error = absolute_error(n)
        file.write(f"Відносна похибка наближення: {r_error:.6f}\n")
        file.write(f"Абсолютна похибка наближення: {a_error:.6f}\n")


def plot_harmonics(n):
    x = np.linspace(0, pi, 1000)

    plt.figure(figsize=(14, 10))
    a0 = get_coefficients(0)
    harmonic = [a0/2 for _ in x]
    plt.plot(x, harmonic, label="Грамоніка 0")

    for k in range(1, n + 1):
        a_n, b_n = get_coefficients(k)
        harmonic = [a_n*cos(k*val) + b_n*sin(k*val) for val in x]
        plt.plot(x, harmonic, label=f"Грамоніка {k}")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_spectrum():
    a_coefficients = []
    b_coefficients = []
    ks = list(range(11))

    for k in ks:
        if k == 0:
            a_k = get_coefficients(k)
            b_k = 0
        else:
            a_k, b_k = get_coefficients(k)
        a_coefficients.append(abs(a_k))
        b_coefficients.append(abs(b_k))

    plt.figure(figsize=(10, 6))
    plt.stem(ks, a_coefficients, "b", markerfmt="bo",
             basefmt=" ", label="|a_n|")
    plt.stem(ks[1:], b_coefficients[1:], "r",
             markerfmt="ro", basefmt=" ", label="|b_n|")
    plt.title("Частотний спектр коефіцієнтів Фур'є")
    plt.xlabel("n")
    plt.ylabel("Амплітуда")
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_fourier(n):
    x = np.linspace(0, pi, 1000)
    y_original = [f(val) for val in x]
    y_fourier = [fourier(val, n) for val in x]

    plt.figure(figsize=(10, 6))
    plt.plot(x, y_original, label="5sin(5πx)")
    plt.plot(x, y_fourier, label=f"Ряд Фур'є порядку {
             n}", color="orange", lw=1)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    n = 10
    save_to_file(n)
    plot_harmonics(n)
    plot_spectrum()
    plot_fourier(n)


if __name__ == "__main__":
    main()
