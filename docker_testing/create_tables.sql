-- Drop tables if they already exist
DROP TABLE IF EXISTS
    ActiveUsers,
    Votes,
    UserCompetitions,
    PlaylistSongs,
    Playlists,
    Songs,
    Competitions,
    Users
CASCADE;

-- Drop the type 'competition_status' if it exists
DROP TYPE IF EXISTS competition_status;

-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Competitions Enum Type
CREATE TYPE competition_status AS ENUM ('active', 'completed', 'upcoming');

-- Create Competitions Table
CREATE TABLE Competitions (
    competition_id SERIAL PRIMARY KEY,
    status competition_status NOT NULL,
    participants_count INTEGER DEFAULT 0,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    winner_playlist_id INTEGER
);

-- Create Playlists Table
CREATE TABLE Playlists (
    playlist_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_votes INTEGER DEFAULT 0,
    average_score FLOAT DEFAULT 0.0
);

-- Create Songs Table
CREATE TABLE Songs (
    song_id SERIAL PRIMARY KEY,
    song_title VARCHAR(100) NOT NULL,
    artist VARCHAR(100) NOT NULL
);

-- Create PlaylistSongs Table
CREATE TABLE PlaylistSongs (
    id SERIAL PRIMARY KEY,
    playlist_id INTEGER NOT NULL,
    song_id INTEGER NOT NULL,
    song_order INTEGER NOT NULL
);

-- Create UserCompetitions Table
CREATE TABLE UserCompetitions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    enrollment_status BOOLEAN DEFAULT TRUE,
    submission_status BOOLEAN DEFAULT FALSE,
    playlist_id INTEGER,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Votes Table
CREATE TABLE Votes (
    vote_id SERIAL PRIMARY KEY,
    voter_user_id INTEGER NOT NULL,
    playlist_id INTEGER NOT NULL,
    vote_score INTEGER NOT NULL CHECK (vote_score >= 1 AND vote_score <= 5),
    vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create ActiveUsers Table
CREATE TABLE ActiveUsers (
    user_id INTEGER PRIMARY KEY,
    last_active_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add Constraints using ALTER TABLE

-- Add Foreign Key and Unique Constraints for Users
ALTER TABLE Playlists
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE;

ALTER TABLE Playlists
    ADD CONSTRAINT fk_competition_id FOREIGN KEY (competition_id) REFERENCES Competitions(competition_id) ON DELETE CASCADE;

ALTER TABLE Playlists
    ADD CONSTRAINT unique_playlist_user UNIQUE (user_id, competition_id);  -- Ensure no duplicates

ALTER TABLE PlaylistSongs
    ADD CONSTRAINT fk_playlist_id FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id) ON DELETE CASCADE;

ALTER TABLE PlaylistSongs
    ADD CONSTRAINT fk_song_id FOREIGN KEY (song_id) REFERENCES Songs(song_id) ON DELETE CASCADE;

ALTER TABLE PlaylistSongs
    ADD CONSTRAINT unique_song_playlist UNIQUE (song_id, playlist_id);  -- Ensure no duplicates

ALTER TABLE UserCompetitions
    ADD CONSTRAINT fk_user_competition_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE;

ALTER TABLE UserCompetitions
    ADD CONSTRAINT fk_user_competition_competition_id FOREIGN KEY (competition_id) REFERENCES Competitions(competition_id) ON DELETE CASCADE;

ALTER TABLE UserCompetitions
    ADD CONSTRAINT fk_user_competition_playlist_id FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id) ON DELETE SET NULL;

ALTER TABLE Votes
    ADD CONSTRAINT fk_voter_user_id FOREIGN KEY (voter_user_id) REFERENCES Users(user_id) ON DELETE CASCADE;

ALTER TABLE Votes
    ADD CONSTRAINT fk_vote_playlist_id FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id) ON DELETE CASCADE;

ALTER TABLE ActiveUsers
    ADD CONSTRAINT fk_active_user_id FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE;

-- Add Enum Type and Constraints for Competitions
ALTER TABLE Competitions
    ADD CONSTRAINT fk_winner_playlist_id FOREIGN KEY (winner_playlist_id) REFERENCES Playlists(playlist_id) ON DELETE SET NULL;

-- Add unique constraints
ALTER TABLE public.Users ADD CONSTRAINT unique_username UNIQUE (username);

ALTER TABLE public.Competitions ADD CONSTRAINT unique_competition UNIQUE (status, start_time);

ALTER TABLE public.Playlists ADD CONSTRAINT unique_user_competition UNIQUE (user_id, competition_id);

ALTER TABLE public.Votes ADD CONSTRAINT unique_vote UNIQUE (voter_user_id, playlist_id);
