a desktop Wordle-style game built with Python and Tkinter.
The game includes a graphical UI, on-screen keyboard, score system, persistent settings, and word validation logic.

It closely mimics the classic Wordle gameplay while adding:
Configurable word length
High score tracking
Local database storage
Custom UI styling and animations

Features
Graphical UI using Tkinter
On-screen keyboard + physical keyboard support
Word lengths from 3 to 6 letters

Color feedback:
Green → correct letter & position
Yellow → letter exists but wrong position
Gray → letter not in word
Score system with bonus for fewer guesses
High score persistence using SQLite

Settings window:
Change word length
Edit high score
Popup dialogs for win / loss
Word validation using local word lists

All dependencies are listed in requirements.txt.
Must activate venv.