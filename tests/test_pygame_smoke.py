from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

try:
    import pygame
except ImportError:
    pygame = None

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipIf(pygame is None, "Pygame is not installed in this environment")
class PygameSmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from main import Game
        cls.game = Game()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_changed_minigames_draw_one_frame(self):
        for name in ("WILL MAZE", "HAY LIN FLIGHT", "CALEB RUNNER", "HEART BREAKER",
                     "TARANEE FIRE SHOT", "CORNELIA EARTH GARDEN", "IRMA WHIRLPOOL"):
            with self.subTest(name=name):
                self.game.start_minigame(name)
                self.game.update_minigame()
                self.game.draw_minigame()
        self.game.leave_minigame()

    def test_galleries_are_curated(self):
        self.game.collection_page = "ART & SPRITES"
        self.game.gallery_for("ACTION POSES")
        self.assertEqual(len(self.game.collection_gallery_files), 8)
        self.game.collection_page = "ART & SPRITES"
        self.game.gallery_for("HORROR TETROMINOES")
        self.assertEqual(len(self.game.collection_gallery_files), 7)
        self.assertTrue(all(path.name.endswith("rotation_0.png") for path in self.game.collection_gallery_files))

    def test_caleb_crouch_hitbox_matches_visible_clearance(self):
        self.game.start_minigame("CALEB RUNNER")
        obstacle=[130.0,self.game.mg_ground,50,34,False,True]
        rect=self.game.caleb_obstacle_rect(obstacle)
        self.assertTrue(self.game.caleb_player_rect(False).colliderect(rect))
        self.assertFalse(self.game.caleb_player_rect(True).colliderect(rect))

    def test_caleb_jump_moves_both_sprite_anchor_and_hitbox(self):
        self.game.start_minigame("CALEB RUNNER")
        ground = self.game.mg_ground
        self.game.handle_minigame_key(pygame.K_SPACE)
        self.assertLess(self.game.mg_vel[1], 0)
        self.game.update_minigame()
        self.assertLess(self.game.mg_player[1], ground)
        self.assertEqual(
            self.game.caleb_player_rect(False).bottom,
            int(self.game.mg_player[1] + 25),
        )

    def test_phobos_alpha_cleanup_keeps_the_dark_costume(self):
        from main import load_clean_alpha

        source = ROOT / "assets/cutscenes/lines100/phobos_action.png"
        cleaned = load_clean_alpha(source)
        components = pygame.mask.from_surface(cleaned, 8).connected_components(4)
        substantial = [mask for mask in components if mask.count() > 100]
        self.assertEqual(len(substantial), 1)

    def test_will_maze_ghosts_leave_the_house_one_by_one(self):
        self.game.start_minigame("WILL MAZE")
        self.assertEqual([ghost["state"] for ghost in self.game.mg_maze_ghosts],
                         ["active", "house", "house", "house"])
        self.assertEqual([ghost["release"] for ghost in self.game.mg_maze_ghosts],
                         [0, 4 * 60, 9 * 60, 15 * 60])

    def test_room_variants_and_action_frames_draw(self):
        self.game.ensure_story100_assets()
        self.assertEqual(len(self.game.story200_action_frames), 14)
        self.game.phobos_room_stage = "room"
        for layout in ("table", "podium"):
            self.game.phobos_room_layout = layout
            self.game.draw_phobos_room()


if __name__ == "__main__":
    unittest.main()
