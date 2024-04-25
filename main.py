
"""
Author:         Lester Pasig
Date:           25 April 2024
Assignment:     Project 2 RPG
Course:         CPSC1050
Lab Section:    002

CODE DESCRIPTION:
Adventure text based RPG in python.

GITHUB Link: https://github.com/kamaboko-g/CPSC1050-Project-2
"""
from character import Character
import random
import os

hero = Character(name="Hero", health = 100, damage = 5)

class Enemy(Character):
    def __init__(self, name: str):
        # Randomize health and damage for the enemy
        health = random.randint(50, 100)
        damage = random.randint(5, 15)
        super().__init__(name, health, damage)


class ExitNotFoundError(Exception):
    def __init__(self, value, message='Invalid command'):
        self.value = value
        self.message = message

    def __str__(self):
        return f"{self.value} -> {self.message}"

class Room():
    def __init__(self, name, description, options):
        self.name = name
        self.description = description
        self.options = [option_name.lower() for option_name in options]
        self.encounter_chance = 0.5  # Adjust encounter chance as needed
        
    def get_name(self):
        # Returns name of the room (capitalized version)
        return self.name
    
    def get_description(self):
        # Returns the description of the room
        return self.description
    
    def get_options(self):
        # Returns the list of options
        return self.options
    
    def list_options(self):
        # Returns a string representation of the exits (capitalized version)
        option_str = ''
        for e in self.options:
            option_str += '\n' + e
        return f'{option_str}'
    
    def trigger_encounter(self):
        # Determines whether an encounter occurs in this room
        return random.random() < self.encounter_chance
    def explore(self):
        # Increases the encounter chance when exploring
        self.encounter_chance += 0.1  # Increase encounter chance by 10%
        print("You decided to explore. The encounter chance has increased!")

    def __str__(self):
        # Returns a string representation of the room including its name, description, and exits
        info = ''
        info += f'{self.name}: {self.description}'
        info += f'\n'
        info += f'\nOptions:'
        info += f'{self.list_options()}'
        return info

class AdventureMap():
    def __init__(self):
        self.rooms = {}

    def add_room(self, room):
        # Adds a room to the map.
        room.options = [option_name.lower() for option_name in room.options]
        self.rooms[room.name.lower()] = room  # Lowercase the room name

    def get_room(self, room_name):
        # Returns a room from the map given its name
        return self.rooms.get(room_name.lower())

    def handle_encounter(self, room):
        if room.name.lower() == "dungeon":
            print("You encountered a fearsome enemy in the dungeon!")
            enemy = Enemy("Fearsome Enemy")
            # Start the battle with the enemy
            battle(hero, enemy)

        elif room.name.lower() == "forest":
            print("You stumbled upon a wild beast in the forest!")
            enemy = Enemy("Wild Beast")
            # Start the battle with the enemy
            battle(hero, enemy)

def battle(player, enemy):
    print("Battle starts!")
    while player.health > 0 and enemy.health > 0:
        # Player's turn
        print(f"{player.name}'s turn:")
        action = input("Choose your action (fight/run): ").strip().lower()
        if action == "fight":
            player.attack(enemy)
            if enemy.health <= 0:
                print(f"{enemy.name} is defeated!")
                break
        elif action == "run":
            if random.random() < 0.5:  # 50% chance of successfully running away
                print("You successfully escaped from the battle!")
                break
            else:
                print("You failed to escape!")
        else:
            print("Invalid action! Please choose 'fight' or 'run'.")

        # Enemy's turn
        if enemy.health > 0:
            print(f"{enemy.name}'s turn:")
            enemy.attack(player)
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
                break

    # Check the result of the battle
    if player.health > 0:
        print("You have won the battle!")
    else:
        print("You have been defeated! Thanks for playing!")
        exit(1)
          
def main():
    adventure_map = AdventureMap()

    print("\nWelcome to Simple Quest! A simple text based RPG adventure! You start out in the Town Center. Enter 'exit' at anytime to exit the game.\n")

    adventure_map.add_room(Room("Town Center", "The center of the town. You can go anywhere from here.", ['Home', 'Tavern', 'Town Well', 'Forest', 'Dungeon']))
    adventure_map.add_room(Room("Tavern", "A bustling tavern where all adventurers gather for a good time!", ['Town Center']))
    adventure_map.add_room(Room("Forest", "The forest in the outskirts of town. There are many wild animals here. Type 'explore' to see if there are enemies around. ", ['Town Center']))
    adventure_map.add_room(Room("Dungeon", "The dark and dreary dungeon. You can fight random mobs here. Proceed at your own risk. Type 'explore' to see if there are any enemies around.", ['Town Center']))
    adventure_map.add_room(Room("Town Well", "The well at the edge of the town. There is particularly interesting about his place...", ['Town Center', 'Dungeon', 'Forest']))
    adventure_map.add_room(Room("Home", "This is where all heroes start.", ['Town Center']))


    current_room = adventure_map.get_room("Home")
    direction = ''

    while direction != 'exit':
        print(f'{current_room}')

        if current_room.trigger_encounter():
            adventure_map.handle_encounter(current_room)

        while True:
            try:
                direction = input("What would you like to do?\n").strip().lower()
                if direction == 'exit':
                    print("Exiting the game. Thanks for playing!")
                    break
                elif direction == 'explore':
                    current_room.explore()
                    break
                next_room = adventure_map.get_room(direction)
                if next_room is None:
                    raise ExitNotFoundError(direction)
                elif direction in current_room.get_options():  # Check exits from current room
                    current_room = next_room
                    break
                else:
                    raise ExitNotFoundError(direction)
            except ExitNotFoundError as enf:
                print(enf)
                continue 

if __name__ == "__main__":
    main()
