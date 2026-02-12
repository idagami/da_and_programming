A unique productivity tool that encourages continuous writing by deleting your text if you stop typing for too long. This "write or lose it" concept helps overcome writer's block and maintains writing momentum through gentle pressure.

## Features

- **Auto-Delete Timer**: Text disappears after 2 seconds of inactivity
- **Countdown Warning**: 10-second countdown before deletion
- **Color-Coded Alerts**:
  - **Green**: Safe - actively typing
  - **Yellow**: Warning - 5 seconds remaining
  - **Pink**: Danger - 3 seconds remaining
  - **Red**: Text deleted
- **Word Counter**: Real-time word count tracking
- **Scrollable Text Area**: Comfortable writing space
- **Visual Timer**: Countdown display to stay aware

## Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework with text widgets and timers

## How It Works

1. Start typing in the text area
2. Keep typing continuously - timer resets with each keystroke
3. If you stop for **2 seconds**, a **10-second countdown** begins
4. Background color changes warn you:
   - Green → Yellow (5 sec left) → Pink (3 sec left) → Red (deleted)
5. Resume typing anytime to reset the countdown
6. Your word count updates in real-time

## Concept & Purpose

This app is designed to:

- **Overcome Writer's Block**: Forces continuous writing without overthinking
- **Prevent Perfectionism**: No time to edit, just write
- **Build Writing Habits**: Encourages flow state and momentum
- **Freewriting Practice**: Great for brainstorming and rough drafts

## Installation

No additional packages required (uses built-in Tkinter)

## Running the Application

```bash
python main.py
```

## Project Structure

- `main.py` - Complete application code
- `logo.png` - Application logo

## Settings

- **Inactivity Timeout**: 2000ms (2 seconds)
- **Countdown Duration**: 10 seconds
- **Yellow Warning**: At 5 seconds
- **Pink Warning**: At 3 seconds
- **Text Area**: 26 lines × 44 characters
- **Font**: Courier 12pt

## Timer Behavior

- Keystroke detection via `<KeyRelease>` event
- Each keystroke cancels existing timers
- New 2-second wait timer starts
- If no keystroke, 10-second countdown begins
- Text deleted when countdown reaches zero

## Requirements

- Python 3.13
- Tkinter (included with Python)

## Tips for Use

- **Don't stop typing!** Keep your thoughts flowing
- Watch the word counter for progress
- Use for first drafts, not final edits
- Perfect for timed writing exercises
- Great for overcoming perfectionism
