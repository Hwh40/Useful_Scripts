import numpy as np

def uncertainty(x, dx, y, dy, operation):
    Q = 0
    Qd = 0

    if operation == '*':
        Q = x * y
        Qd = abs(Q) * (abs(dx / x) + abs(dy / y))
    if operation == '/':
        Q = x / y
        Qd = abs(Q) * (abs(dx / x) + abs(dy / y))
    if operation == '+':
        Q = x + y
        Qd = abs(dx) + abs(dy)
    if operation == '-':
        Q = x - y
        Qd = abs(dx) + abs(dy)
    return Q, Qd

def operations(x, dx, string):
    adds_Q = []
    adds_Qd = []
    op_adds = []
    ops = list(string)
    Q, Qd = uncertainty(x[0], dx[0], x[1], dx[1], ops[0])
    print(Q)
    for i in range(2, len(x)):
        
        if ops[i - 1] == '-' or ops[i - 1] == '+':
            adds_Q.append(Q)
            adds_Qd.append(Qd)
            op_adds.append(ops[i-1])
            Q,Qd = uncertainty(x[i], dx[i], 1, 0, ops[i])
        else:
            Q, Qd = uncertainty(Q, Qd, x[i], dx[i], ops[i - 1])
            print(Q)
    for i in range(len(adds_Q)):
        Q,Qd = uncertainty(adds_Q[i], adds_Qd[i], Q, Qd, op_adds[i - 1] )
    return Q,Qd

def main():
    a,ad = operations([1,2,3,4],[1,2,3,4],'*+*')
    b,bd = operations([3,4], [1,2], '*')
    c,cd = operations([a,b],[ad,bd],'/')
    print(c,cd)

    d,dd = operations([1,2,3,4, 3,4],[1,2,3,4,1,2],'*+*//')
    print(d,dd)

if __name__ == "__main__":
    main()