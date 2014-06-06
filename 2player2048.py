import random
import thread
import threading
import socket
import sys
import termios
import contextlib
import time
import pickle
from termcolor import colored

LEFT = 1
RIGHT = 2
UP = 3
DOWN = 4
BLANK = '.'
mainShutdown = False
client_sock = None
server_sock = None
PORT_NUMBER_1 = 10074
PORT_NUMBER_2 = 10075
connection = 0
WAIT = None
serverExit = False
# board = [['.',2,4,2],
# 		 [16,4,64,4],
# 		 [2,32,128,16],
# 		 [16,64,2,32]]
board = [['.','.','.','.'],
		 ['.','.','.','.'],
		 ['.','.','.','.'],
		 ['.','.','.','.']]
height = 4
width = 4
newTiles = []

def printBoard():
	global newTiles
	print
	for i in range(height):
		for j in range(width):
			if type(board[i][j]) is int:
				if (i,j) in newTiles:
					sys.stdout.write('{:>14}'.format(colored(board[i][j],'green')))
				else:
					sys.stdout.write('{:>14}'.format(colored(board[i][j],'red')))
			else:
				sys.stdout.write('{:>5}'.format(board[i][j]))
		print
	print
	newTiles = []

def generateNewTile():
	global newTiles
	blank = getBlankCells()
	coords = blank[random.randint(0,len(blank)-1)]
	if random.random() <= 0.5:
		board[coords[0]][coords[1]] = 2
	else:
		board[coords[0]][coords[1]] = 4
	newTiles.append((coords[0],coords[1]))

def getBlankCells():
	blank = []
	for i in range(height):
		for j in range(width):
			if board[i][j] == BLANK:
				blank.append((i,j))
	return blank

def makeMove(moveNum):
	global newTiles
	global WAIT
	global board
	moveMade = False

	# copy = copyBoard()
	if moveNum == LEFT:
		print "Moving left"
		for i in range(height):
			for j in range(1,width):
				for k in range(0,j):
					if board[i][j] != BLANK and board[i][k] == BLANK:
						board[i][k] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;
		for i in range(height):
			for j in range(1,width):
				if board[i][j] != BLANK and board[i][j-1] == board[i][j]:
					board[i][j-1] *= 2;
					newTiles.append((i,k))
					board[i][j] = BLANK
					moveMade = True
					break;
		for i in range(height):
			for j in range(1,width):
				for k in range(0,j):
					if board[i][j] != BLANK and board[i][k] == BLANK:
						board[i][k] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;

	elif moveNum == RIGHT:
		print "Moving right"
		for i in range(height):
			for j in range(width-1,-1,-1):
				for k in range(width-1,j,-1):
					if board[i][j] != BLANK and board[i][k] == BLANK:
						board[i][k] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;
		for i in range(height):
			for j in range(width-2,-1,-1):
				if board[i][j] != BLANK and board[i][j+1] == board[i][j]:
					board[i][j+1] *= 2;
					newTiles.append((i,k))
					board[i][j] = BLANK
					moveMade = True
					# break;
		for i in range(height):
			for j in range(width-1,-1,-1):
				for k in range(width-1,j,-1):
					if board[i][j] != BLANK and board[i][k] == BLANK:
						board[i][k] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;
	elif moveNum == UP:
		print "Moving up"
		for i in range(1,height):
			for j in range(width):
				for k in range(0,i):
					if board[i][j] != BLANK and board[k][j] == BLANK:
						board[k][j] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						# printBoard()
						break;
		for i in range(1,height):
			for j in range(width):
					if board[i][j] != BLANK and board[i-1][j] == board[i][j]:
						# print (i,j,k)
						board[i-1][j] *= 2;
						newTiles.append((i-1,j))
						board[i][j] = BLANK
						moveMade = True
						# break;
		for i in range(1,height):
			for j in range(width):
				for k in range(0,i):
					if board[i][j] != BLANK and board[k][j] == BLANK:
						if (i,j) in newTiles:
							newTiles.remove((i,j))
							newTiles.append((k,j))
						board[k][j] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						# printBoard()
						break;
	elif moveNum == DOWN:
		print "Moving down"
		for i in range(height-1,-1,-1):
			for j in range(width):
				for k in range(height-1,i,-1):
					# print (i,j,k)
					if board[i][j] != BLANK and board[k][j] == BLANK:
						board[k][j] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;
		# printBoard()
		for i in range(height-2,-1,-1):
			for j in range(width):
				# print (i,j,k)
				if board[i][j] != BLANK and board[i+1][j] == board[i][j]:
					board[i+1][j] *= 2;
					newTiles.append((i+1,j))
					board[i][j] = BLANK
					moveMade = True
					# break;
		for i in range(height-1,-1,-1):
			for j in range(width):
				for k in range(height-1,i,-1):
					# print (i,j,k)
					if board[i][j] != BLANK and board[k][j] == BLANK:
						if (i,j) in newTiles:
							newTiles.remove((i,j))
							newTiles.append((k,j))
						board[k][j] = board[i][j]
						board[i][j] = BLANK
						moveMade = True
						break;
	return moveMade

def isOver():
	# print "isover"
	for i in range(height):
		for j in range(width):
			# print (i,j)
			tiles = getAdjacentTiles(i,j)
			# print tiles
			for tile in tiles:
				if board[tile[0]][tile[1]] == board[i][j]:
					# sys.stdout.write("false")
					# print tile
					return False
	# print "contains blanks %s"%containsBlanks()
	return not containsBlanks()

def containsBlanks():
	for i in range(width):
		for j in range(height):
			if board[i][j] == '.':
				return True
	return False

def getAdjacentTiles(i,j):
	tiles = []
	if i+1 < height:
		tiles.append((i+1,j))
		if j+1 < width:
			tiles.append((i+1,j+1))
	else:
		tiles.append(i,j)
		if j+1 < width:
			tiles.append((i,j+1))
	return tiles

def sendState(pkt_type):
	# print "SENDING NEW_TILES"
	client_sock.sendall("NEW_TILES")
	client_sock.sendall(pickle.dumps(newTiles))
	time.sleep(1)
	# print "SENDING %s"%pkt_type
	client_sock.sendall(pkt_type)
	client_sock.sendall(pickle.dumps(board))

def clientStart():
	# Create a TCP/IP socket
	global client_sock
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Connect the socket to the port where the server is listening
	if int(sys.argv[1]) == 1:
		server_address = (sys.argv[2], PORT_NUMBER_1)
	else:
		server_address = (sys.argv[2], PORT_NUMBER_2)
	print >>sys.stderr, 'connecting to %s port %s' % server_address
	try:
		client_sock.connect(server_address)
	except:
		print "couldn't connect to peer"
		exit(0)

def hasWon():
	global board
	for i in range(width):
		for j in range(height):
			if board[i][j] == 2048:
				return True
	return False

def closeEverything(serverThread):
	global server_sock
	print "Closed connection on server"
	# connection.close()
	try:
		connection.shutdown(socket.SHUT_RD)
	except:
		pass
	print "waiting for server thread to end"
	serverThread.join()

	print "Closed connection on client"

	# client_sock.close()
	try:
		client_sock.shutdown(socket.SHUT_WR)
	except:
		pass
	print "Either you or the client disconnected"

def server():
	global serverExit
	global connection
	global board
	global newTiles
	global WAIT
	global server_sock
	# Create a TCP/IP socket
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	if int(sys.argv[1]) == 1:
		server_address = ('localhost', PORT_NUMBER_2)
	else:
		server_address = ('localhost', PORT_NUMBER_1)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_sock.bind(server_address)
	# Listen for incoming connections
	server_sock.listen(1)

	 # Wait for a connection
	print >>sys.stderr, 'waiting for a connection'
	connection, client_address = server_sock.accept()
	try:
		print >>sys.stderr, 'connection from', client_address
		state = "NORMAL"
		# Receive the data in small chunks and retransmit it
		while True:
			data = connection.recv(1000)
			# print >>sys.stderr, 'received "%s"' % data
			if data:
				if data == "BOARD" or data == "INITIAL" or data == "NEW_TILES":
					state = data
					# print "STATE: %s"%state
				# elif data == "FIN":
					# break
				else:
					if state == "BOARD":
						board = pickle.loads(data)
						print colored("The other player has made a move",'red')
						printBoard()
						# print "received board"
						WAIT = False
					elif state == "INITIAL":
						board = pickle.loads(data)
						# print "received initial"
						printBoard()
					elif state == "NEW_TILES":
						newTiles = pickle.loads(data)
						# print newTiles
						# print "received new tiles"
					state = "NORMAL"
					# print "STATE: NORMAL"
			else:
				break
	except KeyboardInterrupt:
		pass
	# 	print "server interrupt"
	# 	closeEverything()
		# print "Closed connection on server"
 	 	# connection.close()
 		# break
	finally:
		print "server finally"
 		# closeEverything()
		# Clean up the connection
		# print "Closed connection on server"
		# connection.close()
		serverExit = True
		if not mainShutdown:
			thread.interrupt_main()
		# thread.exit()
		# break
	print "server thread ended"

def run():
	global mainShutdown
	global WAIT
	if len(sys.argv) != 3:
		print "usage: python collaborative2048.py [1/2] [IP_ADDRESS]"
		exit(0)
	serverThread = threading.Thread(target=server,args=tuple())
	serverThread.daemon = True
	serverThread.start()
	try:
		time.sleep(5)
	except:
		pass
	clientStart()

	if int(sys.argv[1]) == 1:
		generateNewTile()
		generateNewTile()
		sendState("INITIAL")
		printBoard()
		WAIT = False
	else:
		WAIT = True
	thread.start_new_thread(logic,tuple())
	try:
		while 1:
			time.sleep(0.1) 
	except KeyboardInterrupt:
		pass
	finally:
		mainShutdown = True
		print "main finally"
		closeEverything(serverThread)
	print "exit main"

def logic():
	global WAIT
	madeMove = False
	with raw_mode(sys.stdin):
		# try:
		while not isOver() and not serverExit:
			while(1):
				if WAIT == True:
					print colored("Waiting for other player to make move...",'red')
					while(WAIT == True):
						if serverExit:
							break
					print "wait now false"
					break
				else:
					madeMove = True
					sys.stdout.write(colored("Make a move: ",'red'))
					move = sys.stdin.read(1)
					print move
					if move == 'i' or move == 'I' or move == 'w' or move == 'W':
						isValidMove = makeMove(UP)
						break
					elif move == 'j' or move == 'J' or move == 'a' or move == 'A':
						isValidMove = makeMove(LEFT)
						break
					elif move == 'k' or move == 'K' or move == 's' or move == 'S':
						isValidMove = makeMove(DOWN)
						break
					elif move == 'l' or move == 'L' or move == 'd' or move == 'D':
						isValidMove = makeMove(RIGHT)
						break
					else:
						print colored("Bad input",'red')
			if isOver():
				break
			if WAIT == False and madeMove:
				madeMove = False
				print "if wait is false"
				if not isValidMove:
					print colored("Moving in that direction doesn't move anything",'red')
				elif containsBlanks():
					generateNewTile()
					sendState("BOARD")
					WAIT = True
				printBoard()
		if not serverExit:
			printBoard()
			if hasWon():
				print colored("You both won!",'red')
			else:
				print colored("You both lost!",'red')
		# except KeyboardInterrupt:
		# 	pass
			# closeEverything()
			# print "main keyboard interrupt"
			# closeEverything()
		# finally:
			# print "main finally"
			# closeEverything()
		# 	print "finally"
		# 	closeClient()

@contextlib.contextmanager
def raw_mode(file):
    old_attrs = termios.tcgetattr(file.fileno())
    new_attrs = old_attrs[:]
    new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
    try:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
        yield
    finally:
        termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)
run()
