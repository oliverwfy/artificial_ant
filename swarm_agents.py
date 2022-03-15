
import numpy as np
import copy


class Ant:

    direction = ["north","east","south","west"]
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]

    def __init__(self, world):
        self.world = copy.deepcopy(world)

        self.matrix_row = len(self.world)
        self.matrix_col = len(self.world[0])

        self.dir = 1
        self.moves = 0
        self.row = 0
        self.col = 0
        self.location_food = set()

    def position(self):
        return (self.row, self.col)

    def left(self):
        self.dir = (self.dir - 1) % 4
        self.move()

    def right(self):
        self.dir = (self.dir + 1) % 4
        self.move()


    def forward(self):
        self.move()


    def move(self):

        self.moves += 1

        ahead_row = self.row + self.dir_row[self.dir]
        ahead_col = self.col + self.dir_col[self.dir]

        self.row = ahead_row if ahead_row < self.matrix_row and ahead_row >= 0 else self.row
        self.col = ahead_col if ahead_col < self.matrix_col and ahead_col >= 0 else self.col

    def update_evidence(self, location):
        self.location_food.add(location)

    def broadcast(self):
        return self.location_food

    def sense_food(self):

        new_row = self.row + self.dir_row[self.dir]
        new_col = self.col + self.dir_col[self.dir]


        ahead_row = new_row if new_row < self.matrix_row and new_row >= 0 else self.row
        ahead_col = new_col if new_col < self.matrix_col and new_col >= 0  else self.col

        if self.world[ahead_row][ahead_col] == "food":
            self.location_food.add((ahead_row,ahead_col))

        return True if self.world[ahead_row][ahead_col] == "food" else False


    def random_walk(self, prob_turning):
        if np.random.random() < prob_turning:
            self.left()

        elif np.random.random() < 2*prob_turning:
            self.right()

        else:
            self.forward()


        return self.position(), self.location_food




def parse_matrix(matrix):

    world = []
    for i, line in enumerate(matrix):
        world.append(list())
        for j, col in enumerate(line):
            if col == "#":
                world[-1].append("food")
            elif col == ".":
                world[-1].append("empty")
            elif col == "S":
                world[-1].append("empty")

    return world


with open("santafe_trail.txt") as matrix:
    world = parse_matrix(matrix)














