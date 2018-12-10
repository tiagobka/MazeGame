from tkinter import *
keyboardKeys = \
    [
        ['q','w','e','r','t','y','u','i','o','p'],
        ['a','s','d','f','g','h','j','k','l','<--'],
        ['z','x','c','v','b','n','m','.','_','Enter'],
    ]


class VirtualKeyboard:
    text = ""
    cursor = [0, 0]
    def displayKeyboard(self, score=0):
        self.keyBoard = Tk()
        self.keyBoard.focus_force()
        self.keyBoard.protocol('WM_DELETE_WINDOW', self.done)
        self.keyBoard.bind("<Key>", self.screenEvent)
        self.keyBoard.title("You scored: " + str(score) + " points")
        label= Label(self.keyBoard,text = "What is your name?")
        label.grid(row=0,column=0, columnspan = 2)
        self.entry=Entry(self.keyBoard, text = "testing")
        self.entry.grid(row=0,column= 2,columnspan= 7,sticky=W+E)
        for i in range(len(keyboardKeys)):
            for j in range(len(keyboardKeys[i])):
                Button(self.keyBoard, text=keyboardKeys[i][j], width=10, command=lambda val= keyboardKeys[i][j]:self.virtualKeyPressed(val),activebackground="grey").grid(row=i+1, column=j)

        self.keyBoard.mainloop()
        return self.text


    def done(self,event=None):
        test = self.entry
        self.text = test.get()
        self.keyBoard.quit()
        self.keyBoard.destroy()

    def screenEvent(self,event):



       # print(event.keycode)
        row = self.cursor[0]
        col = self.cursor[1]
        if (event.keycode == 37):
            self.cursor = [row,(col-1)%10]

        if (event.keycode == 38):
            self.cursor = [((row-1)%3),col]

        if (event.keycode == 39):
            self.cursor = [row,(col + 1) % 10]

        if (event.keycode == 40):
            self.cursor = [((row+1)%3),col]

        row = self.cursor[0]
        col = self.cursor[1]
        for i in range(len(keyboardKeys)):
            for j in range(len(keyboardKeys[i])):
                self.keyBoard.grid_slaves(i+1,j)[0].config(state=NORMAL)
        self.keyBoard.grid_slaves(row+1,col)[0].config(state=ACTIVE)


        if (event.keycode ==27 or event.keycode ==32): #Enter or space pressed (B) button on controller
            self.done()
        elif (event.keycode ==8):
            prevTxt = self.entry.get()[:-1]
            self.entry.delete(0, END)
            # insert the new string, sans the last character
            self.entry.insert(0,prevTxt)
        elif(event.keycode == 13):
            #self.done()
            self.virtualKeyPressed(self.keyBoard.grid_slaves(self.cursor[0] + 1, self.cursor[1])[0].cget("text"))
        else:
            self.entry.insert(END, event.char)




    def virtualKeyPressed(self, val):
        if val == "<--":
            prevTxt = self.entry.get()[:-1]
            self.entry.delete(0, END)
            # insert the new string, sans the last character
            self.entry.insert(0, prevTxt)
        elif val == "Enter":
            self.done()
        else:
            self.entry.insert(END,val)







