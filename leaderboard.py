"""Simple leaderboard module.

This implements a Player class and a Leaderboard class that can
add/remove players, record match results, and produce standings
sorted primarily by win rate (wins / total games), then by total
wins, then by fewer losses, then by name.

Usage example:

>>> lb = Leaderboard("Weekly")
>>> lb.add_player("alice")
>>> lb.add_player("bob")
>>> lb.record_match(winner="alice", loser="bob")
>>> for p in lb.standings():
...     print(p.name, p.win_rate)

"""

from typing import List, Optional


class Player:
    """Represents a player with a win/loss record.

    Attributes kept with the original names for compatibility:
    - name
    - winRecord (int)
    - lossRecord (int)
    """

    def __init__(self, name: str, winRecord: int = 0, lossRecord: int = 0):
        self.name = str(name)
        self.winRecord = int(winRecord)
        self.lossRecord = int(lossRecord)

    def record_win(self, count: int = 1) -> None:
        """Add wins to this player's record."""
        self.winRecord += int(count)

    def record_loss(self, count: int = 1) -> None:
        """Add losses to this player's record."""
        self.lossRecord += int(count)

    @property
    def wins(self) -> int:
        """Get total wins of this player."""
        return self.winRecord

    @property
    def losses(self) -> int:
        """Get total losses of this player."""
        return self.lossRecord

    @property
    def total_games(self) -> int:
        """Get total games of this player."""
        return self.winRecord + self.lossRecord

    @property
    def win_rate(self) -> float:
        """Return win rate as float between 0.0 and 1.0.

        If the player has no games, return 0.0.
        """
        total = self.total_games
        if total == 0:
            return 0.0
        return self.winRecord / total

    def to_dict(self) -> dict:
        return {"name": self.name, "winRecord": self.winRecord, "lossRecord": self.lossRecord}

    @classmethod
    def from_dict(cls, d: dict) -> "Player":
        return cls(d.get("name"), d.get("winRecord", 0), d.get("lossRecord", 0)) # type: ignore

    def __repr__(self) -> str:
        return f"Player(name={self.name!r}, wins={self.winRecord}, losses={self.lossRecord}, win_rate={self.win_rate:.3f})"


class Leaderboard:
    """Manage a collection of players and produce ranked standings.

    Sorting rules for standings (highest ranked first):
    1. Higher win rate (wins / total games)
    2. Higher number of wins
    3. Fewer losses
    4. Alphabetical by name
    """

    def __init__(self, name: str, playerCount: int = 0, players: Optional[List[Player]] = None):
        self.name = str(name)
        # playerCount is optional metadata; keep it but prefer actual list length
        self.playerCount = int(playerCount)
        self.players: List[Player] = list(players) if players else []

    def _find_index(self, name: str) -> int:
        for i, p in enumerate(self.players):
            if p.name == name:
                return i
        return -1

    def add_player(self, name: str, wins: int = 0, losses: int = 0) -> Player:
        """Add a new player. Raises ValueError if a player with the same name exists."""
        if self.get_player(name) is not None:
            raise ValueError(f"player '{name}' already exists")
        p = Player(name, wins, losses)
        self.players.append(p)
        # keep playerCount as metadata in case it was used elsewhere
        self.playerCount = max(self.playerCount, len(self.players))
        return p

    def remove_player(self, name: str) -> None:
        """Remove a player by name. Raises KeyError if not found."""
        idx = self._find_index(name)
        if idx == -1:
            raise KeyError(f"player '{name}' not found")
        self.players.pop(idx)

    def get_player(self, name: str) -> Optional[Player]:
        idx = self._find_index(name)
        return self.players[idx] if idx != -1 else None

    def record_match(self, winner: str, loser: str) -> None:
        """Record a single match result. Both winner and loser must exist.

        This increments winner.winRecord and loser.lossRecord by 1.
        Raises KeyError if a player is missing.
        """
        w = self.get_player(winner)
        l = self.get_player(loser)
        if w is None:
            raise KeyError(f"winner '{winner}' not found")
        if l is None:
            raise KeyError(f"loser '{loser}' not found")
        w.record_win(1)
        l.record_loss(1)

    def standings(self) -> List[Player]:
        """Return the players sorted by the ranking rules described above."""
        # sort by key tuple and reverse to have highest first
        return sorted(
            self.players,
            key=lambda p: (p.win_rate, p.wins, -p.losses, p.name),
            reverse=True,
        )

    def top_n(self, n: int = 10) -> List[Player]:
        return self.standings()[: max(0, int(n))]

    def to_dict(self) -> dict:
        return {"name": self.name, "playerCount": self.playerCount, "players": [p.to_dict() for p in self.players]}

    @classmethod
    def from_dict(cls, d: dict) -> "Leaderboard":
        players = [Player.from_dict(pd) for pd in d.get("players", [])]
        return cls(name=d.get("name", ""), playerCount=d.get("playerCount", len(players)), players=players)

    def __repr__(self) -> str:
        return f"Leaderboard(name={self.name!r}, players={len(self.players)})"


        