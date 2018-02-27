"""
Select admin routes to help introspect the data
"""
from flask import jsonify
from app import app
from app.db import all_charges

@app.route('/admin/charges')
def admin_charges():
	return jsonify(all_charges())
	