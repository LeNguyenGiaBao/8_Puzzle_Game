import tkinter as tk 
import tkinter.ttk as ttk
import time
from Eight_Puzzle import *
from PIL import Image, ImageTk

solution =[]
num=[]


#set entry text when click random
def set_text(num):
    entryInput.delete(0, tk.END)
    text=''
    text = ''.join(str(v) for v in num)
    entryInput.insert(0,text)
    return


#clear button
def clearButton():
	for i in range(3):
		for j in range(3):
			listBt[i][j]['text']=''
			listBt[i][j]['image']=''
			listBt[i][j]['state']='normal'
		

def createTable(num):
	for i in range(3):
		for j in range(3):
			listBt[i][j]["text"]=num[i*3+j]
			if(listBt[i][j]["text"]!=0):
				listBt[i][j]["image"]=photo[num[i*3+j]]
			else:
				listBt[i][j]["text"]=''


#show solution in lbOutput, bottom of the form
def setLabel():
	solutionString = 'Solution: \n'
	global solution
	for i in range(len(solution)):
		solutionString=solutionString+ solution[i] +' --> '
		if(i%7==6):
			solutionString=solutionString+'\n'
	solutionString = solutionString +'Win!!!'
	lbOutput['text']=solutionString
	lbPath['text']='Path cost: ' + str(len(solution))


#swap blank button with neighbour button 
def swapButton(bt0, btAny):
	bt0['text']=btAny['text']
	bt0['state'] = 'normal'
	bt0['image'] = btAny['image']
	btAny['text']=''
	btAny['image']= ''
	btAny['state']='disabled'

#move follow the solution
def move():
	indx = 0
	indy=0
	step=''
	global solution
	if(solution!= []):
		step=solution.pop(0)
		if(solution!= []):
			lbNextstep['text']=solution[0]
	for i in range(3):
		for j in range(3):
			if(listBt[i][j]["text"]==''):
				indx=i
				indy=j
				break
	if(step=='LEFT'):
		swapButton(listBt[indx][indy], listBt[indx][indy-1])
	if(step=='RIGHT'):
		swapButton(listBt[indx][indy], listBt[indx][indy+1])
	if(step=='UP'):
		swapButton(listBt[indx][indy], listBt[indx-1][indy])
	if(step=='DOWN'):
		swapButton(listBt[indx][indy], listBt[indx+1][indy])
		

#find solution from num input
def findSolution(num):
	global solution
	solution, time =  solve(tuple(num))
	lbNextstep['text']=solution[0]
	lbTime['text'] = "{:.5f}".format(float(time))
	setLabel()


#click to use textbox value to find solution
def ClickOK():
	clearButton()
	if(len(str(entryInput.get())))==9 and str(entryInput.get())[0]!='0':
		num=[int(x) for x in str(entryInput.get())]
		createTable(num)
		findSolution(num)

#random number and find solution
def ClickAuto():
	clearButton()
	problem = EightPuzzleProblem(initial=None, goal=(0, 1, 2, 3, 4, 5, 6, 7, 8))
	num = random(problem,random_level=25).state
	set_text(num)
	createTable(num)
	findSolution(num)
	
def AutoRun():
	ClickOK()
	for i in range(len(solution)):
		move()
		time.sleep(0.25)
		root.update()


root = tk.Tk()

#add widget
canvas = tk.Canvas(root, height=560, width=530)
canvas.pack()


frame = tk.Frame(root, bg='gray')
frame.place(relwidth=0.8, relheight=0.9)

soluFrame = tk.Frame(root,bg='white')
soluFrame.place(relwidth=0.8, relheight=0.1, relx=0, rely=0.9)

rightFrame = tk.Frame(root, bg='#8ad4e1')
rightFrame.place(relwidth=0.2, relheight=1, relx=0.8, rely=0)


entryInput = tk.Entry(rightFrame)
entryInput.place(relx=0.1, rely=0.1, relwidth=0.8, height=30)

btOK =tk.Button(rightFrame, text='OK', command=ClickOK)
btOK.place(relx=0.1, rely=0.2)

lbNextstep = tk.Label(rightFrame,  bg='#8ad4e1')
lbNextstep.place(relx=0.1, rely=0.3)

btNextstep = tk.Button(rightFrame, text='Next Step', command=move)
btNextstep.place(relx=0.1, rely=0.35)

btAuto = tk.Button(rightFrame, text='Ramdom', command = ClickAuto)
btAuto.place(relx=0.4, rely=0.2)

lbTime2 = tk.Label(rightFrame, text='Time: ', bg ='#8ad4e1' )
lbTime2.place(relx = 0.1, rely = 0.57)

lbTime = tk.Label(rightFrame,  bg='#8ad4e1')
lbTime.place(relx=0.1, rely=0.6)

lbPath=tk.Label(rightFrame,  bg='#8ad4e1')
lbPath.place(relx=0.1, rely=0.65)

lbOutput = tk.Label(soluFrame)
lbOutput.place(relwidth=1, relheight=1, relx=0, rely=0)


btAutoRun = tk.Button(rightFrame, text='Auto', command = AutoRun)
btAutoRun.place(relx = 0.1, rely=0.42)


#import image
image0 = Image.open("images/ute0.png")
image1 = Image.open("images/ute1.png")
image2 = Image.open("images/ute2.png")
image3 = Image.open("images/ute3.png")
image4 = Image.open("images/ute4.png")
image5 = Image.open("images/ute5.png")
image6 = Image.open("images/ute6.png")
image7 = Image.open("images/ute7.png")
image8 = Image.open("images/ute8.png")
photo0 = ImageTk.PhotoImage(image0)
photo1 = ImageTk.PhotoImage(image1)
photo2 = ImageTk.PhotoImage(image2)
photo3 = ImageTk.PhotoImage(image3)
photo4 = ImageTk.PhotoImage(image4)
photo5 = ImageTk.PhotoImage(image5)
photo6 = ImageTk.PhotoImage(image6)
photo7 = ImageTk.PhotoImage(image7)
photo8 = ImageTk.PhotoImage(image8)
photo =[photo0, photo1, photo2, photo3, photo4, photo5, photo6, photo7, photo8]


#cteate button
bt0 = tk.Button(frame)
bt0.place(relx=0, rely=0, relwidth=1/3, relheight=1/3)
bt1 = tk.Button(frame)
bt1.place(relx=1/3, rely=0, relwidth=1/3, relheight=1/3)
bt2 = tk.Button(frame)
bt2.place(relx=2/3, rely=0, relwidth=1/3, relheight=1/3)
bt3 = tk.Button(frame)
bt3.place(relx=0, rely=1/3, relwidth=1/3, relheight=1/3)
bt4 = tk.Button(frame)
bt4.place(relx=1/3, rely=1/3, relwidth=1/3, relheight=1/3)
bt5 = tk.Button(frame)
bt5.place(relx=2/3, rely=1/3, relwidth=1/3, relheight=1/3)
bt6 = tk.Button(frame)
bt6.place(relx=0, rely=2/3, relwidth=1/3, relheight=1/3)
bt7 = tk.Button(frame)
bt7.place(relx=1/3, rely=2/3, relwidth=1/3, relheight=1/3)
bt8 = tk.Button(frame)
bt8.place(relx=2/3, rely=2/3, relwidth=1/3, relheight=1/3)



listBt =[[bt0, bt1, bt2],
		 [bt3, bt4, bt5],
		 [bt6, bt7, bt8]]


root.mainloop()




