from interfaz import RepresentaTablero
from math import sqrt
import copy
#       a      b    c      d     e     f     g     h
m = [["Br1", "Bn", "Bb", "Bq", "Bk", "Bb", "Bn", "Br2"],  # 8
     ["Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp"],  # 7
     ["", "Wn", "", "", "", "", "", ""],  # 6
     ["", "", "", "", "", "", "", ""],  # 5
     ["", "", "", "", "", "", "", ""],  # 4
     ["", "", "", "", "", "", "", ""],  # 3
     ["Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp"],  # 2
     ["Wr1", "Wn", "Wb", "Wq", "Wk", "Wb", "Wn", "Wr2"]]  # 1
estados = [[]]
tablero = RepresentaTablero(m)
estados.append(copy.deepcopy(m))
pi = [0, 0]
pf = [0, 0]
palabra = ""
movimiento_n = 0
letra = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
numeros = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
control = [0, 0, 0, 0, 0, 0]  # 1: WK 2: BK 3: WR1 4: WR2 5: BR1 6: BR2
peonesblancos = [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0]
blancas = True
def contarMovimientos(x):
    if x % 2 == 0:
        print("Mueve el blanco")
    else:
        print("Mueve el negro")
def comprobarMovimientos(x, y):
    if x[0] == "W":
        y = True
        if x == "Wk":
            control[0] += 1
        elif x == "Wr1":
            control[2] += 1
        elif x == "Wr2":
            control[3] += 1
    else:
        y = False
        if x == "Bk":
            control[1] += 1
        elif x == "Br1":
            control[4] += 1
        elif x == "Br2":
            control[5] += 1
    return y
def enroque(x):
    a = 1
    if movimiento_n % 2 == 0:
        if x == "C" and control[0] == 0 and control[3] == 0 and m[7][5] == "" and m[7][6] == "":
            m[7][6] = m[7][4]
            m[7][5] = m[7][7]
            m[7][4] = ""
            m[7][7] = ""
            mostrarestado(m)
            a = 0
            return True
        if x == "L" and control[0] == 0 and control[2] == 0 and m[7][1] == "" and m[7][2] == "" and m[7][3] == "":
            m[7][3] = m[7][0]
            m[7][2] = m[7][4]
            m[7][4] = ""
            m[7][0] = ""
            mostrarestado(m)
            a = 0
            return True
    elif movimiento_n % 2 != 0:
        if x == "C" and control[1] == 0 and control[5] == 0 and m[0][5] == "" and m[0][6] == "":
            m[0][6] = m[0][4]
            m[0][5] = m[0][7]
            m[0][4] = ""
            m[0][7] = ""
            mostrarestado(m)
            a = 0
            return True
        if x == "L" and control[1] == 0 and control[4] == 0 and m[0][1] == "" and m[0][2] == "" and m[0][3] == "":
            m[0][2] = m[0][4]
            m[0][3] = m[0][0]
            m[0][4] = ""
            m[0][0] = ""
            mostrarestado(m)
            a = 0
            return True
    if a != 0:
        print("No se puede realizar el enroque")
        return False
def torre(pi, pf ):
    legal = True
    if pi[0] == pf[0]:
        if pi[1] > pf[1]:
            numero = -1
        else:
            numero = 1
        for a in range(pi[1], pf[1], numero):
            A = m[a][pi[0]]
            if A != "" and A != x:
                legal = False
                break
    elif pi[1] == pf[1]:
        if pi[0] < pf[0]:
            numero = 1
        else:
            numero = -1
        for F in range(pi[0], pf[0], numero):
            A = m[pf[1]][F]
            if A != "" and A != x:
                legal = False
                break
    elif pi[0] != pi[0] or pi[1] != pf[1]:
        print("El movimiento no es legal")
        return False
    if legal == False:
        print("El movimiento no es legal")
        return False
    else:
        print("El movimiento es legal")
        mover(pi, pf)
        return True
def alfil(pi,pf):
    fila = pi[1]
    legal = True
    if pi[0] > pf[0]:
        contador = -1
    else:
        contador = 1
    if pi[1] > pf[1]:
        contador2 = -1
    else:
        contador2 = 1
    for a in range(pi[0] , pf[0], contador):
        A = m[fila][a]
        if A != "" and A != x:
            legal = False
            break
        fila += contador2
    if legal == False:
        print("El movimiento no es legal")
        return False
    else:
        print("El movimiento es legal")
        mover(pi, pf)
        return True
def Caballo(pi, pf):
    mov1  = pf[0] - pi[0]
    mov2 = pf[1] - pi[1]
    mov = str((mov1**2) + (mov2 **2))
    if mov == str(5) and pi[0] != pf[0] and pi[1] != pf[1]:
        print("El movimiento es legal")
        mover(pi, pf)
        return True
    else:
        print("El movimiento no es legal")
        return False
def Peon(pi,pf):
    legal1 = True
    if blancas == True:
        numero = -1
        numero2 = -2
    else:
        numero = 1
        numero2 = 2
    if peonesblancos[pi[0]] == 0:
        if (pi[1] + numero2 == pf[1] or pi[1] + numero == pf[1]) and pi[0] == pf[0]:
            print("Legal")
            legal = True
        else:
            print("No legal")
            legal = False
    else:
        if pi[1] + numero == pf[1] and pi[0] == pf[0]:
            print("Legal")
            legal = True
        else:
            print("No legal")
            legal = False
    if legal == True:
        for a in range(pi[1], pf[1], numero):
            A = m[a][pi[0]]
            if A != "" and A != x:
                legal1 = False
                break
    if legal1 == False:
        print("El movimiento no es legal")
        return False
    else:
        print("El movimiento es legal")
        mover(pi, pf)
        return True
    peonesblancos[pi[0]] += 1
def movimiento_legal(pi, pf):
    if y == "" or y[0] != x[0]:
        if x[1] == "r":
            return torre(pi, pf)
        elif x[1] == "b":
            mov1 = abs(pi[0] - pf[0])
            mov2 = abs(pi[1] - pf[1])
            if mov1 == mov2:
                return alfil(pi, pf)
            else:
                print("El movimiento no es legal")
                return False
        elif x[1] == "q":
            mov1 = abs(pi[0] - pf[0])
            mov2 = abs(pi[1] - pf[1])
            if mov1 == mov2:
                return alfil(pi, pf)
            else:
                return torre(pi, pf)
        elif x[1] == "n":
            return Caballo(pi, pf)
        elif x[1] == "p":
            return Peon(pi, pf)
        else:
            return mover(pi, pf)
    else:
        print("El movimiento no es legal")
        return False

def canviarnumeros(X, Y):
    X[0] = letra[str(X[0]).upper()]
    Y[0] = letra[str(Y[0]).upper()]
    X[1] = numeros[int(X[1])]
    Y[1] = numeros[int(Y[1])]
    return (X, Y)
def mostrarestado(estado):
    for i in estado:
        print(i)
def mover(pi, pf):
    if movimiento_n % 2 == 0:
        if blancas == True:
            m[pf[1]][pf[0]] = x
            m[pi[1]][pi[0]] = ""
            estados.append(copy.deepcopy(m))
            mostrarestado(m)
            return True
        else:
            print("Debes mover una pieza blanca")
            return False
    else:
        if blancas == False:
            m[pf[1]][pf[0]] = x
            m[pi[1]][pi[0]] = ""
            estados.append(copy.deepcopy(m))
            mostrarestado(m)
            return True
        else:
            print("Debes mover una pieza negra")
            return False
while palabra != "Exit":
    palabra = input("Quieres decir una posicion?")
    if palabra.lower() == "exit":
        palabra = input("Quieres ver los movimientos de la partida?")
        if palabra.lower() == "si":
            for i in estados:
                mostrarestado(i)
                print("------------------")
        break
    else:
        contarMovimientos(movimiento_n)
        movimiento = input("Escribe la poscion inicial y final").upper()
        if len(movimiento) == 4:
            pi[0] = str(movimiento[0])
            pi[1] = int(movimiento[1])
            pf[0] = str(movimiento[2])
            pf[1] = int(movimiento[3])
            print(pi)
            canviarnumeros(pi, pf)
            print(pi)
            x = m[pi[1]][pi[0]]
            y = m[pf[1]][pf[0]]
            blancas = comprobarMovimientos(x, blancas)
            legal = movimiento_legal(pi, pf)
            tablero.actualiza(m)
        elif len(movimiento) == 1:
            legal = enroque(movimiento)
            tablero.actualiza(m)
        else:
            print("Escribe bien la posicion")
        if legal == True:
            movimiento_n += 1
