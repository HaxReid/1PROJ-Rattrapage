from tkinter import *
from random import *

class Case:

  def __init__(self, x1, y1, x2, y2, couleurCase, couleurPion, pion):

    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.couleurCase = couleurCase
    self.couleurPion = couleurPion
    self.pion = pion

###Setter Getter###

  def __eq__(self, other):
      return (self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2)  

  def getCoordCase(self):
    return [self.x1,self.y1,self.x2,self.y2]  

  def getCoordPion(self):
    return [self.x1+10,self.y1+10,self.x2-10,self.y2-10]    

  def setPion(self, val):
    self.pion = val 

  def setCouleurPion(self, val):
    self.couleurPion = val   

###Creation et placement des pions###

  def createCase(self):
    canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2, fill = self.couleurCase)
    
  def placePion(self):
    if self.pion:
      canvas.create_oval(self.x1+10,self.y1+10,self.x2-10,self.y2-10, fill = self.couleurPion)

###Vérification Direction###

  def gauche(self):
    for case in toutes_les_cases:
      if case.x1 == self.x1-40 and case.x2 == self.x2-40 and case.y1 == self.y1:
        return case
    return caseNeutre    

  def droite(self):
    for case in toutes_les_cases:
      if case.x1 == self.x1+40 and case.x2 == self.x2+40 and case.y1 == self.y1:
        return case 
    return caseNeutre      

  def haut(self):
    for case in toutes_les_cases:
      if case.y1 == self.y1-40 and case.y2 == self.y2-40 and case.x1 == self.x1:
        return case  
    return caseNeutre        

  def bas(self):
    for case in toutes_les_cases:
      if case.y1 == self.y1+40 and case.y2 == self.y2+40 and case.x1 == self.x1:
        return case  
    return caseNeutre  

###vérification mouvement###

  def canMove(self,dest):
    caseDest = searchCase(dest)
    if not caseDest:
      return 0
    else:  
      if caseDest.pion or (
       not caseDest.__eq__(self.gauche()) and not caseDest.__eq__(self.gauche().gauche())
       and not caseDest.__eq__(self.droite()) and not caseDest.__eq__(self.droite().droite())
       and not caseDest.__eq__(self.haut()) and not caseDest.__eq__(self.haut().haut())
       and not caseDest.__eq__(self.bas()) and not caseDest.__eq__(self.bas().bas())) or (
       caseDest.__eq__(self.gauche().gauche()) and (
       not self.gauche().pion or self.gauche().couleurPion == self.couleurPion)) or (
       caseDest.__eq__(self.droite().droite()) and (
       not self.droite().pion or self.droite().couleurPion == self.couleurPion)) or (
       caseDest.__eq__(self.haut().haut()) and (
       not self.haut().pion or self.haut().couleurPion == self.couleurPion)) or (
       caseDest.__eq__(self.bas().bas()) and (
       not self.bas().pion or self.bas().couleurPion == self.couleurPion)):

          return 0 
    return 1  
   
###Mouvement###

def move(event):
    global caseDepart,pionClicker
    x,y=event.x,event.y
    if caseDepart and pionClicker:
      coord=canvas.coords(pionClicker)
      deplacement=[[x-10,y-10,x+10,y+10]]
      canvas.coords(pionClicker,deplacement[0])
      
###click###

def click(event):
    global caseDepart,pionClicker,session
    x,y=event.x,event.y
    pionClicker = 0
    caseDepart = 0
    clicker = canvas.find_overlapping(x, y, x, y)
    if len(clicker)>1 :
      coord = canvas.coords(clicker[0])
      caseDepart = searchCase(coord)
      if caseDepart.couleurPion == session:
        pionClicker = 0
      else:  
        pionClicker = clicker[1]
        
###Creation plateau

def plateau():
  global x1,x2,y1,y2
  ite,i,couleurCase = 0,1,'#000000'

  while x1<200 and y1<200:
    if i <= 12:
      couleurPion = '#FF0000'
      toutes_les_cases.append(Case(x1,y1,x2,y2,couleurCase,couleurPion,1))
    elif i > 13:
      couleurPion = '#007FFF'
      toutes_les_cases.append(Case(x1,y1,x2,y2,couleurCase,couleurPion,1))
    else: toutes_les_cases.append(Case(x1,y1,x2,y2,couleurCase,'',0))

    toutes_les_cases[-1].createCase()
    i,ite,x1,x2=i+1,ite+1,x1+40,x2+40

    if ite == 5:
      y1,y2=y1+40,y2+40
      ite,x1,x2=0,5,45

    if i%2 == 0:
      couleurCase='white'
    else: couleurCase='#000000'

  for case in toutes_les_cases:
    case.placePion()  

  bouttonDam.destroy()
  score.pack()

###Trouver la case###

def searchCase(coord):
      for case in toutes_les_cases:
        if case.x1 == coord[0] and case.y1 == coord[1] and case.x2 == coord[2] and case.y2 == coord[3]:
          return case     
      return 0    


###Main###

def end(event):
    global caseDepart, pionClicker,scoreV,scoreJ,session
    x,y=event.x,event.y
    collision = canvas.find_overlapping(x-10,y-10,x+10,y+10)
    coord = canvas.coords(collision[0])
    if caseDepart and pionClicker:
      if not caseDepart.canMove(coord):
        canvas.coords(pionClicker,caseDepart.getCoordPion())
      else:
        caseDest = searchCase(coord)
        if not caseDepart.__eq__(caseDest):
          session=caseDepart.couleurPion
          caseDest.setPion(1)
          caseDest.setCouleurPion(caseDepart.couleurPion)
          canvas.coords(pionClicker, caseDest.getCoordPion())
          caseDepart.setPion(0)
          caseDepart.setCouleurPion('')
          caseSupprimer=0

          if caseDest.__eq__(caseDepart.gauche().gauche()):
              caseSupprimer = caseDepart.gauche()
          elif caseDest.__eq__(caseDepart.droite().droite()):
              caseSupprimer = caseDepart.droite()     
          elif caseDest.__eq__(caseDepart.haut().haut()):
              caseSupprimer = caseDepart.haut()    
          elif caseDest.__eq__(caseDepart.bas().bas()):
              caseSupprimer = caseDepart.bas()  

          if caseSupprimer:
            if caseSupprimer.couleurPion == '#007FFF':
              scoreV += 1
            else: 
              scoreJ +=1  
            score.configure(text='R : {}  vs  B : {}'.format(scoreV,scoreJ)) 
            if scoreJ >= 12:
              score.configure(text='Victoire B : {}'.format(scoreJ)) 
            elif scoreV >= 12:
              score.configure(text='Victoire R : {}'.format(scoreV))   
            z = caseSupprimer.getCoordPion()
            pionSupprimer = canvas.find_overlapping(z[0],z[1],z[2],z[3])
            canvas.delete(pionSupprimer[1])
            caseSupprimer.setPion(0)


###Initialisation des différentes variables###

x1,y1,x2,y2 = 5,5,45,45
x3,y3,x4,y4 = 15,15,35,35
toutes_les_cases = []
caseNeutre = Case(0,0,0,0,'','',0)
scoreV,scoreJ,session = 0,0,''

###Tkinter###

root= Tk()
root.title("Alquerque")
root.geometry("260x245+450+250")
root.configure(bg='white')
canvas=Canvas(root,width=206,heigh=206,bg='black')

font='arial 13 bold'
bouttonDam=Button(root,text='Commencer',font=font,command=plateau, fg='white', bg='red')
score = Label(root, text = 'R : 0  vs  B : 0', font=font, fg='white', bg='red')
canvas.pack()
bouttonDam.pack(padx=3,pady=3)

canvas.bind("<ButtonPress-1>", click)
canvas.bind("<B1-Motion>", move)
canvas.bind("<ButtonRelease-1>", end)
canvas.configure(cursor="hand2")

root.resizable(False,False)
root.mainloop()
