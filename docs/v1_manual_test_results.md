# Example Workflow

## User Account Creation Example Flow

Yasemin’s friend Emily, a Playlistify user and self-proclaimed music connoisseur, wants to prove she has better taste in music than her and invites Yasemin to a Playlistify competition. Yasemin accepts the challenge and starts by signing up for a Playlistify account to create her new user account.

### Step 1: Yasemin Creates an Account
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

# Testing Results

## Creating an Account
**Curl Statement:**

```sh
curl -X 'POST' \
  'http://127.0.0.1:3000/user/signup' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "YazOnPlaylistify",
  "name": "Yasemin Akkaya"
}'
```

**Response:**

```json
{
  "message": "Account created successfully",
  "user_id": 7
}
```

## Logging into the Account
**Curl Statement:**

```sh
curl -X 'POST' \
  'http://127.0.0.1:3000/user/login?username=YazOnPlaylistify' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

**Response:**

```json
{
  "message": "Login Successful"
}
```

## Logging Off
**Curl Statement:**

```sh
curl -X 'POST' \
  'http://127.0.0.1:3000/user/logout?username=YazOnPlaylistify' \
  -H 'accept: application/json' \
  -H 'access_token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmpoZnFsemR6YmViaW5ieHBuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzAwNzg4NjAsImV4cCI6MjA0NTY1NDg2MH0.p32MA6K5Z64pIeeQEr9TLSWVklq-E-z8zU6x84rNChE' \
  -d ''
```

**Response:**

```json
{
  "message": "Logout successful"
}
```

