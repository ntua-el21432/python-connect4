import numpy as np
import sys
import pygame 
import math

ROW_COUNT=6
COLUMN_COUNT=7

BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

SQUARESIZE=100
width=COLUMN_COUNT * SQUARESIZE
height=(ROW_COUNT+1) * SQUARESIZE
size=(width,height)
RADIUS=int(SQUARESIZE/2 -4)

screen=pygame.display.set_mode(size)

def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def is_valid_move(board,col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r

def drop_piece(board,col,row,piece):
    board[row][col]=piece

def print_board(board):
    print(np.flip(board,0))

def is_win(board,piece):
    #horizontal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    #vertical check
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    #positive diagonal check
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True
    #negative diagonal check
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True
    return False

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+(SQUARESIZE/2)),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
    pygame.display.update()

game_over=False
turn=0 
piece : int
board=create_board()
print_board(board)

pygame.init()

draw_board(board)
pygame.display.update()
win_font=pygame.font.SysFont("monospace",80)

while not game_over:

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            sys.exit()
        
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn==0:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
            elif turn==1:
                pygame.draw.circle(screen,YELLOW,(posx,int(SQUARESIZE/2)),RADIUS)
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #player 1
            if turn==0:
                piece=1
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE)) 
                if is_valid_move(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,col,row,piece)

            #player 2
            if turn==1:
                piece=2
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))
                if is_valid_move(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,col,row,piece)

            if is_win(board,piece):
                if piece==1:
                    label=win_font.render("Player 1 wins!!",1,RED)
                    screen.blit(label,(40,10))
                elif piece==2:
                    label=win_font.render("Player 2 wins!!",1,YELLOW)
                    screen.blit(label,(40,10))
                game_over=True

            turn=(turn+1)%2

            draw_board(board)
            print_board(board)

            if game_over:
                pygame.time.wait(5000) #wait 5 seconds


    