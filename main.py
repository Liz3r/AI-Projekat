
import re

#m i n -> velicna table
#na_potezu -> ko je na potezu (X ILI O)
#xValue -> broj mogucnosti za smestanje plocice na treuntnoj tabli za igraca x
#oValue -> broj mogucnosti za smestanje plocice na treuntnoj tabli za igraca o
# M - vrste
# N - kolone

def start_game():

    global m,n,xIgrac,state
    
    pat = re.compile("[0-9][0-9]?")
    inM = input("unesite broj vrsta: ")
    inN = input("unesite broj kolona: ")
    if(not pat.match(inM) or not pat.match(inN)):
        print("unos nije validan (vrste i kolone)")
        return False
    m = int(inM)
    n = int(inN)

    piPat = re.compile("0|1")
    piIn = input("unesite igraca koji je prvi na potezu (0 - covek, 1 - racnar): ")
    
    if(not piPat.match(piIn)):
        print("unos nije validan (prvi igra)")
        return False
    xIgrac = int(piIn)

    if(m < 3 or n < 3):
        print("Velicina table ne validna, najmanja tabla je 5x5")
        return False
    if(xIgrac != 0 and xIgrac != 1):
        print("unos nije validan")
        return False
    state = {
        "xValue": (m-1)*n,
        "oValue": (n-1)*m,
        "matrica": [[None for b in range(n)] for c in range(m)],
        "na_potezu": 0
    }
    return True

def show_table(state):
    global m,n
    tabla_kolone = "  "
    tabla_ivica = "  "
    for i in range(0,n):
        tabla_kolone += " " + chr(ord("A")+i)
        tabla_ivica += " ="
    print(tabla_kolone)
    print(tabla_ivica)

    kolNum = m
    for row in reversed(state["matrica"]):
        redStr = str(kolNum)+"||"
        redIspod = "  "
        for el in row:
            if(el == None):
                redStr += " |"
                redIspod += " -"
            if(el == "X"):
                redStr += "X|"
                redIspod += " -"
            if(el == "O"):
                redStr += "O|"
                redIspod += " -"
        redStr += "|" + str(kolNum)
        print(redStr)
        if(kolNum != 1):
            print(redIspod)
        kolNum -= 1

    print(tabla_ivica)
    print(tabla_kolone)

def is_valid(state,vrsta,kolona):
    global m,n
    if(state["na_potezu"] == 0):
        if(vrsta < m-1 and vrsta >= 0
        and kolona < n and kolona >= 0
        and state["matrica"][vrsta][kolona] == None 
        and state["matrica"][vrsta+1][kolona] == None):
            return True
    else:
        if(vrsta < m and vrsta >= 0
        and kolona < n-1 and kolona >= 0
        and state["matrica"][vrsta][kolona] == None 
        and state["matrica"][vrsta][kolona+1] == None):
            return True
    return False

def racunaj_XOVal(state):
    stanje_provera = {
    "xValue": state["xValue"],
    "oValue": state["oValue"],
    "matrica": state["matrica"].copy(),
    "na_potezu": state["na_potezu"]
    }
    xVal = 0
    oVal = 0
    for row in range(0, m):
        for col in range(0, n):
            stanje_provera["na_potezu"] = 0
            if(is_valid(stanje_provera,row,col)):
                xVal += 1
            stanje_provera["na_potezu"] = 1
            if(is_valid(stanje_provera,row,col)):
                oVal += 1
    return (oVal,xVal)

#odigrava potez
#oblika (int) (char)
#ne bavi se time ko mu je prosledio potez, samo proverava validnost
#i postavlja potez na tablu ako je validan
def igraj_potez(state,potez):
    global m,n

    pat = re.compile("[0-9][0-9]? [A-Z]")
    if(not pat.match(potez)):
        return False
    p = potez.split(" ")
    vrsta = int(p[0])-1
    kolona = ord(p[1])-64-1

    if(vrsta < 0 or vrsta > m or kolona < 0 or kolona > n):
        return False
    if(state["na_potezu"] == 0):
        #provera validnosti poteza
        if(is_valid(state,vrsta,kolona)):
            state["matrica"][vrsta][kolona] = "X"
            state["matrica"][vrsta+1][kolona] = "X"
            #racunaj promenu xVal i oVal i zapamti u stanju
            xo = racunaj_XOVal(state)
            state["oValue"] = xo[0]
            state["xValue"] = xo[1]
            state["na_potezu"] = 1
            return True
        else:
            return False
    else:
        #provera poteza
        if(is_valid(state,vrsta,kolona)):
            state["matrica"][vrsta][kolona] = "O"
            state["matrica"][vrsta][kolona+1] = "O"
            #racunaj promenu xVal i oVal i zapamti u stanju
            xo = racunaj_XOVal(state)
            state["oValue"] = xo[0]
            state["xValue"] = xo[1]
            state["na_potezu"] = 0
            return True
        else:
            return False

def game_in_progress():
    global state
    if(state["na_potezu"] == 0 and state["xValue"] == 0):
        print("kraj igre\nigrac O je pobedio")
        return False
    if((state["na_potezu"] == 1 and state["oValue"] == 0)):
        print("kraj igre\nigrac X je pobedio")
        return False
    return True

def covek_protiv_coveka():
    global state
    while(not start_game()):
        print("Unesite validne vrednosti")
    show_table(state)

    while(game_in_progress()):
        while(not igraj_potez(state,input("unesite potez: "))):
            print("potez je oblika: 1 A | (int) (veliko slovo)\npotez nije validan, pokusajte ponovo: ")
        show_table(state)
        print(state["oValue"],state["xValue"])
        print(proceni_stanje(state))
########################################

def novo_stanje(state,vrsta,kolona):

    novo_stanje_ret = {
    "xValue": state["xValue"],
    "oValue": state["oValue"],
    "matrica": [x.copy() for x in state["matrica"]],
    "na_potezu": state["na_potezu"],
    "potez": str(vrsta+1) + " " + chr(kolona+65)
    }
    if(vrsta < 0 or vrsta > n or kolona < 0 or kolona > m):
        return False
    if(novo_stanje_ret["na_potezu"] == 0):
        #provera validnosti poteza
        if(is_valid(novo_stanje_ret,vrsta,kolona)):
            novo_stanje_ret["matrica"][vrsta][kolona] = "X"
            novo_stanje_ret["matrica"][vrsta+1][kolona] = "X"
            #racunaj promenu xVal i oVal i zapamti u stanju
            xo = racunaj_XOVal(novo_stanje_ret)
            novo_stanje_ret["oValue"] = xo[0]
            novo_stanje_ret["xValue"] = xo[1]
            novo_stanje_ret["na_potezu"] = 1
            return novo_stanje_ret
        else:
            return False
    else:
        #provera poteza
        if(is_valid(novo_stanje_ret,vrsta,kolona)):
            novo_stanje_ret["matrica"][vrsta][kolona] = "O"
            novo_stanje_ret["matrica"][vrsta][kolona+1] = "O"
            #racunaj promenu xVal i oVal i zapamti u stanju
            xo = racunaj_XOVal(novo_stanje_ret)
            novo_stanje_ret["oValue"] = xo[0]
            novo_stanje_ret["xValue"] = xo[1]
            novo_stanje_ret["na_potezu"] = 0
            return novo_stanje_ret
        else:
            return False

def mogucnosti(state):
    retLista = list()
    for row in range(0, n):
        for col in range(0, m):
            ns = novo_stanje(state,row,col)
            if(ns):
                #show_table(ns)
                retLista.append(ns)
    return retLista

def covek_protiv_racunara():
    global state,xIgrac
    while(not start_game()):
        print("Unesite validne vrednosti")
    show_table(state)

    while(game_in_progress()):
        if(state["na_potezu"] == xIgrac):
            while(not igraj_potez(state,input("unesite potez: "))):
                print("potez je oblika: 1 A | (int) (veliko slovo)\npotez nije validan, pokusajte ponovo: ")
            show_table(state)
            print(state["oValue"],state["xValue"])
        else:
            
            #kompjuter igra potez
            stanj = max_value(state,3,[state,-9999],[state,9999])[0]
            potez = stanj["potez"]
            if(not igraj_potez(state,potez)):
                print("nedozvoljen potez: " + potez)
                break
            show_table(state)
    return True

#racunanje poteza racunara##################################

def proceni_stanje(stanje):
    global xIgrac

    if(xIgrac):
        if(stanje["xValue"] == 0):
            return 999
        if(stanje["oValue"] == 0):
            return -999
        ret = stanje["xValue"] - stanje["oValue"]/6
    else:
        if(stanje["oValue"] == 0):
            return 999
        if(stanje["xValue"] == 0):
            return -999
        ret = stanje["oValue"] - stanje["xValue"]/6
    return ret




def max_value(stanje,dubina,alpha,beta):

    nova_stanja = mogucnosti(stanje)
    if(dubina == 0 or len(nova_stanja) == 0):
        return (stanje,proceni_stanje(stanje))
    else:
        for s in nova_stanja:
            alpha = max(alpha,min_value(s,dubina-1,alpha,beta), key = lambda x: x[1])
            if(alpha[1] >= beta[1]):
                return beta
    return alpha

def min_value(stanje,dubina,alpha,beta):

    nova_stanja = mogucnosti(stanje)
    if(dubina == 0 or len(nova_stanja) == 0):
        return (stanje,proceni_stanje(stanje))
    else:
        for s in nova_stanja:
            beta = min(beta,max_value(s,dubina-1,alpha,beta), key = lambda x: x[1])
            if(beta[1] <= alpha[1]):
                return alpha
    return beta

############################################################

#covek_protiv_coveka()
covek_protiv_racunara()

