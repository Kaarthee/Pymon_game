#!/usr/bin/env python3
# -- coding: utf-8 --
"""
Created on Wed Oct 16 22:29:55 2024
Pymon skeleton game
Please make modifications to all the classes to match with requirements provided in the assignment spec document
@author: dipto
@student_id : s4075203
@highest_level_attempted (P/C/D/HD): HD

- Reflection:
- Reference:
"""

import random
from datetime import datetime
import sys

# Random number generator
def generate_random_number(max_number=1):
    return random.randint(0, max_number)


class Location:
    def __init__(self, description, name="New room", w=None, n=None, e=None, s=None):
        self.name = name
        self.description = description
        self.doors = {"west": w, "north": n, "east": e, "south": s}
        self.creatures = []
        self.items = []
        self.neighbors = {}
    
    def get_name(self):
        return self.name

    def add_creature(self, creature):
        self.creatures.append(creature)
        
    def add_item(self, item):
        self.items.append(item)
        
    def connect(self, direction, location):
        opposite_directions = {"north": "south", "south": "north", "east": "west", "west": "east"}
        self.doors[direction] = location
        location.doors[opposite_directions[direction]] = self

    def get_creatures(self):
        return self.creatures
    
    def get_items(self):
        return self.items
    
    def get_description(self):
        return self.description

    
class Item:
    def __init__(self, name, description, is_pickable=True):
        self.name = name
        self.description = description
        self.is_pickable = is_pickable

    def get_name(self):
        return self.name

    def can_pick(self):
        return self.is_pickable


class Creature:
    def __init__(self, nickname, description, location, adoptable=True):
        self.nickname = nickname
        self.description = description
        self.location = location
        self.adoptable = adoptable
        self.energy = 3 

    def get_nickname(self):
        return self.nickname
        
    def get_description(self):
        return self.description

    def get_energy(self):
        return self.energy
    
    def set_energy(self, energy):
        self.energy = energy


class Pymon(Creature):
    def __init__(self, nickname, description, location, name="The player"):
        self.name = name
        self.current_location = location
        self.inventory = []
        super().__init__(nickname, description, location)
        self.energy = 3
        self.b_pymon = []
        self.immunity = False
        self.battle_stats = []
    
    def get_location(self):
        return self.current_location

    def spawn(self, loc):
        if loc is not None:
            loc.add_creature(self)
            self.current_location = loc
            print(f"{self.name} has spawned at {loc.get_name()}")

    def pick_item(self, item_name):
        available_items = self.current_location.get_items()
        item_to_pick = next((item for item in available_items if item.get_name().lower() == item_name.lower() and item.can_pick()), None)
        if item_to_pick:
            self.inventory.append(item_to_pick)  # Add item to the inventory
            self.current_location.items.remove(item_to_pick)  # Remove item from the location
            print(f"{item_to_pick.get_name()} picked up!")
        else:
            print(f"{item_name} is not available in this location or is not pickable.")

    def view_inventory(self):
        if not self.b_pymon:
            print("You have no creatures in the inventory")
        else:
            for creature in self.b_pymon:
                print(f"Creature name - {creature.get_nickname()}")
        if not self.inventory:
            print("Items are empty.")
        else:
            for item in self.inventory:
                print(f"{item.name} - {item.description}")

    def move(self, direction):
        if self.current_location and direction in self.current_location.neighbors:
            new_location = self.current_location.neighbors[direction]
            self.current_location = new_location
            print(f"{self.name} moved to {new_location.get_name()}")
        else:
            print("You can't move in that direction.")

    def challenge(self, creature):
        print(f"{self.name} challenges {creature.get_nickname()} to a battle!")
        wins = 0
        losses = 0
        draws = 0
        rounds = 0

        if self.energy == 0:
            print("You have no energy")
            return  # Stop the function if there's no energy
        while self.energy > 0:
            player_move = input("Choose your move (R)ock, (P)aper, (S)cissors: ").capitalize()
            opponent_move = random.choice(["R", "P", "S"])
            print(f"{creature.get_nickname()} chooses {opponent_move}.")

            if player_move == opponent_move:
                print("It's a draw!")
                draws += 1  # Increment draws here
            elif (player_move == "R" and opponent_move == "S") or \
                (player_move == "P" and opponent_move == "R") or \
                (player_move == "S" and opponent_move == "P"):
                print("You win this round!")
                wins += 1
            else:
                print("You lose this round!")
                losses += 1
                if not self.immunity:
                    self.energy -= 1
                else:
                    print("Magic potion absorbed the loss!")
                    self.immunity = False  # Reset immunity after using it

            rounds += 1

            if wins == 2 and creature.adoptable:
                print(f"{self.name} wins the battle and gains {creature.get_nickname()} as a friend!")
                self.b_pymon.append(creature)  # Add to the inventory or pet list
                break
            elif losses == 2:
                print(f"{self.name} lost the battle and loses energy.")
                # Optionally, code to handle movement to a new location or reset
                break
            print("The battle ends in a draw.")

        
        if self.energy == 0:
            print("GAME OVER")
        result = {"date": datetime.now().strftime("%d/%m/%Y %I:%M%p"),
                "opponent": creature.get_nickname(),
                "wins": wins, "draws": draws, "losses": losses}
        self.battle_stats.append(result)

    def generate_battle_stats(self):
        print(f"Pymon Nickname: {self.nickname}")
        for i, battle in enumerate(self.battle_stats, start=1):
            print(f"Battle {i}, {battle['date']} Opponent: {battle['opponent']}, "
                f"W: {battle['wins']} D: {battle['draws']} L: {battle['losses']}")
        total_wins = sum(b['wins'] for b in self.battle_stats)
        total_draws = sum(b['draws'] for b in self.battle_stats)
        total_losses = sum(b['losses'] for b in self.battle_stats)
        print(f"Total: W: {total_wins} D: {total_draws} L: {total_losses}")




class Record:
    def __init__(self):
        self.locations = []
        self.creatures = []
        self.items = []
        self.import_location() 
        self.import_creatures()
        self.import_items()

    def import_location(self):
        with open('locations.csv', 'r') as file:
            next(file)
            for line in file:
                location_data = line.strip().split(',')
                name = location_data[0]
                description = location_data[1]
                west = location_data[2]
                north = location_data[3]
                east = location_data[4]
                south = location_data[5]
                location = Location( description, name, west, north,east,south)
                self.locations.append(location)

    def import_creatures(self):
        with open('creatures.csv', 'r') as file:
            next(file)
            for line in file:
                creature_data = line.strip().split(',')
                name = creature_data[0]
                description = creature_data[1]
                adoptable = creature_data[2].lower()  # Convert to Boolean
                if adoptable == "no":
                    adoptable = False
                else:
                    adoptable = True
                creature = Creature(name, description, None, adoptable)  # Use the new adoptable attribute
                self.creatures.append(creature)
                

    def import_items(self):
        with open('items.csv', 'r') as file:
            next(file)
            for line in file:
                list_data = line.strip().split(',')
                name = list_data[0]
                description = list_data[1]
                pickable = list_data[2]
                consumable = list_data[3]
                item = {"name": name, "description": description, "pickable": pickable, "consumable": consumable}
                item = Item(name, description, pickable)
                self.items.append(item)

    
    def random_location(self):
        return random.choice(self.locations)
    def generate_random_no(self, max_number = 1):
        return random.randint(0, max_number)
    def distribute_creatures(self):
        for location in self.locations:
            random_creatures = random.sample(self.creatures, k = random.randint(1, len(self.creatures)))
            for creatures in random_creatures:
                location.add_creature(creatures)
            random_items = random.sample(self.items, k = random.randint(1, len(self.items)))
            for items in random_items:
                location.add_item(items)
            
    def random_creatures(self):
        return random.choice(self.creatures)
    def random_items(self):
        return random.choice(self.items)


class Operation:
    def __init__(self):
        self.record = Record()
        # Select a creature and use its attributes to create a Pymon instance
        chosen_creature = self.record.random_creatures()
        self.current_pymon = Pymon(
            nickname=chosen_creature.nickname,
            description=chosen_creature.description,
            location=self.record.random_location()
        )
        self.current_pymon.spawn(self.current_pymon.current_location)
        self.record.distribute_creatures()

    def handle_menu(self):
        while True:
            print("\nPlease issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an item")
            print("5) View Inventory ")
            print("6) Challenge a Creature ")
            print("7) Generate the statistics ")
            print("8) Create a Custom location")
            print("9) Create a Custom Creature")
            print("10) Save Progress")
            print("11) Load Progress")
            print("12) Exit the program")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.inspect_pymon()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                self.move_pymon()
            elif choice == "4":
                item_name = input("Picking what: ")
                self.current_pymon.pick_item(item_name)
            elif choice == "5":
                self.current_pymon.view_inventory()
            elif choice == "6":
                self.select_and_challenge_creature()
            elif choice == "7":
                self.current_pymon.generate_battle_stats()    
            elif choice == "8":
                self.custom_location()
            elif choice == "9":
                self.custom_creature()
            elif choice == "10":
                self.save_game()
            elif choice == "11":
                self.load_game()
            elif choice == "12":
                print("Exiting game.")
                sys.exit()
            else:
                print("Invalid choice, please try again.")
    
    def save_game(self):
        try:
            with open("save2024.csv", "w") as file:
                # Save Pymon details
                file.write(f"Pymon|{self.current_pymon.nickname}|{self.current_pymon.energy}|{self.current_pymon.current_location.name}\n")
                
                # Save inventory items
                for item in self.current_pymon.inventory:
                    file.write(f"Inventory|{item.name}|{item.description}|{item.is_pickable}\n")
                
                # Save battle history
                for battle in self.current_pymon.battle_stats:
                    file.write(f"Battle|{battle['date']}|{battle['opponent']}|{battle['wins']}|{battle['draws']}|{battle['losses']}\n")
            
            print("Game saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        try:
            with open("save2024.csv", "r") as file:
                self.current_pymon.inventory.clear()  # Clear current inventory
                self.current_pymon.battle_stats.clear()  # Clear current battle stats
                
                for line in file:
                    parts = line.strip().split("|")
                    if parts[0] == "Pymon":
                        # Restore Pymon details
                        self.current_pymon.nickname = parts[1]
                        self.current_pymon.energy = int(parts[2])
                        location_name = parts[3]
                        # Locate the corresponding location by name
                        self.current_pymon.current_location = next(
                            (loc for loc in self.record.locations if loc.get_name() == location_name), None
                        )
                    elif parts[0] == "Inventory":
                        # Restore inventory items
                        item_name, item_description, is_pickable = parts[1], parts[2], parts[3] == 'True'
                        self.current_pymon.inventory.append(Item(item_name, item_description, is_pickable))
                    elif parts[0] == "Battle":
                        # Restore battle history
                        battle = {
                            "date": parts[1],
                            "opponent": parts[2],
                            "wins": int(parts[3]),
                            "draws": int(parts[4]),
                            "losses": int(parts[5])
                        }
                        self.current_pymon.battle_stats.append(battle)
            
            print("Game loaded successfully.")
        except Exception as e:
            print(f"Error loading game: {e}")
            
    def custom_location(self):
        name = input("Enter the name of the location: ")
        description = input("Enter the description: ")
        west = input("Enter the connection from west, nothing is present type None: ")
        north =input("Enter the connection from north, nothing is present type None: ")
        east =input("Enter the connection from east, nothing is present type None: ")
        south = input("Enter the connection from south, nothing is present type None: ")
        file =  open ('locations.csv', 'a')
        sentence = name +", "+description+"., "+ west+", "+ north+", "+east+", "+south
        file.write(sentence)
        self.record.import_location()
    
    def custom_creature(self):
        name = input("Enter the creature name: ")
        description = input("Enter description: ") 
        adoptable = input("Is it adoptable(yes/no): ")
        file = open ('creatures.csv', 'a')
        sentence = name +", "+description +", "+adoptable+", "
        file.write(sentence)
        self.record.import_creatures()
    def move_pymon(self):
        direction = input("Enter direction to move (north, south, east, west): ").strip().lower()
        self.current_pymon.move(direction)
    
    def inspect_pymon(self):
        print("\nPymon Information:")
        print(f"Name: {self.current_pymon.get_nickname()}")
        print(f"Description: {self.current_pymon.get_description()}")
        print(f"Energy Level: {self.current_pymon.energy}")

    def inspect_location(self):
        loc = self.current_pymon.get_location()
        print(f"\nCurrent Location: {loc.get_name()}")
        print(f"Description: {loc.get_description()}")
        print("Creatures here:")
        for creature in loc.get_creatures():
            print(f"- {creature.get_nickname()}: {creature.get_description()}")
        print("Items here:")
        for item in loc.get_items():
            print(f"- {item.name} - {item.description}")  # Accessing the attribute directly
        if not loc.get_items():
            print("No items")

    
    def select_and_challenge_creature(self):
        creatures = self.current_pymon.get_location().get_creatures()
        if not creatures:
            print("No creatures here to challenge.")
            return

        print("Creatures available to challenge:")
        for i, creature in enumerate(creatures):
            print(f"{i + 1}) {creature.get_nickname()} - {creature.get_description()}")

        choice = input("Enter the number of the creature you want to challenge: ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(creatures):
                self.current_pymon.challenge(creatures[index])
            else:
                print("Invalid choice. No challenge initiated.")
        except ValueError:
            print("Invalid input. Please enter a number.")



if __name__ == "__main__":  # Start without a location
    ops = Operation()  # Initialize operation with the Pymon instance
    ops.handle_menu()
