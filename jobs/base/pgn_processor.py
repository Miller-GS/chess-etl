from typing import TextIO
import chess.pgn


class PGNProcessor:
    def __init__(self, pgn_stream: TextIO):
        self.pgn_stream = pgn_stream

    def process_all(self) -> list[dict]:
        games = []
        while True:
            game = self.process_game()
            if game is None:
                break
            games.append(game)
        return games

    def process_game(self) -> dict | None:
        game = chess.pgn.read_game(self.pgn_stream)
        if game is None:
            return None

        game_dict = self._process_headers(game.headers)
        game_dict["plies"] = self._process_moves(game)

        return game_dict

    def _process_headers(self, headers: dict) -> dict:
        return {
            "event": headers["Event"] if headers["Event"] != "?" else None,
            "site": headers["Site"] if headers["Site"] != "?" else None,
            "date": headers["Date"] if headers["Date"] != "????.??.??" else None,
            "round": headers["Round"] if headers["Round"] != "?" else None,
            "white": headers["White"] if headers["White"] != "?" else None,
            "black": headers["Black"] if headers["Black"] != "?" else None,
            "result": headers["Result"] if headers["Result"] != "*" else None,
            "white_title": headers.get("WhiteTitle"),
            "black_title": headers.get("BlackTitle"),
            "white_elo": headers.get("WhiteElo"),
            "black_elo": headers.get("BlackElo"),
            "eco": headers.get("ECO"),
            "opening": headers.get("Opening"),
            "variation": headers.get("Variation"),
            "white_fide_id": headers.get("WhiteFideId"),
            "black_fide_id": headers.get("BlackFideId"),
            "event_date": headers.get("EventDate"),
        }

    def _process_moves(self, game: chess.pgn.Game) -> list:
        board = chess.Board()
        moves = []
        for move in game.mainline_moves():
            move_dict = {
                "from_square": chess.square_name(move.from_square),
                "to_square": chess.square_name(move.to_square),
                "moved_unit": board.piece_at(move.from_square).symbol()
                if board.piece_at(move.from_square)
                else None,
                "captured_unit": board.piece_at(move.to_square).symbol()
                if board.piece_at(move.to_square)
                else None,
                "promoted_unit": None,
                "uci": move.uci(),
                "san": board.san(move),
                "color": chess.COLOR_NAMES[board.turn][0],
                "ply": board.ply(),
                "is_promotion": move.promotion is not None,
                "is_capture": board.is_capture(move),
                "is_castling": board.is_castling(move),
                "is_en_passant": board.is_en_passant(move),
                "is_end": False,
            }
            if move_dict["is_en_passant"]:
                move_dict["captured_unit"] = "P" if board.turn == chess.BLACK else "p"
            if move_dict["is_promotion"]:
                move_dict["promoted_unit"] = (
                    chess.PIECE_SYMBOLS[move.promotion].upper()
                    if board.turn == chess.WHITE
                    else chess.PIECE_SYMBOLS[move.promotion].lower()
                )

            board.push(move)
            move_dict["is_check"] = board.is_check()
            move_dict["is_checkmate"] = board.is_checkmate()
            move_dict["is_stalemate"] = board.is_stalemate()
            move_dict["is_insufficient_material"] = board.is_insufficient_material()

            moves.append(move_dict)

        if len(moves) > 0:
            moves[-1]["is_end"] = True
        else:
            moves = None

        return moves
