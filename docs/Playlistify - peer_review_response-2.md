# Peer Review Response

- Feedback:

**/{user\_id}/competitions**  
Since usernames are already unique, it might be better to just pass in the username instead of the user\_id 

* During testing, I somewhat remembered my user\_id but wasn't 100% sure if my user\_id was correct since there was no way to obtain the user\_id again  
  * However, it didn't quite matter since I could just enter any user\_id prior to mine and access their competitions  
  *   
- Response: The purpose of having a user\_id field is that it easily confirms uniqueness and remains immutable, unlike usernames, which can potentially change. Additionally, user\_id serves as a foreign key in several other tables, ensuring consistent relationships. Using user\_id also adds a layer of obscurity, since username is public information.

## 

- Feedback:  /{user\_id}/all/playlists Same thing as above. Pass in username instead of user\_id  
- Response: See above comment.

- Feedback There were a bunch of discrepancies between the API spec and the request/response  
  * Many of the IDs are integers in your code but are stated to be strings in your API spec


- Response: Resolved, all id’s are now integers   
5. Instead of a participants\_count in your Competitions table, you can query the usercompetitions table   
     
   Response \- Not implemented, we feel that a participants\_count will be more readable. 

## **/**

6. I was able to get competitions without being logged in so you might want to check if the person requesting is first logged in  
   

Response: \- No changes made. A person does not need to be logged in to see what competitions are active. 

7. You return an integer for "competition\_id" when your API spec states that it's a string

Response: \-Resolved: Updated API Spec

In your code, your response is just "OK" but in your API spec, it's stated that the response should be:  
{

  "message": "string", /\* Success message or failure reason \*/

  "enrollment\_status": "boolean", /\* true if enrollment is successful, false otherwise \*/

  "competition\_details": {

    "competition\_id": "string", /\* ID of the competition \*/

    "username": "string", /\* Username of the participant \*/

    "start\_time": "string" /\* ISO 8601 format of the competition's start time \*/

  }

 Response: \-Resolved, we updated the API spec. We felt that the extra details were redundant so we just kept the message, and the competition\_id is already known per the request body. 

8. }

Small thing but I think the curly brackets could be a bit more indented to help it look cleaner  
{

  "message": "string", /\* Success message or failure reason \*/

  "enrollment\_status": "boolean", /\* true if enrollment is successful, false otherwise \*/

  "competition\_details": 

    {

        "competition\_id": "string", /\* ID of the competition \*/

        "username": "string", /\* Username of the participant \*/

        "start\_time": "string" /\* ISO 8601 format of the competition's start time \*/

    } 

9. }

Response: \- Fixed

API spec mentions the response should be  
{

  "message": "string",  /\* Success or failure message \*/

  "vote\_status": "boolean"  /\* true if the vote was successfully submitted \*/ but your code only returns an "OK" \- 

Response: Resolved \- updated API spec

10. Votes are 1 \- 5 but for clarification, you should state if a larger number is better or a smaller number is better \- 

Response: Not implementing \- a clarification like this would occur in the user interface

12. I feel like the song\_id shouldn't be an input that the user has to enter \-

Response: Not implementing, the song\_id enforces uniqueness for the backend implementation. 

* When testing, I was able to enter the same song\_title and artist twice by just incrementing song\_id \-

Response: Resolved \- raises appropriate error

13. Adding a song does not return a playlist\_id so the user does not know that 

Response: Resolved \- playlist id in request path

|  While testing, there was no way for me to know what the playlist\_id was at first until I saw the all/playlists endpoint I feel like adding a playlist\_id shouldn't be an input from the user  Response: \-Not implemented: the playlist\_id enforces uniqueness for the backend implementation  We need to pass a competition\_id in the input but also through the request body. Feels a little redundant. Response:  \- resolved \- competition id only in input The submission\_status in the response body json feels redundant as well since the message already states that the playlist submission is successful Response:  \-Resolved, changed code to match API spec.  Adding this to the end because I just realized as I was wrapping up my testing, I feel like there should be a create\_competition endpoint to allow users to create their own competitions Response:  \-Resolved, we have a create\_competition endpoint |
| :---- |

1. You should add try and except to all of your database connections across all of the endpoint functions

Response:  \- Try except is good for these scenarios for errors that are client facing. 

* Some endpoint functions have it and some don't  
  *   
2. You could standardize your SQL queries across all the endpoint functions too. Some endpoints functions have the SQL query directly in the parentheses (e.g.comps \= connection.execute(sqlalchemy.text("SELECT competition\_id, status, participants\_count FROM competitions ")).fetchall() while others are assigned to a variable (e.g. result \= connection.execute(playlist\_exists\_sql, {"playlist\_id": playlist\_id}).fetchone())  
   * Some queries that are stored in variables are also stored differently (e.g. some are just text() and some are sqlalchemy.text())   
   * 

Response: \-The differences are appropriate for each scenario 

3. For error handling, you could standardize either using status\_code \= status.HTTP\_\[insert error code\] or status\_code \= \[error code\]

Response:  \-Resolved, we standardized everything. 

4. Small thing but your table names should be in snake\_case instead of PascalCase (for PostgreSQL)  
   * e.g. active\_users instead of ActiveUsers 

Response: \- It doesn’t have to be snake\_case, we have a consistent schema going. 

## 

5. Line 63 & 65: join\_comp and add\_to\_user are variables that are never really used.  
   * Unless you're looking to use them, I think the code would look cleaner if it just updated/inserted into the database without assigning to a variable  
     Example:

connection.execute(sqlalchemy.text("""UPDATE competitions SET participants\_count \= participants\_count \+ 1 WHERE competition\_id \= :competitionid """), {"competitionid": compid})  
connection.execute(sqlalchemy.text("""INSERT INTO usercompetitions(user\_id, competition\_id, enrollment\_status, submission\_status) VALUES(:uid, :cid, TRUE, FALSE) """), {"uid": get\_user\_id, "cid":compid})  
Instead of:  
join\_comp \= connection.execute(sqlalchemy.text("""UPDATE competitions SET participants\_count \= participants\_count \+ 1 WHERE competition\_id \= :competitionid """), {"competitionid": compid})  
add\_to\_user \= connection.execute(sqlalchemy.text("""INSERT INTO usercompetitions(user\_id, competition\_id, enrollment\_status, submission\_status) VALUES(:uid, :cid, TRUE, FALSE) """), {"uid": get\_user\_id, "cid":compid})  
Response:  \-resolved, got rid of those variable assignments. 

## 

6. Line 105 \- 109: These lines can be indented to be part of the same connection block instead of opening another connection

Response:  \-Resolved, every query is part of the same connection block 

## 

7. Line 152 \- 156: These lines can be indented to be part of the same connection block instead of opening another connection \-

Response:  Not implemented: this will break the code, the connection needs to close there for the logic to work properly. 

8. In your error handling, you're raising a 404 error but also raising a 500 error \- 

Response: resolved, more granular error handling is implemented

9. Line 169: The comp\_message was hard to read and indented weird. I think this can be formatted a little better to help readability 

Response: Resolved \- fixed indentation 

# 

## 

10. You should verify that the username is less than 50 characters and the name is less than 100 characters before signing the user up  
    * Your users schema states varchar(50) for username and varchar(100) for name 

Response: Resolved \- implemented name validation

## 

11. You should check to see if user is already logged in before inserting into the activeusers table 

Response: Resolved \- we raise the appropriate HTTP exception in this case. 

12. Line 52: don't assign the insert into statement to a variable

Response:  \-Resolved, it is not assigned to a variable anymore. 

# 

13. Line 26 \- 34: These lines should be commented out / removed for now since this would give access to potion-exchange.vercel.app to make API calls to your backend

Response:  \-Resolved\! Removed the lines

### 

1, competition\_id should be int not string  
Response:  Resolved

2\. You could make a comment in the response to show that status can only be certain strings   
Response: \-Not implemented \- this would go in the user interface. 

### 

3. router path is not the same as implementation 

Response: resolved 

4. there is no request in your implementation, just parameters. username should be in a request body not in the params to fit api spec 

Response: \- resolved

5. response is not the same as the implementation

Response:  \- resolved

### 

6. request body should also include user\_id in API spec 

Response: \-Resolved and reflected in API spec

7. song\_id should be an int in API spec

Response:  \-Resolved

### 

8. request body should include user\_id in API spec 

Response: \-Resolved

9. all the ids should be ints not strings in API spec

Response:  \-resolved 

10. submission\_status is not present in response

Response:  \-resolved 

### 

11. You could add a comment where vot score can only be between 1-5

Response:  \-Not implementing, this is a feature that would occur in the user interface and it is also in the spec. 

request body in API spec is being treated as parameters in implementation

Response:  \- resolved \- pydantic model and request body used

12. playlist\_id should be an int in API spec

Response:  \-Resolved

13. vote\_user\_id is absent in API spec 

Response  \-Resolved, updated api spec

14. vote\_score in API spec is vote in implementation, making the variable names the same can make things less confusing

Response:  \- resolved changed api spec 

15. when success, the response format is not followed. Instead "OK" is returned. 

Response: \- resolved

### 

17. winner\_playlist\_id should be an int in API spec 

Response: \-Resolved

### 

18. switching between integer and number can be confusing if they are being used for the same thing, in this case the ids. Maybe using integer for the user\_id and competition\_id would make it less confusing since the ids are set up to only be integers in the schema.

Response: \-Resolved made everything integers

19. this function is not implemented

Response:  \-Resolved, deleted from API spec because a similar functionality already exists in /competitions

20. the API spec is confusing since you have the user\_id and the competition\_id as both parameters and in the request body 

Response: Resolved, deleted from API spec because a similar functionality already exists in /competitions

### 

21. user\_id is in both the request body and the parameters but only implemented as parameter  
    Response: \-Resolved  
    

### 

22. user\_id is in both the request body and the parameters but only implemented as parameter

Response: Resolved

23. the use of number when you mean specifically an integer can be confusing 

Response: \-Resolved, updated API spec

24. the response is confusing in the songs values, since its not a list of strings that is returned but a list of jsons that then contain an int and a string 

Response: \- this is not true, a list of strings is returned

25. request body in API spec does not reflect current implementation

Response: \- resolved

26. Username is implemented as a parameter but it is not in the URL 

Response: \- the person logging in may not necessarily be the username their entering as the parameter

27. API spec request body is not implemented, but username is used as parameter

Response: Resolved \- updated api spec

28. no token is returned in response

Response: Resolved \- updated api spec

29. not implemented

Response: Resolved \- removed no use case

competition\_id should also be a foreign key  
Response: It is

## 

31. upcoming is never used

Response: Resolved \- removed

32. What if there are multiple individual artists on one song?

Response: Playlistify v0 does not support this

### 

1. You can use dict(user) to make it a little more clean

Response:  \- Implemented this feedback for pydantic models with more fields

### 

2. You are setting Result \= to the SQL statement that is not returning anything.

Response:  \-No action taken

3. There is no logic for checking if the user is already logged in and thus returns a 500 error \-

Response: Resolved, now raises appropriate errors (400 and 404\)

### 

4. Although your competition code has it so you can not join the same competition, user\_id \= 6 has duplicates.

Response:  \- This was a manual change

5\. When the user\_id does not exist, there is no indication that the user does not exist

Response: Resolved \- implemented

### 

6. If the user or competition does not exist, you get a 500 error, instead try error checking that

Response: \-Resolved, raising appropriate exceptions. 

7. join\_comp is not receiving anything from the SQL so its not needed. 

Response: \-removed variable assignment

8. add\_to\_user is not receiving anything from the SQL so its not needed.

Response:  \-removed variable assignment 

### 

9. competition\_id parameter is not being used 

Response: \- No changes made \- competition\_id is being used.

10. using pydantic BaseModel classes would make the code cleaner.

Response:  \- resolved

11. making multiple dictionaries with information that already is contained in the vote\_info dictionary 

Response: \- resolved, implemented

### 

12. comp\_id \= 1 does not work. It exists and should show that it is active.

Response:  *\-Done, Competition ID \=1 is working*

13. competition\_status has an enum with (active, completed, & upcoming). The current returns do not make much sense with upcoming events. 

Response:  \- resolved, removed upcoming type

### 

14. using dict(song\_request) would make the code look a little cleaner and readable 

Response: \- resolved, no longer need song\_request

15. There is no redundancy check for song\_title and artist so I made like 5 versions of the same song. This is because you can input any song\_id so as long as the id I input is not being used, I can make duplicates.

Response:  \-Resolved \- Raises 400 Error if song is already in playlist

16. When song\_id is already in use, the song title and artist are ignored. To solve 15 and 16, maybe make it so that a song is only found through title and artist instead of using the song\_id that way if it exists you just return that row and if it doesnt, you create the row and return it. 

Response: \- resolved, request only takes song\_id

### 

17. having competition\_id and competition\_id\_body is confusing and not necessary because the body one is only used to check against the other one.

Response: \- Resolved \- removed competition\_id from playlist request body

18. dict(request\_body) would make it cleaner 

Response: \- it wouldn’t make the code that much cleaner, its only two fields

19. 

# 

Consider updating the ER diagram to include votes, active users, and playlist songs.  
Response:  \-Updated ER diagram in github

# 

Right now, it looks like users only have playlists that are connected to competitions. Consider letting users create their own playlists outside of competitions. This would be helpful because users can reuse playlists and wont lose any playlists that are made in competitions   
Response: \-This is not the intended purpose of playlistify, playlistify is only a competition platform. 

# 

Currently, I do not see any insertions to the competitions table. Consider adding a "create competition" endpoint.   
Response:  \-Resolved, create competition endpoint added

# 

Get\_competition\_status selects the winner's playlist ID but I don't see how that logic was inserted into the table. Consider adding a helper function to query the winning average to return that.  
Response: resolved \- upon competition completion (aka all the participants have voted) the winner\_playlist\_id gets updated in the column

# 

There seems to a wide range of functions in competitions. I suggest separating the endpoints for conciseness. For example, competitions should have:

1. Get competitions  
2. Join competitions  
3. Vote on playlist  
4. Get competition results

For endpoints that deal with a competition's playlist creation and submission create a new file and add the remaining functions in it. Use your best judgement to name this file something descriptive. (I couldn't come up with a good name suggestion)   
Response:  \-Not implementing \- we want to keep all competition-pertinent functions in competition

# 

I do not see get user playlist in competitions although it is listed in the API spec. If you plan on adding it, consider moving it to users instead.  
Response:  \- Fixed: removed from API spec because we already have a similar function in competitions. 

# 

Relates to [\#2](https://github.com/eamyzzaj/playlistify/issues/2). Allow the user to search for playlists with the playlist name. This opens up the possibility of the user submitting already made playlists  
Response: . \-No change made: playlists do not have names and are a part of competitions. A goal of playlistify is not to submit premade playlists, but make them for each competition. 

Currently, the endpoint is a bit hard to follow. I apologize if I'm misunderstanding but the next suggestions will regard playlist/song creation.  
In the add\_song\_to\_playlist function, the main functionality is to check if the song is already in the playlist and if not, add the song id to a specific playlist. You can also keep updating the user competitions table. Then you can add in helpers to validate the song insertion.  
Response: We can have more granular error handling by checking song insertion immediately

# 

This will increase readability if you put the logic in another function and call it when adding a song to playlist.   
Response: Helper functions are nice for repeated functionalities but for something that is only done once it is unecessary

# 

Add an additional column in playlist that self increments to determine song order, reduces the manual work you currently have  
Response: Its not much manual work/ latency increase to do this manually vs query for this

# 

Like Spotify, users can add songs to a playlist or to their library. This endpoint will allow users to add songs to the DB.  
Response: \-No changes made, a playlist is specific to a competition. Users do not have a library. 

# 

Once songs are added to the song table, the user can search for a song and it can return the ID so the user does not need to input the song title and artist again when creating a playlist.   
Response: Resolved, implemented

# 

It seems like user id is referenced a lot but since the username is unique, it would be easier for a user to remember their chosen username rather than their id.  
Response:  \-Not implementing, user\_id is the foreign key and it is essential to the backend implementation. 

# 

Some end points return duplicate information such as a success message and a boolean. Others return more information than the user needs   
Response: Resolved implemented 

# 

if (user):  
            result \= connection.execute(sqlalchemy.text("INSERT INTO activeusers(user\_id) VALUES (:uid)"), {"uid": user.user\_id})  
            return {  
                "message": "Login Successful"  
            }

The insert statement does not return anything unless the following syntax is added at the end of the SQL statement:  
RETURNING ...  
But in this case, since you are only returning a success or failure message, maybe remove "result \= " unless you plan on returning something other than the success or failure message.   
Response: \-Resolved, insert does not have that variable assignment anymore. 

I notice that there is inconsistency with how errors are handled. For example in create\_user, there is a try-except block.  
except Exception as e:  
        print(f"Account creation failed: {e}")  
        return {"message": 'Account creation failed', "user\_id": None}

But for the rest of the endpoints in Users, a message is just returned without try and except.  
return {  
                "message": "Login Failed"  
            }

Consider choosing one method of handling errors and keep it consistent throughout the code base and communicate that with the other developers.  
A suggestion is to be consistent with try-except and return a message with return a HTTP code. An example of this can be,  
return {"message": "Account created successfully", "user\_id": newuser\_id), 201  
raise HTTPException(status\_code=500, detail="Account creation failed")   
Response: \-HTTP codes standardized. In some cases, try/except is appropriate for handling the internal server errors. 

# 

For users creating an account, consider validating their username by checking if the input is within the 50 character limit you stated in your schema and ensure that there are no unwanted characters. For the name field, you can add a check to ensure there are no special characters. This will enhance consistency within your database.   
Response: \-Resolved, checks implemented

# 

When deleting a user from the active users table, consider checking if the table has one less row or perform a query to ensure you cannot find the id. This will ensure that the active users table is properly updated.   
Response: \-Not implementing, we know it is properly updated because we get a success message. 

# 

In user\_login, check the active users table to ensure the user has not already logged in. This avoids duplicate user ids in the active users table and encourages the user to log out after using Playlistify to secure their account. \-  
Response: Resolved, 400 error raised if user is logged in. 

# 

The response you currently have is  
\[  
  {  
    "user\_competitions": "List\[competition\_id\]"  
  }  
\]

Which is consistent in both the code and API spec but in an example flow I notice the response is  
\[  
   {  
       "competition\_id": "RockPlaylist01",  
       "status": "completed"  
   },  
   {  
      "competition\_id": "Jazzvibes2024",  
      "status": "active"  
   }  
\] 

So depending on what you wanted, consider adding the status to the code and update the API spec or remove the status from the example flow. Additionally, in the example flow, the user id input is  
{  
  "user\_id": "amir001"  
}   
Response: –Resolved, updated example flow

But the user id should be an int, so consider changing that to an actual ID or changing the input to username instead.

# 

In get\_all\_user\_playlists consider adding a helper function to organize the playlist so the outer function has a concise function of getting the playlists and improves readability.  
This code chunk can go into an organize\_playlist function  
       playlists\_dict \= {}  
        for row in result:  
            if row.playlist\_id not in playlists\_dict:  
                playlists\_dict\[row.playlist\_id\] \= {  
                    "user\_id": user\_id,  
                    "competition\_id": row.competition\_id,  
                    "playlist\_id": row.playlist\_id,  
                    "songs": \[\]  
                }  
            playlists\_dict\[row.playlist\_id\]\["songs"\].append({  
                "song\_id": row.song\_id,  
                "song\_title": row.song\_title  
            })

        playlists \= list(playlists\_dict.values())

Response: No need to make a helper for something we do once

# 

For all queries, consider adding try- except blocks to ensure that data has been properly retrieved and to catch any errors. This will prevent the rest of your code running into an error when nothing is returned and provides meaningful feedback.  
Response:  \-Resolved, appropriate HTTP errors raised

# 

There are two database connections made but there should only be one. When a vote is unsuccessful consider returning a http code other than 404, as it could be misleading. Try returning a 500 or 400 code depending if its a server or client issue.   
Response: The way the logic is implemented there must be two separate connections to handle errors more granularly

# 

Again, there are two database connections here. The connection only closes if a competition is not found so consider taking the second connection out.  
Additionally, there should be error checking for comp\_results to ensure something useful was returned. This function is quite long so consider breaking it into helper functions or adding comments to help readability.    
Response: \-Partially resolved: doing single connections but not using helper functions as that would bulk up the code

# 

I recommend adding sqlalchemy.text() to the text portion of the query just to be more specific. Rather than naming the query "query", try being more specific on what it returns. A suggestion for the variable name could be comp\_stats.  
Additionally, rather than creating a playlist inside this function, considering adding another end point for that.  
For ordering the songs, the current code took me awhile to understand. I suggest adding a column for ordering, where it self increments like an id, it'll make for easier readability and will be easier to manage rather than ordering manually.  \-Partially resolved \- it’s automatic, if you don’t have a playlist it makes it for you\! Fixed the query name. It already increments for songs. 

# 

The overall function is long but it could be broken up into smaller parts for readability and organization. Consider adding a helper function for validating the results from the query. \-Not implementing, we feel that helper functions would bulk up the code and be a detriment to the organization. 

# 

It feels like there are still missing endpoints to this code:

### 

A user is allowed to join a competition but how are competitions created? Maybe allow a user to create their own competition \-Resolved, added a /create endpoint

### 

How does a user have a voter\_user\_id to pass through the function although they have not yet voted?  \-No implementation necessary, voter\_user\_id is simply the user\_id of the person voting. 

### 

Consider revising how songs and playlists are created. Right now it seems like playlists are created when they do not exist when trying to add a song. I suggest having a create playlist option as well, so users have different paths when competing and interacting with your API. \- Not implementing, the automation is a feature that is convenient for the user. 

### 

If there is consistent checks for user enrollment, active competition and any other things, consider making it a helper function to decrease redundancy. \-Not implementing

### 

Consider splitting the endpoints into two files, one named competitions and the other named playlist. This will clearly explain the distinct purpose of each file as your API gets more complex. \-Good idea, but does not change functionality of playlistify. 

## 

Nitpick: userCreateRequest class should be capitalized

### 

1. You're catching all exceptions here and returning 200 codes regardless of what happens. I would consider error code responses in some cases. \-Resolved, raising appropriate error codes.   
2. As a specific example, in the situation where someone tries to signup with a username already in use, you might consider returning 400 or 409 status codes instead of 200\. \-Resolved, raising 400 error.   
3. When accepting the result of your user insert, you might consider using .scalar\_one() instead of .scalar(). \-Good idea, but does not improve the function of signup. 

### 

4. Before inserting a user into the active users table, you should check to make sure they are not already in the active users table. You could then have an additional message to indicate that the user is already logged in. As detailed in the test results, successive login attempts results in a 500 error.  
   Nitpick: Missing a type hint on username function parameter \-Resolved; checks if user is active or if user does not exist and raises appropriate errors. Parameter includes type hint

### 

5. If someone tries to logout a user that doesn't exist, you might consider adding a more indicative error message for this situation, such as: User Does Not Exist. \-Resolved; checks if user exists and raises appropriate errors if necessary. 

### 

- Feedback: I don't see the need for separate transactions within this method. You can execute both queries under the same with db.engine.begin().   
- Response: Resolved \- Everything in this endpoint is in the same with db.engine.begin()

- Feedback: If the only point of executing the first query is to check if the result exists, you could use .one() on your query result, to let sqlalchemy throw the exception. Or, if you want to throw your own exception and keep the current flow, .one\_or\_none() might be better than .fetchone(), as you're already only selecting one result in the SQL statement.   
- Response: We prefer to raise exceptions for readability, granular error messages and consistency with the rest of the code. 

- Feedback: The exception handling here could use some reworking. You catch all exceptions here and return 404 for all of them. In the case that you have a database error or something else, I suggest your throw a generic 500\. Additionally, you're catching your own 404 error ('Playlist not found'), and then throwing a new error with a different message ("Vote unsuccessful"). I would try to avoid catching your own exception by only catching specific exceptions.  
  Nitpick: detail=f"Vote unsuccessful" using string inperpolation when unnecessary.  
- Response: Resolved, more granular errors

- Feedback: Don't see the need for seperate transactions.  
- Response: No implementation, the connection needs to close there for the logic to work. 

- Feedback: Catching your own 404 and throwing a new 500 with a different message. In this case you're eating up the 404 exception, and it gets disguised as a 500\. \-  
- Response: Resolved, implemented 

- Feedback: Nitpick: multiple instances of string interpolation when unnecessary.

This is a bit difficult to read:  
comp\_message \= f"Competition is {comp\_status}.\\\\n" \\  
                                f"User {winner\_username} won with a score of {playlist\_score} on their playlist\!\\\\n" \\  
                                f"Total participants: {num\_players}\\\\n" \\

9.                                 f"Competition length: {comp\_length} minutes"

I think something like this is a bit more readable and might eliminate the need for .replace('\\\\n', '\\n') later on:  
comp\_message \= (  
        f"Competition is {comp\_status}.\\n"  
        f"User {winner\_username} won with a score of {playlist\_score} on their playlist\!\\n"  
        f"Total participants: {num\_players}\\n"  
        f"Competition length: {comp\_length\_minutes} minutes"

- Response: No changes, useful for debugging. 

## 

- Feedback: Sometimes you use standardized HTTP status codes like status\_code=status.HTTP\_400\_BAD\_REQUEST and sometimes you use magic numbers like status\_code=400. Picking one standard would help with uniformity and consistency.

Sometimes you use query parameterization in the query formation step:  
insert\_vote\_sql \= sqlalchemy.text("""  
                                    INSERT INTO votes (voter\_user\_id, playlist\_id, vote\_score)  
                                    VALUES (:voter\_id, :playlist\_id, :vote\_score)

                                      """)  
and sometimes at the same time as query execution:  
song\_order\_sql \= text("""  
            SELECT COUNT(\*) FROM playlistsongs  
            WHERE playlist\_id \= :playlist\_id  
        """)        song\_order \= connection.execute(song\_order\_sql, {"playlist\_id": playlist\_id}).scalar() \+ 1 Picking one standard would help with uniformity and consistency.  
Response: Implemented \- consistent error messages 

- Your exception logging is generally of the form:  
  catch Exception as e:print(f"Some error message: \\n{e}")

If you import logging you can instead do:  
catch Exception as e:logging.exception(e)  
Response: We don’t generally need logging we had leftover print statements from debugging

- Feedback: which provides a lot more information (like a stack trace) that is pretty helpful for debugging.  

Response: We kept try/except in some areas where we felt it was helpful, but standardized the format of all HTTP Exception status\_code 

## 

- Feedback: Remove some [leftover boilerplate](https://github.com/eamyzzaj/playlistify/blob/69e63b115d1e17d298d00ddb0b509a883c190312/src/api/server.py#L26C1-L26C49) from the potion shop code.

Response: Resolved\!\! Ooops 

13.   
- Feedback: Since you already refer to users by their username in signup, signin, and logout, and you're enforcing uniqueness, I think it would be nice to also use usernames for get\_user\_competitions and get\_all\_user\_playlists instead of user\_id in the routes.

Response: No change, the user\_id is the foreign key essential for the backend implementation. 

- Feedback: user/{user\_id}/all/playlists does not return the artist as part of the song data. competition/{competition\_id}/playlists/songs does return the artist as part of the song data. I think it would be nice to always have the artist as part of the song data. \-

Response: No implementation, in the scope of one playlist the artist could be nice info to have, but in the scope of all playlists it could crowd the output too much. 

- Feedback: The API spec details an email field as apart of user signup but this isn't present in the code.

Response:  \-Resolved, the email has been removed from spec.

- Feedback: In the signup endpoint, the API spec details a failure response with only a message, however, a failed execution of this endpoint still results in a response with a user\_id with a null value.   

Response: \-Resolved, error is raised now with only a message. 

- Feedback: The API spec details a password field as apart of user login but this isn't present in the code. Ditto for the token in the response.

Response:  \- Token authentication was determined to be outside of the scope of playlistify. 

- Feedback: The API spec details a get all users endpoint, which isn't present in the code. From a user standpoint this would be cool to use, similar to a search feature on social media. If you did implement it, I suggest only returning username as part of the data, and not user\_id and email. 

Response:  \-Removing endpoint, we have decided this is outside of the scope of playlistify. 

- Feedback: You don't technically need a participants\_count in the Competitions table. You can query the UserCompetitions table to get the participant count.

Response:  \-No action taken, participants\_count is more readable 

- Feedback: The response of submit\_playlist seems to be redundant. I think if you have a message then the true/false status is unnecessary.

Response:  Agreed, the api spec and response body was updated to just return the message

- Feedback: Ditto for vote\_on\_playlist but looking at the code, it only returns "OK". 

Response: \- Agreed, updated API spec

- Feedback: There really is no way to know what playlists to vote on. I cannot see what users or what playlists are apart of a competition. I think an additional endpoint would be really helpful here.

Response:  \- No changes made: This would be a front-end implementation. We have an endpoint to access the playlists for a given competition, and users could vote through the UI on these playlists. 

- Feedback: I don't see the value of letting users choose the song\_id when adding a song to their playlist. From a user perspective, it doesn't really make sense.

Response:  \-song\_id is not something chosen when adding the song to the playlist. It is the backend reference to the correct song.

- Feedback  
  add\_song\_to\_playlist doesn't return a playlist\_id and there is no endpoint explicitly for creating a playlist. When using your API for the first time, I had no idea what to put in as my playlist\_id when submitting my playlist for voting. I did later see that you can fetch playlists by user. You require a playlist\_id AND competition\_id in order to submit a playlist, but the way things are implemented, you cannot have more than one playlist per competition per user. So, I think you have two choices  
  * You give users full control over their playlists, and return the id in add\_song\_to\_playlist, and maybe add an endpoint to create a playlist  
  * OR you can take control of the playlists, and you shouldn't have the user bother with dealing with a playlist\_id

Nitpick: some places in the API spec use integer and some use number.  
Response:  \-Resolved  
