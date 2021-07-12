# Write your code here
import numpy as np

class Solver:
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    def __init__(self, x_, y_, width_, height_):
        self.start_x = x_
        self.start_y = y_
        self.width = width_
        self.height = height_

    def validateMove(self, bo, row, col):
        if row < self.height and row >= 0 and col < self.width and col >= 0 and bo[row, col] == 0:
            return True

    def solve(self, bo, row, col, counter):

        for i in range(8):
            if counter >= self.width * self.height + 1:
                return True
            new_x = row + self.move_x[i]
            new_y = col + self.move_y[i]
            if self.validateMove(bo, new_x, new_y):
                bo[new_x,new_y] = counter
                if self.solve(bo,new_x, new_y, counter+1):
                    return True
                bo[new_x,new_y] = 0
        return False

    def start(self):
        board = np.zeros((self.height, self.width))
        board[self.start_y, self.start_x] = 1
        if self.solve(board, self.start_y, self.start_x,2):
            return board
        else:
            return []

class Board:
     #   11     1
     # 10         2
     #      X
     # 8          4
     #   7      5
    directions_ = {"1": [1, 2], "2": [2, 1], "4": [2, -1], "5": [1, -2], "7": [-1, -2], "8": [-2, -1],
                   "10": [-2, 1], "11": [-1, 2]}

    def __init__(self, width_, height_):
        self.available_moves = -1
        self.moves = []
        self.width = width_
        self.height = height_
        self.uscores = len(str(width_ * height_))
        self.vert_uscores = len(str(height_))
        self.board = [["_" * self.uscores for x in range(0, width_)] for y_ in range(0, height_)]

    def make_move(self, x_, y_, letter_):
        self.board[self.height - y_][x_ - 1] = " " * (self.uscores - 1) + letter_

    def print_board(self):
        print(" " + "-" * (self.width * (self.uscores + 1) + 3))
        for n in range(0, self.height):
            print("{}{}| {} |".format(" " * (self.vert_uscores - len(str(self.height - n))), self.height - n, " ".join(self.board[n])))
        print("-" * (self.width * (self.uscores + 1) + 3))
        last_row = ""
        for n in range(1, self.width + 1):
            last_row += " " * (self.uscores - len(str(n))) + str(n) + " "

        print(" " * self.vert_uscores + "  " + last_row)

    def input_coordinates(self, message_):
        while True:
            print(message_)
            coords_ = input().split()
            if len(coords_) != 2:
                print("Invalid dimensions!")
                continue
            x_ = coords_[0]
            y_ = coords_[1]
            if not x_.isdigit() or not y_.isdigit():
                print("Invalid dimensions!")
                continue
            if self.check_coordinates(int(x_), int(y_)):
                return coords_
            else:
                print("Invalid dimensions!")
                continue

    def check_coordinates(self, x_, y_):
        if x_ not in range(1, self.width + 1) or y_ not in range(1, self.height + 1):
            return False
        if self.board[self.height - y_][x_ - 1] == " " * (self.uscores - 1) + "X":
            return False
        if self.board[self.height - y_][x_ - 1] == " " * (self.uscores - 1) + "*":
            return False
        return True

    def knight_move(self, x_, y_,):
        self.available_moves = 0
        self.moves = []
        for direction_ in self.directions_:
            xn_ = x_ + self.directions_[direction_][0]
            yn_ = y_ + self.directions_[direction_][1]
            if self.check_coordinates(xn_, yn_):
                value = self.count_move(xn_, yn_)
                self.make_move(xn_, yn_, str(value))
                self.available_moves += 1
                self.moves.append([xn_, yn_])

    def count_move(self, x_, y_):
        count_ = 0
        for direction_ in self.directions_:
            xn_ = x_ + self.directions_[direction_][0]
            yn_ = y_ + self.directions_[direction_][1]
            if self.check_coordinates(xn_, yn_):
                count_ += 1
        return count_

    def clear(self):
        for y_ in range(0, self.height):
            for x_ in range(0, self.width):
                if self.board[y_][x_].strip() == "X":
                    self.board[y_][x_] = " " * (self.uscores - 1) + "*"
                elif self.board[y_][x_].strip() != "X" and self.board[y_][x_].strip() != "*":
                    self.board[y_][x_] = "_" * self.uscores

    def player_move(self):
        while True:
            print("Enter your next move: ", end="")
            coords_ = input().split()
            if len(coords_) != 2:
                print("Invalid move!", end="")
                continue
            x_ = coords_[0]
            y_ = coords_[1]
            if not x_.isdigit() or not y_.isdigit():
                print("Invalid move!", end="")
                continue
            if not self.check_coordinates(int(x_), int(y_)):
                print("Invalid move!", end="")
                continue
            if str(self.board[self.height - int(y_)][int(x_) - 1].strip()).isdigit():
                return coords_
            else:
                print("Invalid move!", end="")
                continue

    # def best_move(self):
    #     self.moves.sort(key=lambda mov_: mov_[0], reverse=True)
    #     print(self.moves[0])
    #     return (self.moves[0])[1:]

    def solve_puzzle(self, board_, coords_):
        solutions = []

        for move in self.moves:
            if self.available_moves == 0:
                print("No solution exists!")
                return None

            board.clear()
            board.make_move(move[0], move[1], "X")
            board.knight_move(move[0], move[1])

            # if self.available_moves == 0 and not str(self.board).__contains__("_"):
            #     print("sol")
            #     print(solutions)
            #     return solutions
            # else:
            print(self.available_moves)
            print(self.print_board())
            if self.solve_puzzle([move[0], move[1]]):
                print("Solved")
                return "Solved"
            board.clear()
            self.board[self.height - move[1]][move[0] - 1] = "_" * self.uscores

        print("End recursion")
        return None

    def make_answer(self, board_):
        for y_ in range(0, self.height):
            for x_ in range(0, self.width):
                value_ = int(board_[y_][x_])
                self.board[y_][x_] = " " * (self.uscores - len(str(value_))) + str(value_)


def check_dimensions():
    while True:
        print("Enter your board dimensions:")
        d_ = input().split()
        if len(d_) != 2:
            print("Invalid dimensions!")
            continue
        x_ = d_[0]
        y_ = d_[1]
        if not x_.isdigit() or not y_.isdigit():
            print("Invalid dimensions!")
            continue
        if len(x_) > 2 or len(y_) > 2:
            print("Invalid dimensions!")
            continue
        if int(x_) < 1 or int(y_) < 1:
            print("Invalid dimensions!")
            continue
        return d_


def ask_try():
    while True:
        print("Do you want to try the puzzle? (y/n):")
        answer_ = input()
        if answer_ == "y" or answer_ == "n":
            return answer_
        print("Invalid option")

dimensions = check_dimensions()
board = Board(int(dimensions[0]), int(dimensions[1]))
coordinates = board.input_coordinates("Enter the knight's starting position:")
board.make_move(int(coordinates[0]), int(coordinates[1]), "X")
board.knight_move(int(coordinates[0]), int(coordinates[1]))

solver = Solver(int(coordinates[0]) - 1, board.height - int(coordinates[1]), int(dimensions[0]), int(dimensions[1]))
solution = solver.start()

answer = ask_try()
if answer == "n" and len(solution) == 0:
    print("No solution exists!")
elif answer == "n":
    print("Here's the solution!")
    board.make_answer(solution)
    board.print_board()
elif answer == "y" and len(solution) == 0:
    print("No solution exists!")
elif answer == "y":
    board.print_board()
    visited_square = 1
    while True:
        coordinates = board.player_move()
        board.clear()
        board.make_move(int(coordinates[0]), int(coordinates[1]), "X")
        board.knight_move(int(coordinates[0]), int(coordinates[1]))
        board.print_board()
        visited_square += 1
        if not str(board.board).__contains__("_"):
            print("What a great tour! Congratulations!")
            break
        if board.available_moves == 0:
            print("No more possible moves!")
            print("Your knight visited {} squares!".format(visited_square))
            break

