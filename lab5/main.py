import numpy as np
import time

def timecounter(func):
    def wrapper(*args, **kwargs):
        start_time = time.time() 
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        print(f"Час виконання: {elapsed:.6f} с\n")
        return result
    return wrapper

class Matrix:
    def __init__(self, data):
        self.data = np.array(data, dtype=float)
        self.rows, self.cols = self.data.shape
        self._iter_index = 0

    @classmethod 
    def input(cls, name=""):
        n, m = map(int, input(f"Введіть розміри матриці {name} (n m): ").split())
        print(f"Введіть {n} рядків по {m} чисел:")
        data = [list(map(float, input().split())) for _ in range(n)]
        return cls(data)

    def __add__(self, other):
        return Matrix(self.data + other.data)
    def __sub__(self, other):
        return Matrix(self.data - other.data)
    def __matmul__(self, other):
        return Matrix(self.data @ other.data)  
    @property
    def T(self):
        return Matrix(self.data.T)          

    def __iter__(self):         
        for r in self.data:
            for x in r:
                yield float(x)

    def __str__(self):          
        return str(self.data)

    @timecounter
    def inverse(self):
        try:
            inv = np.linalg.inv(self.data)
            print("Обернена матриця:\n", inv)
            return Matrix(inv)
        except np.linalg.LinAlgError:
            print("Матриця не є оборотною.")
            return None

    @timecounter
    def solve(self, b):
        try:
            b = np.array(b, dtype=float)
            x = np.linalg.solve(self.data, b)
            print("Розв’язок x:\n", x)
            return x
        except np.linalg.LinAlgError:
            print("Неможливо розв’язати систему.")
            return None

    @timecounter
    def vlasnui(self):
        vals, vecs = np.linalg.eig(self.data)
        print("Власні значення:\n", vals)
        print("Власні вектори:\n", vecs)
        return vals, vecs

    @timecounter
    def norm(self):
        val = np.linalg.norm(self.data)
        print("Норма матриці:", val)
        return val

    def transp(self):
        return Matrix(self.data.T)

    def spiral(self):
        a = self.data.copy()
        while a.size:
            for x in a[0]:
                yield float(x)
            a = a[1:].T[::-1]
    def rev_spiral(self):
        a = self.data.copy()
        while a.size:
            for x in a[-1][::-1]:
                yield float(x)
            a = a[:-1].T

def read_vector(n):
    print(f"Введіть вектор з {n} елементів:")
    return list(map(float, input().split()))

def main():
    A = Matrix.input("A")
    B = Matrix.input("B")

    mn = """
1.A + B
2.A - B
3.A * B  (матричне множення)
4.A^T (транспонування)
5.B^T (транспонування)
6.обернена(A) - A^(-1)
7.обернена(B) - B^(-1)
8.Розв’язати A·x = b
9.Власні значення/вектори A
10.Норма A
11.Послідовний обхід A
12.Спіральний обхід A
13.Послідовний обхід B
14.Спіральний обхід B
0.Вихід
"""
    while True:
        print(mn)
        choice = input("Оберіть пункт: ").strip()

        if choice == "1":
            print("A + B =\n", A + B)
        elif choice == "2":
            print("A - B =\n", A - B)
        elif choice == "3":
            print("A * B =\n", A @ B)
        elif choice == "4":
            print("~A =\n", A.T)
        elif choice == "5":
            print("~B =\n", B.T)
        elif choice == "6":
            A.inverse()
        elif choice == "7":
            B.inverse()
        elif choice == "8":
            b = read_vector(A.rows)
            A.solve(b)
        elif choice == "9":
            A.vlasnui()
        elif choice == "10":
            A.norm()
        elif choice == "11":
            print("Елементи A послідовно:", list(A))
        elif choice == "12":
            print("Елементи A по спіралі:", list(A.spiral()))
        elif choice == "13":
            print("Елементи B послідовно:", list(B))
        elif choice == "14":
            print("Елементи B по спіралі:", list(B.spiral()))
        elif choice == "0":
            print("Вихід.")
            break
        else:
            print("Невірний вибір.")

if __name__ == "__main__":
    main()
