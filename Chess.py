from colorama import init, Fore, Back, Style
import re
import os

init()

#Legend
legend = """//Legend
K = King
Q = Queen
B = Bishop
H = Horse
T = Tower
P = Pawn
"""

#Chessboard
chessboard = """ _______________________________________
|     a   b   c   d   e   f   g   h     |
| 8 | X1 | X2 | X3 | X4 | X5 | X6 | X7 | X8 | 8 |
|                                       |
| 7 | X9 | X10 | X11 | X12 | X13 | X14 | X15 | X16 | 7 |
|                                       |
| 6 | X17 | X18 | X19 | X20 | X21 | X22 | X23 | X24 | 6 |
|                                       |
| 5 | X25 | X26 | X27 | X28 | X29 | X30 | X31 | X32 | 5 |
|                                       |
| 4 | X33 | X34 | X35 | X36 | X37 | X38 | X39 | X40 | 4 |
|                                       |
| 3 | X41 | X42 | X43 | X44 | X45 | X46 | X47 | X48 | 3 |
|                                       |
| 2 | X49 | X50 | X51 | X52 | X53 | X54 | X55 | X56 | 2 |
|                                       |
| 1 | X57 | X58 | X59 | X60 | X61 | X62 | X63 | X64 | 1 |
|     a   b   c   d   e   f   g   h     |
 ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾"""

#Pieces
blackPieces = {
    1: "T",
    2: "H",
    3: "B",
    4: "Q",
    5: "K",
    6: "B",
    7: "H",
    8: "T",
    9: "P",
    10: "P",
    11: "P",
    12: "P",
    13: "P",
    14: "P",
    15: "P",
    16: "P",
}
whitePieces = {
    49: "P",
    50: "P",
    51: "P",
    52: "P",
    53: "P",
    54: "P",
    55: "P",
    56: "P",
    57: "T",
    58: "H",
    59: "B",
    60: "Q",
    61: "K",
    62: "B",
    63: "H",
    64: "T"
}
moveRules = {
    "K": [1, 8, 7, 9],
    "Q": [*range(1, 8), *range(8, 64, 8), *range(7, 49, 7), *range(9, 81, 9)],
    "B": [*range(7, 49, 7), *range(9, 81, 9)],
    "H": [6, 10, 15, 17],
    "T": [*range(1, 8), *range(8, 64, 8)],
    "P": [7, 8, 9, 16]
}

#Board numbering
positionNumberDict = {}
indexNum = 0

for i in range(8, 0, -1):
    indexNum += 1
    positionNumberDict[i] = range(8 * indexNum - 7, 8 * indexNum + 1)

positionLetterDict = {}
letterNum = 0

for letter in re.findall("[a-z]", chessboard)[0:8]:
    letterNum += 1
    positionLetterDict[letter] = letterNum

#Error output
def error(num):
    errors = [
        "[ERROR]: Please use the proper move format (e.g. d2)",
        "[ERROR]: You don't have a piece on this field!",
        "[ERROR]: Impossible move!",
        "[ERROR]: Suicide!"
    ]
    print(Style.BRIGHT + Fore.RED + errors[num] + Style.RESET_ALL)

#Check whether the move is correct
def checkMove(pos, turn, start):
    #Move format
    try:
        int(pos[1])
    except:
        error(0)
        return False

    if ord(pos[0]) - 96 > 8 or int(pos[1]) < 1 or int(pos[1]) > 8 or len(pos) != 2 or not pos[0].isalpha():
        error(0)
        return False

    #Check whether the piece belongs to the player
    piece = findPiece(pos)

    if start and (not checkField(piece) or turn == "WHITE" and checkField(piece)[0] != "white" or turn == "BLACK" and checkField(piece)[0] != "black"):
        error(1)
        return False
    
    #Check whether the move is possible
    moveLength = startPiece - piece

    if not start and (abs(moveLength) not in moveRules[(turn == "WHITE" and whitePieces or blackPieces)[startPiece]] or
        checkField(startPiece)[1] == "P" and
            ((turn == "WHITE" and moveLength < 0 or turn == "BLACK" and moveLength > 0) or
            (abs(moveLength) == 7 or abs(moveLength) == 9) and (not checkField(piece) or turn == "WHITE" and checkField(piece)[0] != "black" or turn == "BLACK" and checkField(piece)[0] != "white") or
            abs(moveLength) == 16 and (turn == "WHITE" and startPiece not in range(51, 58) or turn == "BLACK" and startPiece not in range(9, 17)) or
            (abs(moveLength) == 8 or abs(moveLength) == 16) and checkField(piece)) or
        checkField(startPiece)[1] == "T" and
            checkPath(startPiece, piece) or
        checkField(startPiece)[1] == "B" and
            checkPath(startPiece, piece, True) or
        checkField(startPiece)[1] == "Q" and
            (moveStart[0] != moveEnd[0] and moveStart[1] != moveEnd[1] and checkPath(startPiece, piece, True) or (moveStart[0] == moveEnd[0] or moveStart[1] == moveEnd[1]) and checkPath(startPiece, piece))):
        error(2)
        return False
    
    #Check whether the move is suicide
    if not start and checkField(piece) and (turn == "WHITE" and checkField(piece)[0] == "white" or turn == "BLACK" and checkField(piece)[0] == "black"):
        error(3)
        return False
        
    return True

#Locate pieces on the board
def findPiece(pos):
    try:
        letter = pos[0]
        number = int(pos[1])
        return positionNumberDict[number][positionLetterDict[letter] - 1]
    except:
        return None

#Check what's on the field
def checkField(num):
    if num in whitePieces:
        return ["white", whitePieces[num]]
    elif num in blackPieces:
        return ["black", blackPieces[num]]
    else:
        return None

#Check for obstacles on the piece's path
def checkPath(start, end, diagonal=False):
    num = diagonal and (turn == "WHITE" and (ord(moveStart[0]) - 96 > ord(moveEnd[0]) - 96 and 9 or 7) or (ord(moveStart[0]) - 96 < ord(moveEnd[0]) - 96 and 9 or 7)) or (abs(start - end) > 7 and 8 or 1)

    for i in range((end > start and start + num or start - num), end, (end > start and num or -num)):
        if checkField(i):
            return True
    return False

#Main loop
victory = None
whitePoints = 0
blackPoints = 0
turnCount = 0

while True:
    turnCount += 1
    turn = None

    #Chessboard display
    print(legend)
    print(f"""//Points
White: {whitePoints}
Black: {blackPoints}""")
    print("               || CHESS ||")
    tempBoard = chessboard

    #Checker pattern
    fieldBool = False

    for field in range(1, 65):
        search = re.search(" ([A-Z]\d+) (?=\|)", tempBoard)
        colour = fieldBool and (field % 2 == 0 and Back.WHITE or Back.GREEN) or (field % 2 == 0 and Back.GREEN or Back.WHITE)

        if field % 8 == 0:
            fieldBool = not fieldBool

        tempBoard = tempBoard[:search.span()[0]] + colour + search.group() + Style.RESET_ALL + tempBoard[search.span()[1]:]

    #Pieces
    for i in range(1, 65):
        if i in whitePieces:
            tempBoard = re.sub(f" X{i}(?= ) ", Style.BRIGHT + Fore.WHITE + f" {whitePieces[i]} " + Style.RESET_ALL, tempBoard)
        elif i in blackPieces:
            tempBoard = re.sub(f" X{i}(?= ) ", Fore.BLACK + f" {blackPieces[i]} " + Style.RESET_ALL, tempBoard)
        else:
            tempBoard = re.sub(f"X{i}(?= )", " ", tempBoard)
    print(tempBoard)

    #Game end
    if victory:
        print(Style.BRIGHT + Fore.GREEN + f"[GAME END]: {victory} wins!" + Style.RESET_ALL)
        input("Press any key to continue...")
        exit()

    #Check whose turn it is
    if turnCount % 2 != 0:
        turn = "WHITE"
    else:
        turn = "BLACK"

    #Move input
    while True:
        moveStart = input(f"[{turn}]: Input move start: ")
        startPiece = findPiece(moveStart)

        if checkMove(moveStart, turn, True):break
    
    while True:
        moveEnd = input(f"[{turn}]: Input move end: ")
        endPiece = findPiece(moveEnd)

        if checkMove(moveEnd, turn, False):break

    #Modificating the chessboard
    pieces = turn == "WHITE" and "whitePieces" or "blackPieces"

    #Capturing
    if checkField(endPiece):
        enemyPieces = turn == "WHITE" and "blackPieces" or "whitePieces"

        if globals()[enemyPieces][endPiece] == "K":
            victory = turn == "WHITE" and "White" or "Black"

        del globals()[enemyPieces][endPiece]
        globals()[f"{pieces[:5]}Points"] += 1

    #Piece movement
    globals()[pieces][endPiece] = globals()[pieces][startPiece]
    del globals()[pieces][startPiece]

    #Console refreshing
    os.system("cls")