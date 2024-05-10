import interfaz
from interfaz import RepresentaTablero
import copy
from flask import Flask , request , jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


turno=1
Tablero = \
    [["Br","Bn","Bb","Bq","Bk","Bb","Bn","Br"],
    ["Bp","Bp","Bp","Bp","Bp","Bp","Bp","Bp"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["Wp","Wp","Wp","Wp","Wp","Wp","Wp","Wp"],
    ["Wr","Wn","Wb","Wq","Wk","Wb","Wn","Wr"]]
representa = RepresentaTablero(Tablero)

Historial=[]
def mover(movimiento):
    if(len(movimiento)==2 or len(movimiento)==4):
        if(movimiento=="EC" or movimiento=="EL"):
            return enroque(movimiento)
        else:
            movimiento_traducido = traducir(movimiento)
            es_legal = movimientos_legales(movimiento_traducido)
            if es_legal:
                Tablero[movimiento_traducido[2]][movimiento_traducido[3]]=Tablero[movimiento_traducido[0]][movimiento_traducido[1]]
                Tablero[movimiento_traducido[0]][movimiento_traducido[1]]=""
                Historial.append(copy.deepcopy(Tablero))
            return es_legal
    return False
def mostrar(Estado):
    for fila in Estado:
        print (fila)

def traducir(movimiento):

    columnas = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
    movimientoTraducido=[
        8-int(movimiento[1]),
        columnas[movimiento[0].upper()],
        8 - int(movimiento[3]),
        columnas[movimiento[2].upper()]
    ]
    return movimientoTraducido

def enroque(movimiento):
    fila=7
    if(turno%2==0):
        fila=0
    if movimiento == "EC":
        for estado in Historial:
            if len(estado[fila][4])>0 and (estado[fila][4][1]!='k' or estado[fila][7][1]!='r'):
                return False
        if Tablero[fila][5]!='' and Tablero[fila][6]!='':
            return False
        Tablero[fila][6] = Tablero[fila][4]
        Tablero[fila][5] = Tablero[fila][7]

        Tablero[fila][4] = ""
        Tablero[fila][7] = ""
        Historial.append(copy.deepcopy(Tablero))
    if movimiento == "EL":
        for estado in Historial:
            if len(estado[fila][4])>0 and (estado[fila][4][1]!='k' or estado[fila][7][1]!='r'):
                return False
        if Tablero[fila][1]!='' and Tablero[fila][2]!='' and Tablero[fila][3]!='':
            return False
        Tablero[fila][3] = Tablero[fila][0]
        Tablero[fila][2] = Tablero[fila][4]

        Tablero[fila][4] = ""
        Tablero[fila][0] = ""
        Historial.append(copy.deepcopy(Tablero))
    return True

def mover_torre(movimiento):
    if(movimiento[0]==movimiento[2] or movimiento[1]==movimiento[3]):
        if(movimiento[0]==movimiento[2]): #movimiento en horizontal
            paso=1
            if(movimiento[1]>movimiento[3]):
                paso=-1
            for i in range(movimiento[1]+paso,movimiento[3],paso):
                if(Tablero[movimiento[0]][i]!=""):
                    return False
            return True
        if (movimiento[1] == movimiento[3]):  #movimiento en vertical
            paso = 1
            if (movimiento[0] > movimiento[2]):
                paso = -1
            for i in range(movimiento[0]+paso,movimiento[2],paso):

                if(Tablero[i][movimiento[1]]!=""):
                    return False
            return True
    return False
def mover_alfil(movimiento):
    if (movimiento[0] != movimiento[2] and movimiento[1] != movimiento[3]):
        num_casillasH = movimiento[2]-movimiento[0]
        num_casillasV = movimiento[3] - movimiento[1]
        vertical=1 #-1=va hacia abajo
        horizontal=1 #-1=va hacia la derecha
        if(movimiento[0]-movimiento[2]>0):
            vertical=-1 # 1=va hacia arriba
        if(movimiento[1]-movimiento[3]>0):
            horizontal=-1 # 1=va hacia la izquierda

        if(abs(num_casillasH)==abs(num_casillasV)):
            for i in range(1,abs(num_casillasV)):
                cols=movimiento[1]+i*horizontal
                filas=movimiento[0]+i*vertical
                if(Tablero[filas][cols]!=""):
                    return False
            return True

    return False
def mover_caballo(movimiento):
    num_casillasH = abs(movimiento[2] - movimiento[0])
    num_casillasV = abs(movimiento[3] - movimiento[1])
    if(num_casillasH+num_casillasV)!=3:
        return False
    return True
def mover_reina(movimiento):
    return mover_alfil(movimiento) or mover_torre(movimiento)

def mover_peon(movimiento):
    paso=-1
    fila=6
    if(turno%2==0):
        paso=1
        fila=1
    #si muevo hacia atras siempre es ilegal 6->7
    if(paso==1 and movimiento[0]>movimiento[2]) or (paso==-1 and movimiento[0]<movimiento[2]):
        return False
    #si muevo 2 tienen que estar en la misma columna, no tiene que haber nada en medio, tiene que mover recto
    #y tiene que empezar en la fila que toca
    if abs(movimiento[0]-movimiento[2])==2 and Tablero[movimiento[2]][movimiento[3]]=="" and Tablero[movimiento[0]+paso][movimiento[1]]=="" and movimiento[1]==movimiento[3] and movimiento[0]==fila:
        return True
    #si muevo en diagonal tengo que comer una pieza,solo puedo mover una casilla y tiene que haber un peon
    if abs(movimiento[1]-movimiento[3])==1 and abs(movimiento[0]-movimiento[2])==1 and Tablero[movimiento[2]][movimiento[3]]!="":
        return True
    #si muevo normal, solo puedo mover una casilla en linea recta, hacia delante, y no tiene que haber nada delante
    if abs(movimiento[0]-movimiento[2])==1 and movimiento[1]==movimiento[3] and Tablero[movimiento[2]][movimiento[3]]=="":
        return True
    return False
def convertirPieza(movimiento):
    fila=0
    letra="W"
    if(turno%2==0):
        fila=7
        letra="B"
    if(movimiento[2]==fila):
        Tablero[movimiento[0]][movimiento[1]]=letra+"q"
def movimientos_legales(movimiento):

    if (movimiento[0] == movimiento[2] and movimiento[1] == movimiento[3]):
        return False
    if (Tablero[movimiento[0]][movimiento[1]] == ""):
        return False
    if (turno % 2 == 0 and Tablero[movimiento[0]][movimiento[1]][0] == 'W'):
        return False
    if (turno % 2 != 0 and Tablero[movimiento[0]][movimiento[1]][0] == 'B'):
        return False
    if(len(Tablero[movimiento[2]][movimiento[3]])>0):
        if (turno % 2 != 0 and Tablero[movimiento[2]][movimiento[3]][0] == 'W'):
            return False
        if (turno % 2 == 0 and Tablero[movimiento[2]][movimiento[3]][0] == 'B'):
            return False
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'r'):
        return mover_torre(movimiento)
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'b'):
        return mover_alfil(movimiento)
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'b'):
        return mover_alfil(movimiento)
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'n'):
        return mover_caballo(movimiento)
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'q'):
        return mover_reina(movimiento)
    if (Tablero[movimiento[0]][movimiento[1]][1] == 'p'):
        legal= mover_peon(movimiento)
        if legal:
            convertirPieza(movimiento)
            return True
        return legal
    return True

#mostrar(Tablero)
#--------------
# para probar movimientos concretos
pruebas =[]
#pruebas=["a2a3","b8b5","a3a4","c8c5","a4a5","d8d5","b2b3"] #Quitar o poner comentario y poner movimientos
#-------------
contador=0
#entrada = input("Movimiento: ")

#while entrada != "exit":
#    entrada=entrada.upper()
#    legal = mover(entrada)
#    if legal is False:
#        print("MOVIMIENTO ILEGAL")
#    else:
#        turno += 1
#        mostrar(Tablero)
#        print("-----------------------")
#    representa.actualiza(Tablero)
    #------Codigo para realizar pruebas-> darle a pruebas los movimientos que queremos hacer los movimientos
#    if len(pruebas)>contador:
#        entrada=pruebas[contador]
##        contador+=1
    #fin codigo para pruebas
##    else:
##        entrada = input("Movimiento: ")


@app.route("/movimiento_externo" , methods=["POST"])
def movimiento_externo():
    datos = request.json
    mov = datos["movimiento"]
    legal= mover(mov)
    global turno
    if legal is False:
        print("MOVIMIENTO ILEGAL")
    else:
        turno += 1
        mostrar(Tablero)
        print("-----------------------")

    return jsonify(resultado = Tablero)

app.run(debug=True)



