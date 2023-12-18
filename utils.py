import random
import chess
from datasets import load_dataset


def uci_to_san(uci_moves, max_half_moves=None):
    # https://en.wikipedia.org/wiki/Algebraic_notation_(chess)#Formatting
    board = chess.Board()
    san_moves = []
    if max_half_moves: uci_moves = uci_moves[:max_half_moves]
    for move_uci in uci_moves:
        move = chess.Move.from_uci(move_uci)
        san_moves.append(board.san(move))
        board.push(move)
    return san_moves

def uci_to_lan(uci_moves, max_half_moves=None):
    # https://en.wikipedia.org/wiki/Algebraic_notation_(chess)#Long_algebraic_notation
    board = chess.Board()
    lan_moves = []
    if max_half_moves: uci_moves = uci_moves[:max_half_moves]
    for move_uci in uci_moves:
        move = chess.Move.from_uci(move_uci)
        lan_moves.append(board.lan(move))
        board.push(move)
    return lan_moves

def uci_to_fen(uci_moves, max_half_moves=None):
    # https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    board = chess.Board()
    if max_half_moves: uci_moves = uci_moves[:max_half_moves]
    for move in uci_moves:
        board.push_uci(move)
    return board.fen()

def uci_to_bitboard(uci_moves, max_half_moves=None):
    board = chess.Board()
    if max_half_moves: uci_moves = uci_moves[:max_half_moves]
    for move in uci_moves:
        board.push_uci(move)
    return str(board)

templates_moves = [
    "{previous_moves} {next_move}",
    "{previous_moves} and then {next_move}.",
    "{previous_moves} followed by {next_move}.",
    "After '{previous_moves}' play {next_move}.",
    "Continue '{previous_moves}' with {next_move}",
    "In a game of chess, after '{previous_moves}' play {next_move}.",
    "In the game of chess, a good move after '{previous_moves}' is {next_move}.",
    "In chess, after the sequence '{previous_moves}' a good move is {next_move}.",
    "In chess after the moves '{previous_moves}', {next_move} is a good move.",
]

templates_fen_move = [
    "In the position '{position}' play {next_move}.",
    "Given the chess position '{position}', a good next move is {next_move}",
    "Starting from the FEN '{position}', a good next move is {next_move}",
]

templates_bitboard_move = [
    "In the position '{position}' play {next_move}.",
    "Given the chess position '{position}', a good next move is {next_move}",
    "Starting from the bitboard position '{position}', a good move is {next_move}",
]

templates_moves_fen = [
    "After '{previous_moves}' the position is '{position}'.",
    "Generate the FEN representation given the PGN of chess game: '{previous_moves}'. The FEN is '{position}'.",
    "Can you produce the FEN code that corresponds to the provided PGN for the chess game: '{previous_moves}'? The FEN notation obtained is '{position}'.",
    "I would appreciate it if you could generate the Forsyth–Edwards Notation (FEN) that corresponds to the given PGN for the chess game: '{previous_moves}'. The FEN code generated is '{position}'.",
    "Please generate the FEN notation for the chess game using the provided PGN: '{previous_moves}'. The obtained FEN representation is '{position}'.",
    "Would you mind generating the FEN code that corresponds to the given PGN for the chess game? The PGN is '{previous_moves}'. The FEN notation generated is '{position}'.",
    "I request you to generate the FEN notation for the given PGN of the chess game: '{previous_moves}'. The FEN code obtained is '{position}'.",
    "Kindly generate the FEN representation that corresponds to the provided PGN of the chess game '{previous_moves}'. The obtained FEN notation is '{position}'.",
    "Could you generate the FEN code for the chess game using the provided PGN: '{previous_moves}'? The FEN notation generated is '{position}'.",
    "It would be great if you could generate the Forsyth–Edwards Notation (FEN) for the chess game using the given PGN '{previous_moves}'. The FEN representation obtained is '{position}'.",
    "May I request you to produce the FEN notation for the provided PGN of the chess game: '{previous_moves}'? The FEN code obtained is '{position}'.",
    "Please generate the FEN code for the chess game based on the provided PGN: '{previous_moves}'. The FEN notation obtained is '{position}'.",
]

templates_moves_bitboard = [
    "After '{previous_moves}' the bitboard position is '{position}'.",
    "Generate the bitboard representation given the PGN of chess game: '{previous_moves}'. The bitboard is '{position}'.",
    "Can you produce the bitboard code that corresponds to the provided PGN for the chess game: '{previous_moves}'? The bitboard obtained is '{position}'.",
    "I would appreciate it if you could generate the bitboard that corresponds to the given PGN for the chess game: '{previous_moves}'. The bitboard code generated is '{position}'.",
    "Please generate the bitboard for the chess game using the provided PGN: '{previous_moves}'. The obtained bitboard representation is '{position}'.",
    "Would you mind generating the bitboard code that corresponds to the given PGN for the chess game? The PGN is '{previous_moves}'. The bitboard generated is '{position}'.",
    "I request you to generate the bitboard for the given PGN of the chess game: '{previous_moves}'. The bitboard obtained is '{position}'.",
    "Kindly generate the bitboard representation that corresponds to the provided PGN of the chess game '{previous_moves}'. The obtained bitboard notation is '{position}'.",
    "Could you generate the bitboard code for the chess game using the provided PGN: '{previous_moves}'? The bitboard generated is '{position}'.",
    "It would be great if you could generate the bitboard for the chess game using the given PGN '{previous_moves}'. The bitboard representation obtained is '{position}'.",
    "May I request you to produce the bitboard for the provided PGN of the chess game: '{previous_moves}'? The bitboard code obtained is '{position}'.",
    "Please generate the bitboard code for the chess game based on the provided PGN: '{previous_moves}'. The bitboard obtained is '{position}'.",
]

templates_moves_result = [
    "After '{moves}' the result is {result}.",
    "A game of chess with the moves '{moves}' ends with the result {result}.",
]

templates_position_move_result = [
    "Given the chess position '{position}', after the move {next_move} the result is {result}.",
    "Starting from the position '{position}' the move {next_move} is played. The game ends with the result {result}.",
]

templates_moves_result_termination = [
    "After '{moves}' the game ends due to {termination} with the result {result}.",
    "A game of chess with the moves '{moves}' ends with the result {result} due to {termination}.",
]

templates_position_move_result_termination = [
    "Given the chess position '{position}', after the move {next_move} the result is {result} due to {termination}.",
    "Starting from the position '{position}' the move {next_move} is played. The game ends due to {termination} with the result {result}.",
]


choices = [
    "uci_nextmove",
    "san_nextmove",
    "lan_nextmove",
    "lan_nextmove_piece",
    "fen_nextmove",
    "fen_position",
    "bitboard_nextmove",
    "bitboard_position",
    "uci_result",
    "san_result",
    "lan_result",
    "uci_result_termination",
    "san_result_termination",
    "lan_result_termination",
    "fen_move_result",
    "bitboard_move_result",
    "fen_move_result_termination",
    "bitboard_move_result_termination",
]


def transform_example(example, fixed_tfm=None):
    tfm = fixed_tfm if fixed_tfm else random.choice(choices)

    if tfm == "uci_nextmove":
        half_moves = random.randint(1, len(example["Moves"])-2)
        previous_moves = " ".join(example["Moves"][:half_moves])
        next_move = example["Moves"][half_moves]

        template = random.choice(templates_moves)
        result = template.format(previous_moves=previous_moves, next_move=next_move)

    elif tfm == "san_nextmove":
        half_moves = random.randint(1, len(example["Moves"])-2)
        moves = uci_to_san(example["Moves"], max_half_moves=half_moves)
        previous_moves = " ".join(moves[:-1])
        next_move = moves[-1]

        template = random.choice(templates_moves)
        result = template.format(previous_moves=previous_moves, next_move=next_move)

    elif tfm == "lan_nextmove":
        half_moves = random.randint(1, len(example["Moves"])-2)
        moves = uci_to_lan(example["Moves"], max_half_moves=half_moves)
        previous_moves = " ".join(moves[:-1])
        next_move = moves[-1]

        template = random.choice(templates_moves)
        result = template.format(previous_moves=previous_moves, next_move=next_move)

    elif tfm == "lan_nextmove_piece":
        half_moves = random.randint(1, len(example["Moves"])-2)
        moves = uci_to_lan(example["Moves"], max_half_moves=half_moves)
        previous_moves = " ".join(moves[:-1])
        next_move = moves[-1]
        if next_move.startswith("N"):
            next_move_piece = f"Night {next_move[1:]}"
        elif next_move.startswith("B"):
            next_move_piece = f"Bishop {next_move[1:]}"
        elif next_move.startswith("R"):
            next_move_piece = f"Rook {next_move[1:]}"
        elif next_move.startswith("Q"):
            next_move_piece = f"Queen {next_move[1:]}"
        elif next_move.startswith("K"):
            next_move_piece = f"King {next_move[1:]}"
        else:
            next_move_piece = f"Pawn {next_move[1:]}"
        next_move_piece = next_move_piece.replace("-", " to ")
        next_move_piece = next_move_piece.replace("x", " captures ")

        template = random.choice(templates_moves)
        result = template.format(previous_moves=previous_moves, next_move=next_move_piece)

    elif tfm == "fen_nextmove":
        half_moves = random.randint(1, len(example["Moves"])-2)
        position = uci_to_fen(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]

        template = random.choice(templates_fen_move)
        result = template.format(position=position, next_move=next_move)

    elif tfm == "fen_position":
        half_moves = random.randint(1, len(example["Moves"])-2)
        position = uci_to_fen(example["Moves"], max_half_moves=half_moves)
        previous_moves = " ".join(example["Moves"][:half_moves])

        template = random.choice(templates_moves_fen)
        result = template.format(position=position, previous_moves=previous_moves)

    elif tfm == "bitboard_nextmove":
        half_moves = random.randint(1, len(example["Moves"])-2)
        position = uci_to_bitboard(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]

        template = random.choice(templates_bitboard_move)
        result = template.format(position=position, next_move=next_move)

    elif tfm == "bitboard_position":
        half_moves = random.randint(1, len(example["Moves"])-2)
        position = uci_to_bitboard(example["Moves"], max_half_moves=half_moves)
        previous_moves = " ".join(example["Moves"][:half_moves])

        template = random.choice(templates_moves_bitboard)
        result = template.format(position=position, previous_moves=previous_moves)

    elif tfm == "uci_result":
        moves = " ".join(example["Moves"])
        result = example["Result"].lower()

        template = random.choice(templates_moves_result)
        result = template.format(moves=moves, result=result)

    elif tfm == "san_result":
        moves = " ".join(uci_to_san(example["Moves"]))
        result = example["Result"].lower()

        template = random.choice(templates_moves_result)
        result = template.format(moves=moves, result=result)

    elif tfm == "lan_result":
        moves = " ".join(uci_to_lan(example["Moves"]))
        result = example["Result"].lower()

        template = random.choice(templates_moves_result)
        result = template.format(moves=moves, result=result)

    elif tfm == "uci_result_termination":
        moves = " ".join(example["Moves"])
        result = example["Result"].lower()
        termination = example["Termination"].lower().replace("_", " ")

        template = random.choice(templates_moves_result_termination)
        result = template.format(moves=moves, result=result, termination=termination)

    elif tfm == "san_result_termination":
        moves = " ".join(uci_to_san(example["Moves"]))
        result = example["Result"].lower()
        termination = example["Termination"].lower().replace("_", " ")

        template = random.choice(templates_moves_result_termination)
        result = template.format(moves=moves, result=result, termination=termination)

    elif tfm == "lan_result_termination":
        moves = " ".join(uci_to_lan(example["Moves"]))
        result = example["Result"].lower()
        termination = example["Termination"].lower().replace("_", " ")

        template = random.choice(templates_moves_result_termination)
        result = template.format(moves=moves, result=result, termination=termination)

    elif tfm == "fen_move_result":
        half_moves = len(example["Moves"]) - 1
        position = uci_to_fen(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]
        result = example["Result"].lower()

        template = random.choice(templates_position_move_result)
        result = template.format(position=position, next_move=next_move, result=result)

    elif tfm == "bitboard_move_result":
        half_moves = len(example["Moves"]) - 1
        position = uci_to_bitboard(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]
        result = example["Result"].lower()

        template = random.choice(templates_position_move_result)
        result = template.format(position=position, next_move=next_move, result=result)

    elif tfm == "fen_move_result_termination":
        half_moves = len(example["Moves"]) - 1
        position = uci_to_fen(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]
        result = example["Result"].lower()
        termination = example["Termination"].lower().replace("_", " ")

        template = random.choice(templates_position_move_result_termination)
        result = template.format(position=position, next_move=next_move, result=result, termination=termination)


    elif tfm == "bitboard_move_result_termination":
        half_moves = len(example["Moves"]) - 1
        position = uci_to_bitboard(example["Moves"], max_half_moves=half_moves)
        next_move = example["Moves"][-1]
        result = example["Result"].lower()
        termination = example["Termination"].lower().replace("_", " ")

        template = random.choice(templates_position_move_result_termination)
        result = template.format(position=position, next_move=next_move, result=result, termination=termination)

    else:
        raise NotImplementedError(f"Transformation {tfm} is not implemented.")

    return result

