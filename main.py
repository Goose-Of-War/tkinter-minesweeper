import tkinter as tk
from tkinter import ttk
from random import randint as rand
from tkinter import messagebox

def color_change(theme: str):
	'''Even tho originally used for changing theme color, it is also used to update difficulty.'''
	global THEME, DIFFICULTY
	DIFFICULTY = mode_variable.get()
	THEME = theme
	WINDOW['bg'] = Themes[THEME]['bg']
	for slave in WINDOW.grid_slaves():
		if type(slave) == tk.Label: slave.configure(**Themes[THEME],)
		elif type(slave) == tk.Button:
			if slave['text'] == "Save Changes": slave.configure(**Themes[THEME],)

def generate_mines(coord: tuple):
	'''Generates a grid object based on the first clicked co-ordinate.\n The coordinates in a (1,1) distance from them will not be given any mines.'''
	global GRID, GAME_STATE
	#Generate a set of coordinates for mines.
	s = set()
	while len(s)!=Difficulties[DIFFICULTY]['mines']:
		mine = (rand(0, Difficulties[DIFFICULTY]['rows'] - 1), rand(0, Difficulties[DIFFICULTY]['cols']-1))
		if abs(mine[0]-coord[0])>1 and abs(mine[1]-coord[1])>1:
			s.add(mine)
	# print(s)	#Purely for debugging purposes. No cheats.
	#Assigning the buttons their values.
	for i in range(Difficulties[DIFFICULTY]['rows']):
		for j in range(Difficulties[DIFFICULTY]['cols']):
			GRID[(i,j)]['mine'] = (i,j) in s
			GRID[(i,j)]['opened'] = False
			GRID[(i,j)]['neighbour'] = [(I,J) for I in range(max(0,i-1), min(i+2,Difficulties[DIFFICULTY]['rows'])) for J in range(max(0,j-1),min(j+2,Difficulties[DIFFICULTY]['cols'])) if (I,J) in s and (I!=i or J!=j)]
		# 	print(len( GRID[(i,j)]['neighbour']) if not GRID[(i,j)]['mine'] else 'F', end=" ")
		# print()
		#Needless to say, no cheats. Only debugging.
	#Changing the Game State
	GAME_STATE = 'STARTED'

def flag_switch():
	'''Used to switch the state of the flag button and flag state.'''
	global FLAG_BUTTON, FLAG_STATE
	#Switch Flag State
	FLAG_STATE = not FLAG_STATE
	#Invert Colours
	FLAG_BUTTON['bg'] = Themes[THEME]['fg'] if FLAG_BUTTON['bg']==Themes[THEME]['bg'] else Themes[THEME]['bg']
	FLAG_BUTTON['fg'] = Themes[THEME]['fg'] if FLAG_BUTTON['fg']==Themes[THEME]['bg'] else Themes[THEME]['bg']

def count_neighbours(coord: tuple, arg: str):
	'''To count the neighbouring flagged/mine containing buttons.'''
	# Simplified: Checks the 8 surrounding coords for the argument's tautology (boolean value).
	return sum([GRID[(i,j)][arg] for i in range(max(0, coord[0]-1), min(coord[0]+2, Difficulties[DIFFICULTY]['rows'])) for j in range(max(0, coord[1]-1), min(coord[1]+2, Difficulties[DIFFICULTY]['cols'])) if (i!=coord[0] or j!=coord[1])])

def click(coord: tuple, forwarded: bool = False): 
	'''Called on clicking a button. Depending on the button's attributes, different actions will happen.'''
	global GAME_STATE, FLAG_COUNTER, FLAGS_LABEL, NUM_LEFT, FLAG_STATE
	#Checking if first-time initialization is needed.
	if GAME_STATE == 'VICTORY' or GAME_STATE == 'GAME_OVER':
		return 
	if GAME_STATE == 'FIRST-CLICK':
		generate_mines(coord)
	#Checking if the location is to be flagged or clicked.
	if FLAG_STATE:
		#Flagging the location.
		if GRID[coord]['opened']: 
			if GRID[coord]['secondclick'] == False:
				if count_neighbours(coord, 'flagged') == len(GRID[coord]['neighbour']): 
					GRID[coord]['secondclick'] = True
					FLAG_STATE = False
					for I in range(max(0, coord[0]-1), min(coord[0]+2, Difficulties[DIFFICULTY]['rows'])):
						for J in range(max(0, coord[1]-1), min(coord[1]+2, Difficulties[DIFFICULTY]['cols'])):
							if I!=coord[0] or J!=coord[1]: click((I,J), True)
					FLAG_STATE = True
		else:
			FLAG_COUNTER += 1 if GRID[coord]['flagged'] else -1
			GRID[coord]['flagged'] = not GRID[coord]['flagged']
			GRID[coord]['button']['text'] = '' if GRID[coord]['button']['text'] else '⚑'
			FLAGS_LABEL['text'] = FLAG_COUNTER
		pass
	else:
		#Clicking the button. (Only if it's neither opened nor flagged.)
		if GRID[coord]['opened'] == False and GRID[coord]['flagged'] == False:
			GRID[coord]['opened'] = True
			if GRID[coord]['mine']:
				GAME_STATE = 'GAME_OVER'
				for i in range(Difficulties[DIFFICULTY]['rows']):
					for j in range(Difficulties[DIFFICULTY]['cols']):
						if GRID[(i,j)]['flagged']:
							pass
						else:
							if GRID[(i,j)]['mine']:
								GRID[(i,j)]['button']['text'] = 'X'
								GRID[(i,j)]['button']['fg'], GRID[(i,j)]['button']['bg'] = GRID[(i,j)]['button']['bg'], GRID[(i,j)]['button']['fg']
							else:
								GRID[(i,j)]['button']['text'] = len(GRID[(i,j)]['neighbour'])
				if forwarded: 
					return 
			else:
				GRID[coord]['button']['text'] = len(GRID[coord]['neighbour'])
			NUM_LEFT -= 1
			if len(GRID[coord]['neighbour']) == 0:
				click(coord)
		elif GRID[coord]['opened'] == True and GRID[coord]['secondclick'] == False and not forwarded:
			if count_neighbours(coord, 'flagged') == len(GRID[coord]['neighbour']): 
				GRID[coord]['secondclick'] = True
				for I in range(max(0, coord[0]-1), min(coord[0]+2, Difficulties[DIFFICULTY]['rows'])):
					for J in range(max(0, coord[1]-1), min(coord[1]+2, Difficulties[DIFFICULTY]['cols'])):
						if I!=coord[0] or J!=coord[1]: click((I,J), True)
		
	if GAME_STATE == 'GAME_OVER':
		print("Game over caused by:", coord)
		messagebox.showerror(title="You lose", message="You clicked a mine. Game Over.")
		start_game()
		# The following line's code was used purely for debugging purposes. No cheats were used while playing the game for real.
	
	if NUM_LEFT == Difficulties[DIFFICULTY]['mines']:
		
		messagebox.showinfo(title="Congratulations.", message="You have cleared the minefield. You win.")
		start_game()

def settings():
	'''For generating the settings page.'''
	global mode_variable
	for slave in WINDOW.grid_slaves():
		slave.destroy()
	tk.Label(WINDOW, text='Settings', font=FONT, **Themes[THEME],).grid(row=0,column=0,columnspan=5,pady=5, padx=5)
	tk.Label(WINDOW,text='Mode',font=FONT, **Themes[THEME],).grid(row=1,column=0)
	tk.Label(WINDOW,text='Colours',font=FONT, **Themes[THEME],).grid(row=2,column=0,padx=5)
	mC=ttk.Combobox(WINDOW,textvariable=mode_variable,width=15,state='readonly', values=[*Difficulties]); mC.grid(row=1,column=1,columnspan=4, padx=5); mC.current([*Difficulties].index(DIFFICULTY))
	for theme in Themes:
		exec("tk.Button(WINDOW, width=2, height=1, text='⚑', font=FONT, command=lambda: color_change({0}), **Themes[{0}]).grid(row=2, column=1+[*Themes].index({0}))".format('"'+theme+'"'))
	call=tk.Button(WINDOW, text="Save Changes", command=start_game, **Themes[THEME], font=FONT); call.grid(row=4,column=0,columnspan=len(Themes)+1);

def start_game():
	'''Generates grid for buttons.'''
	global GRID, GAME_STATE, WINDOW, FLAG_BUTTON, FLAG_STATE, FLAG_COUNTER, FLAGS_LABEL, NUM_LEFT, DIFFICULTY
	DIFFICULTY = mode_variable.get()
	GRID.clear()
	#Removing older objects.
	for slave in WINDOW.grid_slaves():
		slave.grid_remove()
	#Setting the state of the game.
	GAME_STATE = 'FIRST-CLICK'
	FLAG_STATE = False
	FLAG_COUNTER = Difficulties[DIFFICULTY]['mines']
	NUM_LEFT = Difficulties[DIFFICULTY]['rows'] * Difficulties[DIFFICULTY]['cols']
	#Creating new objects.
	WINDOW['bg'] = Themes[THEME]['bg']
	tk.Label(WINDOW, text='Minesweeper',**Themes[THEME], font=FONT).grid(row=0, column=2, columnspan=Difficulties[DIFFICULTY]['cols']-4)
	FLAG_BUTTON = tk.Button(WINDOW, width=2, height=1, text='⚑', command=flag_switch,**Themes[THEME], font=FONT); FLAG_BUTTON.grid(row=0, column=0)
	FLAGS_LABEL = tk.Label(WINDOW, width=2, height=1, text=FLAG_COUNTER,**Themes[THEME], font=FONT); FLAGS_LABEL.grid(row=0, column=1)
	tk.Button(WINDOW, width=2, height=1, text='S', command=settings,**Themes[THEME], font=FONT).grid(row=0, column=Difficulties[DIFFICULTY]['cols']-2)
	tk.Button(WINDOW, width=2, height=1, text='↻', command=start_game,**Themes[THEME], font=FONT).grid(row=0, column=Difficulties[DIFFICULTY]['cols']-1)
	for i in range(Difficulties[DIFFICULTY]['rows']):
		for j in range(Difficulties[DIFFICULTY]['cols']):
			GRID[(i,j)] = {'opened': False, 'mine': False, 'neighbour': 0, 'flagged': False, 'secondclick': False, 'button': eval('tk.Button(WINDOW, width=2, height=1, command=lambda: click(({},{})), text="", fg=Themes[THEME]["fg"], font=FONT, bg=Themes[THEME]["bg"])'.format(i,j))}	#Replacing this with an exec command, and then adding the button to this dict.
			GRID[(i,j)]['button'].grid(row=i+1, column=j)
	#To quote Heath Ledger's Joker: "And here we go."

GAME_STATE = 'FIRST-CLICK'	#Represents the Game's State at any instance.
FLAG_STATE = False			#Represents whether button click will open mine or plant a flag.
GRID = {}					#Dictionary with coordinate keys and dictionary values. Even the Buttons will be stored in the dicts.
WINDOW = tk.Tk()			#Tkinter Window Object. Where everything front-end will be there.
WINDOW.title("Minesweeper")	#Setting the title.
FLAGS_LABEL = None			#Tkinter Label Object: Will have 'Minesweeper' written on it.
FLAG_BUTTON = None			#Tkinter Button Object: Used to toggle flag option.
NUM_LEFT = 0				#Represents the number of closed mines.
FLAG_COUNTER = 0			#Represents the number of flags left to use. Negative means you are using more flags than needed.

Themes = {
	'Light': {'fg':'#000000', 'bg': '#dddddd'},
	'Dark': {'fg':'#aaaaaa', 'bg': '#000000'},
	'Dark Red': {'fg':'#aa0000', 'bg':'#000000'},
	'Light Red': {'fg': '#880000', 'bg': '#dddddd'}
}
THEME = 'Light'				#By default, light theme will be set
FONT = ('Comic Sans MS', 9, 'bold')

Difficulties = {
	'Easy': {'rows': 14, 'cols': 10, 'mines': 16},
	'Medium': {'rows': 15, 'cols': 12, 'mines': 24},
	'Hard': {'rows': 18, 'cols': 14, 'mines': 32}
}
DIFFICULTY = 'Medium'			#By default, Medium difficulty game will start.
mode_variable = tk.StringVar(WINDOW)
mode_variable.set(DIFFICULTY)

#-----------
#Calling start game for the first time to initialize everything.
start_game()
WINDOW.mainloop()			#mainloop. Any code below this will not work unless the window is closed.