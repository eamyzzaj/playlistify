# Performance Write-Up #

## Fake Data Modeling 
Through a series of [Python scripts](../docker_testing/) for each table and the use of Docker, the distribution of the ~1 million rows of fake data was distributed as below:
* Users: 500,000 rows
* ActiveUsers: 50,000 rows 
* Competitions: 20,000 rows
* UserCompetitions: 50,000 rows (assuming each user participates in a competition)
* Playlists: 50,000 rows
* Songs: 150,000 rows
* PlaylistSongs: 250,000 rows
* Votes: 430,000 rows

This distribution, totaling about 1.5 million rows, prioritizes the `users` as the majority of the data, which accounts for both active and inactive users. The next largest batch of rows lies with the user `votes` table. For all past and currently active competitions, the votes from almost all the users' would occupy a fair amount of space. `Songs` and `PlaylistSongs`, the latter being a table linking playlists and songs, would most likely be the next batch of large data. However, it also has the possibility of being the largest batch, depending on how many songs would be available for the users. However, for performance testing, users and their interactions within **Playlistify** were prioritized. The rest of the rows were distributed randomly amongst the rest of the tables to support endpoint testing.

## Performance results of hitting endpoints ###
The three slowest endpoints were `vote on playlist`, `add song to playlist`, and `get competitions` with times of 559.81 ms, 329.28 ms, and 111.93 ms, respectively. 
| Endpoint  | Purpose | Performance |
| -------------|:-------------:|:-------------:|
| `/users/`     |create user    | 34.92 ms    |
| `/users/sessions`| user login    | 88.93 ms     |
|`/users/logout`|user logout|31.45 ms|
|`/competitions` |get competitions|27.42 ms|
|`/competitions/join` |join competitions|82.83 ms|
|`/competitions/{competition_id}/playlists/songs`|add song to playlist|329.28 ms|
|`/users/{user_id}/all/playlists`|get all user’s playlists|111.93 ms|
|`/competitions/{competition_id}/vote`|vote on playlist|559.81 ms|
|`/competitions/{competition_id}/submit`|submit playlist|34.59 ms|
|`/competitions/{competition_id}/status`|get competition status|33.02 ms|
|`/users/{user_id}/competitions`|get all user's competitions|26.82 ms|
|`/users/users/{user_id}/voting-pattern-trends`|get user's voting pattern trends|46.80 ms|


## Performance tuning ###
#### 1. Vote on playlists ####

Checking if playlist exists:
```
 Index Scan using playlists_pkey on playlists  (cost=0.29..8.31 rows=1 width=4)
   Index Cond: (playlist_id = 50001)
```

Checking if user already voted on playlist:
```
 Index Only Scan using unique_vote on votes  (cost=0.42..4.44 rows=1 width=4)
   Index Cond: ((voter_user_id = 1738530) AND (playlist_id = 50001))
```
Checking if all other users submitted their playlist:
```
 Aggregate  (cost=1047.35..1047.36 rows=1 width=8)
   ->  Index Scan using unique_user_competition_new on usercompetitions  (cost=0.29..1047.34 rows=4 width=0)
         Index Cond: (competition_id = 40026)
         Filter: ((NOT submission_status) AND (user_id <> 1738530))
```
Inserting vote:
```
 Insert on votes  (cost=0.00..0.02 rows=0 width=0)
   ->  Result  (cost=0.00..0.02 rows=1 width=24)
```
Incrementing total votes for playlist:
```
 Update on playlists  (cost=0.29..8.31 rows=0 width=0)
   ->  Index Scan using playlists_pkey on playlists  (cost=0.29..8.31 rows=1 width=10)
         Index Cond: (playlist_id = 50001)
```
Calculating average score:
```
Update on playlists  (cost=952.62..9074.67 rows=0 width=0)
   InitPlan 2
     ->  Index Scan using playlists_pkey on playlists playlists_1  (cost=0.29..8.31 rows=1 width=4)
           Index Cond: (playlist_id = 50001)
   InitPlan 3
     ->  Aggregate  (cost=944.01..944.02 rows=1 width=8)
           ->  Seq Scan on usercompetitions  (cost=0.00..944.00 rows=4 width=0)
                 Filter: (enrollment_status AND (competition_id = 40026))
   ->  Result  (cost=0.29..8122.34 rows=1 width=14)
         One-Time Filter: ((InitPlan 2).col1 = (InitPlan 3).col1)
         ->  Index Scan using playlists_pkey on playlists  (cost=0.29..8.31 rows=1 width=10)
               Index Cond: (playlist_id = 50001)
         SubPlan 1
           ->  Aggregate  (cost=8114.02..8114.03 rows=1 width=32)
                 ->  Seq Scan on votes  (cost=0.00..8114.00 rows=9 width=4)
                       Filter: (playlist_id = playlists.playlist_id)
```
Check if competition can be completed:
```
Update on competitions  (cost=12180.17..12188.20 rows=0 width=0)
   InitPlan 1
     ->  Subquery Scan on winning_playlist  (cost=1027.35..1027.36 rows=1 width=4)
           ->  Limit  (cost=1027.35..1027.35 rows=1 width=12)
                 ->  Sort  (cost=1027.35..1027.36 rows=4 width=12)
                       Sort Key: playlists.average_score DESC
                       ->  Index Scan using unique_user_competition on playlists  (cost=0.29..1027.33 rows=4 width=12)
                             Index Cond: (competition_id = 40026)
   InitPlan 2
     ->  Aggregate  (cost=10141.16..10141.17 rows=1 width=8)
           ->  Hash Join  (cost=10140.13..10141.16 rows=1 width=0)
                 Hash Cond: ((count(*)) = (count(*)))
                 ->  GroupAggregate  (cost=9196.09..9196.69 rows=34 width=12)
                       Group Key: votes.playlist_id
                       ->  Sort  (cost=9196.09..9196.18 rows=34 width=4)
                             Sort Key: votes.playlist_id
                             ->  Hash Join  (cost=1027.38..9195.23 rows=34 width=4)
                                   Hash Cond: (votes.playlist_id = playlists_1.playlist_id)
                                   ->  Seq Scan on votes  (cost=0.00..7039.00 rows=430000 width=4)
                                   ->  Hash  (cost=1027.33..1027.33 rows=4 width=4)
                                         ->  Index Scan using unique_user_competition on playlists playlists_
1  (cost=0.29..1027.33 rows=4 width=4)
                                               Index Cond: (competition_id = 40026)
                 ->  Hash  (cost=944.02..944.02 rows=1 width=8)
                       ->  Aggregate  (cost=944.01..944.02 rows=1 width=8)
                             ->  Seq Scan on usercompetitions  (cost=0.00..944.00 rows=4 width=0)
                                   Filter: (enrollment_status AND (competition_id = 40026))
   InitPlan 3
     ->  Aggregate  (cost=1011.34..1011.35 rows=1 width=8)
           ->  Index Only Scan using unique_user_competition on playlists playlists_2  (cost=0.29..1011.33 ro
ws=4 width=0)
                 Index Cond: (competition_id = 40026)
   ->  Result  (cost=0.29..8.31 rows=1 width=22)
         One-Time Filter: ((InitPlan 2).col1 = (InitPlan 3).col1)
         ->  Index Scan using competitions_pkey on competitions  (cost=0.29..8.30 rows=1 width=6)
               Index Cond: (competition_id = 40026)
```
Update average score for all playlists in completed competition:
```
Update on playlists  (cost=0.29..33483.48 rows=0 width=0)
   ->  Index Scan using unique_user_competition on playlists  (cost=0.29..33483.48 rows=4 width=14)
         Index Cond: (competition_id = 40026)
         SubPlan 1
           ->  Aggregate  (cost=8114.02..8114.03 rows=1 width=32)
                 ->  Seq Scan on votes  (cost=0.00..8114.00 rows=9 width=4)
                       Filter: (playlist_id = playlists.playlist_id)
```
##### Description of explains: #####
The queries above, all used to execute the endpoint of voting on playlists, each have their own cost to run. The most efficient ones take use of primary keys (like in checking if a playlist exists) and indexes (like in checking if a user already voted on a playlists). The most inefficient ones do not. These queries are checking if all others submitted a playlist, calculating/updating average score, and checking if competition can be completed.

For **checking if all others submitted a playlist**, the index would be created by:
```
CREATE INDEX idx_usercompetitions_competition_status_user 
ON usercompetitions (competition_id, submission_status, user_id);
```
After creating this index and re-running explain, the results are now: 
```
 Aggregate  (cost=8.39..8.40 rows=1 width=8)
   ->  Index Only Scan using idx_usercompetitions_competition_status_user on usercompetitions  (cost=0.29..8.38 rows=4 width=0)
         Index Cond: ((competition_id = 40026) AND (submission_status = false))
         Filter: (user_id <> 1738530)
```

For **calculating average score** and **checking if a competition can be completed**, the index would be created by:
```
CREATE INDEX idx_votes_playlist_score
ON votes (playlist_id, vote_score);
```

After creating this index and re-running ecplain, the results are now:
```
 Update on playlists  (cost=27.64..44.28 rows=0 width=0)
   InitPlan 2
     ->  Index Scan using playlists_pkey on playlists playlists_1  (cost=0.29..8.31 rows=1 width=4)
           Index Cond: (playlist_id = 50001)
   InitPlan 3
     ->  Aggregate  (cost=19.04..19.05 rows=1 width=8)
           ->  Bitmap Heap Scan on usercompetitions  (cost=4.32..19.03 rows=4 width=0)
                 Recheck Cond: (competition_id = 40026)
                 Filter: enrollment_status
                 ->  Bitmap Index Scan on idx_usercompetitions_competition_status_user  (cost=0.00..4.32 rows
=4 width=0)
                       Index Cond: (competition_id = 40026)
   ->  Result  (cost=0.29..16.92 rows=1 width=14)
         One-Time Filter: ((InitPlan 2).col1 = (InitPlan 3).col1)
         ->  Index Scan using playlists_pkey on playlists  (cost=0.29..8.31 rows=1 width=10)
               Index Cond: (playlist_id = 50001)
         SubPlan 1
           ->  Aggregate  (cost=8.60..8.61 rows=1 width=32)
                 ->  Index Only Scan using idx_votes_playlist_score on votes  (cost=0.42..8.58 rows=9 width=4
)
                       Index Cond: (playlist_id = playlists.playlist_id)
```
and 
```
 Aggregate  (cost=1011.34..1011.35 rows=1 width=8)
   ->  Index Only Scan using unique_user_competition on playlists  (cost=0.29..1011.33 rows=4 width=0)
         Index Cond: (competition_id = 40026)
```

For all indexes added above, the performance improvements were substantial and brought costs down monumentally. Through index scans, less rows needed to be viewed and filtering by ids is more efficient.

#### 2. Add song to playlist ####
Checking if competition exists and is active, user enrollment, and user's playlist
```
 Nested Loop Left Join  (cost=0.87..24.95 rows=1 width=9)
   ->  Nested Loop Left Join  (cost=0.58..16.63 rows=1 width=9)
         ->  Index Scan using competitions_pkey on competitions c  (cost=0.29..8.30 rows=1 width=8)
               Index Cond: (competition_id = 40026)
         ->  Index Scan using unique_user_competition_new on usercompetitions uc  (cost=0.29..8.31 rows=1 width=5)
               Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
   ->  Index Scan using unique_user_competition on playlists p  (cost=0.29..8.31 rows=1 width=8)
         Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
```
Create new playlist if user doesn't have one:
```
Insert on playlists  (cost=0.00..0.02 rows=1 width=32)
   ->  Result  (cost=0.00..0.02 rows=1 width=32)
```
Update usercompetitions with new playlist id (if necessary):
```
 Update on usercompetitions  (cost=0.29..8.31 rows=0 width=0)
   ->  Index Scan using unique_user_competition_new on usercompetitions  (cost=0.29..8.31 rows=1 width=10)
         Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
```

Check if song is already in user's playlist:
```
 Index Scan using unique_song_playlist on playlistsongs  (cost=0.42..8.44 rows=1 width=4)
   Index Cond: ((song_id = 2) AND (playlist_id = 123))
```

Add song to playlist:
```
 Insert on playlistsongs  (cost=0.00..0.01 rows=0 width=0)
   ->  Result  (cost=0.00..0.01 rows=1 width=16)
```

##### Description of explains: #####
The queries above for adding a song to a playlist have costs that start adding up and affecting performance as data scales up to production level. The plan to optimize is by creating the following indexes:

```
CREATE INDEX idx_usercompetitions_user_competition 
ON usercompetitions (user_id, competition_id);
```
```
CREATE INDEX idx_playlists_user_competition 
ON playlists (user_id, competition_id);
```
```
CREATE INDEX idx_playlistsongs_song_playlist 
ON playlistsongs (song_id, playlist_id);
```

After adding those indexes, the new explains resulted in:
```
 Nested Loop Left Join  (cost=0.87..24.95 rows=1 width=9)
   ->  Nested Loop Left Join  (cost=0.58..16.63 rows=1 width=9)
         ->  Index Scan using competitions_pkey on competitions c  (cost=0.29..8.30 rows=1 width=8)
               Index Cond: (competition_id = 40026)
         ->  Index Scan using idx_usercompetitions_user_competition on usercompetitions uc  (cost=0.29..8.31 rows=1 width=5)
               Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
   ->  Index Scan using idx_playlists_user_competition on playlists p  (cost=0.29..8.31 rows=1 width=8)
         Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
```
and 
```
 Index Scan using idx_playlistsongs_song_playlist on playlistsongs  (cost=0.42..8.44 rows=1 width=4)
   Index Cond: ((song_id = 2) AND (playlist_id = 123)
```
Interestingly, these indexes did not improve the costs. Although it changed which indexes it used to do the index scans (using the new indexes rather than the previous unique ones), the overall cost and efficiency remained the same. Further analysis of this endpoint shows that while an initial call is relatively "slow", subsequent calls increase in speed. Additionally, this could mean that the performance issues of the endpoint is not from the SQL queries themselves but from some other factor.

An `EXPLAIN ANALYZE` also further shows that performance of the "costliest" query is still acceptable.
```
 Nested Loop Left Join  (cost=0.87..24.95 rows=1 width=9) (actual time=3.338..3.342 rows=1 loops=1)
   ->  Nested Loop Left Join  (cost=0.58..16.63 rows=1 width=9) (actual time=2.721..2.723 rows=1 loops=1)
         ->  Index Scan using competitions_pkey on competitions c  (cost=0.29..8.30 rows=1 width=8) (actual time=1.961..1.963 rows=1 loops=1)
               Index Cond: (competition_id = 40026)
         ->  Index Scan using idx_usercompetitions_user_competition_playlist on usercompetitions uc  (cost=0.29..8.31 rows=1 width=5) (actual time=0.738..0.738 rows=1 loops=1)
               Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
   ->  Index Scan using idx_playlists_user_competition on playlists p  (cost=0.29..8.31 rows=1 width=8) (actual time=0.615..0.615 rows=1 loops=1)
         Index Cond: ((user_id = 1738530) AND (competition_id = 40026))
 Planning Time: 4.439 ms
 Execution Time: 4.051 ms
```

### 3. Get all user's playlists ###
Get all playlists:
```

Hash Join  (cost=7034.00..15031.58 rows=250000 width=29)
   Hash Cond: (ps.playlist_id = p.playlist_id)
   ->  Hash Join  (cost=5492.00..12833.27 rows=250000 width=25)
         Hash Cond: (ps.song_id = s.song_id)
         ->  Seq Scan on playlistsongs ps  (cost=0.00..3852.00 rows=250000 width=8)
         ->  Hash  (cost=2738.00..2738.00 rows=150000 width=21)
               ->  Seq Scan on songs s  (cost=0.00..2738.00 rows=150000 width=21)
   ->  Hash  (cost=917.00..917.00 rows=50000 width=8)
         ->  Seq Scan on playlists p  (cost=0.00..917.00 rows=50000 width=8)
 ```
 
##### Description of explains: #####
The query above, which joins three different tables, sees its large cost due to the large tables it has to join from the scaled-up database from the faked data. 

Indexes from the previous endpoint improvements already show some improvement in its cost and execution. Namely, these indexes were:
```
CREATE INDEX idx_playlists_user_competition 
ON playlists (user_id, competition_id);
```
Another index to be added to increase optimization and speeds is:
```
CREATE INDEX idx_playlistsongs_playlist_song
ON playlistsongs (playlist_id, song_id);
```

After adding these two indexes, the resulting explain is as follows:
```
 Nested Loop  (cost=1.13..15.18 rows=5 width=29)
   ->  Nested Loop  (cost=0.71..12.87 rows=5 width=12)
         ->  Index Scan using idx_playlists_user_competition on playlists p  (cost=0.29..8.31 rows=1 width=8)
               Index Cond: (user_id = 1738530)
         ->  Index Only Scan using idx_playlistsongs_playlist_song on playlistsongs ps  (cost=0.42..4.51 rows=5 width=8)
               Index Cond: (playlist_id = p.playlist_id)
   ->  Index Scan using songs_pkey on songs s  (cost=0.42..0.46 rows=1 width=21)
         Index Cond: (song_id = ps.song_id)
```

After the addition of those two indexes, the total cost of the single query that joins three tables went from ~7034 to ~1. With indexes, the query plan can now utilize nested loops and index scans to optimize how it joins and searches the query result. 
 
