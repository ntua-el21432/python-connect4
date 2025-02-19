import numpy as np
import sys
import pygame 
import math
import random

ROW_COUNT=6
COLUMN_COUNT=7

PLAYER=0
AI=1

EMPTY_POS=0
PLAYER_PIECE=1
AI_PIECE=2

WINDOW_LENGTH=4

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

def get_valid_columns(board):
    valid_columns={}
    for col in range(COLUMN_COUNT):
        if is_valid_move(board,col):
            valid_columns.append(col)
    return valid_columns

def count_window(window,piece):
    score=0
    #ai so opponent piece is our piece
    oppon_piec=PLAYER_PIECE
    if piece==PLAYER_PIECE:
        oppon_piece=AI_PIECE
    if window.count(piece)==4:
        score+=1000
    elif window.count(piece)==3 and window.count(EMPTY_POS)==1:
        score+=10
    elif window.count(piece)==2 and window.count(EMPTY_POS)==2:
        score+=5
    elif window.count(oppon_piece)==3 and window.count(EMPTY_POS)==1:
        score-=10
    return score

def heuristic_score(board,piece):
    score=0
    #center column
    center_col_array=[int(i) for i in list(board[:,COLUMN_COUNT//2])]
    center_col_count=center_col_array.count(piece)
    score+=center_col_count * 2
    #horizontal
    for row in range(ROW_COUNT-1):
        row_array=[int(i) for i in list(board[row,:])]
        for col in range(COLUMN_COUNT-3):
            window=row_array[col:col+WINDOW_LENGTH]
            score+=count_window(window,piece)
    
    #vertical
    for col in range (COLUMN_COUNT):
                col_array=[int(i) for i in list(board[:,col])]
                for row in range(ROW_COUNT-3):
                    window=col_array[row:row+WINDOW_LENGTH]
                    score+=count_window(window,piece)

    #positive diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window=[board[row+i][col+i] for i in range(WINDOW_LENGTH)]
            score+=count_window(window,piece)
    
    #negative diagonal
    for row in range(ROW_COUNT-3):
        for col in range(COLUMN_COUNT-3):
            window=[board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
            score+=count_window(window,piece)

    return score

def is_terminal(board):
    return is_win(board,PLAYER_PIECE) or is_win(board,AI_PIECE) or len(get_valid_columns)==0 


def find_best_move(board,piece):
    best_score=-1000
    valid_columns=get_valid_columns(board)
    best_column=random.choice(valid_columns)
    for col in valid_columns:
        row=get_next_open_row(board)
        temp_board=board.copy()
        drop_piece(temp_board,row,col,piece)
        score=heuristic_score(temp_board,piece)
        if score>best_score:
            best_score=score
            best_column=col
    return best_column

def minmax(board,deth,aplha,beta,max_player):
    pass

game_over=False
turn=random.randint(PLAYER, AI)
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
            if turn==PLAYER:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
        pygame.display.update()

        if event.type==pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #player 1
            if turn==PLAYER:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE)) 
                if is_valid_move(board,col):
                    row=get_next_open_row(board,col)
                    drop_piece(board,col,row,PLAYER_PIECE)
                
                if is_win(board,PLAYER_PIECE):
                    label=win_font.render("Player 1 wins!!",1,RED)
                    screen.blit(label,(40,10))
                    game_over=True

                turn=AI
                draw_board(board)
                print_board(board)


    #player 2
    if turn==AI and not game_over:
        col=find_best_move(board,AI_PIECE)
        if is_valid_move(board,col):
            row=get_next_open_row(board,col)
            drop_piece(board,col,row,AI_PIECE)

        if is_win(board,AI_PIECE):
            label=win_font.render("Player 1 wins!!",1,RED)
            screen.blit(label,(40,10))
            game_over=True

        turn=PLAYER
        draw_board(board)
        print_board(board)

    if game_over:
        pygame.time.wait(5000) #wait 5 seconds


    