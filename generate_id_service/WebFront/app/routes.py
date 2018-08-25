
# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup, current_app
from app import app
from .GenerateIdService import GenerateIdService
from flask import jsonify

service = GenerateIdService()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/getCounter', methods=["GET"])
def getCounter():
	return jsonify(service.getCounter())

@app.route('/increment', methods=["POST", "GET"])
def increment():
	service.increment()
	response = app.response_class(
        None,
        status=200,
        mimetype='application/json'
    )
	return response

@app.route('/getId', methods=["GET", "POST"])
def getId():
	name = request.args.get('name')
	response = service.getId(name)
	return response










