# Example Workflows

# User Participating in Competition Example Flow

Christian is invited by a friend to challenge him in a Playlistify competition. They always argue over who gets the aux cord in the car and decide to settle it with a game. Christian and his friend have already made accounts for Playlistify and want to have a definitive indication of who should have authority over the music during their road trips, so they plan to log in and compete against each other.

### Step 1: Christian logs onto his Playlistify account
Christian goes onto the site and enters his credentials to log onto his personal account.

**Christian enters his credentials with POST /user/login:**
```json
{
    "username": "physics_is_fun123"
}
```
**Response:**
```json
{
    "message": "Invalid credentials!"
}
```
He realizes he used a login from a different site and re-enters his information correctly:
```json
{
    "username": "HarmonicWave1"
}
```
**Response:**
```json
{
    "message": "Login successful"
}
```

### Step 2: Christian looks for a competition to join
Christian and his friend don’t feel like creating their own competition to play in. Instead, Christian feels lazy and decides to just look up all competitions to see which they should join.

**He calls GET /competitions/ to see what’s available:**
```json
[
{
    "competition_id": "RockUrSocks11", 
    "status": "Active",
    "participants": 5
},
{
    "competition_id": "OldiesAndGoodies9", 
    "status": "Inactive",
    "participants": 15
}
]
```
Christian receives a list of all competitions. He sees that there’s an active one with only 5 participants and decides that’s the one they will join.

### Step 3: Christian joins the competition
Christian gives the competition id to his friend so that they’ll be in the same one, and they both join.

**He calls POST /competitions/RockUrSocks11/join:**
```json
{
    "username": "HarmonicWave1"
}
```
**Response:**
```json
{
    "message": "Competition Joined", 
    "enrollment_status": true, 
    "competition_details": {
        "competition_id": "RockUrSocks11", 
        "username": "HarmonicWave1", 
        "start_time": "2024-10-13T20:32:23.298252-07:00"
    }
}
```

### Step 4: Christian starts submitting songs into his playlist for the competition
Christian’s friend has let him know that he has also joined the competition. Christian immediately starts submitting songs into his playlist for the competition.

**He submits the first song:**
```json
{
    "song_id": "hotelcalifornia1",
    "song_title": "Hotel California",
    "artist": "Eagles"
}
```
**Response:**
```json
{
    "message": "Song successfully added to playlist",
    "playlist_status": true,
    "song_details": {
        "song_id": "hotelcalifornia1",
        "song_title": "Hotel California",
        "artist": "Eagles"
    }
}
```

### Step 5: Christian finishes his playlist and submits it for voting
Christian submits the playlist using POST /competitions/{competition_id}/submit:
```json
{
    "playlist_id": "1001",
    "competition_id": "RockUrSocks11"
}
```
**Response:**
```json
{
    "message": "Playlist Submit: Successful"
}
```

### Step 6: Christian votes on the winning playlist
Christian enters the voting phase using POST /competitions/{competition_id}/vote and assigns a rating to each playlist.

**Example vote submission:**
```json
{
    "competition_id": "RockUrSocks11",
    "playlist_id": "1002",
    "vote_score": "1"
}
```

**Response:**
```json
{
    "message": "Your votes have been cast! You will be able to see your playlist’s average once the round has concluded"
}
```

### Step 7: Christian logs off
Christian logs off after casting his vote.

**POST /user/logoff:**
```json
{
    "username": "HarmonicWave1"
}
```
**Response:**
```json
{
    "message": "You have successfully signed out"
}
```

# Testing Results

## 1. Christian Logs In
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/user/login?username=HarmonicWave' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

### Response:
```json
{
  "message": "Login Successful"
}
```

## 2. Christian Looks for a Competition to Join
### Curl Statement:
```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/competition/' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE'
```

### Response:
```json
[
  {
    "competition_id": 1,
    "status": "active",
    "participants": 4
  },
  {
    "competition_id": 2,
    "status": "completed",
    "participants": 3
  }
]
```

## 3. Christian Joins the Competition
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/competition/join?username=HarmonicWave&compid=1' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

### Response:
```json
{
  "message": "OK"
}
```

## 4. Christian adds songs to his playlist
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/competition/1/playlists/songs' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6,
  "song_id": 1,
  "song_title": "Juna",
  "artist": "Clairo"
}'
```

### Response:
```json
{
  "message": "Song successfully added to playlist",
  "playlist_status": true,
  "song_details": {
    "song_id": 1,
    "song_title": "Juna",
    "artist": "Clairo"
  }
}
```

## 5. Christian submits his finished playlist for voting
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/competition/1/submit' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 6,
  "playlist_id": 5,
  "competition_id": 1
}'
```

### Response:
```json
{
  "message": "Playlist submission successful",
  "submission_status": true
}
```

## 6. Christian votes on the playlists
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/competition/1/vote?playlist_id=5&voter_user_id=6&vote=5' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

### Response:
```json
"OK"
```

## 7. Christian Logs off
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/user/logoff' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"username": "HarmonicWave1"}'
```

### Response:
```json
{
  "message": "Logoff successful"
}
```

---

# User Checking Stats and Playlist Flow

Amir, a frequent user of Playlistify, wants to quickly log in and check his competition stats and past playlists. He doesn’t plan on participating in any new competitions today but simply wants to review his previous performances.

### Step 1: Amir Logs In
Amir opens the Playlistify app and logs in with his credentials.

**POST /user/login:**
```json
{
    "username": "AmirOnPlatlistify",
    "password": "MySecurePassword"
}
```
**Response:**
```json
{
   "message": "Login successful",
   "token": "abc123token"
}
```

### Step 2: Amir Retrieves His Competition Stats
Once logged in, Amir checks all the competitions he has participated in.

**GET /user/{user_id}/competitions:**
```json
{
  "user_id": "amir001"
}
```
**Response:**
```json
[
   {
       "competition_id": "RockPlaylist01",
       "status": "completed"
   },
   {
      "competition_id": "Jazzvibes2024",
      "status": "active"
   }
]
```

### Step 3: Amir Checks All His Playlists
Amir wants to review all the playlists he has created across different competitions.

**GET /user/{user_id}/all/playlists:**
```json
{
   "user_id": "amir001"
}
```
**Response:**
```json
[
   {
      "playlist_id": "playlist123",
      "competition_id": "RockPlaylist01",
      "songs": ["Bohemian Rhapsody", "Stairway to Heaven", "Hotel California"]
   },
   {
      "playlist_id": "playlist456",
      "competition_id": "Jazzvibes2024",
      "songs": ["Take Five", "So What", "Blue in Green"]
   }
]
```

### Step 4: Amir Logs Off
After reviewing his stats and playlists, Amir logs off.

**POST /user/logoff:**
```json
{
   "Username": "AmirOnPlaylistify"
}
```
**Response:**
```json
{
   "message": "Logoff successful"
}
```

# Testing Results

## 1. Amir Logs in
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/user/login?username=AmirOnPlaylistify' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

### Response:
```json
{
  "message": "Login Successful"
}
```

## 2. Amir retrieves his competition status
### Curl Statement:
```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/user/1/competitions' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE'
```

### Response:
```json
{
  "user_competitions": [
    {
      "competition_id": 1
    }
  ]
}
```

## 3. Amir checks all his playlists
### Curl Statement:
```bash
curl -X 'GET' \
  'http://127.0.0.1:3000/user/1/all/playlists' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE'
```

### Response:
```json
{
  "user_playlists": [
    {
      "user_id": 1,
      "competition_id": 1,
      "playlist_id": 1,
      "songs": [
        {
          "song_id": 1,
          "song_title": "Juna"
        },
        {
          "song_id": 2,
          "song_title": "Let The Light In"
        },
        {
          "song_id": 3,
          "song_title": "I Will"
        }
      ]
    }
  ]
}
```

## 4. Amir Logs off
### Curl Statement:
```bash
curl -X 'POST' \
  'http://127.0.0.1:3000/user/logout?username=AmirOnPlaylistify' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

### Response:
```json
{
  "message": "Logout successful"
}
