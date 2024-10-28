-- Create Users Table
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100),
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Playlists Table (before Competitions and UserCompetitions to resolve foreign key dependencies)
CREATE TABLE Playlists (
    playlist_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_votes INTEGER DEFAULT 0,
    average_score FLOAT DEFAULT 0.0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
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
    winner_playlist_id INTEGER,
    FOREIGN KEY (winner_playlist_id) REFERENCES Playlists(playlist_id)
);

-- Create UserCompetitions Table
CREATE TABLE UserCompetitions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    enrollment_status BOOLEAN DEFAULT TRUE,
    submission_status BOOLEAN DEFAULT FALSE,
    playlist_id INTEGER,
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (competition_id) REFERENCES Competitions(competition_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
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
    song_order INTEGER NOT NULL,
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

-- Create Votes Table
CREATE TABLE Votes (
    vote_id SERIAL PRIMARY KEY,
    voter_user_id INTEGER NOT NULL,
    playlist_id INTEGER NOT NULL,
    vote_score INTEGER NOT NULL CHECK (vote_score >= 1 AND vote_score <= 5),
    vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (voter_user_id) REFERENCES Users(user_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id)
);

-- Create ActiveUsers Table
CREATE TABLE ActiveUsers (
    user_id INTEGER PRIMARY KEY,
    last_active_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Insert sample data into Users table
INSERT INTO Users (username, name) VALUES
('Yaz', 'Yasemin Akkaya'),
('Jazzy', 'Jazzy De Los Santos'),
('Ivana', 'Ivana Thomas'),
('Amir', 'Amir Minabian');

-- Insert sample data into Competitions table
INSERT INTO Competitions (status, participants_count, start_time) VALUES
('active', 2, '2024-10-01 09:00:00'),
('completed', 3, '2024-09-15 09:00:00');

-- Insert sample data into UserCompetitions table
INSERT INTO UserCompetitions (user_id, competition_id) VALUES
(1, 1),
(2, 1),
(3, 2);

-- Insert sample data into Playlists table
INSERT INTO Playlists (user_id, competition_id) VALUES
(1, 1),
(2, 1),
(3, 2);

-- Insert sample data into Songs table
INSERT INTO Songs (song_title, artist) VALUES
('Juna', 'Clairo'),
('Let The Light In', 'Lana Del Ray'),
('I Will', 'The Beatles');

-- Insert sample data into PlaylistSongs table
INSERT INTO PlaylistSongs (playlist_id, song_id, song_order) VALUES
(1, 1, 1),
(1, 2, 2),
(2, 2, 1),
(2, 3, 2),
(3, 1, 1),
(3, 3, 2);

-- Insert sample data into Votes table
INSERT INTO Votes (voter_user_id, playlist_id, vote_score) VALUES
(2, 1, 5),
(1, 2, 4),
(1, 3, 5);

-- Insert sample data into ActiveUsers table
INSERT INTO ActiveUsers (user_id) VALUES
(1),
(2);