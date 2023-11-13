import random
import chess

def load_board(moves_uci):
    """ Load a chess board from a list of moves in UCI format."""
    board = chess.Board()
    for move in moves_uci:
        board.push_uci(move)
    return board

def get_fen_position(moves_uci):
    """ Get the FEN position of a chess board from a list of moves in UCI format."""
    board = load_board(moves_uci)
    return board.fen()

def get_san_moves(moves_uci):
    """ Convert a list of chess moves from UCI to SAN."""
    board = chess.Board()
    san_moves = []
    for move_uci in moves_uci:
        move = chess.Move.from_uci(move_uci)
        san_moves.append(board.san(move))
        board.push(move)
    return san_moves


def make_text_next_move(example):
    """ 
    Generate a text for next move prediction from an example at a random position in the move sequence.
    
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' play d2d4"
    """

    # Pick a random half move, but not the last one
    half_move_count = random.randint(0, len(example["Moves"]) - 1)

    if half_move_count == 0:
        previous_moves = "the Chess starting position"
    else:
        previous_moves = " ".join(example["Moves"][:half_move_count])
    
    next_move = example["Moves"][half_move_count]

    templates = [
        "{previous_moves} {next_move}",
        "{previous_moves} and then {next_move}",
        "{previous_moves} followed by {next_move}",
        "After '{previous_moves}' play {next_move}",
        "In a game of chess, after '{previous_moves}' play {next_move}",
        "In the game of chess, a good move after '{previous_moves}' is {next_move}",
        "In chess, after the sequence '{previous_moves}' a good move is {next_move}",
        "In chess after the moves '{previous_moves}', {next_move} is a good move.",
        
        #"In chess, {next_move} is a good move after the sequence '{previous_moves}'.", # TBD for causal LM
    ]
    template = random.choice(templates)
    return template.format(previous_moves=previous_moves, next_move=next_move)

def make_text_next_move_with_board(example):
    """ 
    Generate a text for next move prediction from an example at a random position in the move sequence converted to FEN position. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "In the position 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2' play d2d4"
    """
    pass

def make_text_next_move_san(example):
    """ 
    Generate a text for next move prediction from an example move sequence converted from UCI to SAN. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e4 e5' play d4"
    Templates can include explicit names of pieces, e.g. "After 'e4 e5' play the pawn to d4"
    """
    pass


def make_text_position_fen(example):
    """ 
    Generate the position FEN resulting from the moves. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' the position is 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2'."
    """
    pass

def make_text_turn(example):
    """ 
    Generate a text for who's turn it is after the moves. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' it's white's turn."
    """
    pass

def make_text_result(example):
    """ 
    Generate a text for the result of the game after the moves. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' the game does not terminate."
    example["Moves"] = ["e2e4", "e7e5", "d2d4", ...] --> "After 'e2e4 e7e5 ...' the game ends in a draw due to insufficient material (score: 1/2-1/2)."
    example["Moves"] = ["e2e4", "e7e5", "d2d4", ...] --> "After 'e2e4 e7e5 ...' the game ends in a win for white due to checkmate (score: 1-0)."
    """
    pass

def make_text_castling(example):
    """ 
    Generate a text for the castling rights after the moves. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' the castling rights are 'KQkq'."
    """
    pass

def make_text_enpassant(example):
    """ 
    Generate a text for the en-passant rights after the moves. 
    example["Moves"] = ["e2e4", "e7e5", "d2d4"] --> "After 'e2e4 e7e5' the en-passant rights are 'e6'."
    """
    pass