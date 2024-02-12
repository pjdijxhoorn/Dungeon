class TempPlayer:
    """ A class for the temporary player. """

    def __init__(self, name, strenght, defence, speed, accuracy, health, player_level, xp, loot, story, attacked=False):
        self.name = name
        self.strenght = strenght
        self.defence = defence
        self.speed = speed
        self.accuracy = accuracy
        self.health = health
        self.player_level = player_level
        self.xp = xp
        self.loot = loot
        self.story = story
        self.attacked = attacked
