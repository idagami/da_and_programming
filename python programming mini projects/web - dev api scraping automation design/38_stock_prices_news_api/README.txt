A script that monitors stock price changes and sends WhatsApp alerts with news.

Features:
Uses Alpha Vantage API for historical stock data.
Uses NewsAPI to fetch the latest news articles about a company.
Detects significant daily stock changes (>5%).
Sends WhatsApp messages via Twilio with the top 3 relevant news headlines if a rapid change occurs.
Supports HTTP proxy setup for Twilio (corporate/firewalled networks).