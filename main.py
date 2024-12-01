import tkinter as tk
from tkinter import messagebox
import random


class FifteenGame:
    def __init__(self, root, size=4):
        self.root = root
        self.size = size
        self.board = self.create_board()
        self.buttons = []
        self.create_widgets()
        self.update_board()

    def create_board(self):
        numbers = list(range(1, self.size**2)) + [0]
        return [numbers[i:i + self.size] for i in range(0, len(numbers), self.size)]

    def create_widgets(self):
        for row in range(self.size):
            button_row = []
            for col in range(self.size):
                btn = tk.Button(
                    self.root,
                    font=("Arial Black", 20),  # Жирный шрифт
                    width=4,
                    height=2,
                    bg="#616161",  # Серый фон кнопки
                    fg="#FFFFFF",  # Белый текст
                    activebackground="#757575",  # Более светло-серый при нажатии
                    relief="flat",
                    command=lambda r=row, c=col: self.move_tile(r, c),
                )
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                button_row.append(btn)
            self.buttons.append(button_row)


        control_frame = tk.Frame(self.root, bg="#424242")  # Темно-серый фон рамки
        control_frame.grid(row=self.size, column=0, columnspan=self.size, pady=10)

        # Кнопка перемешивания
        shuffle_btn = tk.Button(
            control_frame,
            text="Mix",
            font=("Arial Black", 14),
            command=self.shuffle_board,
            bg="#616161",
            fg="#FFFFFF",
            activebackground="#757575",
            relief="flat",
            width=10,
            height=1,
        )
        shuffle_btn.pack(pady=10)

    def update_board(self):
        for row in range(self.size):
            for col in range(self.size):
                value = self.board[row][col]
                btn = self.buttons[row][col]
                if value == 0:
                    btn.config(text="", state="disabled", bg="#424242")
                else:
                    btn.config(text=str(value), state="normal", bg="#616161", fg="#FFFFFF")

    def move_tile(self, row, col):
        empty_row, empty_col = self.find_empty()
        if abs(empty_row - row) + abs(empty_col - col) == 1:  # Проверка соседства
            self.board[empty_row][empty_col], self.board[row][col] = self.board[row][col], self.board[empty_row][empty_col]
            self.update_board()
            if self.check_victory():
                messagebox.showinfo("Congratulations!", "You solved the puzzle!")
                self.shuffle_board()

    def find_empty(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    return row, col

    def check_victory(self):
        flat = sum(self.board, [])
        return flat[:-1] == list(range(1, self.size**2))

    def shuffle_board(self):
        empty_row, empty_col = self.find_empty()
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for _ in range(100):
            random.shuffle(moves)
            for dr, dc in moves:
                new_row, new_col = empty_row + dr, empty_col + dc
                if 0 <= new_row < self.size and 0 <= new_col < self.size:
                    self.board[empty_row][empty_col], self.board[new_row][new_col] = \
                        self.board[new_row][new_col], self.board[empty_row][empty_col]
                    empty_row, empty_col = new_row, new_col
                    break

        self.update_board()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Barley-break")
    root.configure(bg="#424242")

    for i in range(4):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    game = FifteenGame(root)
    root.mainloop()
