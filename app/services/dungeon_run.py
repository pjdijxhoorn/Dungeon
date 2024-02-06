from random import randint


def get_Dungeon_run():
    # ophalen van speler
    # ophalen van training
    # checken of training al gebruikt is voor dungeon run
    # ophalen basestats + gear bij optellen
    # average speed optellen? gebruiken voor extra stats

    # calculatie voor kans tegenkomen van monster per afgelegde meter
    # als monseter tegen komen monster zone ophalen  en mosnter ophalen
    # monster kracht berekenen
    # gevecht met monster
        # meerder beurten totdat of jij of het monster dood is monster moet dezelfde stats hebben?
        # monster dood loot berekenen en toevoegen aan speler? aan het einde ?
        # berekenen opgedane xp
    # einde van de dungeon te gaan xp genoeg om te levelen?
    # loot erbij
    # bonus voor bereiken einde dungeon zonder dood te gaan
    # titles toekennen aan de speler
    return "hello"


def random_number(chance):
    return randint(1, chance)

def get_monster():
    return "nog niks"


# def monster battle
# gebaseerd op stats

# def get monster block
def gain_xp(base_stats, amount):
    base_stats.xp += amount
    # print(f"{base_stats.name} gained {amount} XP!")

    # Check for level up
    while base_stats.xp >= calculate_xp_required(base_stats):
        level_up(base_stats)
    # todo increase base stats

def level_up(base_stats):
    base_stats.level += 1
    remaining_xp = base_stats.xp - calculate_xp_required()
    base_stats.xp = 0 if remaining_xp < 0 else remaining_xp
   # print(f"{self.name} leveled up to level {self.level}!")


def calculate_xp_required(base_stats):
    return 100 + (base_stats.level-1) ** 3