from typing import Union,List
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import sympy as sp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Item(BaseModel):
    A: list
    b:list

def invertible_matrix(A):
    n = len(A)
    E = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        E[i][i] = 1

    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        E[i], E[max_row] = E[max_row], E[i]

        pivot = A[i][i]
        for k in range(i, n):
            A[i][k] /= pivot
        for k in range(n):
            E[i][k] /= pivot

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                for j in range(n):
                    E[k][j] -= factor * E[i][j]

    return E


@app.post("/gauss/")
def gaussian_elimination(item: Item):
    try:
        A = item.A
        b = item.b

        # Check for empty matrices
        if not A or not b or not A[0]:
            raise ValueError("Matrices must not be empty")

        n = len(A)

        # Check for square matrix
        if n != len(A[0]):
            raise ValueError("Matrix A must be square")

        for i in range(n):
            max_row = i
            for k in range(i + 1, n):
                if abs(A[k][i]) > abs(A[max_row][i]):
                    max_row = k
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]

            pivot = A[i][i]

            # Check for division by zero
            if pivot == 0:
                raise ValueError("Division by zero encountered")

            for k in range(i, n):
                A[i][k] /= pivot
            b[i] /= pivot

            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]

            for i in range(n):
                for j in range(n):
                    A[i][j] = round(A[i][j], 3)
                b[i] = round(b[i], 3)

        return b

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
        
@app.post("/simple-iterations/") 
def solve_iteration_method(item: Item):
    try:
        A = item.A
        b = item.b
        size = len(A)
        n = len(A[0])

        # Перевірка, чи вектор b має відповідну довжину
        if len(b) != size:
            raise ValueError("Invalid vector dimension")

        matrix = [[A[i][j] for j in range(n)] for i in range(size)]
        constants = b.copy()

        x = [0] * n  # Початкове наближення
        max_iterations = 1000  # Ліміт ітерацій, щоб уникнути безкінечного циклу
        tolerance = 1e-6  # Точність

        for _ in range(max_iterations):
            x_new = [0] * n
            for i in range(size):
                summation = sum(matrix[i][j] * x[j] for j in range(n))
                x_new[i] = summation + constants[i]

            # Перевірка на збіжність
            if all(abs(x_new[i] - x[i]) < tolerance for i in range(n)):
                break

            x = x_new.copy()

        x = [round(x[i], 4) for i in range(n)]

        return x

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for i in range(n):
        det += ((-1) ** i) * matrix[0][i] * determinant(minor(matrix, 0, i))

    return det

def minor(matrix, row, col):
    return [[matrix[i][j] for j in range(len(matrix[i])) if j != col] for i in range(len(matrix)) if i != row]

def cofactor(matrix):
    return [[((-1) ** (i + j)) * determinant(minor(matrix, i, j)) for j in range(len(matrix[i]))] for i in range(len(matrix))]

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def invertible_matrix(matrix):
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matrix is not invertible")

    cofactor_matrix = cofactor(matrix)
    adjugate_matrix = transpose(cofactor_matrix)

    inverse_matrix = [[adjugate_matrix[i][j] / det for j in range(len(adjugate_matrix[i]))] for i in range(len(adjugate_matrix))]

    return inverse_matrix


@app.post("/least-squares/") 
def least_squares_method(item: Item):
    try:
        A = item.A
        b = item.b
        size = len(A)
        size2 = len(A[0])

        matrix = [
            [float(A[i][j]) for j in range(size2)] for i in range(size)
        ]

        constants = [float(b[i]) for i in range(size)]

        if any(all(value == 0 for value in row) for row in matrix):
            raise HTTPException(status_code=400, detail="Матриця містить нулі. Спробуйте ще раз!")

        matrix_transpose = [[matrix[j][i] for j in range(size)] for i in range(size2)]

        matrix_transpose_by_matrix = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                for k in range(size2):
                    matrix_transpose_by_matrix[i][j] += matrix_transpose[i][k] * matrix[k][j]

        matrix_transpose_by_matrix_invertible = invertible_matrix(matrix_transpose_by_matrix)

        if not matrix_transpose_by_matrix_invertible:
            raise HTTPException(status_code=400, detail="Матриця не може бути оберненою. Спробуйте ще раз!")

        matrix_transpose_by_constants = [0 for _ in range(size)]
        for i in range(size):
            for j in range(size2):
                matrix_transpose_by_constants[i] += matrix_transpose[i][j] * constants[j]

        result = [0 for _ in range(size)]
        for i in range(size):
            for j in range(size):
                result[i] += matrix_transpose_by_matrix_invertible[i][j] * matrix_transpose_by_constants[j]

        result = [round(result[i], 7) for i in range(size)]

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class ChordModel(BaseModel):
    a: float
    b:float
    function:str


@app.post("/chord/") 
def solve_secant_method(chord:ChordModel):
    a = chord.a
    b = chord.b
    function = chord.function

    x = sp.symbols('x')
    fx = sp.sympify(function)

    def find_root(fx, a, b, eps):
        c = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float((float(fx.subs(x, b)) - float(fx.subs(x, a))))
        c1 = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float(
            (float(fx.subs(x, b)) - float(fx.subs(x, a)))) + 1
        while abs(float(c1) - float(c)) > eps:
            if fx.subs(x, a) * fx.subs(x, c) > 0:
                a = c
            else:
                b = c
            c1 = c
            c = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float(
                (float(fx.subs(x, b)) - float(fx.subs(x, a))))
        return c

    try:
        root = find_root(fx, a, b, 0.0001)
        return round(root, 5)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



class NewtonMethodInput(BaseModel):
    function: str

@app.post("/newton/") 
def solve_newton(NewtonMethodInput:NewtonMethodInput):
    a = 1
    b = 2
    function = NewtonMethodInput.function

    x = sp.symbols('x')
    fx = sp.sympify(function)

    def find_root(fx, a, b, eps):
        c = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float((float(fx.subs(x, b)) - float(fx.subs(x, a))))
        c1 = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float(
            (float(fx.subs(x, b)) - float(fx.subs(x, a)))) + 1
        while abs(float(c1) - float(c)) > eps:
            if fx.subs(x, a) * fx.subs(x, c) > 0:
                a = c
            else:
                b = c
            c1 = c
            c = (a * float(fx.subs(x, b)) - b * float(fx.subs(x, a))) / float(
                (float(fx.subs(x, b)) - float(fx.subs(x, a))))
        return c

    try:
        root = find_root(fx, a, b, 0.0001)
        return round(root, 5)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

class er(BaseModel):
    matrix: list
    x:int

@app.post("/newton-inter/") 
async def newton_interpolation(er:er):
    try:
        x = er.x
        D_matrix = er.matrix
        
        result = 0
        size = len(D_matrix)
        for i in range(size):
            temp = 1
            for j in range(i):
                temp *= (x - float(D_matrix[j][0]))
            result += temp * D_matrix[i][1]

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
class Lagrange(BaseModel):
    matrix: list
    x:float

@app.post("/lagrange")
async def lagrange_polynomial(Lagrange:Lagrange):
    try:
        points = Lagrange.matrix
        x = Lagrange.x
        result = 0
        size = len(points)
        for i in range(size):
            temp = 1
            for j in range(size):
                if i != j:
                    temp *= (x - float(points[j][0])) / (float(points[i][0]) - float(points[j][0]))
            result += temp * float(points[i][1])
        
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

class Integral(BaseModel):
    a:int
    b:int
    n:int
    function:str

 
@app.post("/integral")
async def solve_integral(Integral:Integral):
    try:
        a = Integral.a
        b = Integral.b
        n = Integral.n
        function = Integral.function
        x = sp.symbols('x')
        fun = sp.lambdify(x, sp.sympify(function), 'numpy')

        # solve using rectangles
        h = (b - a) / n
        result_rectangles = sum(fun(i) for i in np.linspace(a, b, n)) * h

        # solve using trapezium
        result_trapezium = sum((fun(i) + fun(i + ((a + b) / n))) / 2 for i in np.linspace(a, b, n)) * h

        # solve using Simpson's rule
        result_simpsons = sum((fun(i) + 4 * fun(i + ((a + b) / n) / 2) + fun(i + ((a + b) / n))) / 6 for i in np.linspace(a, b, n)) * h

        return {
            "result_rectangles": round(result_rectangles, 5),
            "result_trapezium": round(result_trapezium, 5),
            "result_simpsons": round(result_simpsons, 5),
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))