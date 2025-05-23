# MiscScripts
A collection of miscellaneous single scripts and lesser projects.

This is just a big repository for any of my scripts that don't require installing any additional libraries or environments, or don't have any reason to be individual repos. I'll add new scripts here as I create them.

Most of these will require Python 3.

## chess.py
This is checkers.

Move pieces by entering a row, column, and direction:
- u for up left
- r for up right
- d for down right
- l for down left

For example, to move your up leftmost piece up and to the right, enter: 62r

I'm not adding a clickable gui

## sokobarn.py
A Sokoban engine. "Barn" is a play on "Barney".

This automatically expects `Microban.txt` to be in the same directory since I made this script to play [Microban by David W Skinner](http://www.abelmartin.com/rj/sokobanJS/Skinner/David%20W.%20Skinner%20-%20Sokoban.htm) in the CLI,
but you can play other sokoban puzzle files by calling them as an argument (E.G. `python sokobarn.py Sasquatch.txt`)

Controls:
- Arrow keys to move the player
- E or Backspace to undo a move
- R to reset the current puzzle
- N to progress to the next puzzle
- P to return to the previous puzzle
- G to jump to any puzzle by entering its ID

Don't undo into negative numbers or you'll make the script sad. I wrote this for me not for you

If tiles display weird you can edit the characters at the top of the script, but if you're actually trying to play sokoban I'd maybe use something else?

## countdown.py
Digital recreations of the 2 main games on [Countdown](https://en.wikipedia.org/wiki/Countdown_(game_show)), that one british game show.

Since half this script is a word game, this requires the wordlist to be in `words.txt` in the same directory. It's not 1:1 with the official countdown wordlist but I pull from [This repo](https://github.com/dwyl/english-words) for most of my scripts that play with english words.
I'm not writing the rules to countdown here so you'll need to look those up as well. They should be in the wikipedia article I linked.

The tileset for the numbers game will be accurate but the show doesn't tell us the letter set publicly. Also, all letters/numbers will immediately get shuffled back into the bag after each round, which they don't do in countdown (for the letters, at least).

Controls:
- On script start:
  - W to play the word game
  - N to play the numbers game
- After a game has finished:
  - Enter to play again
  - W or N to switch games
- During word game:
  - When getting letters:
    - V to get a random vowel
    - C to get a random consonant
    - H to assess the current letters for best possible & best potential words
  - When getting words:
    - Hit enter to submit any word.
    - I think I forgot to make this case insensitive so just use all lower case
- During numbers game:
  - When getting large numbers:
    - Press any number between 0 and 4 to pick the amount of "Large" numbers
  - When selecting numbers:
    - Press any number to select the numbers displayed (0 for the leftmost number, 1 for the second number, etc.)
    - After selecting 2 numbers, press any number to select an operation (Same as selecting numbers), 2nd selected number will be on the right side of the operation
    - Select the same number twice to directly submit it

Any input other than the recognised ones will just kill the script. Same goes if you divide bad and get floating point numbers (Illegal move in countdown)

Sorry if this is esoteric and weird. I made this for practice, as if I ever have a shot at getting on countdown as a bisexual west australian

## vflip.py
A recreation of [Voltorb Flip](https://bulbapedia.bulbagarden.net/wiki/Voltorb_Flip) from the NA/PAL release of Pokemon Heartgold/Soulsilver (The DS one).

The rules are explained in the link above, so I won't elaborate on them here. That said, this includes 2 QoL additions:
- A keybind for marking both 0 and 1 simultaneously
- A row/column marking system for filling in entire lines

This also includes the levelling/score tracking system from the original game, including accurate tilesets. Closing the script will NOT save your score.

"Voltorbs" are represented as 0s in all cases.

For the numbers on the side, the topmost number for each row represents the total value of the row, while the bottom number represents the voltorbs. For the bottom numbers, the leftmost number shows the value.

Controls:
- Arrow keys/WASD to move the cursor
- Enter/Space/5 to flip a tile
- 0 - 3 to toggle the respective note on the currently selected tile
- 4 to toggle BOTH 0 and 1 on the currently selected tile
- R/C to toggle row/column marking mode respectively
  - Row/Column marking mode will toggle ALL marks on that selected line
  - This will not affect flipping tiles
- Press any input between rounds to continue the game

Any unrecognised inputs will kill the script.
