-- PostgreSQL
-- Crear la base de datos
CREATE DATABASE prode_db

-- Crear usuario de la base de datos
CREATE USER prode_user WITH PASSWORD 'Agus1986Pro3350';

-- Otorgar todos los permisos sobre la base de datos
GRANT ALL PRIVILEGES ON DATABASE prode_db TO prode_user;

-- Aplicar los cambios en los permisos​
FLUSH PRIVILEGES;

-- Usar la base de datos​
USE prode_db;

-- Crear tabla Team
CREATE TABLE IF NOT EXISTS team (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    external_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    national BOOLEAN NOT NULL,
    image_name VARCHAR(100) DEFAULT NULL
);

-- Crear tabla Player
CREATE TABLE IF NOT EXISTS player (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    external_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    image_name VARCHAR(100) DEFAULT NULL
);

-- Crear tabla Competition
CREATE TABLE IF NOT EXISTS competition (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    external_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    season VARCHAR(10) NOT NULL,
    start_date TIMESTAMP NOT NULL, 
    end_date TIMESTAMP NOT NULL, 
    top_scorer_id BIGINT NOT NULL,
    champion_id BIGINT NOT NULL,
    image_name VARCHAR(100) DEFAULT NULL,
    FOREIGN KEY(top_scorer_id) references player(id), 
    FOREIGN KEY(champion_id) references team(id) 
);

-- Crear tabla Tournament
CREATE TABLE IF NOT EXISTS tournament (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    competition_id BIGINT NOT NULL,
    open BOOLEAN NOT NULL DEFAULT TRUE,
    registered_participants INT NOT NULL DEFAULT 0,
    participant_limit INT NOT NULL,
    entry_price INT NOT NULL,
    public BOOLEAN NOT NULL,
    password VARCHAR(20) DEFAULT NULL,
    FOREIGN KEY(competition_id) references competition(id) 
);

-- Crear tabla User
CREATE TABLE IF NOT EXISTS user_ (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(20) NOT NULL,
    mail VARCHAR(100) NOT NULL,
    password VARCHAR(20) NOT NULL,
    coins BIGINT NOT NULL DEFAULT 0
);

-- Crear tabla Registration
CREATE TABLE IF NOT EXISTS registration (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    tournament_id BIGINT NOT NULL,
    UNIQUE (user_id,tournament_id),
    FOREIGN KEY(user_id) references user_(id),
    FOREIGN KEY(tournament_id) references tournament(id)
);

-- Crear tabla Score
CREATE TABLE IF NOT EXISTS score (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    tournament_id BIGINT NOT NULL,
    points INT NOT NULL DEFAULT 0,
    UNIQUE (user_id,tournament_id),
    FOREIGN KEY(user_id) references user_(id),
    FOREIGN KEY(tournament_id) references tournament(id)
);

-- Crear type match_status
CREATE TYPE match_status AS ENUM (
  'finished','inprogress','canceled','postponed','notstarted'
);

-- Crear tabla Match
CREATE TABLE IF NOT EXISTS match_ (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    external_id BIGINT UNIQUE NOT NULL,
    competition_id BIGINT NOT NULL,
    date TIMESTAMP NOT NULL, 
    home_team_id BIGINT NOT NULL,
    away_team_id BIGINT NOT NULL,
    home_goals INT NOT NULL DEFAULT 0,
    away_goals INT NOT NULL DEFAULT 0,
    play_off BOOLEAN NOT NULL,
    qualified_team_id BIGINT DEFAULT NULL,
    status match_status NOT NULL, 
    FOREIGN KEY(competition_id) references competition(id), 
    FOREIGN KEY(home_team_id) references team(id), 
    FOREIGN KEY(away_team_id) references team(id), 
    FOREIGN KEY(qualified_team_id) references team(id) 
);

-- Crear tabla Match Prediction
CREATE TABLE IF NOT EXISTS match_prediction (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    tournament_id BIGINT NOT NULL,
    match_id BIGINT NOT NULL,
    home_goals INT DEFAULT NULL,
    away_goals INT DEFAULT NULL,
    qualified_team_id BIGINT DEFAULT NULL,
    evaluated BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id,tournament_id,match_id),
    FOREIGN KEY(user_id) references user_(id),
    FOREIGN KEY(tournament_id) references tournament(id), 
    FOREIGN KEY(match_id) references match_(id) 
);

-- Crear tabla Special Prediction
CREATE TABLE IF NOT EXISTS special_prediction (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    user_id BIGINT NOT NULL,
    tournament_id BIGINT NOT NULL,
    champion_id BIGINT DEFAULT NULL,
    top_scorer_id BIGINT DEFAULT NULL,
    evaluated BOOLEAN DEFAULT FALSE,
    UNIQUE (user_id,tournament_id),
    FOREIGN KEY(user_id) references user(id),
    FOREIGN KEY(tournament_id) references tournament(id),
    FOREIGN KEY(champion_id) references team(id), 
    FOREIGN KEY(top_scorer_id) references player(id) 
);

-- Crear tabla Goalscorers
CREATE TABLE IF NOT EXISTS goalscorers (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    competition_id BIGINT NOT NULL,
    player_id BIGINT NOT NULL,
    goals INT NOT NULL DEFAULT 0,
    UNIQUE (competition_id,player_id),
    FOREIGN KEY(competition_id) references competition(id), 
    FOREIGN KEY(player_id) references player(id) 
);

--VOLVER TODO A CERO, BORRAR BASE DE DATOS Y USUARIO
--REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'prode_user'@'localhost';
--DROP USER 'prode_user'@'localhost';
--DROP DATABASE prode_db;