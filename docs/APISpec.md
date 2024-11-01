
# Competition API

## 1.1 Get Competitions - `/competitions/` (GET)
Fetches all competitions (both current and past). Each competition has specific properties, and all competitions are returned in an array.

**Response:**
```json
[
  {
    "competition_id": "string", 
    "status": "string",
    "participants": "integer"
  },
  {
    "..."
  }
]
```

## 1.2 Join Competition - `/competitions/{competition_id}/join` (POST)
Enrolls a user into a live competition. The `competition_id` must reference an active competition. Users can submit details like their username and score when joining the competition.

**Request:**
```json
{
  "username": "string"
}
```

**Response:**
```json
{
  "message": "string", /* Success message or failure reason */
  "enrollment_status": "boolean", /* true if enrollment is successful, false otherwise */
  "competition_details": {
    "competition_id": "string", /* ID of the competition */
    "username": "string", /* Username of the participant */
    "start_time": "string" /* ISO 8601 format of the competition's start time */
  }
}
```

## 1.3 Add Song to Playlist - `/competitions/{competition_id}/playlists/songs` (POST)
Allows a user to add a song to their playlist during an active competition. The user's identity is extracted from the token in the Authorization header.

**Request:**
```json
{
  "song_id": "string",
  "song_title": "string",
  "artist": "string"
}
```

**Response:**
```json
{
  "message": "string", /* Success or failure message */
  "playlist_status": "boolean", /* true if the song was successfully added, false otherwise */
  "song_details": {
    "song_id": "string",
    "song_title": "string",
    "artist": "string"
  }
}
```

## 1.4 Submit Playlists - `/competitions/{competition_id}/submit` (POST)
Allows a user to submit their playlist after adding all the desired songs during a competition.

**Request:**
```json
{
  "playlist_id": "string",
  "competition_id": "string"
}
```

**Response:**
```json
{
  "message": "string",  /* Success or failure message */
  "submission_status": "boolean"  /* true if the playlist submission was successful */
}
```

## 1.5 Vote on Playlist - `/competitions/{competition_id}/vote` (POST)
Allows users to vote for the best playlist in a competition. After submissions, playlists enter a voting phase where users can rank others’ playlists.

**Request:**
```json
{
  "playlist_id": "string",
  "vote_score": "integer"
}
```

**Response:**
```json
{
  "message": "string",  /* Success or failure message */
  "vote_status": "boolean"  /* true if the vote was successfully submitted */
}
```

## 1.6 Get Competition Results - `/competitions/{competition_id}/status` (GET)
The final results of a competition, revealing the winner and their playlist.

**Response:**
```json
{
  "winner_playlist_id": "string",  /* ID of the winning playlist */
  "winner_username": "string",  /* Username of the competition winner */
  "message": "string"  /* Message detailing the competition outcome */
}
```

## 1.7 Get User Playlist - `/competitions/{competition_id}/playlists/user/{user_id}` (GET)
Get a user’s playlist from a specific competition.

**Request:**
```json
{
  "user_id": "number",
  "competition_id": "number"
}
```

**Response:**
```json
[
  {
    "playlist_id": "number",
    "songs": "List[string]"
  }
]
```

# User API

## 2.1 Get User Competitions - `/user/{user_id}/competitions` (GET)
Get all competitions a user has participated in or is currently participating in.

**Request:**
```json
{
  "user_id": "number"
}
```

**Response:**
```json
[
  {
    "user_competitions": "List[competition_id]"
  }
]
```

## 2.2 Get All User’s Playlists - `/user/{user_id}/all/playlists` (GET)
Get all of a user’s submitted playlists from past competitions.

**Request:**
```json
{
  "user_id": "number"
}
```

**Response:**
```json
[
  {
    "user_id": "number",
    "competition_id": "number",
    "playlist_id": "number",
    "songs": "List[string]"
  }
]
```

## 2.3 Create User Account - `/user/signup` (POST)
Create a new account for a user.

**Request:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response (Success):**
```json
{
  "message": "string",  /* will indicate success */
  "user_id": "integer"
}
```

**Response (Failure):**
```json
{
  "message": "string"  /* failure or error message */
}
```

## 2.4 User Logs in to Account - `/user/login` (POST)
Upon logging in, user is added to an active users table.

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "string",  /* will indicate success/failure */
  "token": "string"  /* auth token */
}
```

## 2.5 Get all Users - `/users/` (GET)
Get all playlistify users.

**Response:**
```json
[
  {
    "user_id": "string",  /* for admin */
    "username": "string",  /* for users */
    "email": "string",
    "name": "string",
    "competitions": [
      {
        "competition_id": "string",
        "status": "boolean"  /* TRUE for active, FALSE for inactive */
      },
      ...
    ]
  },
  ...
]
```

**Response (No Users Found):**
```json
[]
```
