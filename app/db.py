"""
This is a in-memory database. You probably want to replace this with some actual RDBMS solution or at a minimum
sqlite.
"""

MEMORY = [

	{
		"title": "Anti",
		"slug" : "rihanna-anti",
		"description": """Anti is the eighth studio album by Barbadian singer Rihanna.
						It was released on January 27, 2016, through Westbury Road and Roc Nation.""",
		"image_name": "Rihanna_-_Anti.png",
		"price" : 10.99
	},

	{
		"title": "Neck of the Woods",
		"slug" : "neck-of-the-woods",
		"description": """Neck of the Woods is the third studio album by Los Angeles alternative rock band Silversun Pickups.
						  The album was produced by Jacknife Lee (R.E.M., Bloc Party) and was released on May 8, 2012
						  through independent label Dangerbird Records.""",
		"image_name": "Silversun_Pickups_neckofthewoods.jpg",
		"price" : 11.99

	},	


];

def all_songs() -> list:
	"""Get all songs. Returns a copy."""
	return list(MEMORY)

def find_song_by_slug(slug : str) -> dict:
	"""Find a song by slug. Returns none if it cannot find any."""
	for song in MEMORY:
		if song['slug'] == slug:
			return song
	return None