A classic Breakout arcade game built with Python Turtle graphics. Break all the colored blocks using a ball and paddle while managing your lives. Features different block values, increasing difficulty, and score tracking.

## Features

- **Classic Breakout Gameplay**: Bounce the ball to break blocks
- **Color-Coded Scoring System**:
  - Yellow blocks: 1 point
  - Green blocks: 3 points
  - Orange blocks: 5 points + speed increase
  - Red blocks: 7 points + speed increase
- **Lives System**: Start with 2 lives, lose one when ball falls
- **Progressive Difficulty**: Ball speed increases as you hit orange/red blocks
- **Paddle Controls**: Move left/right with arrow keys
- **Score Tracking**: Real-time score and lives display
- **Game Over Screen**: Final score display when lives run out

## Technologies Used

- Python 3.13
- **Turtle Graphics** - Game rendering and animations
- **Object-Oriented Programming** - Separate classes for game components

## How to Play

1. Run the game - the ball starts at the bottom
2. Use **Left Arrow** and **Right Arrow** keys to move the paddle
3. Keep the ball from falling off the bottom of the screen
4. Break all blocks to win
5. Higher colored blocks = more points and faster ball!

## Controls

- **Right Arrow** → Move paddle right
- **Left Arrow** → Move paddle left

## Scoring System

```
Yellow:  1 point
Green:   3 points
Orange:  5 points + 10% speed boost
Red:     7 points + 10% speed boost
```

## Game Mechanics

- **Ball Physics**: Bounces off walls, paddle, and blocks
- **Speed Progression**: Ball accelerates when hitting orange/red blocks
- **Paddle Bounce**: Random horizontal direction after paddle hit
- **Lives**: Lose a life when ball falls below screen
- **Game Over**: Occurs when all lives are lost

## Installation

No additional packages required (uses built-in Turtle)

## Running the Game

```bash
python main.py
```

## Project Structure

```
├── main.py              # Main game loop and logic
├── ball_class.py        # Ball object and movement
├── paddle_class.py      # Paddle controls
├── blocks_class.py      # Block creation
└── scoreboard_class.py  # Score and lives tracking
```

## Game Configuration

- **Screen Size**: 578 × 600 pixels
- **Starting Lives**: 2
- **Block Layout**: 8 rows × 9 columns (72 total blocks)
- **Initial Ball Speed**: 0.1 seconds per move
- **Paddle Movement**: 20 pixels per keypress

## Code Highlights

### Ball Mechanics

- Bounces off left/right walls
- Bounces off top wall with random horizontal direction
- Accelerates when hitting paddle (10% increase)
- Resets position when falling below screen

### Collision Detection

- Ball-to-paddle: Distance < 50 pixels
- Ball-to-block: Distance < 50 pixels
- Boundary detection for walls

## Requirements

- Python 3.x
- Turtle graphics module (included with Python)

## Tips for Playing

- Keep the ball centered for better control
- Aim for orange/red blocks early for challenge
- Watch for speed increases - paddle responsiveness is key
- Position paddle in advance, not reactively

## Future Enhancements

Potential improvements:

- Power-ups (multi-ball, larger paddle, slower ball)
- Level progression with different layouts
- High score persistence
- Sound effects
- Pause functionality
- Different difficulty modes
