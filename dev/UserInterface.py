import Tkinter as tk
from Client import *

class UserInterface:

    def __init__(self):
	self.button_list = list()

    def create_buttons(self, parent_widget):
        ''' Create 3x3 button grid'''
	row_value = 0
	column_value = 0

	for i in range(1,10):
	    button = tk.Button(parent_widget, text=i, width=10, height=5, bg='white')
	    button.bind("<Button-1>", self.button_handler)
	    button.grid(row = row_value, column = column_value, pady=5, padx=5)
				
	    if i%3 == 0:
                row_value = row_value + 1
		column_value = - 1

	    column_value = column_value + 1
	    self.button_list.append(button)

    def button_handler(self, event):
	if self.clientObject.get_semaphore_status():
	    event.widget['background'] = self.clientObject.get_color()
	    event.widget['state'] = 'disabled'
            self.clientObject.send_to_server(event.widget.cget("text"), 0)
    	    self.clientObject.release_lock()

    def reset(self, event):
    	self.create_buttons(self.button_frame)
   
    def main(self):
        main_window = tk.Tk()
    	#Add title, default geometry and background color
   
    	main_window.title("TicTacToe")
    	main_window.geometry("550x500")
	main_window.configure(background='DimGrey')
    
    	heading = tk.Label(main_window, text="Tic Tac Toe", font=('Helvetica',24,'bold'), bg='DimGrey')
    	heading.grid(row=0, column=1)
 
    	#Adding score labels
    	title_frame = tk.Frame(main_window, bg='DimGrey')
    	my_score = tk.Label(title_frame, text = 'Your score : 0 pts', bg='DimGrey')
    	my_score.grid(row=0, column=0)

    	opp_score = tk.Label(title_frame, text = 'Opp score : 0 pts', bg='DimGrey')
    	opp_score.grid(row=1, column=0)

    	self.connect_status = tk.Label(title_frame, text = '(not connected)', font=('Helvetica',11,'italic'), bg='DimGrey')
    	self.connect_status.grid(row=2, column=0)

    	title_frame.grid(row=1, column=0)

    	#Adding buttons to the grid
    	self.button_frame = tk.Frame(main_window)
    	self.create_buttons(self.button_frame)
    	self.button_frame.grid(row=2, column=1)
    	
    	reset_button = tk.Button(main_window, text="Reset", width=5)
    	reset_button.bind("<Button-1>", self.reset)
    	
    	reset_button.grid(row=3, column = 1, pady=5)
	
	self.turn_to_play = tk.Label(main_window, text = 'waiting', bg='DimGrey')
    	self.turn_to_play.grid(row=4, column=0)

	self.clientObject = Client(self.connect_status, my_score, opp_score, self.button_list, self.turn_to_play)

    	main_window.mainloop()

if __name__ == '__main__':
    u_i = UserInterface()
    u_i.main()
