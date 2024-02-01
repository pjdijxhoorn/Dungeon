DROP TABLE IF EXISTS Training, Fitness_profile, player;

-- Create the player table
CREATE TABLE player (
    player_id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    name VARCHAR(255),
    average_score INT,
    training_score INT[],
    fitness_multiplier FLOAT
);

-- Create the Fitness_profile table with a foreign key reference to player
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

-- Create the Training table with a foreign key reference to player
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
    FOREIGN KEY (player_id) REFERENCES player(player_id)
);

INSERT INTO Player (username, password, name, average_score, training_score, fitness_multiplier)
VALUES
  ('user1', '$2a$12$vMbCRTOZcCscO4iA9EbnWeLnYrfEYtM0fr9BopK/QFB/53Ub60/42', 'User One', 425, '{80, 90, 75, 85, 95}', 0.33),
  ('user2', '$2a$12$cuv50PlaZY8gpwa.NgKQCemAkQCeSbKA7GWrjS2Imp7lE4Hd1AZ7W', 'User Two', 429, '{80, 90, 75, 85, 95}', 0.28),
  ('user3', '$2a$12$EArutIUyZoG/yFxuM2bh1.BumQP3NLIIvAnKxcKh/Y/OX39MDlQ4S', 'User Three', 427, '{80, 90, 75, 85, 95}', 0.33),
  ('user4', '$2a$12$1b1hXeBeAL5rNsDeDdFsUu8VLdcA/ZE9IBEUug9b6kmn8t28alPFG', 'User Four', 421, '{80, 90, 75, 85, 95}', 0.30),
  ('user5', '$2a$12$1b1hXeBeAL5rNsDeDdFsUu8VLdcA/ZE9IBEUug9b6kmn8t28alPFG', 'User Five', 3315, '{663, 663, 663, 663, 663}', 0.17);

INSERT INTO Fitness_profile (player_id, bmi, weight_in_kg, height_in_m, date_of_birth, max_heart_frequency, rest_heart_frequency, reserve_heart_frequency)
VALUES
  (1, 25.5, 70.5, 175, TO_DATE('15-01-1990', 'DD-MM-YYYY'), 180, 60, 120),
  (2, 22.0, 65.2, 170, TO_DATE('20-03-1985', 'DD-MM-YYYY'), 175, 58, 115),
  (3, 26.8, 75.0, 180, TO_DATE('10-07-1992', 'DD-MM-YYYY'), 185, 62, 125),
  (4, 23.3, 68.7, 172, TO_DATE('05-05-1988', 'DD-MM-YYYY'), 178, 59, 118),
  (5, 23.9, 80, 1.83,  TO_DATE('05-05-1988', 'DD-MM-YYYY'), 220, 60, 160);

INSERT INTO Training (training_name, distance_in_meters, time_in_seconds, average_speed, training_type, base_score, training_date, player_id)
VALUES
  ('Morning run', 5000, 1800, 10, 'Sprint', 75, TO_DATE('16-01-2024', 'DD-MM-YYYY'), 1),
  ('round the lake', 10000, 2400, 6.25, 'Endurance', 80, TO_DATE('17-01-2024', 'DD-MM-YYYY'), 2),
  ('romantic run towards SO', 8000, 1500, 15, 'Sprint', 90, TO_DATE('18-01-2024', 'DD-MM-YYYY'), 3),
  ('run after icecream-van', 100, 100, 1, 'Sprint', 85, TO_DATE('19-01-2024', 'DD-MM-YYYY'), 4),
  ('ran from scary clown', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 4),
  ('Run forest run', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 5),
  ('forest run forest', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 5),
  ('run run forest', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 5),
  ('spam spam spam', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 5),
  ('egs bacon and spam', 10000, 3600, 39, 'Sprint', 39000, TO_DATE('20-01-2024', 'DD-MM-YYYY'), 5);