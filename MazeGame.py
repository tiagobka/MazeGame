import random
import tkinter as tk
from tkinter import *

class MazeGame():

    def __init__(self):
        self.level = 0
        self.cursor = [0, 0]
        self.dimension = 0
        self.mazeStructure = []
        self.divisions = 0
        self.physCursor = None
        #self.mainWindow = None


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
                print("Level Finished")
                self.canvas.delete("all")





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
        Label(text= "Please Select a level:", width = 100).pack(side=TOP)
        Button(self.mainWindow, text="Level 1", width=100, command = lambda lvl=1: self.levelSelected(lvl)).pack(side=TOP)
        Button(self.mainWindow, text="Level 2", width=100, command = lambda lvl=2: self.levelSelected(lvl)).pack(side=TOP)
        Button(self.mainWindow, text="Level 3", width=100, command = lambda lvl=3: self.levelSelected(lvl)).pack(side=TOP)
        Button(self.mainWindow, text="Level 4", width=100, command = lambda lvl=4: self.levelSelected(lvl)).pack(side=TOP)
        Button(self.mainWindow, text="Level 5", width=100, command = lambda lvl=5: self.levelSelected(lvl)).pack(side=TOP)

    def levelSelected(self,lvl):
        print(lvl)
        self.level = lvl
        self.createMazeStructure()
        self.drawMaze(self.mazeStructure)

    def drawMaze(self, mazeStruct):
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

        menubar = Menu(self.mainWindow)
        menubar.add_command(label=str(self.level))
        self.mainWindow.config(menu=menubar)
        self.mainWindow.mainloop()

def main():
    mg = MazeGame()
    #maze = mg.createMazeStructure()
    mg.createUserInterface()
    # mg.drawMaze(1,maze)

main()
