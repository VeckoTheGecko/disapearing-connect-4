# Disapearing Connect 4
A multiplayer game of connect 4, with a twist! Each time somebody places a new token, their previous token's colour disappears. A game of simple strategy just got a new challenge: memory 🤩.


## Controls
| **Action**                   | **Key(s)**    |
|------------------------------|---------------|
| Move left                    | A,←           |
| Move right                   | D,→           |
| Move to position             | 1,2,3,4,5,6,7 |
| Place                        | Enter,S,↓     |
| Toggle disappearing gamemode | N             |
| Restart                      | R             |
| Quit                         | Esc           |

## Running instructions
### Option 1 (Windows):
The executable is available from this link. Just download, extract and run!
https://drive.google.com/file/d/1l0W9Uf_HQrleNknFSUQqDH1yHpUmdjBQ/view?usp=sharing

### Option 2 (Python):
This game only relies on the `pygame` module in Python. Download and install python, and install the pygame module (the version listed in `requirements.txt`).

Then download this source code, `cd` into this folder and run the `main.py` script.

## Future development
Along with polishing up the codebase (and the UI), I plan on creating a bot for the game so that you can also play it singleplayer.

At this stage I'm not planning on coding difficulty levels, so expect to just have a bot that can absolutely destroy at connect 4.

Also I might look into a replay mode for you to be able to save replays of your games
