from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from leaderboard import Player  # type hint only to avoid circular import

#This class handles all elo rating calculations
class Elo:
    

    #initialize elo system
    #k-factor controls how great the change in elo is after each match
    #high k = rating change more drastically
    #lower k = ratings adjust slower
    def __init__(self, k_factor: float):
        self.k_factor = float(k_factor)
    
    #expected score of player A vs player B
    def expected_score(self, rating_a: float, rating_b: float) -> float:
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    
    #update ratings for winner and loser
    def update_ratings(self, winner: "Player", loser: "Player") -> None:
        #calculate scores
        expected_win = self.expected_score(winner.rating, loser.rating)
        expected_lose = self.expected_score(loser.rating, winner.rating)

        #update ratings
        winner.rating += self.k_factor * (1 - expected_win)
        loser.rating += self.k_factor * (0 - expected_lose)

        #round the final rating to two decimal places for consistency
        winner.rating = round(winner.rating, 2)
        loser.rating = round(loser.rating, 2)