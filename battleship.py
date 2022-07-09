from os import system
from random import randrange
from string import ascii_uppercase, ascii_lowercase
from math import ceil
from time import sleep

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
    symwid=3
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
    numindex,letindex = [],[]
    for i in range(1,11):
        numindex.insert(-i, str(i))
        letindex.append(ascii_lowercase[i-1])
    output, strf, numf = -10,0,0
    for i in range(len(letindex)):
        if str_.find(letindex[i]) != -1:
            output += i
            strf += 1
        if str_.find(numindex[i]) != -1 and ((numindex[i] == "1" and numf == 0) or numindex[i] != "1"):
            output += 10*int(numindex[i]) # all weird numindex checking above to stop 10 from
            numf += 1                     # triggering the system once for 10 and once for 1
    if strf != 1 or numf != 1:
        return "illegal input"
    elif not p2board[output] == "   ":
        return "not empty"
    if vcheck and str_.find("v") != -1: # if vcheck, output + 1000
        output += 1000
    return output

def reverse_decipher(int_:int):
    numindex,letindex = [],[]
    for i in range(1,11):
        numindex.append(str(i))
        letindex.append(ascii_uppercase[i-1])
    output = letindex[int_%10] + numindex[int_//10]
    return output

def wincheck(player:int):
    global p1ships
    global p2ships
    if player == "":
        if p1ships.count(True) == 0:
            return 2
        elif p2ships.count(True) == 0:
            return 1
        else:
            return False
    if player == 2:
        check = p2ships
    else:
        check = p1ships
    if check.count(True) == 0:
        return True
    return False
    
def hitcheck(player:int,pos:int):
    if player == 2:
        global p2ships
        check = p2ships
    else:
        global p1ships
        check = p1ships
    if check[pos] == True:
        check[pos] = False
        return True
    return False

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
    if player == 2:
        global p1board
        print(draw_board(p1board))
        player = "(Player 2)"
    else:
        global p2board
        print(draw_board(p2board))
    if player == 1:
        player = "(Player 1)"
    while True:
        spot = input(f"Where do you want to play? {player}")
        spot = spot.lower()
        if spot == "exit":
            exit()
        output = decipher(spot,"")
        if output == "illegal input":
            print("Input not recognized")
        elif output == "not empty":
            print("You already tried that spot")
        else:
            return output

def p_ships(int_:int):
    system("cls")
    board = empty_board()
    ships = [[5, 4, 3, 3, 2], ["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"]]
    cancel,i = False,0
    loc = [[],[],[],[],[]]
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
                        temppos = pos+j*(vert*9+1)
                        loc[i].append(temppos)
                        board[temppos] = " s "   
        i += 1   
        if cancel:
            cancel = False
            i -= 1
    print(draw_board(board))
    ships_cur = []
    for i in board:
        if i == " s ":
            ships_cur.append(True)
        else:
            ships_cur.append(False)
    if int_ == 2:
        global p2ships
        global p2shiploc
        p2ships = ships_cur.copy()
        p2shiploc = loc.copy()
    else:
        global p1ships
        global p1shiploc
        p1ships = ships_cur.copy()
        p1shiploc = loc.copy()
    input("Ships placed! (press enter to continue...)\n")
    system("cls")
    return

def random_ships(player:int):
    output = []
    noprint = False
    if player == 3:
        player = 2
        noprint = True
    for i in range(100):
        output.append("   ")
    ships = [5, 4, 3, 3, 2]
    i = 0
    loc = [[],[],[],[],[]]
    while i < 5:
        vert = randrange(2)
        pos = randrange(100)
        check = shipcheck(output,ships[i],pos,vert)
        if check == True:
            for j in range(ships[i]):
                temppos = pos+j*(vert*9+1)
                loc[i].append(temppos)
                output[temppos] = " s "
            i += 1  
    if not noprint:
        print(draw_board(output))
    input = output.copy()
    output = []
    for i in input:
        if i == " s ":
            output.append(True)
        else:
            output.append(False)
    if player == 2:
        global p2ships
        global p2shiploc
        p2ships = output.copy()
        p2shiploc = loc.copy()
    else:
        global p1ships
        global p1shiploc
        p1ships = output.copy()
        p1shiploc = loc.copy()


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

def start_game(mode:str):
    global p1ships
    global p2ships
    input_ = ""
    if mode == "AI":
        random_ships(3)
        system("cls")
        print("Starting", mode, "game... ")
        while input_ != "y" and input_ != "n":
            input_ = input("Do you want to place your ships? (y/n) ")
            if input_ == "y":
                p_ships(1)
            elif input_ == "n":
                random_ships(1)
                input("Press enter to continue...")
                system("cls")
            elif input_ == "exit":
                exit()
        while wincheck("") == False:
            system("cls")
            print(p2shiploc)
            spot = p_input("")
            system("cls")
            coordspot = reverse_decipher(spot)
            if p2ships[spot]:
                p2board[spot] = " \033[91m"+"X"+"\033[0m "
                for i in range(5):
                    if p2shiploc[i].count(spot):
                        if shipinfo[2][i] != 1:
                            shipinfo[2][i] -= 1
                            print(coordspot, "is a hit!")
                        else:
                            system("cls")
                            print(coordspot, "sinks a ship!")
                            print(f"You have sunk the enemy's {shipinfo[0][i]}!")
                            print(draw_board(p2board))
                            for j in range(shipinfo[3][i]):
                                p2board[p2shiploc[i][j]] = " \033[91m"+"O"+"\033[0m "
                                for k in range(2):
                                    temp1 = str(p2shiploc[i][j])
                                    if len(str(temp1)) == 1:
                                        temp1 = "0"+temp1
                                    temp2 = str(p2shiploc[i][k])
                                    if len(str(temp2)) == 1:
                                        temp2 = "0"+temp2
                                    if int(temp1[k])+int(str((k*9+1))[k]) < 10 and p2board[int(temp1)+(k*9+1)] == "   ":
                                        p2board[int(temp1)+(k*9+1)] = " X "
                                    if int(temp2[k])-int(str((k*9+1))[k]) > -1 and p2board[int(temp2)-(k*9+1)] == "   ":
                                        p2board[int(temp2)-(k*9+1)] = " X "

                        
                
                
            else:
                print(coordspot, "is a miss.")
                p2board[spot] = " X "
            print(draw_board(p2board))
            sleep(1)
        wincheck(1)
        wincheck(2)
            
    else:
        for i in range(1,3):
            input_ = ""
            while input_ != "y" and input_ != "n":
                input_ = input(f"Do you want to place your ships? (Player {i}) (y/n) ")
                if input_ == "y":
                    p_ships(i)
                elif input_ == "n":
                    random_ships(1)
                    input("Press enter to continue...")
                    system("cls")
                elif input_ == "exit":
                    exit()

def main():
    while True:
        system("cls")
        input_ = input("Play 1v1 or against the AI? ").lower()
        system("cls")
        if input_ == "1v1" or input_ == "mp":
            start_game("1v1")
        elif input_ == "ai" or input_ == "sp":
            start_game("AI")
        elif input_ == "exit":
            exit()

p1board = empty_board()
p2board = empty_board()
p1ships, p2ships = [], []
p1shiploc, p2shiploc = [], []
shipinfo = [["Carrier", "Battleship", "Destroyer", "Submarine", "Patrol Boat"],[5,4,3,3,2],[5,4,3,3,2],[5,4,3,3,2]]

main()

# TBD:
# AI, show ai playing
# (wip)game main()