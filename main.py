import tkinter as tk
from random import randint as rand
from tkinter import messagebox

def generate_mines(coord: tuple):
	'''Generates a grid object based on the first clicked co-ordinate.\n The coordinates in a (1,1) distance from them will not be given any mines.'''
	global ROWS, COLS, NUM_MINES, GRID, GAME_STATE
	#Generate a set of coordinates for mines.
	s = set()
	while len(s)!=NUM_MINES:
		mine = (rand(0, ROWS - 1), rand(0, COLS-1))
		if abs(mine[0]-coord[0])>1 and abs(mine[1]-coord[1])>1:
			s.add(mine)
	# print(s)	#Purely for debugging purposes. No cheats.
	#Assigning the buttons their values.
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)]['mine'] = (i,j) in s
			GRID[(i,j)]['opened'] = False
			GRID[(i,j)]['neighbour'] = [(I,J) for I in range(max(0,i-1), min(i+2,ROWS)) for J in range(max(0,j-1),min(j+2,COLS)) if (I,J) in s and (I!=i or J!=j)]
		# 	print(len( GRID[(i,j)]['neighbour']) if not GRID[(i,j)]['mine'] else 'F', end=" ")
		# print()
		#Needless to say, no cheats. Only debugging.
	#Changing the Game State
	GAME_STATE = 'STARTED'

def flag_switch():
	global FLAG_BUTTON, FLAG_STATE
	#Switch Flag State
	FLAG_STATE = not FLAG_STATE
	#Invert Colours
	FLAG_BUTTON['bg'] = "#000000" if FLAG_BUTTON['bg']=="#ffffff" else "#ffffff"
	FLAG_BUTTON['fg'] = "#000000" if FLAG_BUTTON['bg']=="#ffffff" else "#ffffff"

def count_neighbours(coord: tuple, arg: str):
	'''To count the neighbouring flagged/mine containing buttons.'''
	# Simplified: Checks the 8 surrounding coords for the argument's tautology (boolean value).
	return sum([GRID[(i,j)][arg] for i in range(max(0, coord[0]-1), min(coord[0]+2, ROWS)) for j in range(max(0, coord[1]-1), min(coord[1]+2, COLS)) if (i!=coord[0] or j!=coord[1])])


def click(coord: tuple): 
	'''Called on clicking a button. Depending on the button's attributes, different actions will happen.'''
	global GAME_STATE, FLAG_COUNTER, FLAGS_LABEL, NUM_LEFT, NUM_MINES
	#Checking if first-time initialization is needed.
	if GAME_STATE == 'FIRST-CLICK':
		generate_mines(coord)
	#Checking if the location is to be flagged or clicked.
	if FLAG_STATE:
		#Flagging the location.
		if GRID[coord]['opened']: pass
		else:
			FLAG_COUNTER += 1 if GRID[coord]['flagged'] else -1
			GRID[coord]['flagged'] = not GRID[coord]['flagged']
			GRID[coord]['button']['text'] = None if GRID[coord]['button']['text'] else 'F'
			FLAGS_LABEL['text'] = FLAG_COUNTER
		pass
	else:
		#Clicking the button. (Only if it's neither opened nor flagged.)
		if GRID[coord]['opened'] == False and GRID[coord]['flagged'] == False:
			GRID[coord]['opened'] = True
			if GRID[coord]['mine']:
				GRID[coord]['button']['text'] = 'X'
				GRID[coord]['button']['bg'] = '#ff0000'
				messagebox.showerror(title="You lose", message="You clicked a mine. Game Over.")
				start_game()
			else:
				GRID[coord]['button']['text'] = len(GRID[coord]['neighbour'])
			NUM_LEFT -= 1
		# The following line's code was used purely for debugging purposes. No cheats were used while playing the game for real.
		# print(coord, GRID[coord]['neighbour'], sep=':')
	
	if NUM_LEFT == NUM_MINES:
		messagebox.showinfo(title="Congratulations.", message="You have cleared the minefield. You win.")
		start_game()

def start_game():
	'''Generates grid for buttons.'''
	global ROWS, COLS, GRID, GAME_STATE, WINDOW, FLAG_BUTTON, FLAG_STATE, FLAG_COUNTER, FLAGS_LABEL, RESET_BUTTON, NUM_LEFT
	GRID.clear()
	#Removing older objects.
	for object in WINDOW.grid_slaves():
		del object
	#Setting the state of the game.
	GAME_STATE = 'FIRST-CLICK'
	FLAG_COUNTER = NUM_MINES
	NUM_LEFT = ROWS * COLS
	#Creating new objects.
	tk.Label(WINDOW, text='Minesweeper').grid(row=0, column=1, columnspan=COLS-3)
	FLAG_BUTTON = tk.Button(WINDOW, width=2, height=1, text='F', command=flag_switch, fg="#000000", bg="#ffffff"); FLAG_BUTTON.grid(row=0, column=0)
	FLAGS_LABEL = tk.Label(WINDOW, width=2, height=1, text=FLAG_COUNTER); FLAGS_LABEL.grid(row=0, column=COLS-2)
	RESET_BUTTON = tk.Button(WINDOW, width=2, height=1, text='R', command=start_game); RESET_BUTTON.grid(row=0, column=COLS-1)
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)] = {'opened': False, 'mine': False, 'neighbour': 0, 'flagged': False, 'button': eval('tk.Button(WINDOW, width=2, height=1, command=lambda: click(({},{})), text="")'.format(i,j))}	#Replacing this with an exec command, and then adding the button to this dict.
			GRID[(i,j)]['button'].grid(row=i+1, column=j)
	#To quote Heath Ledger's Joker: "And here we go."

GAME_STATE = 'FIRST-CLICK'	#Represents the Game's State at any instance.
FLAG_STATE = False			#Represents whether button click will open mine or plant a flag.
ROWS = 15					#Number of rows in the grid.
COLS = 12					#Number of columns in the grid
NUM_MINES = 24				#Number of mines in the grid
GRID = {}					#Dictionary with coordinate keys and dictionary values. Even the Buttons will be stored in the dicts.
WINDOW = tk.Tk()			#Tkinter Window Object. Where everything front-end will be there.
WINDOW.title("Minesweeper")	#Setting the title.
FLAGS_LABEL = None			#Tkinter Label Object: Will have 'Minesweeper' written on it.
FLAG_BUTTON = None			#Tkinter Button Object: Used to toggle flag option.
RESET_BUTTON = None			#Tkinter Button Object: Used to restart the game if needed.
NUM_LEFT = 0				#Represents the number of closed mines.
FLAG_COUNTER = 0			#Represents the number of flags left to use. Negative means you are using more flags than needed.
#-----------
#Calling start game for the first time to initialize everything.
start_game()
WINDOW.mainloop()			#mainloop. Any code below this will not work unless the window is closed.