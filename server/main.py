from typing import Union
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, Body
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
    A = item.A
    b = item.b
    n = len(A)
    for i in range(n):
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]

        pivot = A[i][i]
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