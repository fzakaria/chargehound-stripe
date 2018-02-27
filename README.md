# ChargeHound <3 Stripe

This is a sample application showing integration of [Stripe](https://stripe.com) with
[ChargeHound](https://www.chargehound.com).

> You can view a live version of this site running https://chargehound-demo-fzakaria.herokuapp.com. Please note however that it uses an in-memory database.

This is a very minimal [flask](flask.pocoo.org) application. There are many production best practices that have been ommitted in order to provide clarity and simplicity in demonstrating the integration.

To get started all you have to do is `make run`.
This will start a *development server* running on your local host on port *5000*.

```
export STRIPE_PUBLISHABLE_KEY=pk_test_yoursecret
export STRIPE_SECRET_KEY=sk_test_yoursecret
export CHARGEHOUND_SECRET_KEY=test_yoursecret
make run
```

The following routes are expose:

**/** The base path, where you can see some albums and purchase them.

**/charge/<song_slug>** The callback/webhook for stripe to initiate the charge after they've validated the credit card.

**/chargehound/dispute** The callback/webhook for chargehound after they've discovered a dispute from their Stripe integration.

**/admin/charges** An admin view that just returns the current in-memory charges processed.

## Stripe Information

The integration with stripe is using the test keys -- they therefore accept the following test credit card values.

*valid cc* 242 4242 4242 4242

*disupte cc* 4000 0000 0000 0259

*disputed cc as inquiry* 4000 0000 0000 1976

For more information on these test cards please see: https://stripe.com/docs/testing#disputes & https://stripe.com/docs/testing#cards.

You can read also about more about the [ChargeHound+Stripe Integration](https://testing-chargehound-pr-1027.herokuapp.com/docs?template=song-purchase&processor=stripe).

## Heroku Setup

In order to run on heroku the following were set:

```
CHARGEHOUND_SECRET_KEY: test_your_key
CHARGE_HOUND_HOST:      test-api.chargehound.com
FLASK_APP:              chargehound-demo.py
FLASK_DEBUG:            1
PREFERRED_URL_SCHEME:   https
SERVER_NAME:            chargehound-demo-fzakaria.herokuapp.com
STRIPE_PUBLISHABLE_KEY: pk_test_your_key
STRIPE_SECRET_KEY:      sk_test_your_key
WEB_CONCURRENCY:        1
```

The one *gotcha* is that **WEB_CONCURRENCY** should be 1 since we are storing data in memory only -- otherwise gunicorn spawns multiple processes and they don't share data. This not a problem when storing data in a separate process like a database.