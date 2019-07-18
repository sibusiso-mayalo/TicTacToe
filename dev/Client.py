import pickle as pickle
from socket import *
from Enums import *
import threading

class Client:

    def __init__(self, connectWidget, myScore, oppScore, grid, turn):
	self.statusWidget = connectWidget
	self.myScore = myScore
	self.oppScore = oppScore

	self.color = 'DarkViolet'
	self.opp_color = 'Green'
	self.grid = grid

	self.clientConnection = self.connect_to_server()

	server_response_handler = threading.Thread(target=self.handle_response_from_server)
	server_response_handler.daemon = True
	server_response_handler.start()

	self.turn_to_play = turn
	self.semaphore = False
	
    def connect_to_server(self):
        '''This functions connect the client to the server. It binds client socket to port 3000 '''
        tempClient = ''
        try:
            tempClient = socket(AF_INET, SOCK_STREAM)
            tempClient.connect(('127.0.0.1', 3000))
	    print "Connection to server successful."

        except IOError as err:
            print("Client connection to server error:\n", err)
        return tempClient

    def send_to_server(self, data, enumID):
        '''This function sends data to the server '''
        try:
            protocol = Enums.forward_to_server[enumID] + str(data)
            compressed = pickle.dumps(protocol, pickle.HIGHEST_PROTOCOL)
            self.clientConnection.sendall(compressed)
        except IOError as error:
            print ("Position could not be sent to server:\n", error)

    def get_server_response(self):
        ''' This functions gets server responses to the client '''
        messageStream = self.clientConnection.recv(4096)
        messageStream = pickle.loads(messageStream)
        return messageStream

    def release_lock(self):
	self.send_to_server("", 1)
	self.turn_to_play['text'] = 'Opponent\'s turn'
	self.semaphore = False
	print 'released lock'

    def handle_response_from_server(self):
	''' Handle different responses from the server '''
	while True:
	    response = self.get_server_response()
	    print response
	    
	    if response[:7] == Enums.forward_to_client[0]: 
	        #get the position the opponent has played and update UI
	        position = response[7:]
	        button_pressed = self.grid[int(position) - 1]
	        button_pressed['background'] = str(self.opp_color)
                button_pressed['state'] = 'disabled'

	    elif response[:7] == Enums.forward_to_client[1]: 
	        #user has been paired to an opponent UI update
	        self.statusWidget['text'] = 'connected to an opponent' 
	
	    elif response[:7] == Enums.forward_to_client[2]: 
		#Results after each position has been played
		if response[7:].split(',')[0] == 'True':
		    myScore = response[7:].split(',')[1]
	            self.myScore['text'] = 'Your score : ' + myScore+ ' pts'
	            print "winner! "

	    elif response[:7] == Enums.forward_to_client[3]:
		oppScore = response[7:] 
		self.oppScore['text'] = 'Opp score : ' + oppScore+ ' pts'
	    
	    elif response[:7] == Enums.forward_to_client[4]:
	    	self.semaphore = True
		self.turn_to_play['text'] = 'Your turn to play'
		print 'acquired lock'
	    	
    def get_color(self):
    	return self.color

    def get_semaphore_status(self):
	return self.semaphore
	
    
