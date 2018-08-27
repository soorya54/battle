from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# create black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 10, 100, "black")
meteor = Spell("Meteor", 20, 200, "black")
quake = Spell("Quake", 14, 140, "black")

# create white magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 18, 200, "white")

# create items
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heal for 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals for 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item": grenade, "quantity": 5}]

# instantiate person
player1 = Person("Sasuke :", 360, 65, 60, 34, player_spells, player_items)
player2 = Person("Roronoa:", 360, 65, 60, 34, player_spells, player_items)
player3 = Person("Vegeta :", 360, 65, 60, 34, player_spells, player_items)

enemy1 = Person("TOBI  ", 500, 65, 100, 75, [], [])
enemy2 = Person("PAIN", 1200, 65, 45, 25, [], [])
enemy3 = Person("ZETSU ", 500, 65, 100, 75, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!" + bcolors.ENDC)

while running:
    print("=====================")

    print("\n\n")
    print("NAME                   HP                                  MP")
    for player in players:
        player.get_stats()
    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("    Choose action : ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name + " for", dmg, "points.")
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("\n    Choose magic : ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough Magic Points\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "heals", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name, "deals", str(magic_dmg), "points of damage to "
                      + enemies[enemy].name + bcolors.ENDC)
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item : ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage for "
                      + enemies[enemy].name + bcolors.ENDC)

    enemy_choice = 1
    target = random.randrange(0, len(players))
    enemy_dmg = enemies[0].generate_damage()
    players[target].take_damage(enemy_dmg)
    print("Enemy attacks for", enemy_dmg, "points.")

    if enemies[1].get_hp() == 0:
        print(bcolors.OKGREEN + "You Win!!" + bcolors.ENDC)
        running = False
    elif players[0].get_hp() == 0:
        print(bcolors.FAIL + "The Enemy has defeated you!!" + bcolors.ENDC)
        running = False
