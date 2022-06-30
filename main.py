import tkinter as tk
from random import randint as rand
from tkinter import messagebox

def start_game():
	'''Generates grid for buttons.'''
	#Need to add tkinter command too
	global ROWS, COLS, GRID, GAME_STATE, WINDOW
	GRID.clear()
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)] = {'opened': False, 'mine': False, 'button': None} #Replacing this with an exec command, and then adding the button to this dict.
	GAME_STATE = 'FIRST_CLICK'

def generate_mines(coord: tuple):
	'''Generates a grid object based on the first clicked co-ordinate.\n The coordinates in a (1,1) distance from them will not be given any mines.'''
	global ROWS, COLS, NUM_MINES, GRID, GAME_STATE
	s = set()
	while len(s)!=NUM_MINES:
		mine = (rand(0, ROWS - 1), rand(0, COLS-1))
		if abs(mine[0]-coord[0]) and abs(mine[1]-coord[1]):
			s.add(mine)
	for i in range(ROWS):
		for j in range(COLS):
			GRID[(i,j)]['mine'] = (i,j) in s
			GRID[(i,j)]['opened'] = False
	GAME_STATE = 'STARTED'
	

def click(coord: tuple): 
	'''Called on clicking a button. Depending on the button's attributes, different actions will happen.'''
	global GAME_STATE, click_set
	if GAME_STATE == 'FIRST-CLICK':
		generate_mines(coord)
	
	GRID[coord]['opened'] = True

	if GRID[coord]['mine']: del WINDOW
	#Nothing concrete has been filled yet. Will do that part soon.

GAME_STATE = 'FIRST-CLICK'
FLAG_STATE = False
ROWS = 15
COLS = 8
NUM_MINES = 20
GRID = {}
WINDOW = tk.Tk()

click_set = set()