import os
import random
import json


class Color:
  RESET = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  MAGENTA = '\033[95m'
  CYAN = '\033[96m'


class Player:

  def __init__(self, name, magic_type, password):
    self.name = name
    self.magic_type = magic_type
    self.password = password
    self.level = 1
    self.experience = 0
    self.spells = []
    self.kingdoms_won = []  # List to track the kingdoms a player has won
    self.sword_awards = []  # List to track the swords a player has earned
    self.kingdom = " "  # Add the 'kingdom' attribute
    self.magic = 10

  def level_up(self):
    self.level += 1
    print(f"{self.name} leveled up to level {self.level}!")

  def cast_spell(self):
    if self.spells:
      spell = random.choice(self.spells)
      print(f"{self.name} casts {spell}!")
    else:
      print(f"{self.name} has no spells.")

  def login(self, entered_password):
    return entered_password == self.password

  def to_dict(self):
    return {
        'name': self.name,
        'magic_type': self.magic_type,
        'password': self.password,
        'level': self.level,
        'experience': self.experience,
        'spells': self.spells,
        'kingdoms_won': self.kingdoms_won,
        'sword_awards': self.sword_awards,
        'kingdom': self.kingdom,
        'magic': self.magic
    }

  @classmethod
  def from_dict(cls, data):
    player = cls(data['name'], data['magic_type'], data['password'])
    player.level = data['level']
    player.experience = data['experience']
    player.spells = data['spells']
    player.kingdoms_won = data['kingdoms_won']
    player.sword_awards = data['sword_awards']
    return player


class BlackCloverMUD:
  data_folder = "LoadData"
  levels = ['Ignite', 'Illuminate', 'Elite']  # Define levels here

  def __init__(self):
    self.players = []

    # Ensuring the data folder exists
    if not os.path.exists(self.data_folder):
      os.makedirs(self.data_folder)

  def create_player(self, name, magic_type, password):
    for player in self.players:
      if player.name == name:
        print("Username already taken. Please choose a different name.")
        return False

    valid_magic_types = ['Fire', 'Water',
                         'Wind']  # Add more magic types as needed

    if magic_type.capitalize() not in valid_magic_types:
      print("Invalid magic type. Please choose from: ",
            ", ".join(valid_magic_types))

      return

    player = Player(name, magic_type.capitalize(), password)
    self.players.append(player)
    print(
        f"Welcome to the Black Clover MUD, {player.name}! You are a {player.magic_type} mage."
    )
    return True

  def login_player(self, entered_name, entered_password):
    entered_name = input("Enter your name: ")
    entered_password = input("Enter your password: ")

    for player in self.players:
      if player.name == entered_name and player.login(entered_password):
        if player.login(entered_password):
          print(f"Welcome back, {entered_name}!")
          return player
        else:
          print("Incorrect password. Please try again.")
          return None

    print("Player not found. Please create a new account.")
    return None

  def choose_kingdom(self, player):
    print("Choose the kingdom you want to battle in:")
    available_kingdoms = [
        kingdom for kingdom in ["Clover", "Diamond", "Heart", "Spade"]
        if kingdom not in player.kingdoms_won
    ]

    if not available_kingdoms:
      print(
          "You have already won all kingdoms. There are no more battles for you."
      )
      return

    for index, kingdom in enumerate(available_kingdoms, 1):
      print(f"{index}. {kingdom}")

    choice = input(f"Enter your choice (1-{len(available_kingdoms)}): ")

    if choice.isdigit() and 1 <= int(choice) <= len(available_kingdoms):
      selected_kingdom = available_kingdoms[int(choice) - 1]
      player.kingdom = selected_kingdom
      print(
          f"{player.name}, you have chosen the {selected_kingdom} kingdom for battle!"
      )
      self.battle(player)
    else:
      print(
          f"Invalid choice. Please enter a number between 1 and {len(available_kingdoms)}."
      )

  def battle(self, player):
    level_index = 0
    while level_index < len(self.levels):
      level = self.levels[level_index]
      print(
          f"\n{player.name}, you are entering the {level} level battle in the {player.kingdom} kingdom!"
      )
      level_attempts = 3

      while level_attempts > 0:
        print(
            f"Attempt {4 - level_attempts}. Press Enter to start the battle..."
        )
        input()

        # Battle logic (simplified for example)
        player_power = random.randint(1, 10)
        enemy_power = random.randint(1, 10)

        if player_power > enemy_power:  # Player won the battle
          print(Color.BOLD + Color.GREEN + "You won the battle!" + Color.RESET)
          promotion = f"Promotion: {player.name} is now a {level} Mage!"
          print(Color.BOLD + Color.GREEN + promotion + Color.RESET)

          if level == 'Elite':
            sword_award = self.get_sword_award(player.kingdom)
            print(
                f"Congratulations, {player.name}! You've completed the {player.kingdom} kingdom battles and received a {sword_award} as a reward!"
            )
            player.sword_awards.append(sword_award)
            player.kingdoms_won.append(player.kingdom)
            if set(player.sword_awards) == {
                'Demon Slayer', 'Demon Dweller', 'Demon Destroyer',
                'Demon-Majestic'
            }:
              print(
                  f"Congratulations, {player.name}! You are now the Wizard King!"
              )

          level_index += 1
          player.level_up()  # Move to the next level
          break
        else:  # Player lost the battle
          print(Color.BOLD + Color.RED + "You lost the battle!" + Color.RESET)
          level_attempts -= 1

      if level_attempts == 0:
        while True:
          choice = input(
              "Do you want to restart this level or repeat the previous one? (restart/repeat): "
          ).lower()
          if choice == 'restart':
            break  # Restart the current level
          elif choice == 'repeat' and level_index > 0:
            level_index -= 1  # Go back to the previous level
            break
          else:
            print(Color.BOLD + Color.RED +
                  "Invalid choice. Please enter 'restart' or 'repeat'." +
                  Color.RESET)

  def save_game(self, player):
    with open(os.path.join(self.data_folder, f"{player.name}_save.json"),
              'w') as file:
      json.dump(player.to_dict(), file)
    print(Color.BOLD + Color.GREEN + "Game saved successfully." + Color.RESET)

  def get_sword_award(self, kingdom):
    sword_rewards = {
        'Clover': 'Demon Slayer',
        'Diamond': 'Demon Dweller',
        'Heart': 'Demon Destroyer',
        'Spade': 'Demon-Majestic'
    }
    return sword_rewards.get(kingdom, 'Unknown Sword')

  def display_leaderboard(self):
    sorted_players = sorted(self.players,
                            key=lambda x: (len(x.sword_awards), x.level),
                            reverse=True)
    print("Leaderboard:")
    for i, player in enumerate(sorted_players, start=1):
      swords_earned = ', '.join(player.sword_awards)
      kingdoms_won = ', '.join(
          player.kingdoms_won) if player.kingdoms_won else 'None'
      print(
          f"{i}. {player.name} - Level: {player.level}, Swords: {swords_earned}, Kingdoms Conquered: {kingdoms_won}"
      )

  def delete_player_data(self, player_name):
    player_to_delete = next((p for p in self.players if p.name == player_name),
                            None)
    if player_to_delete:
      self.players.remove(player_to_delete)
      save_file_path = os.path.join(self.data_folder,
                                    f"{player_name}_save.json")
      if os.path.exists(save_file_path):
        os.remove(save_file_path)
      print(f"Player data for {player_name} deleted successfully.")
    else:
      print(f"No player found with the name {player_name}.")

  def save_players_data(self):
    data = [player.to_dict() for player in self.players]
    with open(os.path.join(self.data_folder, 'players_data.json'),
              'w') as file:
      json.dump(data, file)
    print("Players' data saved successfully.")

  def load_players_data(self):
    try:
      with open(os.path.join(self.data_folder, 'players_data.json'),
                'r') as file:
        data = json.load(file)
        self.players = [Player.from_dict(player_data) for player_data in data]
    except FileNotFoundError:
      pass
    except Exception as e:
      print(f"An error occurred while loading players' data: {e}")

  def load_game(self, player_name):
    existing_player = next((p for p in self.players if p.name == player_name),
                           None)
    if existing_player:
      print(f"Player {player_name} is already loaded.")
      return existing_player

    try:
      with open(os.path.join(self.data_folder, f"{player_name}_save.json"),
                'r') as file:
        data = json.load(file)
        player = Player.from_dict(data)
        self.players.append(player)
        print(f"Game loaded successfully for {player_name}.")
        return player
    except FileNotFoundError:
      print(f"No saved game found for {player_name}.")
    return None

  def list_players(self):
    print("Current Players:")
    for player in self.players:
      print(f"- {player.name}, {player.magic_type} mage")

  def start_game(self):
    # Load players' data when the game starts
    self.load_players_data()

    with open('welcome.txt', 'r') as file:
      welcome_message = file.read()
      print(Color.BOLD + Color.GREEN + welcome_message + Color.RESET)

    while True:
      print("\n1. " + Color.BLUE + "Create a new player" + Color.RESET +
            "\n2. " + Color.BLUE + "Log in" + Color.RESET + "\n3. " +
            Color.BLUE + "Choose Kingdom" + Color.RESET + "\n4. " +
            Color.BLUE + "List players" + Color.RESET + "\n5. " + Color.BLUE +
            "Leaderboard" + Color.RESET + "\n6. " + Color.BLUE + "Save Game" +
            Color.RESET + "\n7. " + Color.BLUE + "Load Game" + Color.RESET +
            "\n8. " + Color.BLUE + "Delete Player Data" + Color.RESET +
            "\n9. " + Color.RED + "Exit" + Color.RESET)
      choice = input(Color.YELLOW + "Enter your choice: " + Color.RESET)

      if choice == '1':
        name = input("Enter your name: ")
        magic_type = input(
            "Choose your magic type (e.g., Fire, Water, Wind): ")
        password = input("Enter your password: ")
        self.create_player(name, magic_type, password)

      elif choice == '2':
        player = self.login_player()
        if player:
          self.choose_kingdom(player)

      elif choice == '3':
        if not self.players:
          print("No players available. Create a new player first.")
        else:
          self.choose_kingdom(random.choice(self.players))

      elif choice == '4':
        self.list_players()

      elif choice == '5':
        self.display_leaderboard()

      elif choice == '6':
        if not self.players:
          print("No players available. Create a new player first.")
        else:
          self.save_game(
              self.players[-1]
          )  # Save the game for the most recently created or logged in player

      elif choice == '7':
        player_name = input("Enter your name to load the game: ")
        self.load_game(player_name)

      elif choice == '8':
        player_name = input("Enter the name of the player data to delete: ")
        self.delete_player_data(player_name)

      elif choice == '9':
        self.save_players_data()
        print("Thanks for playing! Goodbye.")
        break

      else:
        print(Color.RED + "Invalid choice. Please try again." + Color.RESET)


if __name__ == "__main__":
  game = BlackCloverMUD()
  game.start_game()
