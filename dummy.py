'''
Python: Tkinter
Minesweeper Game
Made in 2020 by Goose
'''

import tkinter as T
from tkinter import ttk as tt
from tkinter import messagebox
from random import randint as rand
from datetime import datetime as dt

truth=[]; text={'':''};  t=0; f=False; r=c=10; m=20; flagdic={}; fB=0; ret=0; num=0; stt=0; clicked=[]; v=0
mC=0; startt=dt.now()
colorschemes={'def':('#f0f0f0','#2b2b2b'),'red':('#e2e2e2','#800000'),'dark':('#2b2b2b','#b1b1b1'),'darkred':('#0b0b0b','#af0000')}; buttons={'T':'t'}
modes={'Beginner':(10,9,9), 'Easy':(13,11,17), 'Medium':(17,14,42), 'Hard':(20,16,66), 'Extreme':(25,23,135)}
theme='def'; ncol,ccol='#f0f0f0','#2b2b2b'; mode='Easy'; r,c,m=modes['Easy']

def colorch(f):
    global theme; global ncol; global ccol
    exec('C{0}.configure(state=T.NORMAL)'.format(theme),buttons)
    theme=f; ncol,ccol=colorschemes[f]
    exec('C{0}.configure(state=T.DISABLED)'.format(theme),buttons)
    buttons['ncol'],buttons['ccol']=ncol,ccol

def count(n,s=1):
    nr=n//c; nc=n-nr*c; count=0
    
    for i in range(nr-1,nr+2):
        for j in range(nc-1,nc+2):
            if (-1<i<r) and (-1<j<c) and (truth[i][j]==s or truth[i][j]==str(s))  and not (i*c+j==n) : 
                count+=1
        
    return count

def secondclick(n):
    pass
    global f; f_=f
    f=False
    if count(n,s='f')==int(text['B{0}'.format(n)]):
        nr=n//c; nc=n-nr*c
        for i in range(nr-1,nr+2):
            for j in range(nc-1,nc+2):
                if (-1<i<r) and (-1<j<c) and not (i*c+j==n): click(i*c+j)
        exec('B{}.configure(command=None)'.format(n),buttons)
    f=f_

def gameover():
    global v
    if not v:
        for i in range(r):
            for j in range(c):
                if truth[i][j]==1: exec('B{0}.configure(text="\u2600")'.format(i*c+j),buttons)
        messagebox.showinfo("GAME OVER","Sorry, you lose.\nThe game will not retry as soon as you close this dialog box.")
        v=True
        for i in list(T.Grid.grid_slaves(ms)): 
            try: i.configure(state=T.DISABLED)
            except: continue
        ret.configure(state=T.NORMAL); stt.configure(state=T.NORMAL)

def flag():
    global f
    if f: fB.configure(bg=ncol,fg=ccol,text='\u2690')
    else: fB.configure(bg=ccol,fg=ncol,text='\u2691')
    f=not f

def victorycheck():
    global v
    if not v:
        for i in flagdic:
            if str(flagdic[i])=='0': break
        else: 
            et=dt.now()
            delt=et-startt
            messagebox.showinfo("CONGRATS","You won. Congratulations. You took {} minutes and {} seconds.\nThe game will not automatically restart. Click the '\u21bb' button to restart or the settings button to change the dimensions and mines.".format(delt.seconds//60,delt.seconds%60))
            v=True
            for i in list(T.Grid.grid_slaves(ms)): 
                try: i.configure(state=T.DISABLED)
                except: continue
            ret.configure(state=T.NORMAL); stt.configure(state=T.NORMAL)

def flagclick(n):
    if text['B{}'.format(n)]=='\u2691':
        truth[n//c][n-c*(n//c)]=flagdic[n]; del flagdic[n]; exec('B{0}.configure(text=""); text["B{0}"]=""'.format(n),buttons)
    else:
        flagdic[n]=truth[n//c][n-c*(n//c)]; truth[n//c][n-c*(n//c)]='f'; exec('B{0}.configure(text="\u2691"); text["B{0}"]="\u2691"'.format(n),buttons)
    num.configure(text=m-len(flagdic))

def click(n):
    global t; global truth; global startt
    if t==0:                                #First Click
        startt=dt.now()
        truth=set()
        while len(truth)<m:
            p=rand(0,r*c-1)
            if (abs(p-n) not in (0,1,c-1,c,c+1)): 
                truth.add(p)
        truth=[[int((c*i+j) in truth) for j in range(c)]  for i in range(r)]
        t=1; click(n)
    elif f: flagclick(n)
    elif text['B{}'.format(n)]=='\u2691': pass
    elif truth[n//c][n-c*(n//c)]==1:        #Mine
        
        exec('B{0}.configure(text="\u2600"); text["B{0}"]="\u2600"'.format(n),buttons)
        truth[n//c][n-c*(n//c)]='1'
        gameover()
    elif text['B{}'.format(n)]=='':         #Not Mine, but First Click
        
        exec('B{0}.configure(text={1},command=lambda: secondclick({0}), fg=ncol,bg=ccol); text["B{0}"]="{1}"'.format(n,count(n)+count(n,'f')),buttons)
        global clicked; clicked+=['B{}'.format(n)]
        if text['B%d'%n]=='0': secondclick(n)
    else:                                   #Not mine, second click
        exec('B{}.configure(command=None)'.format(n),buttons)
    clicked=list(set(clicked))
    if (len(clicked)==(r*c)-m):
        victorycheck()

def save():
    global r,c,m,mode; r,c,m=modes[mV.get()]; mode=mV.get()
    ms.configure(bg=ncol)
    retry()

def settings():
    ms.geometry('200x120+20+20')
    global mC; ms.configure(bg='#f0f0f0')
    try:
        for i in list(T.Grid.grid_slaves(ms)): i.destroy()
    except: pass
    L=T.Label(ms,text='Settings',font=('Comic Sans MS',10,'underline')); L.grid(row=0,column=0,columnspan=5,pady=5)
    Mc=T.Label(ms,text='Mode',font=('Comic Sans MS',10)); Mc.grid(row=1,column=0)
    mC=tt.Combobox(ms,textvariable=mV,width=15,state='readonly'); mC['values']=[i for i in modes]; mC.grid(row=1,column=1,columnspan=4); mC.current([i for i in modes].index(mode))
    call=T.Button(ms,text="Save Changes",command=save); call.grid(row=4,column=0,columnspan=len(colorschemes)+1); cL=T.Label(ms,text='Colours',font=('Comic Sans MS',10)); cL.grid(row=2,column=0,padx=5)
    for i in range(1,len(colorschemes)+1): 
        exec('C{0}=T.Button(ms,bg="{1}",fg="{3}",text="\u2691",command=lambda: colorch("{0}"),width=3); C{0}.grid(row=2,column={2}); buttons["C{0}"]=C{0}'.format( list(colorschemes.keys())[i-1], list(colorschemes.values())[i-1][0], i, list(colorschemes.values())[i-1][1] ),{'ms':ms,'buttons':buttons,'colorschemes':colorschemes,'T':T,'C{}'.format(1):0,'colorch':colorch} )
    colorch(theme)

buttons={'text':text,'secondclick':secondclick, 'ncol':ncol, 'ccol':ccol,'T':T}
ms=T.Tk(); ms.title("Minesweeper"); ms.geometry('300x400+25+25')
mV=T.StringVar()    #Mode combobox get variable
lb=T.Label(text='\n',height=8,width=10); lb.grid(row=0,column=0)
lb_=T.Label(height=2,width=10); lb_.grid(row=3,column=2)
def retry():
    ms.geometry("")
    global fB; global ret; global t; global num; global stt; global buttons; global flagdic; global f; global clicked; global v
    try: 
        for i in buttons: pass
        for i in list(T.Grid.grid_slaves(ms)): i.destroy()
    except: print(0)
    t=0; flagdic={}; f=False; clicked=[]; v=False
    num=T.Label(ms,text=(m-len(flagdic)),bg=ncol,fg=ccol,font=('Comic Sans MS',8)); num.grid(row=0,column=1)
    fB=T.Button(ms,height=1,width=2,text='\u2690',command=flag,bg=ncol,fg=ccol); fB.grid(row=0,column=0)
    L=T.Label(ms,text="Minesweeper",font=('Comic Sans MS',10,'bold'),bg=ncol,fg=ccol); L.grid(row=0,column=2,columnspan=c-4)
    stt=T.Button(ms,text='\u2699',command=settings,bg=ncol,fg=ccol,font=('Arial',10,'bold')); stt.grid(row=0,column=c-2)
    ret=T.Button(ms,text='\u21bb',width=2,height=1,command=retry,bg=ncol,fg=ccol); ret.grid(row=0,column=c-1)
    for i in range(1,r+1):
        for j in range(c): exec("B{0}=T.Button(ms,width=2,height=1,command=lambda: click({0}), bg=ncol, fg=ccol); B{0}.grid(row={1},column={2}); buttons.update(dict([('B{0}',B{0})])); ".format(c*(i-1)+j,i,j), ({'click':click,'T':T,'B{}'.format(r*(i-1)+j):0,'ms':ms, 'buttons':buttons, 'ncol':ncol, 'ccol':ccol}))
    for i in range(r*c):
        text['B{}'.format(i)]=''

TITLE=T.Label(ms,text="Minesweeper",font=('Arabic Typesetting',30),fg='#008800'); TITLE.grid(row=1,column=1)
START=T.Button(ms,text="Start",font=('Arabic Typesetting',18),command=retry,width=10); START.grid(row=2,column=1)

ms.mainloop()