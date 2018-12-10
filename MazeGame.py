import random
import tkinter as tk
from tkinter import *
import datetime
from tkinter import simpledialog
from VirtualKeyboard import VirtualKeyboard


class scoretable():
    def __init__(self):
        self.name = []
        self.time = []
        self.out_from_file()

## add new score and switch it to the firsl element of list maximum 10 elements the last one will be replaced
    def addscore(self, name, time,lvl):
        score = int(((16.5 * lvl - 8.5) - time) * 10 / (lvl))
        self.name.append(name)
        self.time.append(score)
        self.name = [x for _, x in sorted(zip(self.time, self.name),reverse =True)]
        self.time.sort(reverse = True)
        self.in_to_file()



## sort Algorithm that will sort the best score base on time (I dont think we need that)
    def insertionSort(self):
        for index in range(1, len(self.time)):
            currentvalue = self.time[index]
            position = index
            while position > 0 and self.time[position - 1] > currentvalue:
                self.time[position] = self.time[position - 1]
                self.name[position], self.name[position - 1] = self.name[position - 1], self.name[position]
                position = position - 1
                self.time[position] = currentvalue

    def isNewRecord(self,totalTime, lvl):
        score = int(((16.5 * lvl - 8.5) - totalTime) * 10 / (lvl))
        if (score > int(self.time[len(self.time)-1]) or len(self.time) < 10):
            return True
        else:
            return False
    def score(self,totalTime,lvl):
        return int(((16.5 * lvl - 8.5) - totalTime) * 10 / (lvl))



## export scores to file txt----variable need to be string type to export to file
    def in_to_file(self):
        file = open("score.dat", "w")
        if len(self.name) > 10:
            max = 10
        else:
            max = len(self.name)
        #t = open("time.txt", "w")
        for i in range(0, max):
            file.write(str(self.name[i]) + ":"+ str(self.time[i]) + "\n")
            #t.write(str(self.time[i]) + "\n")
        #n.close()
        file.close()
## import scores to program -> use when start new game
    def out_from_file(self):

        with open("score.dat", "r") as file:
            line = file.readline()
            while(line):
                self.name.append(line.split(":")[0].strip())
                self.time.append(int(line.split(":")[1].strip()))
                line = file.readline()


class MazeGame():

    def __init__(self):
        self.level = 0
        self.cursor = [0, 0]
        self.dimension = 0
        self.mazeStructure = []
        self.divisions = 0
        self.physCursor = None
        self.score= scoretable()
        self.startTime = 0
        self.firstMove = True
        self.scoreMenu = None
        self.vk = VirtualKeyboard()


    def createMazeStructure(self):
        lvl = self.level * 10
        maze = []
        for i in range(lvl):
            row = []
            for j in range(lvl):
                row.append(0)
            maze.append(row)

        # Prim's algorithm for maze creation
        walls = []

        x = random.randint(0, lvl - 1)
        y = random.randint(0, lvl - 1)

        maze[y][x] = 4
        self.cursor[0] = y
        self.cursor[1] = x
        lst = self.getWalls(y, x, maze, lvl)
        walls.extend(lst)
        lst.clear()

        while (len(walls) >= 1):

            j0, i0, j, i = walls[random.randint(0, len(walls) - 1)]
            walls.remove((j0, i0, j, i))

            if (maze[j][i] == 0):  # if is wall
                maze[j][i] = 1
                maze[j0][i0] = 1

                y, x = j, i
                lst = self.getWalls(y, x, maze, lvl)
                walls.extend(lst)
                lst.clear()
        maze[y][x] = 3
        self.mazeStructure = maze
        return maze


    def updateCursor(self,y,x):

        if (self.firstMove):
            self.startTime = datetime.datetime.now()
            self.firstMove = False

        if(not self.outOfBound(y, x, len(self.mazeStructure))):
            #if (self.mazeStructure[y][x]==1): #if is path
            if (self.mazeStructure[y][x] != 0): #if is not wall

                    self.canvas.move(self.physCursor, (x-self.cursor [1])*self.divisions,(y-self.cursor [0])*self.divisions)
                    self.cursor[0] = y
                    self.cursor[1] = x

            if (self.mazeStructure[y][x] == 3):
                # Momentarely unbind keyboard keys
                self.canvas.master.unbind_all("<Right>")
                self.canvas.master.unbind_all("<Left>")
                self.canvas.master.unbind_all("<Up>")
                self.canvas.master.unbind_all("<Down>")
                self.canvas.delete("all")
                self.canvas.forget()
                self.mainWindow.bind("<Key>", self.keyPress)
                self.firstMove = True
                endtime = datetime.datetime.now()
                totalTime = (endtime-self.startTime).total_seconds()
                if self.score.isNewRecord(totalTime, self.level):
                    answer = self.vk.displayKeyboard(self.score.score(totalTime,self.level))
                    #answer = simpledialog.askstring("New High Score!", "What is your name",
                    #                                parent=self.mainWindow)
                    if (answer or answer!= ""):
                        self.score.addscore(answer,totalTime,self.level)
                self.f.pack()


    def getWalls(self, y, x, maze, dim):
        walls = []

        r = x + 2
        l = x - 2
        u = y - 2
        d = y + 2

        if (not self.outOfBound(y, r, dim)):  # check right
            if (maze[y][r] == 0):
                walls.append((y, r - 1, y, r))

        if (not self.outOfBound(y, l, dim)):  # check left
            if (maze[y][l] == 0):
                walls.append((y, l + 1, y, l))

        if (not self.outOfBound(u, x, dim)):  # check up
            if (maze[u][x] == 0):
                walls.append((u + 1, x, u, x))

        if (not self.outOfBound(d, x, dim)):  # check down
            if (maze[d][x] == 0):
                walls.append((d - 1, x, d, x))

        return walls

    def outOfBound(self, y, x, dim):
        if (y < 0 or y >= dim):
            return True
        if (x < 0 or x >= dim):
            return True
        return False

    def drawMenu(self):


        self.f = Frame(self.mainWindow, width = 100 )
        Label( self.f, text= "Please Select a level:", width = 100).pack(side=TOP)
        Button( self.f, text="Level 1", width=100, command = lambda lvl=1: self.levelSelected(lvl), takefocus=False,activebackground="grey").pack(side=TOP)
        Button( self.f, text="Level 2", width=100, command = lambda lvl=2: self.levelSelected(lvl), takefocus=False,activebackground="grey").pack(side=TOP)
        Button( self.f, text="Level 3", width=100, command = lambda lvl=3: self.levelSelected(lvl), takefocus=False,activebackground="grey").pack(side=TOP)
        Button(self.f, text="Level 4", width=100, command = lambda lvl=4: self.levelSelected(lvl), takefocus=False,activebackground="grey").pack(side=TOP)
        Button( self.f, text="Level 5", width=100, command = lambda lvl=5: self.levelSelected(lvl), takefocus=False,activebackground="grey").pack(side=TOP)
        self.f.pack(side = TOP)
        #self.f.focus_force()
        #self.f.bind("<Key>", self.keyPress)

    def levelSelected(self,lvl):
        self.level = lvl
        self.createMazeStructure()
        self.drawMaze(self.mazeStructure)
        self.f.forget()


    def drawMaze(self, mazeStruct):
        self.mainWindow.unbind("<Key>")
        lvl = self.level * 10
        #print(self.mainWindow.winfo_height())
        divisions = (800)/lvl
        self.divisions = divisions
        #canvas1 = tk.Canvas(relief=FLAT, background="#D2D2D2", height=800, width=800)
        #canvas1 = tk.Canvas(relief=FLAT, height=1200, width=1200)

        for i in range(lvl):
            row = i * divisions
            for j in range(lvl):
                col = j * divisions
                if (mazeStruct[i][j] == 1): #It is a Path
                    self.canvas.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="white")
                elif (mazeStruct[i][j] == 0):#It is a wall
                    self.canvas.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="black")
                elif (mazeStruct[i][j] == 4):#It is the starting point
                    self.canvas.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="green")
                elif (mazeStruct[i][j] == 3):#It is the ending point
                    self.canvas.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="red")
        cursory = self.cursor[0] * divisions
        cursorx = self.cursor[1] * divisions
        #oval = canvas1.create_oval(cursorx, cursory, cursorx + divisions - 1, cursory + divisions - 1, fill="blue")
        self.physCursor = self.canvas.create_oval(cursorx, cursory, cursorx + divisions - 1, cursory + divisions - 1, fill="blue")

        self.canvas.pack(side=TOP)

        self.mainWindow.bind_all( "<Left>", self.leftKey)
        self.mainWindow.bind_all("<Right>", self.rightKey)
        self.mainWindow.bind_all("<Up>", self.upKey)
        self.mainWindow.bind_all("<Down>", self.downKey)
        #self.canvas = canvas1

        #return canvas1


    def leftKey(self,event):
        self.updateCursor(self.cursor[0],self.cursor[1]-1)

    def rightKey(self,event):
        self.updateCursor(self.cursor[0], self.cursor[1] + 1)


    def upKey(self,event):
        self.updateCursor(self.cursor[0] - 1, self.cursor[1])


    def downKey(self,event):
        self.updateCursor(self.cursor[0] + 1, self.cursor[1])

    def createUserInterface(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.title("The Maze Game")
        c = self.level
        self.mainWindow.geometry("800x800")
        self.drawMenu()
        self.canvas = tk.Canvas(relief=FLAT, background="#D2D2D2", height=800, width=800)
        self.mainWindow.focus_set()
        self.mainWindow.bind("<Key>", self.keyPress)

        menubar = Menu(self.mainWindow)
        menubar.add_command(label="Check Scores", command = lambda event = None:self.scoreButton(event) )
        #menubar.bind("<Tab>", self.scoreButton)

        self.mainWindow.config(menu=menubar)
        self.mainWindow.mainloop()


    def scoreButton(self,event):
        if (self.scoreMenu):
            self.scoreMenu.destroy()
            del(self.scoreMenu)
            self.scoreMenu = None
        else:
            self.scoreMenu = tk.Toplevel()
            self.scoreMenu.title("Score")
            Label(self.scoreMenu,text = "Player").grid(row=0, column = 0)
            Label(self.scoreMenu, text="Score").grid(row=0, column=1)
            for i,n in enumerate(self.score.name):
                Label(self.scoreMenu,text = n, width = 20, anchor = "e",borderwidth=2,relief="groove").grid(row = i +1, column = 0)
                Label(self.scoreMenu, text=self.score.time[i], width = 20,borderwidth=2,relief="groove").grid(row=i + 1, column=1)

    def keyPress(self,event):
        #print(event.keycode )

        if (event.keycode == 9):
            self.scoreButton(event)
            #print(self.f.slaves())
        if (event.keycode == 38):
            if self.level == 0:
                self.level = 5
                self.f.slaves()[1:][4].config(state = "active")
            elif self.level > 1:
                self.level -=1
                for i in self.f.slaves()[1:]:
                    i.config(state="normal")
                self.f.slaves()[self.level].config(state='active')


        if (event.keycode == 40):
            if self.level == 0:
                self.level = 1
                self.f.slaves()[1:][0].config(state = "active")
            elif self.level < 5:
                self.level +=1
                for i in self.f.slaves()[1:]:
                    i.config(state="normal")
                self.f.slaves()[self.level].config(state='active')

        if (event.keycode == 13):
            if (self.level !=0):
                self.f.slaves()[self.level].invoke()

def main():
    mg = MazeGame()
    mg.createUserInterface()

main()
