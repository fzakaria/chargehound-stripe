from flask import render_template, url_for
from app import app
from app.db import SONGS_DB

@app.route('/')
@app.route('/songs')
def index():
	songs = list(SONGS_DB) # create a copy
	# add the song url
	for song in songs:
		song['image_url'] = url_for('static', filename="img/{image_name}".format(image_name=song['image_name']))

	return render_template('index.html', songs=songs)
