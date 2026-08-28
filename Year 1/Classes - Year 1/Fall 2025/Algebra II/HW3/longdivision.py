from fractions import Fraction

def trim(p):
    i=0
    while i<len(p)-1 and p[i]==0: i+=1
    return p[i:]

def long_div_steps(A, B):
    # A,B: lists of coeffs high->low. Works over rationals.
    A=[Fraction(c) for c in trim(A)]
    B=[Fraction(c) for c in trim(B)]
    m,n=len(A)-1,len(B)-1
    if m<n: print("Quotient = 0, Remainder =", A); return [Fraction(0)], A
    Q=[Fraction(0)]*(m-n+1)
    R=A[:]
    step=1
    while len(R)-1>=n and any(R):
        coeff = R[0]/B[0]
        shift = len(R)-len(B)
        Q[shift]=Q[shift]+coeff
        # subtract coeff*x^shift * B from R
        sub = [Fraction(0)]*shift + [coeff*b for b in B]
        R = [r - s for r,s in zip(R+[], sub + [Fraction(0)]*(len(R)-len(sub)))]
        R = trim(R)
        print(f"step {step}: coeff={coeff} * x^{shift}  remainder={R}")
        step+=1
    print("Quotient :", Q)
    print("Remainder:", R if R else [Fraction(0)])
    return Q, (R if R else [Fraction(0)])

# Your example: (x^3 - 6x^2 + 9x + 3) ÷ (x + 1)
long_div_steps([1,-6,9,3],[1,1])
