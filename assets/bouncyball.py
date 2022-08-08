import os
import keyboard

def draw_board(board:list):
    output = ""
    for row in board:
        for i in row:
            output += i
        output += "\n"
    return output
    
def empty_board(wid:int, hgt:int):
    output = []
    for row in range(hgt):
        output.append([" "] * wid)
    return output

def phys(x:float,y:float,xvel:float,yvel:float,wid:int,hgt:int):
    x += xvel
    y += yvel
    xvel *= 0.8
    if -0.5 < xvel < 0.5:
        xvel = 0
    if y <= 0:
        y = 0
        if -1 < yvel < 1:
            yvel = 0
        else:
            yvel = -yvel / 2
    else:
        yvel -= 0.1
    if x < 0:
        x = 0
        xvel = -xvel
    elif x > wid:
        x = wid
        xvel = -xvel
    if y > hgt:
        y = hgt
        yvel = -yvel
    return x, y, xvel, yvel

def main():
    x = 50
    y = 2
    xvel = 0
    yvel = 0
    board = empty_board(100,40)
    olds = []
    while True:
        while len(olds) > 10:
            old = olds.pop(0)
            board[old[0]][old[1]] = " "
        wid = len(board[0])-1
        hgt = len(board)-1
        intx, inty = int(round(x)), -int(round(y))-1
        board[inty][intx] = "o"
        olds.append((inty,intx))
        x, y, xvel, yvel = phys(x, y, xvel, yvel, wid, hgt)
        if keyboard.is_pressed("a"):
            xvel -= 0.7
        elif keyboard.is_pressed("d"):
            xvel += 0.7
        if keyboard.is_pressed("w") and y == 0:
            yvel += 2
        if keyboard.is_pressed("e"):
            exit()
        output = draw_board(board)
        output += "wad to move, e to exit"
        os.system("cls")
        print(output)

if __name__ == "__main__":
    main()