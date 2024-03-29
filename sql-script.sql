DROP TABLE IF EXISTS Training, Fitness_profile, player_base_stats, Monsters, random_encounters, Gear,equipped_gear, Clan, player;

CREATE TABLE player (
    player_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    name VARCHAR(255),
    main_score INT,
    training_score INT[],
    fitness_multiplier FLOAT
);

CREATE TABLE player_base_stats (
    player_base_stats_id SERIAL PRIMARY KEY,
    player_id INT UNIQUE,
    strength INT,
    defence INT,
    speed INT,
    health INT,
    accuracy INT,
    player_level INT,
    xp INT,
    loot INT,
    xp_remaining INT,
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

CREATE TABLE Fitness_profile (
    profile_id SERIAL PRIMARY KEY,
    player_id INT UNIQUE,
    bmi FLOAT,
    weight_in_kg FLOAT,
    height_in_m FLOAT,
    date_of_birth DATE,
    max_heart_frequency INT,
    rest_heart_frequency INT,
    reserve_heart_frequency INT,
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);


CREATE TABLE Training (
    training_id SERIAL PRIMARY KEY,
    training_name VARCHAR(255),
    distance_in_meters INT,
    time_in_seconds INT,
    average_speed FLOAT,
    training_type VARCHAR(255),
    base_score INT,
    training_date DATE,
    player_id INT,
    already_used_for_dungeon_run BOOLEAN,
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);


CREATE TABLE Monsters (
    monster_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    defence INT,
    strength INT,
    health INT,
    speed INT,
    accuracy INT,
    zone_difficulty VARCHAR(255)
);


CREATE TABLE Random_encounters (
    encounter_id SERIAL PRIMARY KEY,
    encounter_text VARCHAR(255),
    encounter_stat_type VARCHAR(255),
    encounter_stat INT
);


CREATE TABLE Gear (
    gear_id SERIAL PRIMARY KEY,
    gear_name VARCHAR(255),
    gear_class VARCHAR(255),
    gear_slot VARCHAR(255),
    gear_stat_type VARCHAR(255),
    gear_stat INT,
    gear_price INT,
    buy_able BOOLEAN
);


CREATE TABLE equipped_gear (
    equipped_gear_id SERIAL PRIMARY KEY,
    player_id INT,
    equipped_slot_head INT,
    equipped_slot_weapon INT,
    equipped_slot_armor INT,
    equipped_slot_boots INT,
    equipped_slot_title INT,
    FOREIGN KEY (player_id) REFERENCES player(player_id),
    FOREIGN KEY (equipped_slot_head) REFERENCES Gear(gear_id),
    FOREIGN KEY (equipped_slot_weapon) REFERENCES Gear(gear_id),
    FOREIGN KEY (equipped_slot_armor) REFERENCES Gear(gear_id),
    FOREIGN KEY (equipped_slot_boots) REFERENCES Gear(gear_id),
    FOREIGN KEY (equipped_slot_title) REFERENCES Gear(gear_id)
);


CREATE TABLE Clan (
    clan_id SERIAL PRIMARY KEY,
    player_id INT,
    clan_name VARCHAR(255),
    clan_role VARCHAR(255),
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

INSERT INTO Player (username, password, name, main_score, training_score, fitness_multiplier)
VALUES
  ('user1', '$2a$12$vMbCRTOZcCscO4iA9EbnWeLnYrfEYtM0fr9BopK/QFB/53Ub60/42', 'User One', 430, '{80, 95, 75, 85, 95}', 0.33),
  ('user2', '$2a$12$cuv50PlaZY8gpwa.NgKQCemAkQCeSbKA7GWrjS2Imp7lE4Hd1AZ7W', 'User Two', 425, '{80, 90, 75, 85, 95}', 0.28),
  ('user3', '$2a$12$EArutIUyZoG/yFxuM2bh1.BumQP3NLIIvAnKxcKh/Y/OX39MDlQ4S', 'User Three', 435, '{85, 95, 75, 85, 95}', 0.33),
  ('user4', '$2a$12$1b1hXeBeAL5rNsDeDdFsUu8VLdcA/ZE9IBEUug9b6kmn8t28alPFG', 'User Four', 445, '{80, 90, 95, 85, 95}', 0.30),
  ('user5', '$2a$12$Yw/6PvhHd5c3X02zyFonXO9NsrGZkvXclI8/CcKdmYnWecBnKxVnC', 'User Five', 450, '{80, 85, 90, 95, 100}', 0.34),
  ('user6', '$2a$12$q.e6Hi0RqVJbq2nDgidX4O/DWMY4UB1YIKZxfMqfBVEa3PV5TDd.i', 'User Six', 475, '{85, 90, 95, 100, 105}', 0.35),
  ('user7', '$2a$12$BFaWTz8aKajzAbgI7Epx0eZQGNDjuGU5ynL4ile54jQzQV1/1i/PS', 'User Seven', 500, '{90, 95, 100, 105, 110}', 0.36),
  ('user8', '$2a$12$sc7YYLq6sKVhYXGg1wWCXunWXhYr1/UtK6eagKeNCWQdOtZqHIIW6', 'User Eight', 525, '{95, 100, 105, 110, 115}', 0.37),
  ('user9', '$2a$12$n4vajXJ65xOb4FL01b4kjeYnqsacTkSFrE.RfgMYCIHLBhJr9oosW', 'User Nine', 550, '{100, 105, 110, 115, 120}', 0.38),
  ('user10', '$2a$12$OMg82PdM6.P1dvS64u34nOdoFkzS3Dqufqi2bw/.y6p6K4Jz59Tzm', 'User Ten', 575, '{105, 110, 115, 120, 125}', 0.39),
  ('user11', '$2a$12$U/HFoeSNxaeGi21KqWmjiOlmftlLKgN06J/UEIpIOaEz8omKPYLnS', 'User Eleven', 600, '{110, 115, 120, 125, 130}', 0.40),
  ('user12', '$2a$12$A4tI7jPDWDzxZeM0QFaSiO132KuN.zCjgrB5vMSkcXra56KVKYxmi', 'User Twelve', 625, '{115, 120, 125, 130, 135}', 0.41),
  ('user13', '$2a$12$EKvqvV1hAcLGY425NnUYZO/7iZImsATZfBqASRoR7lMUE0deh0vL6', 'User Thirteen', 650, '{120, 125, 130, 135, 140}', 0.42),
  ('user14', '$2a$12$2sNbJyNfNbmhkhHozOnJJ.Ae8LwpqYbmznJRSLfbJBVz095SBJPXC', 'User Fourteen', 675, '{125, 130, 135, 140, 145}', 0.43);


INSERT INTO player_base_stats (player_id, strength, defence, speed, health, accuracy, player_level, xp, loot, xp_remaining)
VALUES
(1, 5, 5, 5, 100, 5, 1, 0, 0, 100),
(2, 20, 20, 20, 200, 90, 2, 0, 10000, 500),
(3, 9, 13, 10, 100, 12, 1, 0, 0, 100),
(4, 11, 9, 13, 100, 11, 1, 0, 0, 100),
(5, 10, 11, 9, 100, 14, 1, 0, 0, 100),
(6, 14, 12, 8, 100, 10, 1, 0, 0, 100),
(7, 8, 14, 12, 100, 10, 1, 0, 0, 100),
(8, 13, 7, 11, 100, 13, 1, 0, 0, 100),
(9, 10, 12, 14, 100, 8, 1, 0, 0, 100),
(10, 12, 10, 7, 100, 15, 1, 0, 0, 100),
(11, 11, 14, 9, 100, 10, 1, 0, 0, 100),
(12, 7, 8, 15, 100, 14, 1, 0, 0, 100),
(13, 15, 11, 10, 100, 8, 1, 0, 0, 100),
(14, 9, 15, 13, 100, 9, 1, 0, 0, 100);


INSERT INTO Fitness_profile (player_id, bmi, weight_in_kg, height_in_m, date_of_birth, max_heart_frequency, rest_heart_frequency, reserve_heart_frequency)
VALUES
(1, 25.5, 70.5, 175, TO_DATE('15-01-1990', 'DD-MM-YYYY'), 180, 60, 120),
(2, 22.0, 65.2, 170, TO_DATE('20-03-1985', 'DD-MM-YYYY'), 175, 58, 115),
(3, 26.8, 75.0, 180, TO_DATE('10-07-1992', 'DD-MM-YYYY'), 185, 62, 125),
(4, 23.3, 68.7, 172, TO_DATE('05-05-1988', 'DD-MM-YYYY'), 178, 59, 118),
(5, 24.0, 70.0, 175, TO_DATE('15-01-1991', 'DD-MM-YYYY'), 182, 60, 122),
(6, 23.5, 68.0, 172, TO_DATE('20-03-1986', 'DD-MM-YYYY'), 176, 58, 116),
(7, 25.0, 75.0, 180, TO_DATE('10-07-1993', 'DD-MM-YYYY'), 186, 62, 126),
(8, 24.5, 72.0, 178, TO_DATE('05-05-1989', 'DD-MM-YYYY'), 180, 60, 120),
(9, 23.0, 67.0, 170, TO_DATE('12-09-1990', 'DD-MM-YYYY'), 178, 59, 119),
(10, 24.3, 73.0, 176, TO_DATE('23-11-1987', 'DD-MM-YYYY'), 183, 61, 123),
(11, 22.8, 66.0, 174, TO_DATE('17-02-1992', 'DD-MM-YYYY'), 179, 60, 119),
(12, 25.5, 76.0, 182, TO_DATE('29-08-1988', 'DD-MM-YYYY'), 188, 63, 128),
(13, 24.7, 71.0, 177, TO_DATE('14-04-1995', 'DD-MM-YYYY'), 182, 61, 123),
(14, 23.2, 69.0, 173, TO_DATE('21-06-1994', 'DD-MM-YYYY'), 177, 59, 118);


INSERT INTO Training (training_name, distance_in_meters, time_in_seconds, average_speed, training_type, base_score, training_date, player_id, already_used_for_dungeon_run)
VALUES
('Morning run', 8000, 1800, 10, 'Sprint', 75, TO_DATE('16-01-2024', 'DD-MM-YYYY'), 1, FALSE),
('round the lake', 10000, 2400, 6.25, 'Endurance', 80, TO_DATE('17-01-2024', 'DD-MM-YYYY'), 2, FALSE),
('romantic run towards SO', 8000, 1500, 15, 'Sprint', 90, TO_DATE('18-01-2024', 'DD-MM-YYYY'), 3, FALSE),
('run after icecream-van', 100, 100, 1, 'Sprint', 85, TO_DATE('19-01-2024', 'DD-MM-YYYY'), 4, FALSE),
('ran from scary clown', 6000, 2700, 4.44, 'Sprint', 95, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 4, FALSE),
('Evening Walk', 3000, 1800, 5, 'Endurance', 60, TO_DATE('21-01-2024', 'DD-MM-YYYY'), 5, FALSE),
('Hill Climb', 4000, 2400, 4, 'Endurance', 65, TO_DATE('22-01-2024', 'DD-MM-YYYY'), 6, FALSE),
('Speed Run', 5000, 1500, 10, 'Sprint', 70, TO_DATE('23-01-2024', 'DD-MM-YYYY'), 7, FALSE),
('Trail Run', 6000, 2700, 6.66, 'Endurance', 75, TO_DATE('24-01-2024', 'DD-MM-YYYY'), 8, FALSE),
('City Jog', 7000, 2100, 7.14, 'Endurance', 80, TO_DATE('25-01-2024', 'DD-MM-YYYY'), 9, FALSE),
('Beach Run', 8000, 1600, 12.5, 'Endurance', 85, TO_DATE('26-01-2024', 'DD-MM-YYYY'), 10, FALSE),
('Forest Hike', 9000, 3600, 5, 'Endurance', 65, TO_DATE('27-01-2024', 'DD-MM-YYYY'), 11, FALSE),
('Mountain Trek', 10000, 4800, 3.75, 'Endurance', 70, TO_DATE('28-01-2024', 'DD-MM-YYYY'), 12, FALSE),
('Park Sprint', 2000, 600, 20, 'Sprint', 90, TO_DATE('29-01-2024', 'DD-MM-YYYY'), 13, FALSE),
('Night Jog', 3500, 1500, 7, 'Endurance', 75, TO_DATE('30-01-2024', 'DD-MM-YYYY'), 14, TRUE);


INSERT INTO Monsters (name, defence, strength, health, speed, accuracy, zone_difficulty)
VALUES
('Rat', 2, 2, 3, 4, 4, 'easy'),
('Slime', 1, 1, 2, 3, 3, 'easy'),
('Gnome', 3, 4, 4, 5, 6, 'easy'),
('Spider', 2, 3, 3, 4, 4, 'easy'),
('Bat', 1, 1, 2, 2, 2, 'easy'),
('Snake', 1, 2, 2, 3, 3, 'easy'),
('Kobold', 2, 3, 3, 4, 4, 'easy'),
('Skeleton', 3, 4, 4, 5, 6, 'easy'),
('Zombie', 5, 5, 6, 7, 8, 'easy'),
('Orc', 20, 22, 25, 23, 24, 'medium'),
('Goblin', 18, 20, 22, 20, 21, 'medium'),
('Troll', 22, 24, 26, 24, 25, 'medium'),
('stoned golem', 22, 24, 26, 24, 25, 'medium'),
('ghost', 22, 24, 26, 24, 25, 'medium'),
('mummy', 22, 24, 26, 24, 25, 'medium'),
('Ghoul', 23, 25, 27, 25, 26, 'medium'),
('Specter', 24, 26, 28, 26, 27, 'medium'),
('Wraith', 25, 27, 29, 27, 28, 'medium'),
('Lizardman', 24, 26, 28, 27, 28, 'medium'),
('Centaur', 25, 27, 29, 28, 29, 'medium'),
('vampire', 22, 24, 26, 24, 25, 'medium'),
('harpy', 22, 24, 26, 24, 25, 'medium'),
('Yeti', 40, 42, 45, 43, 44, 'hard'),
('Cyclops', 35, 38, 40, 38, 39, 'hard'),
('Manticore', 50, 52, 55, 50, 51, 'hard'),
('Necromancer', 38, 40, 42, 40, 41, 'hard'),
('Werewolf', 25, 28, 30, 28, 29, 'hard'),
('demon', 25, 28, 30, 28, 29, 'hard'),
('minotaur', 25, 28, 30, 28, 29, 'hard'),
('banshee', 25, 28, 30, 28, 29, 'hard'),
('Chimera', 40, 42, 45, 43, 44, 'hard'),
('Gorgon', 38, 40, 42, 40, 41, 'hard'),
('Jinn', 48, 50, 52, 50, 51, 'hard'),
('Giant', 42, 45, 48, 45, 46, 'hard'),
('Basilisk', 30, 35, 38, 35, 36, 'hard'),
('Cerberus', 48, 50, 52, 50, 51, 'hard'),
('suing lawyers', 48, 50, 52, 50, 51, 'hard'),
('5,389 orcs', 48, 50, 52, 50, 51, 'hard'),
('Mother in law', 80, 90, 150, 96, 98, 'boss'),
('Dragon', 75, 80, 130, 88, 90, 'boss'),
('lich-king', 75, 80, 120, 88, 90, 'boss'),
('hydra', 75, 80, 180, 88, 90, 'boss'),
('kraken', 75, 80, 200, 88, 90, 'boss'),
('Phoenix', 85, 88, 250, 92, 95, 'boss'),
('Siren', 70, 75, 160, 82, 85, 'boss'),
('Banshee', 72, 78, 180, 85, 88, 'boss');

INSERT INTO Random_encounters (encounter_text, encounter_stat_type, encounter_stat)
VALUES
('A mischievous squirrel challenges you to a dance-off! Lose 3 speed points, but gain street cred.', 'speed', -3),
('You encounter a group of singing mushrooms. Your accuracy improves by 8 points as you join their harmony.', 'accuracy', 8),
('A clumsy wizard turns you into a rubber chicken. Your defences drop by 5 points, but your enemies find you hilarious.', 'defence', -5),
('You stumble upon a talking rock. It insults you, but you gain wisdom. Your XP increases by 15 points.', 'xp', 15),
('An enchanted mirror reflects your true self. Lose 5 accuracy points, but gain self-awareness.', 'accuracy', -5),
('You accidentally step on a banana peel. Your speed decreases by 4 points, and you learn the importance of caution.', 'speed', -4),
('A group of friendly ghosts offers you spectral tea. Your health is restored by 15 points, and you make new ghostly friends.', 'health', 15),
('A disco ball descends from the sky, and you can’t resist dancing. Lose 2 defence points.', 'defence', -2),
('A lawyer left a curse of income tax you have to pay 10 coins form your loot to continue.', 'loot', -10),
('You encounter a dragon layer however there you see that the dragon is out to lunch so you loot his treasure.', 'loot', 100),
('Curse duck of doom you should know better then picking up a duck inn a dungeon.', 'health', -5),
('You meet a sitcom witch to teach you a valuable lesson she turns you to the opposite gender nothing happens with you stats its just strange.', 'health', 0),
('You rescue a lost kitten, and its grateful owner turns out to be a wealthy merchant. You got 25 loot as a token of appreciation for your kindness.', 'loot', 25),
('Operations Paul, the guardian of coding standards, sends you an animated GIF expressing his displeasure with the recent code changes. Lose 15 XP points as you attempt to decode his GIF-based feedback.', 'xp', -15),
('Hyperactive hamster insists you join their wheel workout. You gained 7 speed points.', 'speed', 7),
('You meet one of the developers he gives you a cheat if you stop being annoying and go away.', 'health', 100);




INSERT INTO Gear (gear_id, gear_name, gear_class, gear_slot, gear_stat_type, gear_stat, gear_price, buy_able)
VALUES
(0, 'empty', 'common', 'all', 'none', 0, 0, False),
(1, 'Baseball Cap', 'common', 'Head', 'defence', 10, 20, True),
(2, 'Iron Sword', 'uncommon', 'Weapon', 'strength', 15, 50, True),
(3, 'Leather Armor', 'common', 'Armor', 'defence', 10, 30, True),
(4, 'Twig', 'legendary', 'Weapon', 'accuracy', 90, 100, True),
(5, 'Steel Armor', 'uncommon', 'Armor', 'defence', 20, 60, True),
(6, 'Water Pistol', 'common', 'Weapon', 'speed', 7, 15, True),
(7, 'Silver Dagger', 'epic', 'Weapon', 'strength', 60, 80, True),
(8, 'Chainmail', 'uncommon', 'Armor', 'defence', 20, 70, True),
(9, 'Pink Boots', 'common', 'Boots', 'speed', 18, 25, True),
(10, 'Fork', 'common', 'Weapon', 'strength', 3, 5, True),
(11, 'Mr. Spaghetti arms', 'common', 'Title', 'strength', 5, 0, False),
(12, 'mace of sharpness(stick with knife tied to it)', 'common', 'Weapon', 'strength', 2, 20, True),
(13, 'huge rock', 'common', 'Weapon', 'strength', 3, 20, True),
(14, 'horny helmet', 'common', 'Head', 'defence', 3, 20, True),
(15, 'big spender', 'epic', 'Title', 'defence', 3, 1500, True),
(16, 'boots of running really fast', 'epic', 'Boots', 'speed', 15, 100, True),
(17, 'rat on a stick(hey its better then nothing)', 'common', 'Weapon', 'Boots', 1, 1, True),
(18, 'really impressive title', 'legendary', 'Title', 'strength', 15, 0, False);

INSERT INTO equipped_gear (player_id, equipped_slot_head, equipped_slot_weapon, equipped_slot_armor, equipped_slot_boots, equipped_slot_title)
VALUES
(1, 0, 0, 0, 0, 0),
(2, 4, 7, 8, 10, 11),
(3, 3, 5, 6, 9, 11),
(4, 2, 4, 8, 9, 11),
(5, 1, 7, 5, 10, 11),
(6, 6, 3, 8, 9, 11),
(7, 4, 1, 2, 9, 11),
(8, 2, 5, 7, 10, 11),
(9, 1, 9, 4, 10, 11),
(10, 3, 6, 8, 9, 11);

INSERT INTO Clan (player_id, clan_name, clan_role)
VALUES
  (1, 'Sassy Sisters', 'Leader'),
  (2, 'Sassy Sisters', 'Member'),
  (3, 'Sassy Sisters', 'Member'),
  (4, 'Sassy Sisters', 'Member'),
  (5, 'Sassy Sisters', 'Member'),
  (6, 'Glitter Bandits', 'Leader'),
  (7, 'Glitter Bandits', 'Member'),
  (8, 'Glitter Bandits', 'Member'),
  (9, 'Glitter Bandits', 'Member'),
  (10, 'Glitter Bandits', 'Member'),
  (11, 'Swole Patrol', 'Leader'),
  (12, 'Swole Patrol', 'Member'),
  (13, 'Swole Patrol', 'Member'),
  (14, 'Swole Patrol', 'Member');
