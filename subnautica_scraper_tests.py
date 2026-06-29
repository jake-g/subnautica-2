import unittest

from subnautica_scraper import clean_game_string
from subnautica_scraper import is_junk_string
from subnautica_scraper import UE_NOISE


class TestSubnauticaScraper(unittest.TestCase):
  """Unit tests for Subnautica 2 telemetry decoder logic."""

  def test_is_junk_string(self):
    """Verifies Unreal Engine noise filtering logic."""
    # Test length threshold
    self.assertTrue(is_junk_string("abc"))
    self.assertFalse(is_junk_string("valid_string"))

    # Test exact noise matches
    for noise in UE_NOISE:
      self.assertTrue(is_junk_string(noise))
      self.assertTrue(is_junk_string(noise.upper()))

    # Test symbol thresholds
    self.assertTrue(is_junk_string("///"))
    self.assertTrue(is_junk_string("..."))
    self.assertTrue(is_junk_string("***"))

    # Test prefixes
    self.assertTrue(is_junk_string("UE4_SaveGame"))
    self.assertTrue(is_junk_string("ue5_config"))

    # Test valid game assets
    self.assertFalse(is_junk_string("BP_Scanner"))
    self.assertFalse(is_junk_string("DA_Titanium"))
    self.assertFalse(is_junk_string("/Game/Maps/CoralGardens"))

  def test_clean_game_string(self):
    """Verifies prefix stripping and spacing for game assets."""
    self.assertEqual(clean_game_string("/Game/Maps/Shallow"), "Maps/Shallow")
    self.assertEqual(clean_game_string("/Script/CoreUObject/Class"),
                     "CoreUObject/Class")
    self.assertEqual(clean_game_string("/Data/Blueprints/BP_Seamoth"),
                     "Seamoth")
    self.assertEqual(clean_game_string("BP_OxygenTank_Small"), "Oxygen Tank")
    self.assertEqual(clean_game_string("_DA_Copper_"), "Copper")


if __name__ == "__main__":
  unittest.main()
