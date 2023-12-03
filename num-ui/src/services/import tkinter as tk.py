import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
import numpy as np

# Define global variables
entries = []
const_entries = []
secant_method_points = []
size_entry = None
result_label = None
result_label_least_squares = None
size_entry_least_squares = None
size_entry_least_squares_for_system = []
entries_least_squares = []
#size_entry_newton_method = None
frame_newton_method = None
entries_newton_method = []
fx_entry_newton_method = None
entrie_function_newton_method = ""
fun_graph_newton_method = ""
result_newton_method = None
entrie_function_secant_method = ""
fun_graph_secant_method = ""
result_secant_method = None
a_secant_method = None
b_secant_method = None
entries_least_squares_for_system = []
const_entries_least_squares_for_system = []
size_entry_iteration_method = []
entries_iteration_method = []
const_entries_iteration_method = []
size_entry_lagrange = None
entries_lagrange_polinomial = []
frame_labrange_polinomial = None
size_entry_newton_interpolation = None
entries_newton_interpolation = []
frame_newton_interpolation = None

def matrix_multiplication(A, B):
    n = len(A)
    m = len(B[0])
    C = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(len(B)):
                C[i][j] += A[i][k]*B[k][j]
    return C

def multiply_matrix_by_vector(A, b):
    n = len(A)
    m = len(b)
    c = [0 for _ in range(n)]
    for i in range(n):
        for j in range(m):
            c[i] += A[i][j]*b[j]
    return c

def gaussian_elimination(A, b):
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


def create_entries():
    global entries
    global const_entries

    size = int(size_entry.get())

    for widget in frame.winfo_children():
        widget.destroy()

    entries = [[tk.Entry(frame, width=5) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            entries[i][j].grid(row=i, column=j)

    const_entries = [tk.Entry(frame, width=5) for _ in range(size)]
    for i in range(size):
        const_entries[i].grid(row=i, column=size)


def gauss_gui():
    global size_entry
    global result_label
    global frame

    # Create the GUI
    root = tk.Tk()
    root.title("Gaussian Elimination")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Size:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    size_entry = tk.Entry(root, width=5)
    size_entry.grid(row=0, column=1, padx=5, pady=5)

    size_button = tk.Button(root, text="Create Entries", command=create_entries)
    size_button.grid(row=0, column=2, padx=5, pady=5)

    frame = tk.Frame(root)
    frame.grid(row=1, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_gauss)
    solve_button.grid(row=2, column=0, columnspan=3, pady=10)

    result_label = tk.Label(root, text="Result: ")
    result_label.grid(row=3, column=0, columnspan=3, pady=5)

    root.mainloop()

def create_entries_least_squares():
    global entries_least_squares
    global const_entries_least_squares

    size = int(size_entry_least_squares.get())

    for widget in frame_least_squares.winfo_children():
        widget.destroy()

    entries_least_squares = [[tk.Entry(frame_least_squares, width=5) for _ in range(2)] for _ in range(size)]
    for i in range(size):
        for j in range(2):
            entries_least_squares[i][j].grid(row=i+1, column=j)
    x_label = tk.Label(frame_least_squares, text="x")
    x_label.grid(row=0, column=0, padx=5, pady=5)
    y_label = tk.Label(frame_least_squares, text="y")
    y_label.grid(row=0, column=1, padx=5, pady=5)

def solve_least_squares():
    sum_x = 0
    sum_y = 0
    sum_x_squared = 0
    sum_xy = 0
    size = int(size_entry_least_squares.get())
    for i in range(size):
        sum_x += float(entries_least_squares[i][0].get())
        sum_y += float(entries_least_squares[i][1].get())
        sum_x_squared += float(entries_least_squares[i][0].get())**2
        sum_xy += float(entries_least_squares[i][0].get())*float(entries_least_squares[i][1].get())

    a = (size*sum_xy - sum_x*sum_y)/(size*sum_x_squared - sum_x**2)
    b = (sum_y - a*sum_x)/size
    result = [a, b]
    result_label_least_squares.config(text=f"Result: {result}")
    return result


def least_squares_gui():
    global size_entry_least_squares
    global frame_least_squares
    global result_label_least_squares

    root = tk.Tk()
    root.title("Least Squares")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Nuber of Points:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    size_entry_least_squares = tk.Entry(root, width=5)
    size_entry_least_squares.grid(row=0, column=1, padx=5, pady=5)

    size_button = tk.Button(root, text="Create Entries", command=create_entries_least_squares)
    size_button.grid(row=0, column=2, padx=5, pady=5)

    frame_least_squares = tk.Frame(root)
    frame_least_squares.grid(row=1, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_least_squares)
    solve_button.grid(row=2, column=0, columnspan=3, pady=10)

    result_label_least_squares = tk.Label(root, text="Result: ")
    result_label_least_squares.grid(row=3, column=0, columnspan=3, pady=5)

    frame_graph = tk.Frame(root)
    frame_graph.grid(row=4, column=0, columnspan=3, pady=10)

    def create_graph():
        plt.clf()
        a,b = solve_least_squares()
        size = int(size_entry_least_squares.get())
        x = [float(entries_least_squares[i][0].get()) for i in range(size)]
        y = [float(entries_least_squares[i][1].get()) for i in range(size)]
        plt.plot(x, y, 'o')
        plt.plot(x, [a*x[i]+b for i in range(size)])

        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #set new size of window to fit graph
        root.geometry("800x800")

    graph_button = tk.Button(root, text="Graph", command=create_graph)
    graph_button.grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()

# def create_entries_newton_method():
#     global entries_newton_method
#     global const_entries_newton_method
#     global fx_entry_newton_method
#
#     size = int(size_entry_newton_method.get())
#
#     for widget in frame_newton_method.winfo_children():
#         widget.destroy()
#
#
#     entries_newton_method = [tk.Entry(frame_newton_method, width=5) for _ in range(size+1)]
#     for i in range(size+1):
#         entries_newton_method[i].grid(row=1, column=i)
#         x_label = tk.Label(frame_newton_method, text=f"x^{size-i}")
#         x_label.grid(row=0, column=i, padx=5, pady=5)
#     fx_label = tk.Label(frame_newton_method, text="=")
#     fx_label.grid(row=1, column=size+1, padx=5, pady=5)
#     fx_entry_newton_method = tk.Entry(frame_newton_method, width=5)
#     fx_entry_newton_method.grid(row=1, column=size+2, padx=5, pady=5)

def solve_newton_method():
    global entries_newton_method
    global entrie_function_newton_method
    global fun_graph_newton_method
    global fx_entry_newton_method
    global result_newton_method
    #size = int(size_entry_newton_method.get())+1
    #poww=size-1
    ans=0

    # if fx_entry_newton_method.get()!="0":
    #     tempp=entries_newton_method[-1].get()
    #     entries_newton_method[-1].delete(0,tk.END)
    #     entries_newton_method[-1].insert(0,round((float(tempp)-float(fx_entry_newton_method.get())),1))
    #     fx_entry_newton_method.delete(0,tk.END)
    #
    # fx_string = ""
    # for i in entries_newton_method:
    #     if poww!=0:
    #         if i.get()!="0":
    #             fx_string=fx_string+i.get()+"*x**"+str(poww)+"+"
    #         poww=poww-1
    #     else:
    #         if i.get()!="0":
    #             fx_string=fx_string+i.get()

    temp = ""
    sd = 1
    flag = False
    fun = str(entrie_function_newton_method.get())
    for it in fun:
        if flag == True:
            sd += 1
            temp = temp + it
        if it == '=':
            flag = True

    fun_len = len(fun)
    fun = fun[0:fun_len - sd]
    fun = fun + "-" + temp

    x=sp.symbols('x')
    fx = sp.sympify(fun)
    fun_graph_newton_method = fx
    f_prime = sp.diff(fx, x)
    f_prime_simplified = sp.simplify(f_prime)

    ans = fx.subs(x, 0)
    if ans>=0:
        flag=True
    else:
        flag=False

    i=1
    #x^4-16*x-64=0
    #x^2+3*x-4=0
    while True:
        ans = fx.subs(x, i)
        if ans>=0 and flag==False:
            break
        if ans<0 and flag==True:
            break
        if ans>=0:
            flag=True
        if ans<0:
            flag=False
        i=i+1

    temp=round(i,1)
    ee=1
    x1=temp - (float(fx.subs(x, temp))/float(f_prime_simplified.subs(x, temp)))
    x1=round(x1,5)
    while ee>0.0001:
        x0=x1
        x1=x0 - (fx.subs(x, x0)/f_prime_simplified.subs(x, x0))
        ee=abs(x1-x0)
        x1=round(x1,5)

    result_newton_method = x1

    result_label_newton_method.config(text=f"Result: {x1}")

def newton_method_gui():
    #global size_entry_newton_method
    global frame_newton_method
    global entrie_function_newton_method
    global result_label_newton_method

    root = tk.Tk()
    root.title("Newton's Method")

    size_Label = tk.Label(root, text="Enter the function: ")
    size_Label.grid(row=0, column=0, padx=5, pady=5)

    entrie_function_newton_method = tk.Entry(root, width=40)
    entrie_function_newton_method.grid(row=0, column=1, padx=5, pady=5)

    # size_button = tk.Button(root, text="Create Entries", command=create_entries_newton_method)
    # size_button.grid(row=0, column=2, padx=5, pady=5)
    #
    # frame_newton_method = tk.Frame(root)
    # frame_newton_method.grid(row=1, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_newton_method)
    solve_button.grid(row=2, column=0, columnspan=3, pady=10)

    result_label_newton_method = tk.Label(root, text="Result: ")
    result_label_newton_method.grid(row=3, column=0, columnspan=3, pady=5)

    frame_graph = tk.Frame(root)
    frame_graph.grid(row=4, column=0, columnspan=3, pady=10)

    def create_graph():
        plt.clf()
        global fun_graph_newton_method
        global result_newton_method
        x = sp.symbols('x')
        x_axis = []
        y_axis = []

        for i in np.linspace(float(result_newton_method)-1,float(result_newton_method)+1, 1000):
            x_axis.append(i)
            y_axis.append(fun_graph_newton_method.subs(x, i))
        plt.plot(x_axis, y_axis)

        x_axis = []
        y_axis = []
        for i in np.linspace(float(result_newton_method)-1,float(result_newton_method)+1, 1000):
            x_axis.append(i)
            y_axis.append((float(sp.diff(fun_graph_newton_method,x).subs(x, result_newton_method)))*(i-result_newton_method)+float(fun_graph_newton_method.subs(x, result_newton_method)))
        plt.plot(x_axis, y_axis)

        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')

        plt.plot(result_newton_method, fun_graph_newton_method.subs(x, result_newton_method), 'o')

        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #set new size of window to fit graph
        root.geometry("800x800")

    graph_button = tk.Button(root, text="Graph", command=create_graph)
    graph_button.grid(row=5, column=0, columnspan=3, pady=10)

    root.geometry("400x400")

    root.mainloop()

# def create_entries_secant_method():
#     global entries_secant_method
#     global const_entries_secant_method
#     global fx_entry_secant_method
#
#     size = int(size_entry_secant_method.get())
#
#     for widget in frame_secant_method.winfo_children():
#         widget.destroy()
#
#     entries_secant_method = [tk.Entry(frame_secant_method, width=5) for _ in range(size+1)]
#     for i in range(size+1):
#         entries_secant_method[i].grid(row=1, column=i)
#         x_label = tk.Label(frame_secant_method, text=f"x^{size-i}")
#         x_label.grid(row=0, column=i, padx=5, pady=5)
#     fx_label = tk.Label(frame_secant_method, text="=")
#     fx_label.grid(row=1, column=size+1, padx=5, pady=5)
#     fx_entry_secant_method = tk.Entry(frame_secant_method, width=5)
#     fx_entry_secant_method.grid(row=1, column=size+2, padx=5, pady=5)

def solve_secant_method():
    global entries_secant_method
    global fx_entry_secant_method
    global entrie_function_secant_method
    global fun_graph_secant_method
    global secant_method_points
    global result_secant_method
    global a_secant_method
    global b_secant_method
    # size = int(size_entry_secant_method.get())+1
    #
    # if fx_entry_secant_method.get()!="0":
    #     tempp=entries_secant_method[-1].get()
    #     entries_secant_method[-1].delete(0,tk.END)
    #     entries_secant_method[-1].insert(0,round((float(tempp)-float(fx_entry_secant_method.get())),1))
    #     fx_entry_secant_method.delete(0,tk.END)
    #
    # fx_string = ""
    # for i in entries_secant_method:
    #     fx_string=fx_string+i.get()+"*x**"+str(size-1)+"+"
    #     size=size-1
    #
    # fx_string=fx_string[:-1]
    # fx = sp.sympify(fx_string)
    # x=sp.symbols('x')
    temp = ""
    sd = 1
    flag = False
    fun = str(entrie_function_secant_method.get())
    for it in fun:
        if flag == True:
            sd += 1
            temp = temp + it
        if it == '=':
            flag = True

    fun_len = len(fun)
    fun = fun[0:fun_len - sd]
    fun = fun + "-" + temp

    x = sp.symbols('x')
    fx = sp.sympify(fun)
    fun_graph_secant_method = fx
    secant_method_points.append(float(a_secant_method.get()))

    def find_root(fx, a, b, eps):
        c = (a*float(fx.subs(x,b)) - b*float(fx.subs(x,a)))/float((float(fx.subs(x,b)) - float(fx.subs(x,a))))
        c1 = (a*float(fx.subs(x,b)) - b*float(fx.subs(x,a)))/float((float(fx.subs(x,b)) - float(fx.subs(x,a))))+1
        while abs(float(c1) - float(c)) > eps:
            secant_method_points.append(c)
            if fx.subs(x,a) * fx.subs(x,c) > 0:
                a = c
            else:
                b = c
            c1 = c
            c = (a*float(fx.subs(x,b)) - b*float(fx.subs(x,a)))/float((float(fx.subs(x,b)) - float(fx.subs(x,a))))
        return c

    root = find_root(fx, float(a_secant_method.get()), float(b_secant_method.get()), 0.0001)
    result_label_secant_method.config(text=f"Result: x = {round(root,5)}")


def secant_method_gui():
    global size_entry_secant_method
    global frame_secant_method
    global result_label_secant_method
    global entrie_function_secant_method
    global a_secant_method
    global b_secant_method

    root = tk.Tk()
    root.title("Secant Method")

    size_Label = tk.Label(root, text="Enter the function: ")
    size_Label.grid(row=0, column=0, padx=5, pady=5)

    entrie_function_secant_method = tk.Entry(root, width=40)
    entrie_function_secant_method.grid(row=0, column=1, padx=5, pady=5)

    a_label = tk.Label(root, text="a: ")
    a_label.grid(row=1, column=0, padx=5, pady=5)

    a_secant_method = tk.Entry(root, width=5)
    a_secant_method.grid(row=1, column=1, padx=5, pady=5)

    b_label = tk.Label(root, text="b: ")
    b_label.grid(row=2, column=0, padx=5, pady=5)

    b_secant_method = tk.Entry(root, width=5)
    b_secant_method.grid(row=2, column=1, padx=5, pady=5)

    # size_button = tk.Button(root, text="Create Entries", command=create_entries_secant_method)
    # size_button.grid(row=0, column=2, padx=5, pady=5)
    #
    # frame_secant_method = tk.Frame(root)
    # frame_secant_method.grid(row=1, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_secant_method)
    solve_button.grid(row=3, column=0, columnspan=3, pady=10)

    result_label_secant_method = tk.Label(root, text="Result: ")
    result_label_secant_method.grid(row=4, column=0, columnspan=3, pady=5)

    frame_graph = tk.Frame(root)
    frame_graph.grid(row=5, column=0, columnspan=3, pady=10)


    def create_graph():
        plt.clf()
        global fun_graph_secant_method
        global secant_method_points
        global result_secant_method
        global b_secant_method
        x = sp.symbols('x')
        x_axis = []
        y_axis = []
        for i in np.linspace(float(secant_method_points[0])-1, max(float(b_secant_method.get()),secant_method_points[-1]+1), 1000):
            x_axis.append(i)
            y_axis.append(fun_graph_secant_method.subs(x, i))

        plt.plot(x_axis, y_axis)

        x_axis = []
        y_axis = []
        for i in secant_method_points:
            x_axis.append(i)
            y_axis.append(fun_graph_secant_method.subs(x, i))
        plt.plot(x_axis, y_axis, 'o')

        for i in secant_method_points:
            x_axis = []
            y_axis = []
            x_axis.append(float(b_secant_method.get()))
            x_axis.append(i)
            y_axis.append(fun_graph_secant_method.subs(x, float(b_secant_method.get())))
            y_axis.append(fun_graph_secant_method.subs(x, i))
            plt.plot(x_axis, y_axis)

        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        #plt.xlim(float(secant_method_points[0])-1,float(secant_method_points[-1])+1)
        #plt.ylim(-10,10)


        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        #set new size of window to fit graph
        root.geometry("800x800")

    graph_button = tk.Button(root, text="Graph", command=create_graph)
    graph_button.grid(row=6, column=0, columnspan=3, pady=10)

    root.geometry("400x400")

    root.mainloop()

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

def solve_least_squares_for_system():
    global entries_least_squares_for_system
    global result_label_least_squares
    global const_entries_least_squares_for_system

    size = int(size_entry_least_squares_for_system[0].get())
    size2 = int(size_entry_least_squares_for_system[1].get())
    matrix = [[float(entries_least_squares_for_system[i][j].get() if entries_least_squares_for_system[i][j].get() else 0) for j in range(size-1)] for i in range(size2)]
    constants = [float(const_entries_least_squares_for_system[i].get() if const_entries_least_squares_for_system[i].get() else 0) for i in range(size2)]

    matrix_transpose = [[matrix[j][i] for j in range(size2)] for i in range(size-1)]

    #matrix_transpose_by_matrix = matrix_multiplication(matrix_transpose, matrix);

    matrix_transpose_by_matrix = [[0 for _ in range(size-1)] for _ in range(size-1)]
    for i in range(size-1):
        for j in range(size-1):
            for k in range(size2):
                matrix_transpose_by_matrix[i][j] += matrix_transpose[i][k]*matrix[k][j]

    matrix_transpose_by_matrix_invertible = invertible_matrix(matrix_transpose_by_matrix)

    matrix_transpose_by_constants = [0 for _ in range(size-1)]
    for i in range(size-1):
        for j in range(size2):
            matrix_transpose_by_constants[i] += matrix_transpose[i][j]*constants[j]

    result = [0 for _ in range(size-1)]
    for i in range(size-1):
        for j in range(size-1):
            result[i] += matrix_transpose_by_matrix_invertible[i][j]*matrix_transpose_by_constants[j]

    result = [round(result[i], 7) for i in range(size-1)]

    result_label_least_squares.config(text=f"Result: {result}")

def create_entries_least_squares_for_system():
    global size_entry_least_squares_for_system
    global entries_least_squares_for_system
    global const_entries_least_squares_for_system

    size = int(size_entry_least_squares_for_system[0].get())
    size2 = int(size_entry_least_squares_for_system[1].get())

    for widget in frame_least_squares.winfo_children():
        widget.destroy()

    entries_least_squares_for_system = [[tk.Entry(frame_least_squares, width=5) for _ in range(size-1)] for _ in range(size2)]
    for i in range(size2):
        for j in range(size-1):
            entries_least_squares_for_system[i][j].grid(row=i, column=j)

    const_entries_least_squares_for_system = [tk.Entry(frame_least_squares, width=5) for _ in range(size2)]
    for i in range(size2):
        const_entries_least_squares_for_system[i].grid(row=i, column=size)

def least_squares_for_system_gui():
    global size_entry_least_squares_for_system
    global frame_least_squares
    global result_label_least_squares

    root = tk.Tk()
    root.title("Least Squares")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Nuber of columns:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    columns = tk.Entry(root, width=5)
    columns.grid(row=0, column=1, padx=5, pady=5)

    size_label2 = tk.Label(root, text="Nuber of rows:")
    size_label2.grid(row=1, column=0, padx=5, pady=5)

    rows = tk.Entry(root, width=5)
    rows.grid(row=1, column=1, padx=5, pady=5)

    size_entry_least_squares_for_system.append(columns)
    size_entry_least_squares_for_system.append(rows)

    size_button = tk.Button(root, text="Create Entries", command=create_entries_least_squares_for_system)
    size_button.grid(row=3, column=1, padx=5, pady=5)

    frame_least_squares = tk.Frame(root)
    frame_least_squares.grid(row=2, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_least_squares_for_system)
    solve_button.grid(row=4, column=1, columnspan=3, pady=10)

    result_label_least_squares = tk.Label(root, text="Result: ")
    result_label_least_squares.grid(row=5, column=1, columnspan=3, pady=5)

    root.mainloop()

def solve_iteration_method():
    global size_entry_iteration_method
    global entries_iteration_method
    global const_entries_iteration_method

    #get the matrix and constants from the gui
    size = int(size_entry_iteration_method[0].get())
    size2 = int(size_entry_iteration_method[1].get())
    matrix = [[float(entries_iteration_method[i][j].get() if entries_iteration_method[i][j].get() else 0) for j in range(size-1)] for i in range(size2)]
    constants = [float(const_entries_iteration_method[i].get() if const_entries_iteration_method[i].get() else 0) for i in range(size2)]

    x = []
    n = len(matrix)
    for j in range(n):
        k = matrix[j][j]
        for i in range(n):
            matrix[j][i] /= -k
        matrix[j][j] = 0
        constants[j] /= k

    r=0
    x=constants.copy()
    tmp=sum(x)+2*0.00001
    while abs(sum(x)-tmp)>0.00001:
        tmp=sum(x)
        t=[0]*n
        for i in range(n):
            t[i]=sum(x[j]*matrix[i][j] for j in range(n))+constants[i]
        r+=1
        x=t.copy()

    x = [round(x[i], 4) for i in range(size2)]

    result_label_iteration_method.config(text=f"Result: {x}")

def create_entries_iteration_method():
    global size_entry_iteration_method
    global entries_iteration_method
    global const_entries_iteration_method

    size = int(size_entry_iteration_method[0].get())
    size2 = int(size_entry_iteration_method[1].get())

    for widget in frame_iteration_method.winfo_children():
        widget.destroy()

    entries_iteration_method = [[tk.Entry(frame_iteration_method, width=5) for _ in range(size-1)] for _ in range(size2)]
    for i in range(size2):
        for j in range(size-1):
            entries_iteration_method[i][j].grid(row=i, column=j)

    const_entries_iteration_method = [tk.Entry(frame_iteration_method, width=5) for _ in range(size2)]
    for i in range(size2):
        const_entries_iteration_method[i].grid(row=i, column=size)

def iteration_method_gui():
    global frame_iteration_method
    global result_label_iteration_method
    global entrie_function_iteration_method
    global size_entry_iteration_method

    root = tk.Tk()
    root.title("Iteration Method")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Nuber of columns:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    columns = tk.Entry(root, width=5)
    columns.grid(row=0, column=1, padx=5, pady=5)

    size_label2 = tk.Label(root, text="Nuber of rows:")
    size_label2.grid(row=1, column=0, padx=5, pady=5)

    rows = tk.Entry(root, width=5)
    rows.grid(row=1, column=1, padx=5, pady=5)

    size_entry_iteration_method.append(columns)
    size_entry_iteration_method.append(rows)

    size_button = tk.Button(root, text="Create Entries", command=create_entries_iteration_method)
    size_button.grid(row=3, column=1, padx=5, pady=5)

    frame_iteration_method = tk.Frame(root)
    frame_iteration_method.grid(row=2, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=solve_iteration_method)
    solve_button.grid(row=4, column=1, columnspan=3, pady=10)

    result_label_iteration_method = tk.Label(root, text="Result: ")
    result_label_iteration_method.grid(row=5, column=1, columnspan=3, pady=5)

    root.mainloop()

def create_entries_lagrange_polinomial():
    global entries_lagrange_polinomial
    global size_entry_lagrange
    global frame_labrange_polinomial

    size = int(size_entry_lagrange.get())

    for widget in frame_labrange_polinomial.winfo_children():
        widget.destroy()

    entries_lagrange_polinomial = [[tk.Entry(frame_labrange_polinomial, width=5) for _ in range(2)] for _ in range(size)]
    for i in range(size):
        for j in range(2):
            entries_lagrange_polinomial[i][j].grid(row=i+1, column=j)
    x_label = tk.Label(frame_labrange_polinomial, text="x")
    x_label.grid(row=0, column=0, padx=5, pady=5)
    y_label = tk.Label(frame_labrange_polinomial, text="y")
    y_label.grid(row=0, column=1, padx=5, pady=5)

def lagrange_polinomial(x):
    global entries_lagrange_polinomial
    global size_entry_lagrange
    global frame_labrange_polinomial

    size = int(size_entry_lagrange.get())
    result = 0
    for i in range(size):
        temp = 1
        for j in range(size):
            if i!=j:
                temp *= (x - float(entries_lagrange_polinomial[j][0].get()))/(float(entries_lagrange_polinomial[i][0].get()) - float(entries_lagrange_polinomial[j][0].get()))
        result += temp*float(entries_lagrange_polinomial[i][1].get())
    return result

def lagrange_polinomial_gui():
    global size_entry_lagrange
    global frame_labrange_polinomial
    global a_lagrange_entry
    global b_lagrange_entry
    global h_lagrange_entry

    root = tk.Tk()
    root.title("Lagrange Polinomial")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Nuber of Points:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    size_entry_lagrange = tk.Entry(root, width=5)
    size_entry_lagrange.grid(row=0, column=1, padx=5, pady=5)

    size_button = tk.Button(root, text="Create Entries", command=create_entries_lagrange_polinomial)
    size_button.grid(row=0, column=2, padx=5, pady=5)

    frame_labrange_polinomial = tk.Frame(root)
    frame_labrange_polinomial.grid(row=1, column=0, columnspan=3, pady=10)

    a_lagrange_label = tk.Label(root, text="a: ")
    a_lagrange_label.grid(row=2, column=0, padx=5, pady=5)

    a_lagrange_entry = tk.Entry(root, width=5)
    a_lagrange_entry.grid(row=2, column=1, padx=5, pady=5)

    b_lagrange_label = tk.Label(root, text="b: ")
    b_lagrange_label.grid(row=2, column=2, padx=5, pady=5)

    b_lagrange_entry = tk.Entry(root, width=5)
    b_lagrange_entry.grid(row=2, column=3, padx=5, pady=5)

    h_lagrange_label = tk.Label(root, text="h: ")
    h_lagrange_label.grid(row=2, column=4, padx=5, pady=5)

    h_lagrange_entry = tk.Entry(root, width=5)
    h_lagrange_entry.grid(row=2, column=5, padx=5, pady=5)

    def create_graph_lagrange():
        plt.clf()
        a = float(a_lagrange_entry.get())
        b = float(b_lagrange_entry.get())
        h = float(h_lagrange_entry.get())
        hh = (b-a)/h
        x = np.arange(a, b+hh, hh)
        y = [lagrange_polinomial(x[i]) for i in range(len(x))]
        plt.plot(x, y)
        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_graph_lagrange)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        for i in range(int(size_entry_lagrange.get())):
            plt.plot(float(entries_lagrange_polinomial[i][0].get()), float(entries_lagrange_polinomial[i][1].get()), 'o')

        root.geometry("800x800")

    frame_graph_lagrange = tk.Frame(root)
    frame_graph_lagrange.grid(row=4, column=0, columnspan=3, pady=10)

    solve_button = tk.Button(root, text="Solve", command=create_graph_lagrange)
    solve_button.grid(row=3, column=0, columnspan=3, pady=10)


    root.mainloop()

def create_entries_newton_interpolation():
    global entries_newton_interpolation
    global size_entry_newton_interpolation
    global frame_newton_interpolation

    size = int(size_entry_newton_interpolation.get())

    for widget in frame_newton_interpolation.winfo_children():
        widget.destroy()

    entries_newton_interpolation = [[tk.Entry(frame_newton_interpolation, width=5) for _ in range(2)] for _ in range(size)]
    for i in range(size):
        for j in range(2):
            entries_newton_interpolation[i][j].grid(row=i+1, column=j)
    x_label = tk.Label(frame_newton_interpolation, text="x")
    x_label.grid(row=0, column=0, padx=5, pady=5)
    y_label = tk.Label(frame_newton_interpolation, text="y")
    y_label.grid(row=0, column=1, padx=5, pady=5)

def create_D_matrix_newton_interpolation():
    global entries_newton_interpolation
    global size_entry_newton_interpolation
    global frame_newton_interpolation

    size = int(size_entry_newton_interpolation.get())
    D_matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        D_matrix[i][0] = float(entries_newton_interpolation[i][1].get())
    for j in range(1, size):
        for i in range(size-j):
            D_matrix[i][j] = (D_matrix[i+1][j-1] - D_matrix[i][j-1])/(float(entries_newton_interpolation[i+j][0].get()) - float(entries_newton_interpolation[i][0].get()))
    return D_matrix

def newton_interpolation(x, D_matrix):
    global entries_newton_interpolation
    global size_entry_newton_interpolation
    global frame_newton_interpolation

    size = int(size_entry_newton_interpolation.get())
    result = 0
    for i in range(size):
        temp = 1
        for j in range(i):
            temp *= (x - float(entries_newton_interpolation[j][0].get()))
        result += temp*D_matrix[0][i]
    return result

def newton_interpolation_gui():
    global size_entry_newton_interpolation
    global frame_newton_interpolation
    global a_newton_interpolation_entry
    global b_newton_interpolation_entry
    global h_newton_interpolation_entry

    root = tk.Tk()
    root.title("Newton Interpolation")

    root.geometry("400x400")

    size_label = tk.Label(root, text="Nuber of Points:")
    size_label.grid(row=0, column=0, padx=5, pady=5)

    size_entry_newton_interpolation = tk.Entry(root, width=5)
    size_entry_newton_interpolation.grid(row=0, column=1, padx=5, pady=5)

    size_button = tk.Button(root, text="Create Entries", command=create_entries_newton_interpolation)
    size_button.grid(row=0, column=2, padx=5, pady=5)

    frame_newton_interpolation = tk.Frame(root)
    frame_newton_interpolation.grid(row=1, column=0, columnspan=3, pady=10)

    a_newton_interpolation_label = tk.Label(root, text="a: ")
    a_newton_interpolation_label.grid(row=2, column=0, padx=5, pady=5)

    a_newton_interpolation_entry = tk.Entry(root, width=5)
    a_newton_interpolation_entry.grid(row=2, column=1, padx=5, pady=5)

    b_newton_interpolation_label = tk.Label(root, text="b: ")
    b_newton_interpolation_label.grid(row=2, column=2, padx=5, pady=5)

    b_newton_interpolation_entry = tk.Entry(root, width=5)
    b_newton_interpolation_entry.grid(row=2, column=3, padx=5, pady=5)

    h_newton_interpolation_label = tk.Label(root, text="h: ")
    h_newton_interpolation_label.grid(row=2, column=4, padx=5, pady=5)

    h_newton_interpolation_entry = tk.Entry(root, width=5)
    h_newton_interpolation_entry.grid(row=2, column=5, padx=5, pady=5)

    def create_graph_newton_interpolation():
        D_matrix = create_D_matrix_newton_interpolation()
        plt.clf()
        a = float(a_newton_interpolation_entry.get())
        b = float(b_newton_interpolation_entry.get())
        h = float(h_newton_interpolation_entry.get())
        hh = (b-a)/h
        x = np.arange(a, b+hh, hh)
        y = [newton_interpolation(x[i], D_matrix) for i in range(len(x))]
        plt.plot(x, y)
        canvas = FigureCanvasTkAgg(plt.gcf(), master=frame_graph_newton_interpolation)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        for i in range(int(size_entry_newton_interpolation.get())):
            plt.plot(float(entries_newton_interpolation[i][0].get()), float(entries_newton_interpolation[i][1].get()), 'o')

        root.geometry("800x800")

    solve_button = tk.Button(root, text="Solve", command=create_graph_newton_interpolation)
    solve_button.grid(row=3, column=0, columnspan=3, pady=10)

    frame_graph_newton_interpolation = tk.Frame(root)
    frame_graph_newton_interpolation.grid(row=4, column=0, columnspan=3, pady=10)

    root.mainloop()

def solve_integral():
    global result_label_integral_1
    global result_label_integral_2
    global result_label_integral_3
    global entrie_function_integral
    global a_integral_entry
    global b_integral_entry
    global n_integral_entry

    x = sp.symbols('x')
    fun = sp.sympify(entrie_function_integral.get())
    a = float(a_integral_entry.get())
    b = float(b_integral_entry.get())
    n = int(n_integral_entry.get())

    #solve using rectangles
    h = (b-a)/n
    result = 0
    for i in np.linspace(a,b,n):
        result += fun.subs(x, i)
    result = result*h
    result_label_integral_1.config(text=f"(rectangles) Result: {round(result, 5)}")
    #solve using trapezium
    result = 0
    for i in np.linspace(a,b,n):
        result += (fun.subs(x, i)+fun.subs(x, i+((a+b)/n)))/2
    result = result*h
    result_label_integral_2.config(text=f"(trapezium) Result: {round(result, 5)}")
    #solve using simpson's rule
    result = 0
    for i in np.linspace(a,b,n):
        result += (fun.subs(x, i)+4*fun.subs(x, i+((a+b)/n)/2)+fun.subs(x, i+((a+b)/n)))/6
    result = result*h
    result_label_integral_3.config(text=f"(simpson's rule) Result: {round(result, 5)}")

def integral_gui():
    global frame_integral
    global result_label_integral_1
    global result_label_integral_2
    global result_label_integral_3
    global entrie_function_integral
    global a_integral_entry
    global b_integral_entry
    global n_integral_entry

    root = tk.Tk()
    root.title("Integral")

    root.geometry("400x400")

    a_integral_label = tk.Label(root, text="a: ")
    a_integral_label.grid(row=0, column=0, padx=5, pady=5)

    a_integral_entry = tk.Entry(root, width=5)
    a_integral_entry.grid(row=0, column=1, padx=5, pady=5)

    b_integral_label = tk.Label(root, text="b: ")
    b_integral_label.grid(row=0, column=2, padx=5, pady=5)

    b_integral_entry = tk.Entry(root, width=5)
    b_integral_entry.grid(row=0, column=3, padx=5, pady=5)

    n_integral_label = tk.Label(root, text="n: ")
    n_integral_label.grid(row=0, column=4, padx=5, pady=5)

    n_integral_entry = tk.Entry(root, width=5)
    n_integral_entry.grid(row=0, column=5, padx=5, pady=5)

    entrie_function_integral = tk.Entry(root, width=40)
    entrie_function_integral.grid(row=1, column=0, columnspan=6, padx=5, pady=5)

    solve_button = tk.Button(root, text="Solve", command=solve_integral)
    solve_button.grid(row=2, column=0, columnspan=6, pady=10)

    result_label_integral_1 = tk.Label(root, text="(rectangles) Result: ")
    result_label_integral_1.grid(row=3, column=0, columnspan=6, pady=5)

    result_label_integral_2 = tk.Label(root, text="(trapezium) Result: ")
    result_label_integral_2.grid(row=4, column=0, columnspan=6, pady=5)

    result_label_integral_3 = tk.Label(root, text="(simpson's rule) Result: ")
    result_label_integral_3.grid(row=5, column=0, columnspan=6, pady=5)

    root.mainloop()

def main():
    root = tk.Tk()
    root.title("Linear Algebra Solver")

    root.geometry("400x400")

    gauss_button = tk.Button(root, text="Gaussian Elimination", command=gauss_gui)
    gauss_button.grid(row=0, column=0, padx=5, pady=5)

    least_squares_button = tk.Button(root, text="Least Squares", command=least_squares_gui)
    least_squares_button.grid(row=0, column=1, padx=5, pady=5)

    least_squares_button = tk.Button(root, text="Least Squares System", command=least_squares_for_system_gui)
    least_squares_button.grid(row=0, column=2, padx=5, pady=5)

    newton_method_button = tk.Button(root, text="Newton's Method", command=newton_method_gui)
    newton_method_button.grid(row=1, column=0, padx=5, pady=5)

    newton_method_button = tk.Button(root, text="Secant method", command=secant_method_gui)
    newton_method_button.grid(row=1, column=1, padx=5, pady=5)

    iteration_method_button = tk.Button(root, text="Iteration method", command=iteration_method_gui)
    iteration_method_button.grid(row=1, column=2, padx=5, pady=5)

    lagrange_polinomial_button = tk.Button(root, text="Lagrange Polinomial", command=lagrange_polinomial_gui)
    lagrange_polinomial_button.grid(row=2, column=0, padx=5, pady=5)

    newton_interpolation_button = tk.Button(root, text="Newton Interpolation", command=newton_interpolation_gui)
    newton_interpolation_button.grid(row=2, column=1, padx=5, pady=5)

    integral_button = tk.Button(root, text="Integral", command=integral_gui)
    integral_button.grid(row=2, column=2, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
