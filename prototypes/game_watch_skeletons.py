"""One-screen endless minigame skeletons inspired by Game & Watch pacing.

The mechanics are original W.I.T.C.H.-themed state machines.  They do not use
Nintendo artwork, layouts, timing tables or code.  A pygame adapter can draw
each state on the existing 860x1060 canvas.  There is deliberately no victory
state: difficulty rises until ``status == 'lost'``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random


@dataclass
class BlunkTreasureDiveState:
    """Move Blunk between Cedric's boat and treasure under the tentacles."""

    seed: int = 0
    path_length: int = 5
    position: int = 0
    carried: int = 0
    banked: int = 0
    lives: int = 3
    tick_count: int = 0
    strike_position: int | None = None
    strike_frames: int = 0
    status: str = "playing"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    @property
    def level(self) -> int:
        return 1 + self.banked // 8

    def move(self, direction: int) -> bool:
        if self.status != "playing" or direction not in (-1, 1):
            return False
        self.position = max(0, min(self.path_length, self.position + direction))
        if self.position == self.path_length and direction > 0:
            self.carried += 1
        if self.position == 0 and self.carried:
            self.banked += self.carried
            self.carried = 0
        self._check_strike()
        return True

    def tick(self) -> None:
        if self.status != "playing":
            return
        self.tick_count += 1
        if self.strike_frames:
            self.strike_frames -= 1
            self._check_strike()
            if not self.strike_frames:
                self.strike_position = None
        interval = max(18, 64 - self.level * 3)
        if self.tick_count % interval == 0 and self.strike_position is None:
            self.strike_position = self._rng.randint(1, self.path_length)
            self.strike_frames = max(4, 12 - self.level // 2)

    def _check_strike(self) -> None:
        if self.strike_frames and self.position == self.strike_position:
            self.lives -= 1
            self.carried = 0
            self.position = 0
            self.strike_frames = 0
            self.strike_position = None
            if self.lives <= 0:
                self.status = "lost"


@dataclass
class FallingRescueState:
    """Catch falling Meridian citizens and bounce them toward a portal."""

    seed: int = 0
    lanes: int = 3
    catcher_lane: int = 1
    lives: int = 3
    score: int = 0
    tick_count: int = 0
    objects: list[list[float | int]] = field(default_factory=list)
    status: str = "playing"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    @property
    def level(self) -> int:
        return 1 + self.score // 12

    def move(self, delta: int) -> None:
        if self.status == "playing":
            self.catcher_lane = max(0, min(self.lanes - 1, self.catcher_lane + delta))

    def tick(self) -> None:
        if self.status != "playing":
            return
        self.tick_count += 1
        spawn_interval = max(24, 78 - self.level * 4)
        if self.tick_count % spawn_interval == 0:
            self.objects.append([self._rng.randrange(self.lanes), 0.0, 0])
        speed = 1.8 + min(5.2, self.level * 0.22)
        for obj in self.objects[:]:
            obj[1] = float(obj[1]) + speed
            if float(obj[1]) < 100.0:
                continue
            if int(obj[0]) == self.catcher_lane:
                obj[2] = int(obj[2]) + 1
                if int(obj[2]) >= 2:
                    self.objects.remove(obj)
                    self.score += 1
                else:
                    obj[1] = 18.0
                    obj[0] = min(self.lanes - 1, int(obj[0]) + 1)
            else:
                self.objects.remove(obj)
                self.lives -= 1
                if self.lives <= 0:
                    self.status = "lost"
                    return


@dataclass
class CorneliaManholeState:
    """Move one stone cover between cracks in a Meridian street."""

    seed: int = 0
    holes: int = 4
    cover: int = 1
    lives: int = 3
    score: int = 0
    tick_count: int = 0
    travellers: list[list[int]] = field(default_factory=list)
    status: str = "playing"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def move_cover(self, delta: int) -> None:
        if self.status == "playing":
            self.cover = max(0, min(self.holes - 1, self.cover + delta))

    def tick(self) -> None:
        if self.status != "playing":
            return
        self.tick_count += 1
        level = 1 + self.score // 10
        if self.tick_count % max(26, 82 - level * 4) == 0:
            self.travellers.append([self._rng.randrange(self.holes), 0])
        for traveller in self.travellers[:]:
            traveller[1] += 1
            if traveller[1] < max(14, 32 - level):
                continue
            self.travellers.remove(traveller)
            if traveller[0] == self.cover:
                self.score += 1
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.status = "lost"


@dataclass
class IrmaOilPanicState:
    """Catch dark-water drops, then dump the full vessel on Phobos's guards."""

    seed: int = 0
    lanes: int = 3
    lane: int = 1
    capacity: int = 3
    stored: int = 0
    lives: int = 3
    score: int = 0
    tick_count: int = 0
    drops: list[list[float | int]] = field(default_factory=list)
    status: str = "playing"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def move(self, delta: int) -> None:
        if self.status == "playing":
            self.lane = max(0, min(self.lanes - 1, self.lane + delta))

    def dump(self) -> bool:
        if self.status != "playing" or self.stored < self.capacity:
            return False
        self.score += self.stored * 3
        self.stored = 0
        return True

    def tick(self) -> None:
        if self.status != "playing":
            return
        self.tick_count += 1
        level = 1 + self.score // 18
        if self.tick_count % max(20, 68 - level * 3) == 0:
            self.drops.append([self._rng.randrange(self.lanes), 0.0])
        speed = 2.0 + min(6.0, level * 0.25)
        for drop in self.drops[:]:
            drop[1] = float(drop[1]) + speed
            if float(drop[1]) < 100.0:
                continue
            self.drops.remove(drop)
            if int(drop[0]) == self.lane and self.stored < self.capacity:
                self.stored += 1
                self.score += 1
            else:
                self.lives -= 1
                if self.lives <= 0:
                    self.status = "lost"


GAME_WATCH_PROTOTYPES = (
    BlunkTreasureDiveState,
    FallingRescueState,
    CorneliaManholeState,
    IrmaOilPanicState,
)
