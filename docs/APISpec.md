
# Competition API

## 1.1 Get Competitions - `/competitions/` (GET)
Fetches all competitions (both current and past). Each competition has specific properties, and all competitions are returned in an array.

**Response:**
```json
[
  {
    "competition_id": "integer", 
    "status": "string",
    "participants": "integer"
  },
  {
    "..."
  }
]
```

## 1.2 Join Competition - `/competitions/{competition_id}/participants` (POST)
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
}
```

## 1.3 Add Song to Playlist - `/competitions/{competition_id}/playlists/{playlist_id}/songs` (POST)
Allows a user to add a song to their playlist during an active competition. The user's identity is extracted from the token in the Authorization header.

**Request:**
```json
{
  "song_id": "integer"
}
```

**Response:**
```json
{
  "message": "string", /* Success or failure message */
  "playlist_status": "boolean", /* true if the song was successfully added, false otherwise */
  "song_details": {
    "song_id": "integer",
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
  "user_id": "integer",
  "playlist_id": "integer",
  "competition_id": "integer"
}
```

**Response:**
```json
{
  "message": "string",  /* Success or failure message */
}
```

## 1.5 Vote on Playlist - `/competitions/{competition_id}/votes` (POST)
Allows users to vote for the best playlist in a competition. After submissions, playlists enter a voting phase where users can rank others’ playlists.

**Request:**
```json
{
  "playlist_id": "integer",
  "voter_user_id": "integer",
  "vote": "integer"
}
```

**Response:**
```json
{
  "message": "string",  /* Success or failure message */
}
```

## 1.6 Get Competition Results - `/competitions/{competition_id}/status` (GET)
The final results of a competition, revealing the winner and their playlist.

**Response:**
```json
{
  "winner_playlist_id": "integer",  /* ID of the winning playlist */
  "winner_username": "string",  /* Username of the competition winner */
  "message": "string"  /* Message detailing the competition outcome */
}
```


# User API

## 2.1 Get User Competitions - `/users/{user_id}/competitions` (GET)
Get all competitions a user has participated in or is currently participating in.


**Response:**
```json
[
  {
    "user_competitions": "List[competition_id]"
  }
]
```

## 2.2 Get All User’s Playlists - `/users/{user_id}/all/playlists` (GET)
Get all of a user’s submitted playlists from past competitions.

**Request:**
```json
{
  "user_id": "integer"
}
```

**Response:**
```json
[
  {
    "user_id": "integer",
    "competition_id": "integer",
    "playlist_id": "integer",
    "songs": "List[string]"
  }
]
```

## 2.3 Create User Account - `/users/` (POST)
Create a new account for a user.

**Request:**
```json
{
  "username": "string"
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

## 2.4 User Logs in to Account - `/users/sessions` (POST)
Upon logging in, user is added to an active users table.

**Request:**
```json
{
  "username": "string"
}
```

**Response:**
```json
{
  "message": "string",  /* will indicate success/failure */
}
```


## 2.6 Get User Voting Pattern Trends - `/users/{user_id}/voting-pattern-trends` (GET)
Gets insights into how a user's voting behavior has evolved across different competitions.

**Response:**
```json
{
  "user_id": "integer",                    /* ID of the user */
  "total_votes_cast": "integer",           /* total number of votes cast by the user */
  "average_score_given": "float",          /* average score given by the user */
  "voting_trend_analysis": [               /* array of voting trend details */
    {
      "vote_id": "integer",                /* ID of the vote */
      "vote_score": "integer",             /* score given in this vote */
      "previous_vote_score": "integer or null", /* previous vote score, null if not available */
      "next_vote_score": "integer or null"      /* next vote score, null if not available */
    },
    {
      "...": "..."
    }
  ],
  "message": "string"                      /* success or failure message */
}

```
