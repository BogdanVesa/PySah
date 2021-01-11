import pygame as p
import ChessEngine

p.init()

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("ImagesChess/"+ piece +".png"), (SQ_SIZE, SQ_SIZE))

def main():
    p.init()
    p.display.set_caption('Pysah')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False

    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                if move.isPawnPromotion:
                                    gs.whiteToMove = not gs.whiteToMove
                                    pieceType = getChoice(screen, gs)
                                    gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + pieceType
                                    gs.whiteToMove = not gs.whiteToMove
                                moveMade = True
                                animate =True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks=[sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        if moveMade:
            if animate:
                animatedMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver =True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS)
        p.display.flip()

'''''
Highlight
'''''
def highLight(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c =sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #patrat selectat
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #miscari posibile
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highLight(screen, gs ,validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color(236, 217, 198), p.Color(96, 64, 32)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def getChoice(screen, gs):
    allycolor ='w' if gs.whiteToMove else 'b'
    p.draw.rect(screen, p.Color(153, 102, 51), p.Rect(WIDTH // 2 - 100, HEIGHT // 2, SQ_SIZE * 4 - 40, SQ_SIZE))
    screen.blit(IMAGES[allycolor + 'Q'], p.Rect(WIDTH//2-100, HEIGHT//2, SQ_SIZE, SQ_SIZE))
    screen.blit(IMAGES[allycolor + 'R'], p.Rect(WIDTH//2-50, HEIGHT//2, SQ_SIZE, SQ_SIZE))
    screen.blit(IMAGES[allycolor + 'N'], p.Rect(WIDTH//2, HEIGHT//2, SQ_SIZE, SQ_SIZE))
    screen.blit(IMAGES[allycolor + 'B'], p.Rect(WIDTH//2+50, HEIGHT//2, SQ_SIZE, SQ_SIZE))
    p.display.update(HEIGHT//2, HEIGHT//2, (WIDTH//2-200), (WIDTH//2+200))
    while True:
        for event in p.event.get():
            if event.type == p.MOUSEBUTTONDOWN:
                if HEIGHT//2 < event.pos[1] < HEIGHT//2+50:
                    if WIDTH//2-100 < event.pos[0] < WIDTH//2-50:
                        return "Q"
                    elif WIDTH//2-50 < event.pos[0] < WIDTH//2:
                        return "R"
                    elif WIDTH//2 < event.pos[0] < WIDTH//2+50:
                        return "N"
                    elif WIDTH//2+50 < event.pos[0] < WIDTH//2+100:
                        return "B"


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
'''''
Animatie
'''''
def animatedMove(move, screen, board, clock):
    global colors
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framePerSquare = 10
    frameCount =(abs(dr)+ abs(dc)) * framePerSquare
    for frame in range(frameCount+1):
        r, c =(move.startRow + dr*frame/frameCount, move.startCol + dc*frame/frameCount )
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow+move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2- textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))
if __name__ == "__main__":
    main()
