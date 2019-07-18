import pickle as pickle
from socket import *
import threading
from Enums import *
from Core import *

class Server:

    def __init__(self):
        #Bind socket
        self.serverSock = socket(AF_INET, SOCK_STREAM)
        self.serverSock.bind(("127.0.0.1", 3000))
        self.serverSock.listen(5)
        
        self.onlineClients = dict()
	self.coreObjects = dict()
	self.locks = dict()
	self.waiting_to_pair = list()

    	print ("Setup finished.")

    def listen_for_connections(self):
        ''' Listen for incoming requests '''
        while True:
            print("Listening for connections..")
            client, address = self.serverSock.accept()

            if len(self.waiting_to_pair) < 1:
                self.waiting_to_pair.append(client)
                print ("New client connection ", address)
	    	
	    else:
                #Connect a client to an opponent
		print ("New client connection ", address)

	        self.onlineClients[client] = self.waiting_to_pair[0] 
		self.onlineClients[self.waiting_to_pair[0]] = client
			
		self.coreObjects[client] = Core() 
		self.coreObjects[self.waiting_to_pair[0]]= Core()

		semaphore = threading.BoundedSemaphore(value = 1)
		self.locks[client] = semaphore
		self.locks[self.waiting_to_pair[0]] = semaphore
		self.get_lock(client)
			
	        self.send_to_client(Enums.forward_to_client[1] + str(True), client)
		self.send_to_client(Enums.forward_to_client[1] + str(True), self.waiting_to_pair[0])
		self.send_to_client(Enums.forward_to_client[4] , client)

		#Threads to handle requests from clients
		player1_handler = threading.Thread(target = self.handle_client_request, args=('play request',client))
		player1_handler.daemon = True

		player2_handler = threading.Thread(target = self.handle_client_request, args=('play request',self.onlineClients[client]))
		player2_handler.daemon = True
		
		player1_handler.start()
		player2_handler.start()

		self.waiting_to_pair.remove(self.waiting_to_pair[0] )
		print "Sucessfully paired two players."

    def handle_client_request(self, name, clientSockt):
    	while True:
            message = self.receiveMessage(clientSockt, 4096)
	    print 'Received ' + message[:len(message)] + ' from ', clientSockt 
          		
	    if message[:len(message) - 1] == Enums.forward_to_server[0]:
		self.handled_a_played_position(message, clientSockt)
	
	    elif message[:len(message)] == Enums.forward_to_server[1]:
		self.locks[clientSockt].release()
		self.get_lock(self.onlineClients[clientSockt])

    def get_lock(self, clientSock):
	print 'attempt by ', clientSock
	if self.locks[clientSock].acquire():
            self.send_to_client(Enums.forward_to_client[4], clientSock) #inform client they have acquired the lock
	    print 'acquired by', clientSock
		
    def handled_a_played_position(self, message, clientSockt):
	 '''Client has played a position '''
	 position = message[len(message) - 1:]
	 myCoreObject = self.coreObjects.get(clientSockt)
	 results = myCoreObject.get_play(position) #True/False

	 if results:
	     myScore = self.get_score(myCoreObject)		    
	     concat = str(results) +','+ str(myScore) 
		         
	     #send the position played + score update to the opponent to be disabled on their UI
	     self.send_to_client(Enums.forward_to_client[0] + str(position), self.onlineClients[clientSockt] )
	     self.send_to_client(Enums.forward_to_client[3] + str(myScore), self.onlineClients[clientSockt] )

	     self.send_to_client(Enums.forward_to_client[2] + concat, clientSockt) #send results to the player (you)
	 else:
	     self.send_to_client(Enums.forward_to_client[0] + str(position), self.onlineClients.get(clientSockt))	
		
    def get_score(self, myObject):
	myScore = myObject.get_score()
	return myScore

    def receiveMessage(self, clientSocket, size):
        messageStream = clientSocket.recv(size)
        messageStream = pickle.loads(messageStream)
        return messageStream

    def send_to_client(self, raw_data, clientSocket):
        '''This function sends data to a client '''
        try:
            data = pickle.dumps(raw_data, pickle.HIGHEST_PROTOCOL)
            clientSocket.sendall(data)
        except IOError as error:
            print ("Position could not be sent to client:\n", error)

if __name__ == '__main__':
    server = Server()
    server.listen_for_connections()
