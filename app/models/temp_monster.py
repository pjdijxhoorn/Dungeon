class TempMonster:
    """ A class for the temporary monster. """

    def __init__(self, name, strength, defence, speed, accuracy, health, zone_difficulty, attacked=False):
        self.name = name
        self.strength = strength
        self.defence = defence
        self.speed = speed
        self.accuracy = accuracy
        self.health = health
        self.zone_difficulty = zone_difficulty
        self.attacked = attacked
