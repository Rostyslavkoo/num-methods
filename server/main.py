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
    
@app.post("/least-squares/") 
def solve_least_squares_for_system(item: Item):
    try:
        A = item.A
        b = item.b
        size = len(A)
        size2 = len(A[0])
        
        matrix = [[float(A[i][j]) for j in range(size2)] for i in range(size)]
        constants = [float(b[i]) for i in range(size)]

        matrix_transpose = [[matrix[j][i] for j in range(size)] for i in range(size2)]

        matrix_transpose_by_matrix = [[0 for _ in range(size2)] for _ in range(size2)]
        for i in range(size2):
            for j in range(size2):
                for k in range(size):
                    matrix_transpose_by_matrix[i][j] += matrix_transpose[i][k] * matrix[k][j]

        for i in range(size2):
            if matrix_transpose_by_matrix[i][i] != 0:
                matrix_transpose_by_matrix_invertible = invertible_matrix(matrix_transpose_by_matrix)
            else:
                raise HTTPException(status_code=400, detail="Matrix is not invertible")

        matrix_transpose_by_constants = [0 for _ in range(size2)]
        for i in range(size2):
            for j in range(size):
                matrix_transpose_by_constants[i] += matrix_transpose[i][j] * constants[j]

        result = [0 for _ in range(size2)]
        for i in range(size2):
            for j in range(size2):
                result[i] += matrix_transpose_by_matrix_invertible[i][j] * matrix_transpose_by_constants[j]

        result = [round(result[i], 7) for i in range(size2)]

        return result

    except (ValueError, IndexError) as e:
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
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))