Check the price of an Amazon product and send an email if the price drops below a threshold.

Key Steps:
Fetch the product page with requests.
Parse HTML with BeautifulSoup and extract the price (span.a-offscreen).
Convert the price to float.
Compare with the desired_price.
If current price is lower, send email using SMTP with Gmail credentials.

Notes:
Only works for Amazon pages where price is visible without login.
Regex is used to clean the price string.