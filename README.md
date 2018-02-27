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

## Stripe Information

The integration with stripe is using the test keys -- they therefore accept the following test credit card values.

*valid cc* 242 4242 4242 4242

*disupte cc* 4000 0000 0000 0259

*disputed cc as inquiry* 4000 0000 0000 1976

For more information on these test cards please see: https://stripe.com/docs/testing#disputes & https://stripe.com/docs/testing#cards.