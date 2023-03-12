# yt-timestamp-to-twb

![demo](diagrams/demo.gif)

Lets you paste YouTube description timestamps into a box and it will try its
best to convert that to a TWB-formatted .csv file.

Useful when digging up old vods that have timestamps but you want to ingest them
into a database like TWB, STR etc.

## How to use

* Download and unzip [latest release](https://github.com/hugh-braico/yt-timestamp-to-twb/releases)
* Run the exe
* Choose a filename to save your output csv data to
* Fill out all the information relevant to the event in the left pane
* Paste timestamps in the centre pane
* Click "Create CSV", the right pane should display errors/results
* The data will be saved to the filename you chose, don't copy stuff from the 
  right pane!

## Team format

There is a great deal of freedom in writing the teams:

* Full (Cerebella), abbreviated (CE, BE), and colloquial (Bella) names are okay
    * Mixing and matching between them is fine too
* Arbitary amount of space between characters are ok.
* Case insensitive.
* You can optionally use `N` to denote empty slots in a team.
    * eg. `Filia/N/N` for solo Filia
    * eg. `CE, Band, N` for duo bella/band
* Fuzzy-matched, so even spelling errors (Cerabella) are usually okay.

However, there are some hard rules:

* Characters must be separated with `,`, `/`, or `|`
    * So `Bella/Band` is fine, but `BellaBand` is not.
* The entire team must be enclosed in `()` or `<>`.
    * So `SeaJay (VA/CE/BB)` is fine, but `SeaJay VA/CE/BB` is not.
    * This is to make it easy to tell where the player name ends.
    * You can't use `[]` because that's usually reserved for sponsor tags.

Examples of valid teams:

* `(AN/CE/BB)`
* `<Annie,Cerebella,Band>`
* `(Annie, Bella, Band)`
* `<  Anee,   ceroBELLA,    Beeg Bando     >`

## Entire timestamp line format

* Timestamp must be `hours:minutes:seconds` or `minutes:seconds`
* Player name followed optionally by a team
    * If the team isn't supplied, you will have to fix the csv manually!
* Must be a "vs" or "versus" in between

In summary:

```
(optional hour:)minutes:seconds P1Name (optional team1) vs/versus P2Name (optional team2)`
```

Examples:

* `1:40:42 No Funny Name (FI/CE/BB) vs ComicBookGuy (MF/BD/DB)`
* `6:26 Drip vs Gojirark`
* `0:41:08 Greenhood <Eliza, Annie, Robo> vs Aeiry <Brella, Annie, Band>`

## Build your own .exe release

```bash
pyinstaller --onefile -w -i assets/bigband.ico main.py
```

## TODO

* .exe packaging
* Make diagrams/demo.gif
* Migrate to pytwb when that becomes a thing
