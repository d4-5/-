import json
from math import cos, sin, pi


def load_coefficients(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)

    coefficients = [(coeff['A'], coeff['B']) for coeff in data['coefficients']]

    return coefficients


def calculate_signal(coefficients):
    extend_coefficients = []
    for i in range(len(coefficients) - 2, 0, -1):
        A, B = coefficients[i]
        extend_coefficients.append((A, -B))
    coefficients.extend(extend_coefficients)

    signal = []
    for i in range(len(coefficients)):
        s = 0
        for k, (A, B) in enumerate(coefficients):
            angle = 2 * pi * k * i / len(coefficients)
            s += A * cos(angle) + B * sin(angle)

        s = (abs(round(s, 1)))
        signal.append(s)

    return signal


def main():
    filename = "coefficients.json"
    coefficients = load_coefficients(filename)

    for i, (A, B) in enumerate(coefficients):
        print(f"C{i} = {A} + i*{B}")

    signal = calculate_signal(coefficients)
    print("Signal:")
    for s in signal:
        print(s)


if __name__ == "__main__":
    main()
