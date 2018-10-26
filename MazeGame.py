import random
import tkinter as tk
from tkinter import *
class MazeGame():

    def __init__(self):
        self.level = 1

    def calSize(self):
        if (True):
            print("hello")

        #do something
    def calLocation(self):
         if (True):
             print("hi")


    def createMazeStructure(self,lvl):
        lvl = lvl*10
        maze = []
        for i in range(lvl):
            row = []
            for j in range(lvl):
                row.append(0)
            maze.append(row)

        walls = []

        x = random.randint(0, lvl-1)
        y = random.randint(0, lvl-1)

        maze[y][x] = 4
        lst = self.getWalls(y,x,maze,lvl)
        walls.extend(lst)
        lst.clear()

        while (len(walls) >= 1):

            j0,i0,j,i= walls[random.randint(0,len(walls)-1)]
            walls.remove((j0,i0,j, i))

            if (maze[j][i] == 0): #if is wall
                maze[j][i] = 1
                maze[j0][i0] = 1

                y,x = j, i
                lst = self.getWalls(y, x, maze, lvl)
                walls.extend(lst)
                lst.clear()
        maze[y][x]=3



        return maze

    def getWalls(self,y,x,maze,dim):
        walls = []

        r = x+2
        l = x-2
        u = y-2
        d = y+2

        if (not self.outOfBound(y,r,dim)): #check right
            if (maze[y][r]==0):
                walls.append ((y,r-1,y,r))

        if (not self.outOfBound(y,l,dim)): #check left
            if (maze[y][l]==0):
                walls.append ((y,l+1,y,l))

        if (not self.outOfBound(u,x,dim)): #check up
            if (maze[u][x]==0):
                walls.append ((u+1,x,u,x))

        if (not self.outOfBound(d,x,dim)): #check down
            if (maze[d][x]==0):
                walls.append ((d-1,x,d,x))

        return walls





    def outOfBound(self,y,x,dim):
        if (y <0 or y>=dim):
            return True
        if (x <0 or x>=dim):
            return True
        return False




        #if (r == dim):



    def drawMaze(self, lvl,mazeStruct):
        lvl = lvl*10
        divisions = 800/lvl
        mw = tk.Tk()
        mw.title('The game')
        mw.geometry("1000x900")  # You want the size of the app to be 500x500
        tk.Button(master=mw, text="screenSize", command=lambda i=mw: exec(i))

        canvas1 = Canvas(mw, relief=FLAT, background="#D2D2D2",height = 800, width = 800)
        canvas1.pack()

        for i in range(lvl):
            row = i*divisions
            for j in range(lvl):
                col = j*divisions
                if(mazeStruct[i][j]==1):
                    canvas1.create_rectangle(col, row, col+divisions-1, row+divisions-1, fill="white")
                elif(mazeStruct[i][j]==0):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="blue")
                elif(mazeStruct[i][j]==4):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="green")
                elif(mazeStruct[i][j]==3):
                    canvas1.create_rectangle(col, row, col + divisions - 1, row + divisions - 1, fill="red")


        #buttonBG = canvas1.create_rectangle(0, 0, 100, 30, fill="grey40", outline="grey60")



        mw.mainloop()


    def exec(self, i):
        print (i.size)



mg = MazeGame()
maze = mg.createMazeStructure(2)
mg.drawMaze(2,maze)