# Sadboi

A discord bot that saves, loads, and plays playlists for Rythm and other audio bots using the "!" command. 
However, it still lacks the saving & loading features as it is in pre-alpha phase.

**You can use the `?help` command to know about all available commands**

The bot currently uses "?" as a prefix.

(Bots using different prefixes require modification of files)


## **Current features & how to use them**:
1. Joining and leaving VC (*By using ?join & ?leave commands respectively*)

2. Playing playlists by typing "!play {NameofPlaylist}"  by iterating through sbdb.json for the song names in the specified playlist. (*By using ?playlist "NameofPlayList". Currently saved playlists are only placeholders for testing purposes*)

3. Clearing messages. Requires mod powers. (*By using ?clear {amount}. Default amount is 10.*)

4. Repeating messages. (*By using ?echo {message}.*)

5. Adding & removing songs in playlists. (*By using ?addsong {SongName} & ?rmsong {SongName} respectively.*)

6. Viewing songs in playlists and all playlists. (*By using ?v {PlaylistName} & ?vpl respectively.*)

7. Creating & deleting playlists. (*By using ?cpl {PlaylistName} and ?dpl {PlaylistName} respectively*)

8. Moving songs up and down in a specific playlist. (*By using ?movup {PlaylistName} {SongName} and ?movdn {PlaylistName} {SongName} respectively*)

9. Shuffling, and playing a specific playlist. (*By using ?shuffleplay {PlaylistName}*)

## **Planned features**:
1. Add error checking.

2. Save playlists from Rythm currently playing playlist.

3. Remove case sensitivity for playlists & songs, while also allowing spaces to be saved in the database.

Currently in **pre-alpha phase**
