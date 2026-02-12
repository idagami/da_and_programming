1. ISS Overhead Notifier (Python – API + SMTP + dotenv)

Checks if the ISS is currently overhead your location at night and sends an email alert.
Uses requests to fetch ISS and sunrise/sunset data from public APIs.
Compares ISS coordinates to user location and checks local time for darkness.
Automatically sends a Gmail alert using smtplib when conditions are met.

2. Daily Joke App (Python – Tkinter + API)

Displays a random two-part joke with GUI using Tkinter.
Fetches jokes from the JokeAPI and shows setup and delivery interactively.
Includes buttons for “Next joke” and “Show answer,” plus a fun emoji animation.
Uses PhotoImage for backgrounds and buttons for a visually appealing layout.