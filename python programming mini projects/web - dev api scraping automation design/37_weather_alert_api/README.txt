Weather Alert via WhatsApp (Python – Requests + Twilio)
A script that checks the weather forecast and sends alerts via WhatsApp using Twilio.

Features:
Uses OpenWeatherMap API to get 2-day forecasts in 3-hour intervals for a specified location.
Detects rain or serious weather conditions by analyzing weather codes.
Sends WhatsApp messages automatically for serious atmospheric conditions using the Twilio API.
Supports HTTP proxy setup for Twilio requests (useful for corporate networks).
Fully configurable via .env for API keys, Twilio credentials, and phone numbers.

How it works:
Fetch weather forecast from OpenWeatherMap.
Check each 3-hour segment for precipitation or extreme conditions.
Send an alert message through WhatsApp if serious weather is expected.