import tkinter as tk
import numpy as np
import random

class SudokuGUI:

    def __init__(self, master):
        self.master = master
        master.title("Sudoku Solver")

        self.original_matrice = [[4, 5, 0, 2, 6, 0, 9, 0, 0],
                                 [0, 0, 0, 0, 0, 0, 0, 8, 4],
                                 [8, 1, 0, 0, 0, 7, 0, 0, 0],
                                 [0, 0, 3, 5, 8, 0, 4, 0, 7],
                                 [7, 0, 0, 3, 0, 0, 1, 6, 8],
                                 [9, 8, 0, 7, 4, 6, 0, 5, 0],
                                 [6, 7, 2, 8, 0, 0, 3, 0, 0],
                                 [0, 0, 0, 1, 9, 2, 0, 0, 6],
                                 [0, 9, 8, 6, 7, 3, 5, 0, 2]]
        self.matrice = np.copy(self.original_matrice).tolist()

        self.cells = [[tk.Entry(master, width=2, font=("Arial", 24), borderwidth=1, justify='center') for _ in range(9)] for _ in range(9)]

        for i in range(9):
            for j in range(9):
                self.cells[i][j].grid(row=i, column=j)
                if self.matrice[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.matrice[i][j]))
                    self.cells[i][j].config(state='normal')
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for row in range(3):
                    for col in range(3):
                        self.cells[i + row][j + col].grid(padx=(0, 2), pady=(0, 2),ipadx=5, ipady=5)
                for row in range(1, 3):
                    for col in range(1, 3):
                        self.cells[i + row][j + col].grid(padx=(0, 2), pady=(0, 2),ipadx=5, ipady=5)

        self.solve_button = tk.Button(master, text="Solve", command=self.solve_gui)
        self.solve_button.grid(row=9, column=0, columnspan=4)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.grid(row=9, column=5, columnspan=4)

        self.regenerer_button = tk.Button(master, text="Regenerer", command=self.regenerer)
        self.regenerer_button.grid(row=10, column=2, columnspan=4)

    def possible(self, row, column, number):
        for i in range(9):
            if self.matrice[row][i] == number or self.matrice[i][column] == number:
                return False

        y0 = (row // 3) * 3
        x0 = (column // 3) * 3

        for i in range(3):
            for j in range(3):
                if self.matrice[y0+i][x0+j] == number:
                    return False
        return True

    def solve(self):
        for i in range(9):
            for j in range(9):
                if self.matrice[i][j] == 0:
                    for num in range(1, 10):
                        if self.possible(i, j, num):
                            self.matrice[i][j] = num
                            if self.solve():
                                return True
                            self.matrice[i][j] = 0
                    return False
        return True

    def regenerer(self):
        self.matrice = np.zeros((9, 9))
        self.solve()

        for i in range(1,9):
            for j in range(1,9):
                x = random.randint(0, 1)
                if x == 1:
                    self.matrice[i][j] = 0
        print(self.matrice)

        # Arrondir les valeurs de la matrice à des entiers
        self.matrice = np.round(self.matrice).astype(int)

        for i in range(9):
            for j in range(9):
                if self.matrice[i][j] != 0:
                    self.cells[i][j].delete(0, 'end')
                    self.cells[i][j].insert(0, str(self.matrice[i][j]))
                    self.cells[i][j].config(state='normal')
                else:
                    self.cells[i][j].delete(0, 'end')
                    self.cells[i][j].config(state='normal')

        # Ajouter des bordures épaisses pour marquer les limites des sous-grilles 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                for row in range(3):
                    for col in range(3):
                        self.cells[i + row][j + col].grid(padx=(0, 2), pady=(0, 2))
                for row in range(1, 3):
                    for col in range(1, 3):
                        self.cells[i + row][j + col].grid(padx=(0, 2), pady=(0, 2))

        return self.matrice

    def solve_gui(self):
        if self.solve():
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].delete(0, 'end')
                    self.cells[i][j].insert('end', str(self.matrice[i][j]))

    def reset(self):
        self.matrice = np.copy(self.original_matrice).tolist()
        for i in range(9):
            for j in range(9):
                self.cells[i][j].delete(0, 'end')
                if self.matrice[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.matrice[i][j]))
                else:
                    self.cells[i][j].config(state='normal')

root = tk.Tk()
my_gui = SudokuGUI(root)
root.mainloop()
