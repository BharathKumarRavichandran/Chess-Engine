from os import system, name   
from time import sleep 

import math
import random

import chess
from pick import pick

# Game state variables
game_over = False
player2   = "COMPUTER"


# General functions
def clear():
    '''
    Function to clear terminal window
    '''
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


# Engine algorithms 
def evaluate_board_score(board, move, is_player1_turn):
    '''
    Function to evaluate board score and return the board score
    '''
    score = random.random()
    ## Check some things about this move:
    # score += 10 if board.is_capture(move) else 0
    # To actually make the move:
    board.push(move)
    # Now check some other things:
    for (piece, value) in [(chess.PAWN, 1), 
                           (chess.BISHOP, 4), 
                           (chess.KING, 0), 
                           (chess.QUEEN, 10), 
                           (chess.KNIGHT, 5),
                           (chess.ROOK, 3)]:
        score += len(board.pieces(piece, is_player1_turn)) * value
        score -= len(board.pieces(piece, not is_player1_turn)) * value
    score += 100 if board.is_checkmate() else 0

    return score


def minimax (curDepth, nodeIndex, maxTurn, scores, targetDepth): 
    '''
    Function to find optimal value using mini-max algorithm
    '''
    # base case: targetDepth reached 
    if (curDepth == targetDepth):  
        return scores[nodeIndex] 
      
    if (maxTurn): 
        return max(minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth), minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth)) 
    else: 
        return min(minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth), minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth)) 


# Game initialization functions
def print_meta():
    '''
    Function to print game's meta data
    '''
    print("\n")
    print("Chess 1.0.0")
    print("Copyright(C) Bharath Kumar Ravichandran")
    print("License : GPL3+: GNU GPL version 3 or later")


def print_game_instructions():
    '''
    Function to print game instructions
    '''
    pass


def get_player2():
    '''
    Function to get number of players(Single player or Multiplayer)
    '''
    pick_title = 'Please select number of players to play the game: '
    pick_options = ['Single player', 'Two player']
    pick_option, index = pick(pick_options, pick_title)
    player2 = "COMPUTER" if(index==0) else "Player2"
    return(player2)


def initialize_game():
    '''
    Function to initialize all game state and data
    '''
    global player2
    player2 = get_player2()
    board = chess.Board()
    return board

# Game functions
def get_opponent_move(board):
    '''
    Function to return optimal opponent move using mini-max algorithm by evaluating board score.
    ''' 
    moves = list(board.legal_moves)
    scores = []
    
    for index, move in enumerate(moves):
        board_copy = board.copy()
        # go through board and return a score
        move.score = evaluate_board_score(board_copy, move, board.turn)
        moves[index].score = move.score
        scores.append(move.score)
  
    treeDepth = math.log(len(scores), 2)
    #index = minimax(0, 0, True, scores, treeDepth)
    optimal_move = moves[index]

    return(optimal_move)


def render_board(board):
    '''
    Function to clear game screen and re-render chessboard and restore game state
    '''
    clear()
    print_meta()
    print("\n")
    print(board)
    print("\n")


def whose_turn(board):
    '''
    Function to return the color of current player
    '''
    if board.turn:
        return "WHITE"
    return "BLACK"


def get_player_move(board, player_turn):
    '''
    Function to prompt current player's input.
    Moves piece and changes player_turn accordingly and returns.
    '''
    move_uci = input("Player{}::Enter your move (in UCI): ".format(player_turn))
    move = chess.Move.from_uci(move_uci)
    
    if move in board.legal_moves:
        board.push(move)
        render_board(board)

        player_turn = print_move(move_uci, player_turn, False)
    
    else:
        render_board(board)
        print("Sorry, the entered move is not possible")
    
    return(player_turn)
      

def print_move(move_uci, player_turn, is_player_computer):
    '''
    Function to print past move and changes & returns player_turn accordingly
    '''
    move_from = move_uci[:2]
    move_to = move_uci[2:4]
    promotion = move_uci[3]
    if(is_player_computer):
        print("Computer moved piece from {} to {}".format(move_from, move_to))
    else:
        print("Player{} moved piece from {} to {}".format(player_turn, move_from, move_to))
    
    if(player_turn==1):
        player_turn = 2
    elif(player_turn==2 or is_player_computer):
        player_turn = 1
    
    return player_turn
  
board = initialize_game()
render_board(board)


while not game_over:
    player_turn = 1
    
    while(player_turn==1):
        player_turn = get_player_move(board, player_turn)
        
    while(player_turn==2):

        if(player2=="COMPUTER"):
            player2_move_uci = get_opponent_move(board)
            player2_move = chess.Move.from_uci(player2_move_uci)
            board.push(player2_move)

            player_turn = print_move(player2_move_uci, player_turn, True)
            
        else:
            player_turn = get_player_move(board, player_turn) 


    game_over = board.is_game_over()
        
