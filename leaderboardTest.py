import unittest
from leaderboard import Player, Leaderboard
from elo import Elo

class TestLeaderboard(unittest.TestCase):
    """Unit tests for the Player class."""

    def test_player_init(self):
        p = Player("test_player")
        self.assertEqual(p.name, "test_player")
        self.assertEqual(p.wins, 0)
        self.assertEqual(p.losses, 0)
        self.assertEqual(p.rating, 1500.0)

        p_custom = Player("custom", winRecord=5, lossRecord=3, rating=1600.5)
        self.assertEqual(p_custom.name, "custom")
        self.assertEqual(p_custom.wins, 5)
        self.assertEqual(p_custom.losses, 3)
        self.assertEqual(p_custom.rating, 1600.5)

    def test_record_win_loss(self):
        """Test recording wins and losses."""
        p = Player("test")
        p.record_win()
        self.assertEqual(p.wins, 1)
        p.record_win(3)
        self.assertEqual(p.wins, 4)

        p.record_loss()
        self.assertEqual(p.losses, 1)
        p.record_loss(2)
        self.assertEqual(p.losses, 3)

    def test_total_games(self):
        """Test the total_games property."""
        p = Player("test", winRecord=5, lossRecord=3)
        self.assertEqual(p.total_games, 8)
        p_new = Player("new")
        self.assertEqual(p_new.total_games, 0)

    def test_win_rate(self):
        """Test the win_rate property, including the zero games case."""
        p_no_games = Player("new")
        self.assertEqual(p_no_games.win_rate, 0.0)

        p_5_3 = Player("5_3", winRecord=5, lossRecord=3)
        self.assertAlmostEqual(p_5_3.win_rate, 5 / 8)

        p_all_win = Player("all_win", winRecord=10, lossRecord=0)
        self.assertAlmostEqual(p_all_win.win_rate, 1.0)

        p_all_loss = Player("all_loss", winRecord=0, lossRecord=7)
        self.assertAlmostEqual(p_all_loss.win_rate, 0.0)

    def test_to_from_dict(self):
        """Test serialization and deserialization."""
        p1 = Player("data", 10, 5, 1550.0)
        p1_dict = p1.to_dict()
        expected_dict = {"name": "data", "winRecord": 10, "lossRecord": 5, "rating": 1550.0}
        self.assertDictEqual(p1_dict, expected_dict)

        p2 = Player.from_dict(p1_dict)
        self.assertEqual(p2.name, "data")
        self.assertEqual(p2.wins, 10)
        self.assertEqual(p2.losses, 5)
        self.assertEqual(p2.rating, 1550.0)


class TestElo(unittest.TestCase):
    """Unit tests for the Elo class."""

    def test_expected_score(self):
        """Test the expected_score calculation."""
        elo = Elo(k_factor=32)

        # Equal ratings
        score_equal = elo.expected_score(1500, 1500)
        self.assertAlmostEqual(score_equal, 0.5)

        # 400 points difference (higher rating A)
        score_400_diff = elo.expected_score(1900, 1500)
        self.assertAlmostEqual(score_400_diff, 1 / (1 + 10 ** (-1)), places=4) # Approx 0.9091

        # 400 points difference (lower rating A)
        score_neg_400_diff = elo.expected_score(1500, 1900)
        self.assertAlmostEqual(score_neg_400_diff, 1 / (1 + 10 ** (1)), places=4) # Approx 0.0909

    def test_update_ratings(self):
        """Test updating ratings after a match."""
        elo = Elo(k_factor=30)
        winner = Player("W", rating=1600)
        loser = Player("L", rating=1500)

        initial_winner_rating = winner.rating
        initial_loser_rating = loser.rating

        expected_win = elo.expected_score(initial_winner_rating, initial_loser_rating)
        expected_lose = elo.expected_score(initial_loser_rating, initial_winner_rating)

        elo.update_ratings(winner, loser)

        # Winner's rating should increase
        self.assertTrue(winner.rating > initial_winner_rating)
        # Loser's rating should decrease
        self.assertTrue(loser.rating < initial_loser_rating)

        # Check the new rating calculation based on the formula
        expected_new_winner_rating = initial_winner_rating + elo.k_factor * (1 - expected_win)
        expected_new_loser_rating = initial_loser_rating + elo.k_factor * (0 - expected_lose)

        self.assertAlmostEqual(winner.rating, round(expected_new_winner_rating, 2))
        self.assertAlmostEqual(loser.rating, round(expected_new_loser_rating, 2))


class TestLeaderboard(unittest.TestCase):
    """Unit tests for the Leaderboard class."""

    def setUp(self):
        # Create a new leaderboard before each test
        self.lb = Leaderboard("TestBoard")
        self.lb.elo = Elo(k_factor=32) # Ensure elo is available for record_match

    def test_add_player_success(self):
        """Test adding a player."""
        p = self.lb.add_player("test1")
        self.assertIsInstance(p, Player)
        self.assertEqual(len(self.lb.players), 1)
        self.assertEqual(self.lb.playerCount, 1)
        self.assertEqual(self.lb.players[0].name, "test1")

    def test_add_player_duplicate(self):
        """Test adding a player with an existing name."""
        self.lb.add_player("test1")
        with self.assertRaises(ValueError):
            self.lb.add_player("test1")

    def test_get_find_player(self):
        """Test finding and getting a player."""
        self.lb.add_player("alice")
        self.lb.add_player("bob")
        
        # Test find_index
        self.assertEqual(self.lb.find_index("alice"), 0)
        self.assertEqual(self.lb.find_index("bob"), 1)
        self.assertEqual(self.lb.find_index("charlie"), -1)
        
        # Test get_player
        self.assertIsNotNone(self.lb.get_player("alice"))
        self.assertIsNone(self.lb.get_player("charlie"))

    def test_remove_player(self):
        """Test removing a player."""
        self.lb.add_player("p1")
        self.lb.add_player("p2")
        
        self.lb.remove_player("p1")
        self.assertEqual(len(self.lb.players), 1)
        self.assertIsNone(self.lb.get_player("p1"))
        
        # Test removing a non-existent player
        with self.assertRaises(KeyError):
            self.lb.remove_player("p3")

    def test_record_match_keyerror(self):
        """Test record_match with missing players."""
        self.lb.add_player("alice")
        
        # Missing loser
        with self.assertRaises(KeyError) as cm:
            self.lb.record_match(winner="alice", loser="bob")
        self.assertIn("'bob' not found", str(cm.exception))

        # Missing winner
        with self.assertRaises(KeyError) as cm:
            self.lb.record_match(winner="charlie", loser="alice")
        self.assertIn("'charlie' not found", str(cm.exception))