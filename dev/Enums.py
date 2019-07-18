class Enums:

    forward_to_server = ["SEN_PLY", "SEN_RLS"]
    forward_to_client = ["RCV_PLY", "RCV_CSS", "RCV_RST", "RCV_SUD","RCV_LAQ"]


    '''Explanantion of the enums:
       SEN_PLY - Send Play : Send the action(position) of the client to the server and subsequently to the opponent
       SEN_RLS - Send Release: Informs the server that the client wishes to release the lock as they have played a move sucesssfully

       RCV_PLY - Receive Play : Updates the client about the action of the opponent
       RCV_CSS - Receive Connection Status : Returns the pair ID to the client
       RCV_SUD - Receive Score Update : Update score label of the opponent when [user/you] have won
       RCV_LAQ - Receive Lock Acquired Update: Inform a client that it has acquired the lock and only it can make a move
  
    '''
