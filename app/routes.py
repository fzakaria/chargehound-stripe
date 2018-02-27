from flask import render_template, url_for, request, abort
from app import app,stripe_keys
from app.db import all_songs, find_song_by_slug
import stripe


@app.context_processor
def inject_constants():
	"""Inject a set of constants into the processor"""
	return dict(stripe_pub_key=stripe_keys['publishable_key'])

@app.route('/charge/<song_slug>', methods=['POST'])
def charge(song_slug : str):
	song = find_song_by_slug(song_slug)
	if song is None:
		abort(404)

	customer = stripe.Customer.create(
		email=request.form['stripeEmail'],
		source=request.form['stripeToken']
	)

	charge = stripe.Charge.create(
		customer=customer.id,
		amount=int(song['price'] * 100), #amount in cents
		currency='usd',
		description='Song Purchase'
	)

	return render_template('charge.html', amount=charge.amount, email=customer.email)

@app.route('/')
@app.route('/songs')
def index():
	# add the song url
	songs = all_songs()
	for song in songs:
		song['image_url'] = url_for('static', filename="img/{image_name}".format(image_name=song['image_name']))

	return render_template('index.html', songs=songs)
