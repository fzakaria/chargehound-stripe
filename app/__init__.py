from flask import Flask
import stripe
import os
import chargehound

# We’re creating a dictionary with Stripe’s tokens, publishable_key and secret_key which are 
# being pulled out of the current environmental variables.
# We’re not hardcoding these keys, since it’s bad practice to put sensitive data into source control.
stripe_keys = {
  'secret_key': os.environ['STRIPE_SECRET_KEY'],
  'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY']
}

# Setup our chargehound client with the secret key that is fetched from environment variable
# we also change the host to the test API forcibly -- as this is a test application specifically
chargehound.api_key = os.environ['CHARGEHOUND_SECRET_KEY']
chargehound.host = 'https://test-api.chargehound.com'

stripe.api_key = stripe_keys['secret_key']

#  The __name__ variable passed to the Flask class is a Python predefined variable,
# which is set to the name of the module in which it is used
app = Flask(__name__)

from app import routes