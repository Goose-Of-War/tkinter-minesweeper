import tkinter as tk
from random import randint as rand
from tkinter import messagebox

def start_game():
	'''Generates grid for buttons.'''
	#Need to add tkinter command too
	global ROWS, COLS, GRID, GAME_STATE, WINDOW
	GRID.clear()
	for object in WINDOW.grid_slaves():
		del object
	tk.Label(WINDOW, text='Minesweeper').grid(row=0, column=0, columnspan=COLS)
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)] = {'opened': False, 'mine': False, 'neighbour': 0, 'button': eval('tk.Button(WINDOW, width=2, height=1, command=lambda: click(({},{})), text="")'.format(i,j))} #Replacing this with an exec command, and then adding the button to this dict.
			GRID[(i,j)]['button'].grid(row=i+1, column=j)
	GAME_STATE = 'FIRST-CLICK'

def generate_mines(coord: tuple):
	'''Generates a grid object based on the first clicked co-ordinate.\n The coordinates in a (1,1) distance from them will not be given any mines.'''
	global ROWS, COLS, NUM_MINES, GRID, GAME_STATE
	s = set()
	while len(s)!=NUM_MINES:
		mine = (rand(0, ROWS - 1), rand(0, COLS-1))
		if abs(mine[0]-coord[0])>1 and abs(mine[1]-coord[1])>1:
			s.add(mine)
	print(s)
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)]['mine'] = (i,j) in s
			GRID[(i,j)]['opened'] = False
			GRID[(i,j)]['neighbour'] = [(I,J) for I in range(max(0,i-1), min(i+2,ROWS)) for J in range(max(0,j-1),min(j+2,COLS)) if (I,J) in s and (I!=i or J!=j)]
			print(len( GRID[(i,j)]['neighbour']) if not GRID[(i,j)]['mine'] else 'F', end=" ")
		print()
	GAME_STATE = 'STARTED'

def click(coord: tuple): 
	'''Called on clicking a button. Depending on the button's attributes, different actions will happen.'''
	global GAME_STATE, click_set
	if GAME_STATE == 'FIRST-CLICK':
		generate_mines(coord)
	
	GRID[coord]['opened'] = True
	if GRID[coord]['mine']: 
		GRID[coord]['button']['text'] = "F"
	else:
		GRID[coord]['button']['text'] = len(GRID[coord]['neighbour'])
		print(coord, GRID[coord]['neighbour'], sep=':')
	#Nothing concrete has been filled yet. Will do that part soon.

GAME_STATE = 'FIRST-CLICK'
FLAG_STATE = False
ROWS = 15
COLS = 12
NUM_MINES = 24
GRID = {}
WINDOW = tk.Tk()
WINDOW.title("Minesweeper")

start_game()
WINDOW.mainloop()