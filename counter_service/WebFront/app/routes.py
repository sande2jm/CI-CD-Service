
# coding=utf-8

from flask import render_template, flash, redirect, session, url_for, request, g, Markup, current_app
from app import app
from .CounterService import CounterService
from flask import jsonify

service = CounterService()

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

@app.route('/setCounter', methods=["POST"])
def setCounter():
	value = request.args.get('value')
	
	service.setCounter(value)
	response = app.response_class(
        None,
        status=200,
        mimetype='application/json'
    )
	return response











