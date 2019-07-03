from Board import Board
from Cube import Cube
from Player import Player
from settings import *
import numpy as np
import pygame

class Env():
    def __init__(self, size: int):
        self.size = size

    def reset(self):
        self.player = Player((10, 10), 2)
        self.board = Board(self.size)
        self.board.place_snack(self.player.body)
        return self.state()


    def state(self):
        position = self.player.body[0]
        up = 0
        if (position[1] == 0):
            up = 1

        right = 0
        if (position[0] == SIZE - 1):
            right = 1

        down = 0
        if (position[1] == SIZE - 1):
            down = 1

        left = 0
        if (position[0] == 0):
            left = 1

        state = np.array([up, right, down, left])
        state = np.roll(state, -1 * self.player.action + 1)
        state = np.delete(state, 2)  # remove down
        return state


    def step(self, action: int):
        self.player.move(action)
        r = self.player.update(self.board)
        done = self.player.alive == False
        return self.state(), r, done


    def sprites(self):
        sprites = pygame.sprite.Group()
        if (self.player.alive):
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)

        for position in self.player.body:
            cube = Cube(position, color)
            sprites.add(cube)

        sprites.add(Cube(self.board.snack, (0, 255, 0)))
        return sprites
