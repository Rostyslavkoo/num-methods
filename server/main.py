from typing import Union
from fastapi.middleware.cors import CORSMiddleware

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