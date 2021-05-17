""" Best move generation """

from random import choice
from settings import EVALUATION_POINTS, INF, LETTERS
import abstract as abstract
from pprint import pprint
from datetime import datetime


letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
letters2 = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}


def convert_position(string):
    '''
    '''
    x, y = string[0], string[1]
    x = letters[x]
    y = 8 - int(y)
    return x, y


def best_move(board, turn="black", depth=2):
    """ This function generates the best move for the given position and turn """
    # print("Chosing the move on the following board...")
    chosen_move = minimax(abstract.AbstractBoardADT(copy=(board.moves, board.content)), depth, -INF, INF, False)[0]
    # print("MINIMAX OUTPUT:", chosen_move)
    # print("Looking for", chosen_move[0])
    for row in board.content:
        for piece in row:
            # print(piece)
            try:
                # print(piece, str(piece.pos))
                if piece.pos == chosen_move[0]:
                    # print("Found!")
                    # print("CHOSEN MOVE:", chosen_move)
                    return piece, chosen_move[1]
            except AttributeError:
                pass
    # print("Chose.")


def multidepth_best_move(board, turn="black"):
    """ This function generates the best move for the given position and turn """
    # print("Chosing the move on the following board...")
    pprint(board.content)
    for depth in range(1, 4):
        t1 = datetime.now()
        chosen_move = minimax(abstract.AbstractBoardADT(copy=(board.moves, board.content)), depth, -INF, INF, False)[0]
        t2 = datetime.now()
        print(f"Minimax (depth = {depth}) took {t2-t1}. Chosen move: {chosen_move}")
    # print("MINIMAX OUTPUT:", chosen_move)
    # print("Looking for", chosen_move[0])
    for row in board.content:
        for piece in row:
            # print(piece)
            try:
                # print(piece, str(piece.pos))
                if piece.pos == chosen_move[0]:
                    # print("Found!")
                    # print("CHOSEN MOVE:", chosen_move)
                    return piece, chosen_move[1]
            except AttributeError:
                pass
    # print("Chose.")


def minimax(abstract_board: abstract.AbstractBoardADT, depth: int, alpha, beta, player_turn):
    """ Returns the best move for the black side """
    if abstract_board.is_game_over() or depth == 0:
        # print("returning None, depth =", depth)
        return None, evaluate_board(abstract_board)
    moves = abstract_board.possible_computer_moves()
    # print("Possible moves:", moves)
    current_best_move = choice(moves)

    if player_turn:
        # print("Maximizing board")
        current_max = -INF
        for move in moves:
            piece_from_pos(abstract_board, move[0]).move(convert_position(move[1]))
            new_evaluation = minimax(abstract_board, depth - 1, alpha, beta, False)[1]
            abstract_board.revert_last_move()
            if new_evaluation > current_max:
                current_max = new_evaluation
                current_best_move = (move[0], move[1])
                # print(f"Move {current_best_move} returned evaluation {new_evaluation}, new record")
            alpha = max(alpha, new_evaluation)
            if beta <= alpha:
                break

        return current_best_move, current_max
    else:
        # print("Minimizing board")
        current_min = INF
        for move in moves:
            piece_from_pos(abstract_board, move[0]).move(convert_position(move[1]))
            new_evaluation = minimax(abstract_board, depth - 1, alpha, beta, True)[1]
            abstract_board.revert_last_move()
            if new_evaluation < current_min:
                current_min = new_evaluation
                current_best_move = (move[0], move[1])
                # print(f"Move {current_best_move} returned evaluation {new_evaluation}, new record")
            beta = min(beta, new_evaluation)
            if beta <= alpha:
                break
        return current_best_move, current_min


def piece_from_pos(board, str_pos):
    x, y = LETTERS.index(str_pos[0]), 8 - int(str_pos[1])
    return board.content[y][x]


def evaluate_board(board):
    sum_ = 0
    for row in board.content:
        for piece in row:
            if str(piece) != "0":
                sum_ += EVALUATION_POINTS[str(piece)]
    # print(sum_)
    return sum_


if __name__ == "__main__":
    pass
