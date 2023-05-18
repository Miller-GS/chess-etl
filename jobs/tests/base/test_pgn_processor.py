from unittest import TestCase
from base.pgn_processor import PGNProcessor
from io import StringIO


class TestPGNProcessor(TestCase):
    def test_process_game_should_return_none_when_no_game(self):
        pgn_stream = StringIO("")
        pgn_processor = PGNProcessor(pgn_stream)
        self.assertIsNone(pgn_processor.process_game())

    def test_process_game_should_return_all_headers(self):
        pgn_stream = StringIO(
            """[Event "Event"]
[Site "Site"]
[Date "Date"]
[Round "Round"]
[White "White"]
[Black "Black"]
[Result "Result"]
[WhiteTitle "WhiteTitle"]
[BlackTitle "BlackTitle"]
[WhiteElo "WhiteElo"]
[BlackElo "BlackElo"]
[ECO "ECO"]
[Opening "Opening"]
[Variation "Variation"]
[WhiteFideId "WhiteFideId"]
[BlackFideId "BlackFideId"]
[EventDate "EventDate"]
        """
        )
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["event"], "Event")
        self.assertEqual(game["site"], "Site")
        self.assertEqual(game["date"], "Date")
        self.assertEqual(game["round"], "Round")
        self.assertEqual(game["white"], "White")
        self.assertEqual(game["black"], "Black")
        self.assertEqual(game["result"], "Result")
        self.assertEqual(game["white_title"], "WhiteTitle")
        self.assertEqual(game["black_title"], "BlackTitle")
        self.assertEqual(game["white_elo"], "WhiteElo")
        self.assertEqual(game["black_elo"], "BlackElo")
        self.assertEqual(game["eco"], "ECO")
        self.assertEqual(game["opening"], "Opening")
        self.assertEqual(game["variation"], "Variation")
        self.assertEqual(game["white_fide_id"], "WhiteFideId")
        self.assertEqual(game["black_fide_id"], "BlackFideId")
        self.assertEqual(game["event_date"], "EventDate")

    def test_process_game_should_return_header_with_none_when_missing(self):
        pgn_stream = StringIO('[Event "Event"]')
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["event"], "Event")
        self.assertIsNone(game["site"])
        self.assertIsNone(game["date"])
        self.assertIsNone(game["round"])
        self.assertIsNone(game["white"])
        self.assertIsNone(game["black"])
        self.assertIsNone(game["result"])
        self.assertIsNone(game["white_title"])
        self.assertIsNone(game["black_title"])
        self.assertIsNone(game["white_elo"])
        self.assertIsNone(game["black_elo"])
        self.assertIsNone(game["eco"])
        self.assertIsNone(game["opening"])
        self.assertIsNone(game["variation"])
        self.assertIsNone(game["white_fide_id"])
        self.assertIsNone(game["black_fide_id"])
        self.assertIsNone(game["event_date"])
        self.assertIsNone(game["plies"])

    def test_process_game_should_return_correct_amount_of_plies(self):
        pgn_stream = StringIO("1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(len(game["plies"]), 8)

    def test_process_game_ply_should_have_from_square(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["from_square"], "e2")
        self.assertEqual(game["plies"][1]["from_square"], "e7")

    def test_process_game_ply_should_have_to_square(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["to_square"], "e4")
        self.assertEqual(game["plies"][1]["to_square"], "e5")

    def test_process_game_ply_should_have_moved_unit(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["moved_unit"], "P")
        self.assertEqual(game["plies"][1]["moved_unit"], "p")

    def test_process_game_ply_should_identify_captured_unit(self):
        pgn_stream = StringIO("1. e4 d5 2. exd5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["captured_unit"], None)
        self.assertEqual(game["plies"][1]["captured_unit"], None)
        self.assertEqual(game["plies"][2]["captured_unit"], "p")

        self.assertEqual(game["plies"][0]["is_capture"], False)
        self.assertEqual(game["plies"][1]["is_capture"], False)
        self.assertEqual(game["plies"][2]["is_capture"], True)

    def test_process_game_ply_should_identify_promoted_unit(self):
        pgn_stream = StringIO(
            "1. e4 d5 2. e5 d4 3. e6 d3 4. exf7+  Kd7 5. fxg8=Q dxc2 6. Qf3 cxb1=N"
        )
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["promoted_unit"], None)
        self.assertEqual(game["plies"][8]["promoted_unit"], "Q")
        self.assertEqual(game["plies"][11]["promoted_unit"], "n")

        self.assertEqual(game["plies"][0]["is_promotion"], False)
        self.assertEqual(game["plies"][8]["is_promotion"], True)
        self.assertEqual(game["plies"][11]["is_promotion"], True)

    def test_process_game_ply_should_have_uci(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["uci"], "e2e4")
        self.assertEqual(game["plies"][1]["uci"], "e7e5")

    def test_process_game_ply_should_have_san(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["san"], "e4")
        self.assertEqual(game["plies"][1]["san"], "e5")

    def test_process_game_ply_should_have_color(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["color"], "w")
        self.assertEqual(game["plies"][1]["color"], "b")

    def test_process_game_ply_should_have_ply_number(self):
        pgn_stream = StringIO("1. e4 e5")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["ply"], 0)
        self.assertEqual(game["plies"][1]["ply"], 1)

    def test_process_game_ply_should_identify_castling(self):
        pgn_stream = StringIO("1. e4 e5 2. Bc4 Bc5 3. Nf3 Nf6 4. O-O O-O")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_castling"], False)
        self.assertEqual(game["plies"][1]["is_castling"], False)
        self.assertEqual(game["plies"][6]["is_castling"], True)
        self.assertEqual(game["plies"][7]["is_castling"], True)

    def test_process_game_ply_should_identify_en_passant(self):
        pgn_stream = StringIO("1. e4 d5 2. e5 f5 3. exf6")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_en_passant"], False)
        self.assertEqual(game["plies"][1]["is_en_passant"], False)
        self.assertEqual(game["plies"][4]["is_en_passant"], True)
        self.assertEqual(game["plies"][4]["captured_unit"], "p")

    def test_process_game_ply_should_identify_check(self):
        pgn_stream = StringIO("1. e4 e5 2. Qh5 Nf6 3. Qxf7+ Kxf7")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_check"], False)
        self.assertEqual(game["plies"][1]["is_check"], False)
        self.assertEqual(game["plies"][4]["is_check"], True)

    def test_process_game_ply_should_identify_checkmate(self):
        # Fool's mate
        pgn_stream = StringIO("1.f3 e6 2.g4 Qh4#")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_checkmate"], False)
        self.assertEqual(game["plies"][1]["is_checkmate"], False)
        self.assertEqual(game["plies"][3]["is_checkmate"], True)
        self.assertEqual(game["plies"][3]["is_check"], True)

    def test_process_game_ply_should_identify_stalemate(self):
        # Fastest stalemate possible
        pgn_stream = StringIO(
            "1. e3 a5 2. Qh5 Ra6 3. Qxa5 h5 4. h4 Rah6 5. Qxc7 f6 6. Qxd7+ Kf7 7. Qxb7 Qd3 8.Qxb8 Qh7 9. Qxc8 Kg6 10. Qe6 1/2-1/2"
        )
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_stalemate"], False)
        self.assertEqual(game["plies"][1]["is_stalemate"], False)
        self.assertEqual(game["plies"][18]["is_stalemate"], True)
        self.assertEqual(game["plies"][18]["is_checkmate"], False)
        self.assertEqual(game["plies"][18]["is_check"], False)

    def test_process_game_ply_should_identify_insufficient_material(self):
        # K vs K - The game was made artificially by removing all pieces from the board except the two kings.
        pgn_stream = StringIO(
            """1. e4 d5 2. exd5 Qxd5 3. Bb5+ Qxb5 4. Nc3 Qxb2 5. Bxb2 Bg4 6. Qxg4 Nf6 7. Qxg7
Bxg7 8. Nd5 Nxd5 9. Bxg7 Ne3 10. Bxh8 Nxg2+ 11. Ke2 Nc6 12. Nf3 Nd4+ 13. Nxd4
Kd7 14. Kf3 Rxh8 15. Kxg2 c5 16. Rab1 cxd4 17. Rxb7+ Ke6 18. Rxa7 Rc8 19. Rxe7+
Kxe7 20. Re1+ Kf6 21. Re7 Rxc2 22. Rxf7+ Ke5 23. Rxh7 Rxa2 24. Rh4 Rxd2 25. Rxd4
Rxf2+ 26. Kg3 Kxd4 27. Kh3 Rxh2+ 28. Kxh2 1/2-1/2"""
        )
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_insufficient_material"], False)
        self.assertEqual(game["plies"][1]["is_insufficient_material"], False)
        self.assertEqual(game["plies"][54]["is_insufficient_material"], True)

    def test_process_game_ply_should_identify_end(self):
        pgn_stream = StringIO("1. e4 e5 2. Qh5 Nf6 3. Qxf7+ Kxf7")
        pgn_processor = PGNProcessor(pgn_stream)

        game = pgn_processor.process_game()

        self.assertEqual(game["plies"][0]["is_end"], False)
        self.assertEqual(game["plies"][1]["is_end"], False)
        self.assertEqual(game["plies"][5]["is_end"], True)

    def test_process_all_should_return_list_of_games(self):
        pgn_stream = StringIO(
            "1. e4 e5 2. Qh5 Nf6 3. Qxf7+ Kxf7\n\n1. e4 e5 2. Qh5 Nf6 3. Qxf7+ Kxf7"
        )
        pgn_processor = PGNProcessor(pgn_stream)

        games = pgn_processor.process_all()

        self.assertEqual(len(games), 2)
