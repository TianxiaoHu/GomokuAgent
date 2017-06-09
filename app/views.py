import os
from flask import render_template, request, jsonify, Response
from app import app
from AI1 import strategy


@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/_start', methods=['GET'])
def start():
	return 'Success'


@app.route('/_player_set', methods=['GET'])
def player_set():
	position = request.args.get('position', '')
	board = request.args.get('board')
	board = eval(board)
	player_0 = set()
	player_1 = set()
	for i in range(15):
		for j in range(15):
			if board[i][j] == 2:
				player_0.add((i, j))
			elif board[i][j] == 1:
				player_1.add((i, j))
	board = (player_0, player_1)
	print board
	print position
	stone = tuple(int(i) for i in position.split(','))
	action = (stone[0], stone[1])
	state = (board, position, 1, 15)
	ai_action = strategy(state)
	print ai_action
	winner = None
	# next_action, winner = game.web_play(action)
	if isinstance(ai_action, tuple):
		stone = (ai_action[0], ai_action[1])
	else:
		stone = None
	return jsonify(next_move=stone, winner=winner)


@app.route("/_qrcode")
def qrcode():
	return render_template('contact.html')
