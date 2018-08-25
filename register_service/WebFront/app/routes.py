
# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup, current_app
from app import app
from .RegisterService import RegisterService
from flask import jsonify

service = RegisterService()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/registerUser', methods=["POST", "GET"])
def registerUser():
	uid = request.args.get('uid')
	name = request.args.get('name')
	service.registerUser(uid, name)
	response = app.response_class(
        None,
        status=200,
        mimetype='application/json'
    )
	return response










