
# User Account Creation Example Flow

Yasemin’s friend Emily, a Playlistify user and self-proclaimed music connoisseur, wants to prove she has a better taste in music than her and invites Yasemin to a Playlistify competition. Yasemin accepts the challenge and starts by signing up for a Playlistify account to create her new user account.

### Step 1: Yasemin creates an account
Yasemin navigates to the signup page to create her account. She provides her details and sends a request to create her new profile:

**Yasemin calls POST /user/signup with the following details:**
```json
{
    "username": "YazOnPlaylistify",
    "name": "Yasemin Akkaya"
}
```

**Response:**
```json
{
    "message": "Account created successfully",
    "userid": "user12345"
}
```

### Step 2: Yasemin Logs In
After her account is created, Yasemin needs to log in to access the competition features and set up her profile.

**Yasemin calls POST /user/login with her credentials:**
```json
{
    "username": "YazOnPlaylistify"
}
```

**Response:**
```json
{
    "message": "Login successful"
}
```

### Step 3: Yasemin Logs Off
After browsing through the Playlistify platform, Yasemin decides to log off for the day and rest before the competition.

**Yasemin calls POST /user/logoff with the token received during login:**

**Response:**
```json
{
    "message": "Logoff successful"
}
```

---

# User Participating in Competition Example Flow

Christian is invited by a friend to challenge him in a Playlistify competition. They always argue over who gets the aux cord in the car and decide to settle it with a game. Christian and his friend have already made accounts for Playlistify and want to have a definitive indication of who should have authority over the music during their road trips, so they plan to log in and compete against each other.

### Step 1: Christian logs onto his Playlistify account
Christian goes onto the site and enters his credentials to log onto his personal account.

**Christian enters his credentials with POST /user/login:**
```json
{
	"username":	"physics_is_fun123"
}
```
**Response:**
```json
{
	"message":	"Invalid credentials!"
}
```
He realizes he used a login from a different site and re-enters his information correctly:
```json
{
	"username":	"HarmonicWave1"
}
```
**Response:**
```json
{
	"message":	"Login successful"
}
```

### Step 2: Christian looks for a competition to join
Christian and his friend don’t feel like creating their own competition to play in. Instead, Christian feels lazy and decides to just look up all competitions to see which they should join.

**He calls GET /competitions/ to see what’s available:**
```json
[
{
    "competition_id": 	"RockUrSocks11", 
    "status": 		"Active",
    "participants": 	5
},
{
    "competition_id": 	"OldiesAndGoodies9", 
    "status": 		"Inactive",
    "participants": 	15
}
]
```
Christian receives a list of all competitions. He sees that there’s an active one with only 5 participants and decides that’s the one they will join.

### Step 3: Christian joins the competition
Christian gives the competition id to his friend so that they’ll be in the same one, and they both join.

**He calls POST /competitions/RockUrSocks11/join:**
```json
{
	"username":	"HarmonicWave1"
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
	"username":	"HarmonicWave1"
}
```
**Response:**
```json
{
	"message": "You have successfully signed out"
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
       "competition_id": "11",
   },
   {
      "competition_id": "4",
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
