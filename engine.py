from os import system, name   
from time import sleep 

import math
import random

import chess
from pick import pick

# Game meta
__game_name__ = "Chess"
__version__   = "1.0.0"
__author__    = "Bharath Kumar Ravichandran"
__license__   = "GNU GPL v3+"


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
    # Evaluate board score by checking some things about the given move:
    # score += 10 if board.is_capture(move) else 0
    # To actually make the move:
    board.push(move)
    for (piece, value) in [(chess.PAWN, 1), 
                           (chess.BISHOP, 4), 
                           (chess.KING, 0), 
                           (chess.QUEEN, 10), 
                           (chess.KNIGHT, 5),
                           (chess.ROOK, 3)]:
        score += len(board.pieces(piece, is_player1_turn)) * value
        score -= len(board.pieces(piece, not is_player1_turn)) * value
    score += 100 if board.is_checkmate() else 0

    return(score)


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
def print_game_init_ascii_art():
    print(r"""
                                                                                        
 ██████╗██╗  ██╗███████╗███████╗███████╗     ██╗    ██████╗     ██████╗ 
██╔════╝██║  ██║██╔════╝██╔════╝██╔════╝    ███║   ██╔═████╗   ██╔═████╗
██║     ███████║█████╗  ███████╗███████╗    ╚██║   ██║██╔██║   ██║██╔██║
██║     ██╔══██║██╔══╝  ╚════██║╚════██║     ██║   ████╔╝██║   ████╔╝██║
╚██████╗██║  ██║███████╗███████║███████║     ██║██╗╚██████╔╝██╗╚██████╔╝
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝     ╚═╝╚═╝ ╚═════╝ ╚═╝ ╚═════╝                                                           
    
    """)
    return(None)


def print_game_page_ascii_art():
    print(r"""
      
  ______   __                                              __         ______        ______  
 /      \ |  \                                           _/  \       /      \      /      \ 
|  $$$$$$\| $$____    ______    _______   _______       |   $$      |  $$$$$$\    |  $$$$$$\
| $$   \$$| $$    \  /      \  /       \ /       \       \$$$$      | $$$\| $$    | $$$\| $$
| $$      | $$$$$$$\|  $$$$$$\|  $$$$$$$|  $$$$$$$        | $$      | $$$$\ $$    | $$$$\ $$
| $$   __ | $$  | $$| $$    $$ \$$    \  \$$    \         | $$      | $$\$$\$$    | $$\$$\$$
| $$__/  \| $$  | $$| $$$$$$$$ _\$$$$$$\ _\$$$$$$\       _| $$_  __ | $$_\$$$$ __ | $$_\$$$$
 \$$    $$| $$  | $$ \$$     \|       $$|       $$      |   $$ \|  \ \$$  \$$$|  \ \$$  \$$$
  \$$$$$$  \$$   \$$  \$$$$$$$ \$$$$$$$  \$$$$$$$        \$$$$$$ \$$  \$$$$$$  \$$  \$$$$$$ 
                                                                                                                                                                                     
    """)
    return(None)



def print_meta():
    '''
    Function to print game's meta data
    '''
    print("{} {}".format(__game_name__, __version__))
    print("Copyright(C) {}".format(__author__))
    print("License: GPL3+: GNU GPL version 3 or later")
    return None


def print_game_instructions():
    '''
    Function to print game instructions
    '''
    print(" Instructions to play:")
    print(" * Enter all moves in UCI protocol. (Example: g1h3 and e7e8q incase of promotion)")
    print(" * Enter r in input to restart the game.")
    print(" * Enter q in input to quit the game.")
    return None


def get_player2():
    '''
    Function to get number of players(Single player or Multiplayer)
    '''
    pick_title = 'Please select number of players to play the game: '
    pick_options = ['Single player', 'Two player']
    pick_option, index = pick(pick_options, pick_title)
    player2 = "COMPUTER" if(index==0) else "Player2"
    return(player2)


def prompt_two_option_pick(pick_title, pick_options):
    '''
    Function to display two option pick by passing title and options
    It returns a boolean value 'True' for index 0 and 'False' for index 1
    '''
    pick_option, index = pick(pick_options, pick_title)
    pick_bool = True if(index==0) else False
    return(pick_bool)


def initialize_game():
    '''
    Function to initialize all game state and data
    '''
    player2 = get_player2()
    board = chess.Board()
    data = {
        'board': board,
        'player2': player2
    }
    return(data)

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
    print_game_page_ascii_art()
    print_meta()
    print_game_instructions()
    print("\n")
    print(board.unicode(borders=True))
    print("\n")
    return None


def whose_turn(board):
    '''
    Function to return the color of current player
    '''
    if board.turn:
        return("WHITE")
    return("BLACK")


def get_player_move(board, player_turn):
    '''
    Function to prompt current player's input.
    Moves piece and changes player_turn accordingly and returns.
    '''
    move_uci = None
    restart_game = False
    
    while(move_uci==None or move==None):  
        move_uci = None
        while(move_uci==None):
            try:
                move_uci = input("Player{}::Enter your move: ".format(player_turn))
                
                if move_uci and move_uci[0] == "q":
                    pick_title = 'Do you want to quit the game? '
                    pick_options = ['Yes', 'No']
                    quit_game = prompt_two_option_pick(pick_title, pick_options)
                    if(quit_game):
                        raise KeyboardInterrupt()
                    move_uci = None
                    
                elif move_uci and move_uci[0] == "r":
                    pick_title = 'Do you want to restart the game? '
                    pick_options = ['Yes', 'No']
                    restart_game = prompt_two_option_pick(pick_title, pick_options)
                    if(restart_game):
                        data = {
                            'player_turn': player_turn,
                            'restart_game': restart_game
                        }
                        return(data)
                    move_uci = None

            except KeyboardInterrupt:
                exit_game()
        
        try:
            move = chess.Move.from_uci(move_uci)
        except:
            move = None
            render_board(board)
            print("Sorry, entered move is invalid. Please try again.")

    if move in board.legal_moves:
        board.push(move)
        render_board(board)

        player_turn = print_move(move_uci, player_turn, False)
    
    else:
        render_board(board)
        print("Sorry, entered move is invalid. Please try again.")
    
    data = {
        'player_turn': player_turn,
        'restart_game': restart_game
    }
    return(data)
      

def print_move(move_uci, player_turn, is_player_computer):
    '''
    Function to print past move and changes & returns player_turn accordingly
    '''
    move_uci = str(move_uci)
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
    
    return(player_turn)


def exit_game():
    print("Closing game...")
    sleep(1)
    exit()

def start_game():
    '''
    Main function of the game which starts/runs the game
    '''
    print_game_init_ascii_art()
    sleep(2)
    while True:
        # Game state variables
        game_over    = False
        player2      = "COMPUTER"
        restart_game = False

        game_data = initialize_game()
        board = game_data['board']
        player2 = game_data['player2']

        render_board(board)

        while not(game_over or restart_game):
            player_turn = 1
            
            while(player_turn==1 and restart_game==False):
                move_data = get_player_move(board, player_turn)
                player_turn = move_data['player_turn']
                restart_game = move_data['restart_game']
                
            while(player_turn==2 and restart_game==False):

                if(player2=="COMPUTER"):
                    player2_move_uci = str(get_opponent_move(board))
                    try:
                        player2_move = chess.Move.from_uci(player2_move_uci)
                    except:
                        print("Invalid move returned by computer.")
                        player2_move_uci = None
                        player2_move = None
                    board.push(player2_move)

                    player_turn = print_move(player2_move_uci, player_turn, True)
                    
                else:
                    move_data = get_player_move(board, player_turn)
                    player_turn = move_data['player_turn']
                    restart_game = move_data['restart_game']
                    if(restart_game==True):
                        continue

            game_over = board.is_game_over()

            if(game_over):
                pick_title = 'Do you want to restart the game? '
                pick_options = ['Yes', 'No']
                restart_game = prompt_two_option_pick(pick_title, pick_options)
                

        if not restart_game:
            return None  

    return None  
    
    
start_game()

