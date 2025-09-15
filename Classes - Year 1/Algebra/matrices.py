# matlatex.py
from sympy import Matrix, symbols, latex, S, I

# ---- LaTeX pmatrix ----
def pmatrix(M: Matrix) -> str:
    rows = [" & ".join(latex(e) for e in row) for row in M.tolist()]
    return r"\begin{pmatrix} " + r" \\ ".join(rows) + r" \end{pmatrix}"

# ---- Row ops (in-place, return M for chaining) ----
def row_swap(M: Matrix, i: int, j: int) -> Matrix:
    M.row_swap(i, j)
    return M

def row_scale(M: Matrix, i: int, k) -> Matrix:
    M.row_op(i, lambda v, _: k*v)
    return M

def row_add(M: Matrix, target: int, src: int, k) -> Matrix:
    M.row_op(target, lambda v, j: v + k*M[src, j])
    return M

# ---- RREF ----
def rref(M: Matrix):
    R, pivots = M.rref()
    return R, pivots

# ---- Multiply ----
def matmul(A: Matrix, B: Matrix) -> Matrix:
    return A*B

# ---- Tiny demo ----
if __name__ == "__main__":
    x1, x2, x3, x4 = symbols("x1 x2 x3 x4")

    A = Matrix([[0, 1],
                [-1, 0]])
    
    B = Matrix([[0,I],
                [I,0]])
    
    Id = Matrix([[1,0],
                 [0,1]])
    
    X = Matrix([[x1, x2],
                [x3, x4]])

    print("A^2:")
    print(pmatrix(matmul(A, A)))

    #M = Matrix([[1, 2, 1],[2, 1, -1],[3, 0, 1]])
    #row_swap(M, 0, 2)
    #row_scale(M, 0, 1/3)
    #row_add(M, 1, 0, -2)
    #row_add(M, 2, 0, -1)
    #print("After row ops:")
    #print(pmatrix(M))

    #R, piv = rref(M)
    #print("RREF:")
    #print(pmatrix(R))
    #print("Pivots:", piv)
