import interfaz
from interfaz import RepresentaTablero
import copy
from flask import Flask , request , jsonify
from flask_cors import CORS
from math import sqrt
app = Flask(__name__)
CORS(app)
#       a      b    c      d     e     f     g     h
m = [["Br1", "Bn", "Bb", "Bq", "Bk", "Bb", "Bn", "Br2"],  # 8
     ["Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp", "Bp"],  # 7
     ["", "", "", "", "", "", "", ""],  # 6
     ["", "", "", "", "", "", "", ""],  # 5
     ["", "", "", "", "", "", "", ""],  # 4
     ["", "", "", "", "", "", "", ""],  # 3
     ["Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp", "Wp"],  # 2
     ["Wr1", "Wn", "Wb", "Wq", "Wk", "Wb", "Wn", "Wr2"]]  # 1
estados = [[]]
tablero = RepresentaTablero(m)
estados.append(copy.deepcopy(m))
palabra = ""
movimiento_n = 0
letra = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
numeros = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0}
control = [0, 0, 0, 0, 0, 0]  # 1: WK 2: BK 3: WR1 4: WR2 5: BR1 6: BR2
blancas = True
def contarMovimientos(x):
    if x % 2 == 0:
        print("Mueve el blanco")
        color = "Blanco"
    else:
        print("Mueve el negro")
        color = "Negro"
    return color
def comprobarMovimientos(x):
    z = True
    if x[0] == "W" and movimiento_n % 2 == 0:
        z = True
        if x == "Wk":
            control[0] += 1
        elif x == "Wr1":
            control[2] += 1
        elif x == "Wr2":
            control[3] += 1
    elif x[0] == "B" and movimiento_n % 2 != 0:
        z = False
        if x == "Bk":
            control[1] += 1
        elif x == "Br1":
            control[4] += 1
        elif x == "Br2":
            control[5] += 1
    return z
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
def torre(mov, x, y):
    legal = True
    if mov[0] == mov[2]:
        if mov[1] > mov[3]:
            numero = -1
        else:
            numero = 1
        for a in range(mov[1], mov[3], numero):
            A = m[a][mov[0]]
            if A != "" and A != x:
                legal = False
                break
    elif mov[1] == mov[3]:
        if mov[0] < mov[2]:
            numero = 1
        else:
            numero = -1
        for F in range(mov[0], mov[2], numero):
            A = m[mov[3]][F]
            if A != "" and A != x:
                legal = False
                break
    elif mov[0] != mov[0] or mov[1] != mov[3]:
        print("El movimiento no es legal")
        return False
    if legal == False:
        print("El movimiento no es legal")
        return False
    else:
        print("El movimiento es legal")
        mover(mov, x, y)
        return True
def alfil(mov, x ,y):
    fila = mov[1]
    legal = True
    if mov[0] > mov[2]:
        contador = -1
    else:
        contador = 1
    if mov[1] > mov[3]:
        contador2 = -1
    else:
        contador2 = 1
    for a in range(mov[0], mov[2], contador):
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
        mover(mov, x, y)
        return True
def Caballo(mov, x, y):
    mov1 = mov[2] - mov[0]
    mov2 = mov[3] - mov[1]
    mov = str((mov1 ** 2) + (mov2 ** 2))
    if mov == str(5) and mov[0] != mov[2] and mov[1] != mov[3]:
        print("El movimiento es legal")
        mover(mov, x, y)
        return True
    else:
        print("El movimiento no es legal")
        return False
def Peon(mov,x,y):
    legal = True
    legal1 = True
    if blancas == True:
        numero = -1
        numero2 = -2
        color = "B"
    else:
        numero = 1
        numero2 = 2
        color = "W"
    if mov[1] == 1 or mov[1] == 6: #Movimiento 2 casillas peon
        if (mov[1] + numero2 == mov[3] or mov[1] + numero == mov[3]) and mov[0] == mov[2] and y == "":
            if m[mov[3]][mov[2] + 1] == color + "p" : #Captura al paso
                m[mov[1] + numero][mov[0]] = color + "p"
                m[mov[1]][mov[0]] = ""
                m[mov[3]][mov[2] + 1] = ""

                mostrarestado(m)
                return True
            elif m[mov[3]][mov[2] - 1] == color + "p":
                m[mov[1] + numero][mov[0]] = color + "p"
                m[mov[1]][mov[0]] = ""
                m[mov[3]][mov[2] - 1] = ""
                mostrarestado(m)
                return True
            else:
                legal = True
        else:
            legal = False
    elif mov[0] != mov[2]: #Peon mata
        if ((mov[0] + 1 == mov[2] or mov[0] - 1 == mov[2]) and mov[1]  + numero == mov[3]) and y != "":
            legal1 = True
        else:
            legal1 = False
    else: #Movimiento 1 casilla peon
        if mov[1] + numero == mov[3] and mov[0] == mov[2]:
            legal = True
        else:
            legal = False

    if legal == True:
        for a in range(mov[1], mov[3], numero):
            A = m[a][mov[0]]
            if A != "" and A != x:
                legal1 = False
                break
    else:
        legal1 = False
    if legal1 == False:
        print("El movimiento no es legal")
        return False
    else:
        print("El movimiento es legal")
        piezas = {"reina" : "q" , "caballo" : "n" , "alfil" : "b" , "torre" : "r1"}
        if (blancas == True and mov[3] == 0) or (blancas == False and mov[3] == 7):
            canvio = True
            canvioPeon = input("Por que pieza quieres canviar el peon: Reina, Caballo, Alfil o Torre").lower()
            if blancas == True:
                color = "W"
            else:
                color = "B"
        else:
            canvio = False
        if canvio == True:
            m[mov[3]][mov[2]] = color + piezas[canvioPeon]
            m[mov[1]][mov[0]] = ""
            mostrarestado(m)
        else:
            mover(mov, x, y)
        return True

def movimiento_legal(mov , x,y):
    if y == "" or y[0] != x[0]:
        if x[1] == "r":
            return torre(mov, x, y)
        elif x[1] == "b":
            mov1 = abs(mov[0] - mov[2])
            mov2 = abs(mov[1] - mov[3])
            if mov1 == mov2:
                return alfil(mov,  x, y)
            else:
                print("El movimiento no es legal")
                return False
        elif x[1] == "q":
            mov1 = abs(mov[0] - mov[2])
            mov2 = abs(mov[1] - mov[3])
            if mov1 == mov2:
                return alfil(mov, x, y)
            else:
                return torre(mov, x, y)
        elif x[1] == "n":
            return Caballo(mov, x, y)
        elif x[1] == "p":
            return Peon(mov,x,y)
        else:
            return mover(mov, x, y)
    else:
        print("El movimiento no es legal")
        return False
def canviarnumeros(X):
    X[0] = letra[str(X[0]).upper()]
    X[2] = letra[str(X[0]).upper()]
    X[1] = numeros[int(X[1])]
    X[3] = numeros[int(X[1])]
    return (X)
def mostrarestado(estado):
    for i in estado:
        print(i)
def mover(mov, x ,y):
    if movimiento_n % 2 == 0:
        if blancas == True:
            m[mov[3]][mov[2]] = x
            m[mov[1]][mov[0]] = ""
            estados.append(copy.deepcopy(m))
            mostrarestado(m)
            return True
        else:
            print("Debes mover una pieza blanca")
            return False
    elif movimiento_n % 2 !=  0:
        if blancas != True:
            m[mov[3]][mov[2]] = x
            m[mov[1]][mov[0]] = ""
            estados.append(copy.deepcopy(m))
            mostrarestado(m)
            return True
        else:
            print("Debes mover una pieza negra")
            return False

#while palabra != "Exit":
#    palabra = input("Quieres decir una posicion?")
#    if palabra.lower() == "exit":
#        palabra = input("Quieres ver los movimientos de la partida?")
#        if palabra.lower() == "si":
#            for i in estados:
#                mostrarestado(i)
#                print("------------------")
#        break
#    else:
#        movimiento = input("Escribe la poscion inicial y final").upper()
#        contarMovimientos(movimiento_n)
#        set_movimientos(movimiento , blancas, legal)


@app.route("/movimiento_externo" , methods=["POST"])
def movimiento_externo():
    global movimiento_n
    datos = request.json
     #palabra = input("Quieres decir una posicion?")
    #if palabra.lower() == "exit":
     #   palabra = input("Quieres ver los movimientos de la partida?")
      #  if palabra.lower() == "si":
       #     for i in estados:
        #        mostrarestado(i)
         #       print("------------------")
    movimiento = datos["movimiento"]
    canviarnumeros(movimiento)
    x = m[movimiento[1]][movimiento[0]]
    y = m[movimiento[3]][movimiento[2]]
    contarMovimientos(movimiento_n)
    blancas = comprobarMovimientos(x)
    legal = movimiento_legal(movimiento, x, y)
    print(blancas)
    print(movimiento_n)
    tablero.actualiza(m)
    tablero.actualiza(m)
    if legal == True:
        movimiento_n += 1
    return jsonify(resultado = m)

app.run(debug=True)