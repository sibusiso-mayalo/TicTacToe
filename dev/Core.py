class Core:

    def __init__(self):
        self.myScore = 0
        self.history = list()
        self.winningsTable = self.populate_winnings()

    def get_play(self, position):
	self.add_to_history(int(position))
	return self.validate_win()

    def add_to_history(self, position):
        '''Add the position to the list of previously played positions (history).
           Sort the list using merge-sort'''
        self.history.append(position)
	self.history.sort()
	#print "History : ", self.history

    def populate_winnings(self):
        ''' Pre-computed winning combinations'''
	dictionary = 	{6:(1,2,3),
                         12:(1,4,7),
                         15:[(1,5,9),(2,5,8),(3,5,7),(4,5,6)],
                         18:(3,6,9),
                         24:(7,8,9)}      
	return dictionary

    def validate_win(self):
	'''From the list of played positions, check if there is a winning combination '''
        win = False
	tripple_sum = 0

	if len(self.history) > 2:
	    for index in range(0, len(self.history)-2):
		if (index+2) <= len(self.history):
		    	    
		    tripple_from_list = (self.history[index], self.history[index+1], self.history[index+2])
		    tripple_sum = self.history[index] + self.history[index+1] + self.history[index+2]
		    
		    if tripple_sum == 15:
			win  = self.validate_fifteen(tripple_from_list, tripple_sum)
		    else:
		        if self.populate_winnings().get(tripple_sum) != None:
			    winningCombo  = self.populate_winnings().get(tripple_sum) 
			    if winningCombo == tripple_from_list:
			        win = True
        	    if win:
            		self.myScore += tripple_sum
	    		self.reset_game()
        return win

    def validate_fifteen(self, list_to_test, summ):
	'''Check if the combination of numbers adding up to fifteen is a win'''
	win = False

	first_element = list_to_test[0]
	winningCombo = self.populate_winnings().get(summ)[first_element-1]

	if winningCombo == list_to_test:
	    win = True
	return win

    def get_score(self):
	'''Return score '''
	return self.myScore
		    
    def reset_game(self):
	'''Clear all the positions played previously by the pla '''
        self.history = list()
