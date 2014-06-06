import random
import thread
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
client_sock = None
PORT_NUMBER_1 = 10028
PORT_NUMBER_2 = 10029
connection = 0
WAIT = None
# board = [['.','.','.','.'],
		 # ['.','.','.','.'],
		 # ['.','.','.','.'],
		 # ['.','.','.','.']]

board = [['.',2,4,2],
		 [16,4,64,4],
		 [2,32,128,16],
		 [16,64,2,32]]
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

def copyBoard():
	copy = []
	for i in range(width):
		temp = []
		for j in range(height):
			temp.append(board[i][j])
		copy.append(temp)
	return copy

def makeMove(moveNum):
	global newTiles
	global WAIT
	global board
	moveMade = False

	# copy = copyBoard()
	if moveNum == LEFT:
		print "moving left"
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
		print "moving right"
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
		print "moving up"
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
		print "moving down"
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

def getAdjacentTiles(i,j):
	tiles = []
	if i+1 < height:
		tiles.append((i+1,j))
	if j+1 < width:
		tiles.append((i,j+1))
	if i-1 >= 0:
		tiles.append((i-1,j))
	if j-1 >= 0:
		tiles.append((i,j-1))
	return tiles

def sendState(pkt_type):
	print "SENDING NEW_TILES"
	client_sock.sendall("NEW_TILES")
	client_sock.sendall(pickle.dumps(newTiles))
	time.sleep(1)
	print "SENDING %s"%pkt_type
	client_sock.sendall(pkt_type)
	client_sock.sendall(pickle.dumps(board))

def clientStart():
	# Create a TCP/IP socket
	global client_sock
	client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	if int(sys.argv[1]) == 1:
		server_address = ('localhost', PORT_NUMBER_1)
	else:
		server_address = ('localhost', PORT_NUMBER_2)
	print >>sys.stderr, 'connecting to %s port %s' % server_address
	client_sock.connect(server_address)

def containsBlanks():
	for i in range(width):
		for j in range(height):
			if board[i][j] == '.':
				return True
	return False

def hasWon():
	for i in range(width):
		for j in range(height):
			if board[i][j] == 2048:
				return True
	return False

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

def server():
	global connection
	global board
	global newTiles
	global WAIT
	# Create a TCP/IP socket
	server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# Bind the socket to the port
	if int(sys.argv[1]) == 1:
		server_address = ('localhost', PORT_NUMBER_2)
	else:
		server_address = ('localhost', PORT_NUMBER_1)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	server_sock.bind(server_address)
	# Listen for incoming connections
	server_sock.listen(1)

	while True:
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
	            		print "STATE: %s"%state
	            	else:
		            	if state == "BOARD":
		            		board = pickle.loads(data)
		            		print colored("The other player has made a move",'red')
		            		printBoard()
		            		print "received board"
		            		WAIT = False
		            	elif state == "INITIAL":
		            		board = pickle.loads(data)
		            		print "received initial"
		            		printBoard()
		            	elif state == "NEW_TILES":
		            		newTiles = pickle.loads(data)
		            		print newTiles
		            		print "received new tiles"
		            	state = "NORMAL"
		            	print "STATE: NORMAL"
	            else:
	                break
	    except KeyboardInterrupt:
	    	print "Closed connection on server"
	    	connection.close()
	    	break     
	    finally:
	        # Clean up the connection
	    	print "Closed connection on server"
	        connection.close()
	        break

def run():
	global WAIT
	# if len(sys.argv) != 2:
	# 	print "usage: python collaborative2048.py [1/2]"
	# 	exit(0)
	# thread.start_new_thread(server,())
	# time.sleep(5)
	# clientStart()

	# if int(sys.argv[1]) == 1:
	# generateNewTile()
	# generateNewTile()
		# sendState("INITIAL")
	printBoard()
	# print isOver()
		# WAIT = False
	# else:
		# WAIT = True

	with raw_mode(sys.stdin):
		try:
			while not isOver():
				while(1):
					print colored("Make a move: ",'red')
					move = sys.stdin.read(1)
					# print "SELECTED: %s"%move
	                # if not move or move == chr(4):
	                #     break
					# print "wait is %s"%WAIT
					# if WAIT == True:
					# 	print "Waiting for other player to make move..."
					# 	break
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
				if not isValidMove:
					print colored("You can't move in that direction!",'red')
				elif containsBlanks():
					generateNewTile()
				# printBoard()
				# sys.stdout.write("is over")
				# print isOver()
				if isOver():
					# print "breaking"
					break
				# if WAIT == False:
					# sendState("BOARD")
				printBoard()
					# WAIT = True
			printBoard()
			# sys.stdout.write("has won")
			# print hasWon()
			if hasWon():
				print colored("You won!",'red')
			else:
				print colored("You lost!",'red')
		except KeyboardInterrupt:
			# closeClient()
			pass
		finally:
			# closeClient()
			pass

run()
