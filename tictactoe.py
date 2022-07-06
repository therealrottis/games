from random import randrange
from os import system
from time import sleep

def draw_board(inputlist:list):
    list_ = inputlist.copy()
    output = ""
    iterations = 1
    while iterations < 12:
        while iterations % 4 != 0:
            output += list_.pop(0)
            iterations += 1
            if iterations % 4 != 0:
                output += "|"   
        output += "\n"
        if not iterations > 10: 
            output += "-+-+-\n"
        iterations += 1
    return output
def compile_list(inputlist:list):

    list_ = inputlist
    row1 = list_[:3] # group all possible matches into 3-long lists
    row2 = list_[3:6]
    row3 = list_[6:]
    col1 = list_[0], list_[3], list_[6]
    col2 = list_[1], list_[4], list_[7]
    col3 = list_[2], list_[5], list_[8]
    diag1 = list_[0], list_[4], list_[8]
    diag2 = list_[2], list_[4], list_[6]
    rows = [row1, row2, row3] # group all lists into one
    cols = [col1, col2, col3]
    diags = [diag1, diag2]
    all = [rows, cols, diags]
    return all

def search_lines(inputlist:list, find:str, x:str, y:str):
    all = inputlist.copy()
    list_2 = sorted([x, y, find])
    matches = []
    for i in range(len(all)):
        for j in range(len(all[i])):
            if sorted(all[i][j]) == list_2:
                for k in range(len(all[i][j])):
                    if all[i][j][k] == find:
                        matches.insert(len(matches), [i, j, k])
    if matches != []:
        if len(matches) != 1:
            for i in range(len(matches) - 1): # removes random possible matches until 1 left
                matches.pop(randrange(0, len(matches)))
        if matches[0][0] == 0:
            matches = matches[0][1] * 3 + matches[0][2] # horizontal
        elif matches[0][0] == 1:
            matches = matches[0][2] * 3 + matches[0][1] # vertical
        elif matches[0][1] == 0:
            matches = 4 * matches[0][2] # diagonal, tl rb
        else:
            matches = 2 + 2 * matches[0][2] # diagonal, tr lb
        return matches
    else:
        return "not found"
    
def ai_move(list_:list): # inputs both compiled and uncompiled lists
    if len(list_) == 9:
        list_ = compile_list(list_) # V "searches" has all to be searched combos V
    searches = ["o", "o", "x", "x", " ", "o", " ", " ", " ", "x", "o", "x"]
    i = 0
    while i < 12:
        move = search_lines(list_, " ", searches[i], searches[i + 1]) # winning?
        i += 2
        if move == "not found":
            continue    
        sleep(1)
        return move
    return

def wincheck(inputlist):
    list_ = inputlist.copy()
    num = 0
    if len(list_) == 9:
        list_ = compile_list(list_) 
    if search_lines(list_, "x", "x", "x") != "not found":
        return "x"
    elif search_lines(list_, "o", "o", "o") != "not found":
        return "o"
    else: 
        for i in range(len(list_[0])):
            for j in range(len(list_[0][i])):
                if not " " in list_[0][i][j]:
                    num += 1
    if num == 9:
        return True
    else:
        return False

def player_move(inputlist):
    list_ = inputlist
    global pnum
    print(draw_board(list_))    
    while True:
        if mode != "ai":
            print(f"Player {pnum}:")
        move = input("Where do you want to play? (1-9 or row, col)\n")
        if move == "exit":
            exit()
        if (len(move) != 4 and len(move) != 1):
            print(f'"{move}" could not be interpreted')
            continue
        if len(move) == 2:
            system("cls")
            print("Move out of range:", move)
            continue
        if len(move) >= 3:
            move = (int(move[0]) - 1) * 3 + int(move[3])
        move = int(move) - 1 
        if move > 9 or move < 0:
            print("Move out of range:", move)
            continue
        if list_[move] != " ":
            print("That's already taken!")
            continue
        else:
            return move
    
def empty_list():
    list_ = [" "]
    while len(list_) < 9:
        list_.append(" ")
    return list_

def ai_game():
    list_ = empty_list()
    global tally_singlep
    global tally_ai
    while True:
        if wincheck(list_) == False:
            print(f"You: {tally_singlep} AI: {tally_ai}")
            list_[player_move(list_)] = "x"
            system("cls")
            print(f"You: {tally_singlep} AI: {tally_ai}")
            print(draw_board(list_))
            if wincheck(list_) == False:
                print("The AI is thinking...")
                list_[ai_move(list_)] = "o"
                system("cls")
        else:
            win = wincheck(list_)
            if win == "x":
                win = "You"
                tally_singlep += 1
            elif win == "o":
                win = "The AI"
                tally_ai += 1
            else:
                win = "Nobody"
            system("cls")
            print(f"You: {tally_singlep} AI: {tally_ai}")            
            print(f"{draw_board(list_)} \n{win} won!")
            input("press enter to continue... ")
            return 

def mp_game():
    list_ = empty_list()
    global tally_multip1
    global tally_multip2
    global multip_firstturn
    global pnum
    pnum = multip_firstturn
    if multip_firstturn == 2:
        t1 = ["o", 1]
        t2 = ["x", 2]
    else:
        t1 = ["x", 2]
        t2 = ["o", 1]        
    while True:
        if wincheck(list_) == False:
            print(f"Player 1: {tally_multip1} Player 2: {tally_multip2}")  
            list_[player_move(list_)] = t1[0]
            pnum = t1[1]
            system("cls")
            print(f"Player 1: {tally_multip1} Player 2: {tally_multip2}")    
            if wincheck(list_) == False:
                list_[player_move(list_)] = t2[0]
                pnum = t2[1]
                system("cls") 
        else:
            win = wincheck(list_)
            if win == "x":
                win = "Player 1"
                tally_multip1 += 1
                multip_firstturn = 2
            elif win == "o":
                win = "Player 2"
                tally_multip2 += 1
                multip_firstturn = 1
            else:
                win = "Nobody"
            system("cls")
            print(f"Player 1: {tally_multip1} Player 2: {tally_multip2}")              
            print(f"{draw_board(list_)} \n{win} won!")
            input("press enter to continue... ")
            return     

tally_singlep = 0
tally_ai = 0
tally_multip1 = 0
tally_multip2 = 0
multip_firstturn = 1
pnum = 0
while True:
    system('cls')
    if tally_singlep + tally_ai > 0:
        print(f"You: {tally_singlep}, AI: {tally_ai}\n")    
    elif tally_multip1 + tally_multip2 > 0:
        print(f"Player 1: {tally_multip1}, Player 2: {tally_multip2}\n")    
    mode = input("AI or 1v1 ").lower() # mode selec
    print(mode)
    if mode == "exit":
        exit()
    elif mode == "ai" or mode == "sp":
        system("cls")
        ai_game()
    elif mode == "1v1" or mode == "mp":
        system("cls")
        mp_game()