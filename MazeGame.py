import random
import tkinter as tk
from tkinter import *


def key(event):
    print("pressed", repr(event.char))


class MazeGame():

    def __init__(self):
        self.level = random.randint(1, 4)
        self.cursor = [0, 0]



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

        return maze

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

    def drawMaze(self, lvl, mazeStruct, mw):
        lvl = self.level * 10
        divisions = (self.level * 600) / ((3) * lvl)

        canvas1 = tk.Canvas(relief=FLAT, background="#D2D2D2", height=1200, width=1200)
        for i in range(lvl):
            row = i * divisions
            for j in range(lvl):
                col = j * divisions
                if (mazeStruct[i][j] == 1):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="white")
                elif (mazeStruct[i][j] == 0):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="black")
                elif (mazeStruct[i][j] == 4):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="green")
                elif (mazeStruct[i][j] == 3):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="red")
        cursory = self.cursor[0] * divisions
        cursorx = self.cursor[1] * divisions
        oval = canvas1.create_oval(cursorx, cursory, cursorx + divisions - 1, cursory + divisions - 1, fill="blue")

        return canvas1

    def createUserInterface(self, maze):
        mainWindow = tk.Tk()

        mainWindow.title("The Maze Game")
        mainWindow.geometry("1000x1000")

        canvas = self.drawMaze(2, maze, mainWindow)
        canvas.pack(side=LEFT)

        menubar = Menu(mainWindow)
        menubar.add_command(label="HI")
        mainWindow.config(menu=menubar)

        ''''var = IntVar(mainWindow)
        var.set(1)  # initial value
        Label(text="Level:").pack()
        option = OptionMenu(mainWindow, var,1,2,3,4,5,6,7,8,9,10)
        option.pack()

        def changelevel(canvas, mainWindow):
            canvas.destroy()
            maze = mg.createMazeStructure(var.get())
            canvas = self.drawMaze(var.get(),maze,mainWindow)
            canvas.pack(side = LEFT)
            print(var.get())
        Button(mainWindow, text = "Change Level", command = lambda canvas=canvas, mainWindow = mainWindow:changelevel(canvas,mainWindow)).pack()'''

        mainWindow.mainloop()


mg = MazeGame()
maze = mg.createMazeStructure()
mg.createUserInterface(maze)
# mg.drawMaze(1,maze)
