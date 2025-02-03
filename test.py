import unittest
from main import BlackCloverMUD  # Replace with your actual module name


class TestBlackCloverMUD(unittest.TestCase):

  def setUp(self):
    self.game = BlackCloverMUD()

  def test_create_player_success(self):
    result = self.game.create_player("White", "Fire", "newpass123")
    self.assertTrue(result)
    self.assertIn("White", [player.name for player in self.game.players])

  def test_create_player_existing_name(self):
    self.game.create_player("ExistingPlayer", "Water", "existingpass")
    result = self.game.create_player("ExistingPlayer", "Wind", "newpass123")
    self.assertFalse(result)

  def test_login_player_success(self):
    self.game.create_player("LoginPlayer", "Fire", "loginpass")
    player = self.game.login_player("LoginPlayer", "loginpass")
    self.assertIsNotNone(player)
    self.assertEqual(player.name, "LoginPlayer")

  def test_login_player_failure(self):
    self.game.create_player("LoginPlayer2", "Water", "loginpass2")
    player = self.game.login_player("LoginPlayer2", "wrongpass")
    self.assertIsNone(player)


if __name__ == '__main__':
  unittest.main()
