# User Stories and Exceptions

## User Stories

1. **As a competitive person,** I want to be able to see my rank compared to other users, so that I can outcompete all users on the platform.  
   - **Exception:** Two people have the same wins/rank.  
     If two people have the same number of wins, the game will place them on the same rank and notify both users that they are tied, prompting them to a challenge.

2. **As an outspoken person,** I want to comment on playlists that I rank so that my opinion is heard.  
   - **Exception:** Reaching character/word limit.  
     If a user tries to submit a rank/comment that is too verbose, there will be an imposed character or word limit that doesn’t allow them to submit until under the limit with a warning.

3. **As an impatient person,** I want the games to last no longer than 10 minutes so that I can get the round results without waiting too long.  
   - **Exception:** Time limit reached before player submits playlist.  
     If the 10-minute maximum limit is reached before the player submits their playlist, the game will automatically submit whatever they have so far for them.

4. **As a creative person,** I want to be able to add photos to go along with my playlists.  
   - **Exception:** Invalid upload format: must be a .png.  
     If the image is not the correct format, the playlist will default to having no image associated.

5. **As someone who likes to play with friends from school or work,** I want to be able to host my own match locally.  
   - **Exception:** Maximum number of players exceeded.  
     After the maximum number of players is met, players will not be able to log into the match.

6. **As someone creative,** I don’t want to use the provided themes—I want to write and submit my own.  
   - **Exception:** Exceeding the maximum number of characters.  
     If the maximum number of characters is exceeded, users will be prompted to resubmit a shorter theme.

7. **As a person who values fairness,** I want to make sure that every competitor votes so that no one goes without any reviews.  
   - **Exception:** Competitor refuses to vote before the time limit is reached.  
     If someone does not vote on the playlist, theirs does not get uploaded to the system for ranking.

8. **As someone who wants to continue listening to the playlists,** I want to make sure that they are a reasonable length.  
   - **Exception:** Playlist is too long or too short.  
     If the playlist is shorter than 5 songs, it will not be considered. If the playlist is longer than 50 songs, the first 50 songs will be considered.

9. **As someone who values integrity,** I don’t want others to see my playlist until they have submitted their own.  
   - **Exception:** One person is done before the others.  
     The person who is done first will have a waiting message before the ranking appears.

10. **As someone who likes to try new playlists,** I want to be able to save a record of my playlist and other users' playlists after rounds so that I can listen to them after.  
    - **Exception:** Download failed.  
      If the playlist download is unsuccessful due to either incompatibility, lack of local storage, or some other issue, it notifies the user that the download did not succeed.

11. **As someone who likes variety in my playlists,** I want to make sure there are no duplicate songs on the playlists, so that I don’t listen to the same song twice throughout the same listen.  
    - **Exception:** Song is already in the playlist.  
      If a player tries to add a song to the playlist that they’ve already added, the game will not allow them to add it again and send them an error message.

12. **As someone who hates to lose,** I want to be able to wager rematches so that I have another chance to win.  
    - **Exception:** Other players do not want to rematch.  
      The person suggesting the rematch will get a notification that one or more players denied the request. If 0 players want to rematch, there is no rematch.
