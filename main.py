import tkinter as tk
from random import randint as rand
from tkinter import messagebox

def generate_grid(grid_object: dict, coord: tuple):
	'''Generates a grid object based on the first clicked co-ordinate.\n The coordinates in a (1,1) distance from them will not be given any mines.'''
	global rows, columns, number_of_mines
	s = set()
	while len(s)!=number_of_mines:
		mine = (rand(0, rows - 1), rand(0, columns-1))
		if abs(mine[0]-coord[0]) and abs(mine[1]-coord[1]):
			s.add(mine)
	for i in range(rows):
		for j in range(columns):
			grid_object[(i,j)]['mine'] = (i,j) in s
			grid_object[(i,j)]['opened'] = False
	click(coord)
	

def click(coord: tuple): 
	'''Called on clicking a button. Depending on the button's attributes, different actions will happen.'''
	pass

GAME_STATE = 'FIRST-CLICK'
FLAG_STATE = False
rows = 15
columns = 8
number_of_mines = 20
GRID = {}