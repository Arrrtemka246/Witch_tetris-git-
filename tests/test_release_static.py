from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from collections import deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_main_without_pygame():
    fake = types.ModuleType("pygame")
    sys.modules.setdefault("pygame", fake)
    spec = importlib.util.spec_from_file_location("witch_tetris_main", ROOT / "main.py")
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


game = load_main_without_pygame()


class ReleaseStaticTests(unittest.TestCase):
    def test_release_version_and_exact_tetromino_bases(self):
        self.assertEqual(game.BUILD_VERSION, "6.36.1")
        self.assertEqual(game.BASE_SHAPES, {
            "I": [(0, 0), (0, 1), (0, 2), (0, 3)],
            "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
            "T": [(0, 0), (1, 0), (2, 0), (1, 1)],
            "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
            "Z": [(1, 0), (2, 0), (0, 1), (1, 1)],
            "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
            "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
        })

    def test_start_speed_changes_gravity_not_story_lines(self):
        instance = game.Game.__new__(game.Game)
        instance.lines = 0
        values = []
        for speed in range(1, 6):
            instance.start_speed = speed
            values.append(instance.fall_interval())
            self.assertEqual(instance.lines, 0)
        self.assertEqual(values, [32, 28, 24, 20, 17])

    def test_will_maze_is_connected_and_inside_arena(self):
        width, height, tunnel_y, walls = game.build_will_maze()
        self.assertEqual((width, height, tunnel_y), (28, 31, 15))
        open_cells = {(x, y) for y in range(height) for x in range(width) if (x, y) not in walls}
        seen = {(13, 23)}; queue = deque(seen)
        while queue:
            cell = queue.popleft()
            for direction in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = game.will_maze_step(cell, direction, walls, width, height, tunnel_y)
                if nxt is not None and nxt not in seen:
                    seen.add(nxt); queue.append(nxt)
        self.assertEqual(seen, open_cells)
        self.assertEqual(game.will_maze_step((0, tunnel_y), (-1, 0), walls, width, height, tunnel_y), (width - 1, tunnel_y))
        self.assertLessEqual(122 + width * 22, 930)
        self.assertLessEqual(166 + height * 22, 905)

    def test_bricks_and_invaders_are_inside_arena(self):
        arena = (70, 145, 860, 760)
        for x, y, width, height in game.heart_brick_layout(arena, 7):
            self.assertGreaterEqual(x, arena[0]); self.assertGreaterEqual(y, arena[1])
            self.assertLessEqual(x + width, arena[0] + arena[2]); self.assertLessEqual(y + height, arena[1] + arena[3])
        invaders = game.taranee_invader_layout(arena, 7)
        self.assertEqual(len({round(item[0], 4) for item in invaders}), 10)
        for x, y in invaders:
            self.assertGreaterEqual(x - 18, arena[0]); self.assertLessEqual(x + 18, arena[0] + arena[2])
            self.assertGreaterEqual(y - 14, arena[1]); self.assertLessEqual(y + 14, arena[1] + arena[3])

    def test_music_file_is_in_only_the_correct_route(self):
        early = ROOT / "assets/audio/music/phase_0_99_phobos/Arrogant_Prince_of_the_Obsidian_Court.mp3"
        late = ROOT / "assets/audio/music/phobos_route/Phobos_theme_1.mp3"
        self.assertTrue(early.is_file())
        self.assertFalse(late.exists())
        self.assertTrue((ROOT / "assets/audio/music/phobos_route/Phobos_main_theme_3_phase.mp3").is_file())
        self.assertTrue((ROOT / "assets/audio/collection/witch_ending.mp3").is_file())


if __name__ == "__main__":
    unittest.main()
