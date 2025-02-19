import numpy as np
import sys

ROW_COUNT=6
COLUMN_COUNT=7

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


game_over=False
turn=0 
piece : int
board=create_board()
print_board(board)

while not game_over:
    #player 1
    if turn==0:
        piece=1
        col=int(input("Player 1 make your move(0-6):"))
        if is_valid_move(board,col):
            row=get_next_open_row(board,col)
            drop_piece(board,col,row,piece)

    #player 2
    if turn==1:
        piece=2
        col=int(input("Player 2 make your move(0-6):"))
        if is_valid_move(board,col):
            row=get_next_open_row(board,col)
            drop_piece(board,col,row,piece)
    
    print_board(board)
    if is_win(board,piece):
        print("Player", piece, "wins!!")
        sys.exit()
    turn=(turn+1)%2