from os import system
from random import randrange
from string import ascii_uppercase, ascii_lowercase
from math import ceil

# wip: end of file for more details

def draw_board(inputlist):
    if len(inputlist) == 0:
        return "inputted list empty"
    if len(inputlist) == 100:
        list_ = []
        for i in range(10):
            temp = []
            for j in range(10):
                temp.append(str(inputlist[i*10+j]))
            list_.append(temp)
    else:
        list_=inputlist.copy()
    output=""
    symwid=len(str(list_[0][0]))
    wid=len(list_[0])
    lsep = "   "
    lheaders = []
    theaders = lsep
    for i in range(10):
        lheaders.append(str(i + 1))
        theaders += " "*ceil(symwid/2)+ascii_uppercase[i]+" "*(symwid//2)
        lheaders[i] += " "
        if len(lheaders[i]) < 3:
            lheaders[i] = " "+lheaders[i]
    theaders += "\n"
    top = lsep+"┌" + ("─"*symwid + "┬")*(wid-1) + "─"*symwid + "┐\n"
    mid = lsep+"├" + ("─"*symwid + "┼")*(wid-1) + "─"*symwid + "┤\n"
    bot = lsep+"└" + ("─"*symwid + "┴")*(wid-1) + "─"*symwid + "┘\n"
    output = theaders+top
    for i in range(10):
        output += lheaders[i]+"│"
        for j in range(10):
            output += list_[i][j]+"│"
        output += "\n"
        if i < 9:
            output += mid
    output += bot
    return output

def decipher(str_:str, vcheck:bool): # deciphers coordinate input into list pos
    if str_ == "exit":
        return "exit"
    numindex,letindex = [],[]
    for i in range(1,11):
        numindex.insert(-i, str(i))
        letindex.append(ascii_lowercase[i-1])
    output, strf, numf = -10,0,0
    for i in range(len(letindex)):
        if str_.find(letindex[i]) != -1:
            output += i
            strf += 1
        if str_.find(numindex[i]) != -1:
            output += 10*int(numindex[i])
            numf += 1
    if strf != 1 or numf != 1:
        return "illegal input"
    elif not p2board[output] == "   ":
        return "not empty"
    if vcheck and str_.find("v") != -1: # if vcheck, output + 1000
        output += 1000
    return output

def shipcheck(board:list, length:int, pos:int, v:bool):
    if len(str(pos)) != 2:
        strpos = "0"+str(pos)
    else:
        strpos = str(pos)
    if int(strpos[-(not v)]) + length > 10:
        return "out of board"
    for i in range(length):
        pos += (v * 9 + 1) * bool(i)
        if board[pos] != "   ":
            return "clipping"
        if (pos != 99)*(board[(pos +1) * (pos != 99)] != "   ") or (pos != 0)*(board[(pos -1) * (pos != 0)] != "   ") or (pos <= 89)*(board[(pos +10) * (pos <= 89)] != "   ") or (pos > 9)*(board[(pos -10) * (pos > 9)] != "   "):
            return "too close"
    return True

def p_input(player:int):
    if player == "" or player == 1:
        global p2board
        print(draw_board(p2board))
    else:
        global p1board
        print(draw_board(p1board))
    spot = input("Where do you want to play? ")
    if spot == "exit":
        return "exit"
    spot = spot.lower()
    output = decipher(spot)
    print(output)
    if output == "illegal input":
        print("Input not recognized")
        return False
    elif output == "not empty":
        print("You already tried that spot")
        return False
    return output

def p_ships(int_:int):
    system("cls")
    board = empty_board()
    ships = [[5, 4, 3, 3, 2], ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"]]
    cancel,i = False,0
    while i < len(ships[0]):
        vert = False
        print(draw_board(board))
        pos = decipher(input(f"Where do you want to place your {ships[1][i]}? (v vor vertical placement) "), 1)
        system("cls")
        if pos == "illegal input":
            print("Input not recognized")
            cancel = True
        elif pos == "exit":
            exit()
        elif pos > 100:
            pos -= 1000
            vert = True
        if cancel == False:
            if board[pos] != "   ":
                print("There is already a ship there")
                cancel = True
            elif cancel == False:
                check = shipcheck(board,ships[0][i],pos,vert)
                if check != True:
                    if check == "clipping":
                        print("Ship is clipping other ship")
                        cancel = True
                    elif check == "out of board":
                        print("Ship is out of the board")
                        cancel = True
                    elif check == "too close":
                        print("You can't place a ship next to another ship")
                        cancel = True
                if cancel == False:
                    for j in range(ships[0][i]):
                        board[pos+j*(vert*9+1)] = " s "   
        i += 1   
        if cancel:
            cancel = False
            i -= 1
    print(draw_board(board))
    input("Ships placed! (press enter to continue...)\n")
    ships_cur = []
    for i in board:
        if i == " s ":
            ships_cur.append(True)
        else:
            ships_cur.append(False)
    if int_ == 2:
        global p2ships
        p2ships = ships_cur.copy()
    else:
        global p1ships
        p1ships = ships_cur.copy()
    return


def empty_board():
    output = []
    for i in range(100):
        output.append("   ")
    return output

def random_board(w:int, h:int, sym:list):
    w = 10
    h = 10
    if sym == "":
        sym = ["*", "x", " ", "o"]
        multi = 3
        for i in range(len(sym)):
            sym[i] = sym[i] * multi
    output = []
    for i in range(h):
        filllist = []
        for j in range(w):
            filllist.append(sym[randrange(len(sym))])
        output.append(filllist)
    return output

p1board = empty_board()
p2board = empty_board()
p1ships, p2ships = [], []

p_ships("")
print(draw_board(p1ships))
print(draw_board(p2ships))


# TBD:
# wincheck
# AI
# game main()