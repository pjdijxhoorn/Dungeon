class TempPlayer:
    """ A class for the temporary player. """

    def __init__(self, name, strength, defence, speed, accuracy, health, player_level, xp, loot, story, attacked=False):
        self.name = name
        self.strength = strength
        self.defence = defence
        self.speed = speed
        self.accuracy = accuracy
        self.health = health
        self.player_level = player_level
        self.xp = xp
        self.loot = loot
        self.story = story
        self.attacked = attacked
