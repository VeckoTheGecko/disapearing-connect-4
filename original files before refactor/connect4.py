import pygame

# Initializing all the methods etc.
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((850, 850))  # (width,height)

# title and icon
pygame.display.set_caption("Connect 4")
icon = pygame.image.load("assets/four.png")
pygame.display.set_icon(icon)

# loading the player
connect4Image = pygame.image.load("assets/connect4.png")  # 800*700
greytokenImage = pygame.image.load("assets/greytoken.png")  # 88*88
redtokenImage = pygame.image.load("assets/redtoken.png")
yellowtokenImage = pygame.image.load("assets/yellowtoken.png")
win_font = pygame.font.Font("assets/freesansbold.ttf", 64)


def connect4():
    screen.blit(connect4Image, (25, 125))


def grey(x, y):
    screen.blit(greytokenImage, (x, y))


def red(x, y):
    screen.blit(redtokenImage, (x, y))


def yellow(x, y):
    screen.blit(yellowtokenImage, (x, y))


def list_get(lst, string):
    try:
        idx = lst.index(string)
    except:
        return "invalid move"
    return idx


def wintext(turn):
    text = win_font.render((str(turn) + " wins.").upper(), True, (0, 0, 0))
    screen.blit(text, (300, 300))


def iswin(board, turn, row, pos):
    # y=x diagonal
    diagonal1 = [1, 1]
    diagonal2 = [-1, 1]
    rowwin = [0, 1]
    columnwin = [1, 0]
    winconditions = [diagonal1, diagonal2, rowwin, columnwin]
    for condition in winconditions:
        n = 0
        tempcoord = [row, pos]
        while board[tempcoord[0]][tempcoord[1]] == turn:
            if (
                0 <= tempcoord[0] - condition[0] <= 5
                and 0 <= tempcoord[1] - condition[1] <= 6
            ):
                if (
                    board[tempcoord[0] - condition[0]][tempcoord[1] - condition[1]]
                    == turn
                ):
                    tempcoord[0] -= condition[0]
                    tempcoord[1] -= condition[1]
                else:
                    break
            else:
                break

        while board[tempcoord[0]][tempcoord[1]] == turn:
            if board[tempcoord[0]][tempcoord[1]] == turn:
                n += 1
            tempcoord[0] += condition[0]
            tempcoord[1] += condition[1]
            if not ((0 <= tempcoord[0] <= 5 and 0 <= tempcoord[1] <= 6)):
                break
        if n >= 4:
            return True
    return False


players = ["red", "yellow"]
turn = "red"
columnsX = [68.5, 177, 284.5, 392, 500.5, 607.5, 715.5]  # using original png
rowsY = [84, 197, 308, 421, 530.5, 644]
rowsY.reverse()  # so that 0,0 is in the bottom left
# adjusting for layout (+25 or +125) and calibrating to the top-left corner (-44)
for i in range(len(columnsX)):
    columnsX[i] += 25 - 44
for i in range(len(rowsY)):
    rowsY[i] += 125 - 44

pos = 3
state = "ready"
game = "inplay"
board = [["" for i in range(7)] for i in range(6)]


# the game loop
###anything that you want to appear consistently (ie. background colour, images, text etc.) needs to be in the running loop
running = True
while running:
    screen.fill((255, 255, 255))  # background colour; RGB tuple
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # checking if a key is pressed
        if state == "falling":
            freeze = True
        if event.type == pygame.KEYDOWN:  # only done once key pushed down
            if event.key == pygame.K_LEFT:
                if pos > 0:
                    pos -= 1
            if event.key == pygame.K_RIGHT:
                if pos < 6:
                    pos += 1
            if event.key == pygame.K_RETURN or event.key == pygame.K_DOWN:
                if state == "ready" and game != "over":
                    state = "falling"
                    temp = []
                    for i in board:
                        temp.append(i[pos])
                    row = list_get(temp, "")
                    if row != "invalid move":
                        board[row][pos] = turn
                        if iswin(board, turn, row, pos):
                            game = "over"
                        elif turn == "red":
                            turn = "yellow"
                        else:
                            turn = "red"

                    else:
                        state = "ready"

                    state = "ready"  ###
                print(board)

    if state == "ready":
        if turn == "red":
            red(columnsX[pos], 18)
        if turn == "yellow":
            yellow(columnsX[pos], 18)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == "red":
                red(columnsX[j], rowsY[i])
            elif board[i][j] == "yellow":
                yellow(columnsX[j], rowsY[i])
            else:
                pass

    connect4()
    if game == "over":
        wintext(turn)

    pygame.display.update()  # this needed to update the screen
