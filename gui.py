from tkinter import Button, Frame, Label, Menu, Tk
from tkinter.constants import LEFT, RIDGE, TOP
from tkinter.messagebox import askokcancel, askyesno, showinfo
from random import sample
from time import time
from copy import deepcopy
from functools import partial

class App:
    def __init__(self) -> None:
        '''
        This is the initialization of the class. It sets the basic properties for the tkinter window and then calls out other functions in order to create the complete game.
        '''

        self.root = Tk()

        self.root.title("Sudoku")
        self.root.geometry("320x480+480+120")
        self.root.config(bg="#818181")
        self.root.resizable(False, False)

        self.board, self.sol = self.createGame()
        self.grid, self.nums = [[] for i in range(9)], []
        self.cur, self.erase = ' ', False
        self.start = time()

        self.createMenu()
        self.createBoard()

    def createMenu(self) -> None:
        '''
        It creates the menubar of the tkinter window.
        '''

        menubar = Menu(self.root)
        menubar.add_command(label="New Game", command=partial(self.changeGame, 0))
        menubar.add_command(label="Restart", command=partial(self.changeGame, 1))
        menubar.add_command(label="Eraser", command=self.eraser)
        menubar.add_command(label="Check", command=self.checkStatus)
        self.root.config(menu=menubar)

    @staticmethod
    def createGame() -> list:
        '''
        It creates the sudoku and returns two lists, one of which is the display grid and the other one is the solution set to the puzzle.
        '''

        row, col = [[i * 3 + j for i in sample(range(3), 3) for j in sample(range(3), 3)] for k in range(2)]
        num = sample(range(1, 10), 9)
        board = [[num[(3*(r%3)+r//3+c)%9] for c in col] for r in row]
        sol = deepcopy(board)

        for i in sample(range(81), 51):
            board[i//9][i%9] = ' '

        return board, sol

    def createBoard(self) -> None:
        '''
        It creates the all the widgets that are to be enclosed within the window. Basically it creates the grid of numbers, all input options and the required buttons
        '''

        for i, item in enumerate(self.board):
            if (i % 3 == 0):
                self.createSpace(self.root, TOP)
            frame = Frame(self.root, bg="#818181")
            frame.pack(side=TOP)
            for j in range(9):
                if (j % 3 == 0 and j != 0):
                    self.createSpace(frame, LEFT)
                self.grid[i].append(Button(frame, text=item[j], width=2, height=1, bg='#000000', fg='#ffffff', font=('arial', 12, 'bold'), relief=RIDGE, cursor="hand2", command=partial(self.enterNumber, i, j)))
                self.grid[i][j].pack(side=LEFT, padx=1, pady=1)
                if (item[j] != ' '):
                    self.grid[i][j].config(activebackground='#ff0000')

        frame = Frame(self.root, bg="#818181")
        frame.pack(side=TOP)
        for i in range(9):
            self.nums.append(Button(frame, text=i+1, width=2, height=1, bg='#6688ff', fg='#ffffff', font=('arial',12 , 'bold'), relief=RIDGE, cursor="hand2", command=partial(self.setNumber, i+1)))
            self.nums[i].pack(side=LEFT, padx=2, pady=12)
        
        frame = Frame(self.root, bg="#818181")
        frame.pack(side=TOP)
        for i in (("Finish", self.finishGame), ("Exit", self.exitGame)):
            Button(frame, text=i[0], width=8, font=('arial', 13), relief=RIDGE, cursor="hand2", command=i[1]).pack(side=LEFT, padx=15, pady=10)

    def enterNumber(self, i, j) -> None:
        '''
        It replaces the blank space to a number in the grid. Just by clicking on any the buttons in the grid the blank space is replaced by the selected number from the input options.
        '''

        btn = self.board[i][j]
        if self.cur != ' ' and btn == ' ':
            self.grid[i][j].config(text=self.cur, bg="#6688ff")
        if self.erase == True and self.board[i][j] == ' ':
            self.grid[i][j].config(text=' ', bg="#000000")

    def setNumber(self, num) -> None:
        '''
        It sets the current input number from the input options.
        '''

        self.erase = False
        if (self.cur != ' '):
            self.nums[self.cur-1].config(bg="#6688ff")
        self.cur = num
        self.nums[num-1].config(bg="#000000")
        for i in self.grid:
            for j in i:
                if j["text"] == num:
                    j.config(bg="#6688ff")
                else:
                    j.config(bg="#000000")

    def changeGame(self, choice) -> None:
        '''
        It is used to create a new game or restart the previous game.
        '''

        if choice == 0:
            self.board, self.sol = self.createGame()
        else:
            pass
        for i, item in enumerate(self.grid):
            for j in range(9):
                num = self.board[i][j]
                if num != ' ':
                    item[j].config(text=num, bg="#000000", activebackground="#ff0000")
                else:
                    item[j].config(text=num, bg="#000000", activebackground="#ffffff")
            self.nums[i].config(bg="#6688ff")

    def eraser(self) -> None:
        '''
        It is used to erase any number on the grid as the name suggests.
        '''

        self.cur, self.erase = ' ', True
        for i in range(9):
            self.nums[i].config(bg="#6688ff")
            for j in range(9):
                self.grid[i][j].config(bg="#000000")

    def checkStatus(self) -> None:
        '''
        It checks whether the user is going correct or wrong.
        '''

        self.cur = ' '
        for i in range(9):
            self.nums[i].config(bg="#6688ff")
            for j in range(9):
                btn = self.grid[i][j]
                if btn["text"] != self.sol[i][j] and btn["text"] != ' ':
                    btn.config(bg="#ff0000")
                else:
                   btn.config(bg="#000000")

    def finishGame(self) -> None:
        '''
        It ends the game when the sudoku is complete.
        '''

        flag = 0
        for i in range(9):
            for j in range(9):
                if self.grid[i][j]["text"] != self.sol[i][j]:
                    flag = 1
                    break
        if flag == 1:
            showinfo("Error", "Game is not over yet")                    
        else:
            ch = askokcancel("Game Over", f"You have completed the game.\n\nTime taken : {self.timeTaken(self.start, time())} seconds\n\nDo you wish to restart?")
            if ch == 1:
                self.changeGame(1)
            else:
                self.root.destroy()

    def exitGame(self) -> None:
        '''
        It helps in exiting the game.
        '''

        ch = askyesno("Confirm Exit", "Are you sure you want to leave?")
        if ch == 1:
            self.root.destroy()

    @staticmethod
    def createSpace(frame, side) -> None:
        '''
        It is used to create blank spaces the grid to make it more neat.
        '''

        l = Label(frame, bg="#818181", font=("arial", 3))
        l.pack(side=side)

    @staticmethod
    def timeTaken(beg, end) -> int:
        return int(end - beg)

if __name__ == "__main__":
    app = App()
    app.root.mainloop()