from flask import render_template, url_for, request, abort, Response
from app import app,stripe_keys
from app.db import all_songs, find_song_by_slug, insert_charge, find_slug_by_charge
import stripe
import chargehound
"""
The main routes this app supports:

/ The base path, where you can see some albums and purchase them.
/charge/<song_slug> The callback for stripe to initiate the charge after they've validated the credit card.
/chargehound/dispute The callback/webhook for chargehound after they've discovered a dispute from their Stripe integration.
/admin/charges An admin view that just returns the current in-memory charges processed.
"""

@app.context_processor
def inject_constants():
	"""Inject a set of constants into the processor"""
	return dict(stripe_pub_key=stripe_keys['publishable_key'])

@app.route('/charge/<song_slug>', methods=['POST'])
def charge(song_slug : str):
	"""This is a callback after stripe has verified the customers payment information.
	   They provide us with a token which we can then perform a charge -- which has already been validated.
	   We store the returned charge_id though in the case of any future disputes"""
	song = find_song_by_slug(song_slug)
	if song is None:
		abort(404)

	customer = stripe.Customer.create(
		email=request.form['stripeEmail'],
		source=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
		customer=customer.id,
		#amount in cents
		amount=int(song['price'] * 100),
		currency='usd',
		description='Song Purchase'
	)

	# record the charge for potential disputes later
	# we only reecord the id and slug -- this is equivalent to a
	# join table
	insert_charge(charge.id, song_slug)

	return render_template('charge.html', amount=song['price'], email=customer.email)

@app.route('/chargehound/dispute', methods=['POST'])
def dispute():
	"""Chargehound will call this method once it has polled a dispute from Stripe.
	   (Stripe integration must be setup with your account)
	   Chargehound helps resolve disputes by providing a programmatic way to respond to disputes. 
	   Using the dispute_id we lookup the charge and find the evidence needed to fight the dispute!"""

	# Retrieve the request's body and parse it as JSON
	event_json = request.json

	# 1) Handle the dispute.created event
	if event_json['type'] == 'dispute.created':
		# The id of the dispute.
		# The id used by your payment processor is also used by Chargehound.
		dispute_id = event_json['dispute']
		# Fetch the dispute from Stripe
		dispute = stripe.Dispute.retrieve(dispute_id)
		charge_id = dispute.charge
		app.logger.info('Received a dispute with id:%s and charge_id:%s', dispute_id, charge_id)

		# 2) Collect your evidence to send to Chargehound.
		song_slug = find_slug_by_charge(charge_id)
		song = find_song_by_slug(song_slug)

		# 3) POST your evidence to the Chargehound API to respond
		chargehound.Disputes.submit(dispute_id,
			template = 'song-purchase',
			fields = {
				# purchase url needs to have the full fqdn of your server
				'purchase_url': url_for('charge', song_slug=song_slug, _external=True),
				'song_artist': song['artist'],
				'song_name': song['title'],
				# max 25 characters
				'charge_statement_descriptor': "chargehound dispute."
			})
	
	return Response(status=200, mimetype='application/json')

@app.route('/')
@app.route('/songs')
def index():
	"""This is the main home index"""

	# add the song url
	songs = all_songs()
	for song in songs:
		song['image_url'] = url_for('static', filename="img/{image_name}".format(image_name=song['image_name']))

	return render_template('index.html', songs=songs)
