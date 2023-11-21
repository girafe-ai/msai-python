from .complex import Complex  # noqa: F401


def main():
    import pandas as pd

    complex1 = Complex(1, 2)
    complex2 = Complex(3, 4)
    print(complex1 + complex2)


if __name__ == "__main__":
    main()
