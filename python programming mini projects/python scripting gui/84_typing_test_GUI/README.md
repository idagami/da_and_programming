A desktop typing speed test application that measures your typing performance in Words Per Minute (WPM). Challenge yourself with random text passages and track your typing speed in a clean, user-friendly interface.

## Features

- **Timed Test**: 3-minute typing challenge
- **Random Text Selection**: Multiple text templates for variety
- **Real-time Countdown**: Visual timer display
- **WPM Calculation**: Automatic words-per-minute scoring
- **Dual Text Display**: Side-by-side text preview and typing area
- **Scrollable Interface**: Easy navigation through longer texts
- **Maximized Window**: Full-screen experience for focused typing

## Technologies Used

- **Python 3.x**
- **Tkinter** - GUI framework with scrollbars and text widgets
- **Custom Text Templates** - Variety of typing passages

## How to Use

1. Click **"Start"** to begin - a random text will appear
2. Type the displayed text in the typing area
3. Complete as much as possible within 3 minutes
4. Your WPM (Words Per Minute) result will be displayed
5. Click **"Reset"** to clear and try again

## WPM Calculation

```
WPM = (Total Characters ÷ 5) ÷ (Time in Minutes)
```

Standard formula: Every 5 characters = 1 word

## Installation

No additional packages required (uses built-in Tkinter)

## Running the Application

```bash
python main.py
```

## Project Structure

- `main.py` - Main application GUI
- `text_templates_class.py` - Collection of typing test passages
- `logo.png` - Application logo

## Window Settings

- Starts maximized for full-screen experience
- Color scheme: Yellow background with blue accents
- Font: Courier (fixed-width for typing)
- Test duration: 180 seconds (3 minutes)

## Requirements

- Python 3.13
- Tkinter (included with Python)

## Author

Desktop application for testing and improving typing speed
