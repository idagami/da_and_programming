# imp: on first run always drops error 'flask not installed'. just hit RUN again

The project imitates a live online store (e-commerce). 
Admin (user_id = 1) added as first user so that some products can be uploaded onto the store page.
I used Stripe API to handle the payments. 
I used fake credit card number (recommended by Stripe: 4242424242424242 exp date: any from future, CVC: 123).
The payment "fake" went through, the order confirmation provided, the order saved in My orders tab.
Confirmation email ent to user.

For a real payment, webhook must be used. More: https://docs.stripe.com/stripe-cli/install?install-method=windows
