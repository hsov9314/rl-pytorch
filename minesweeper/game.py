import pygame
from minesweeper.piece import Piece
from minesweeper.board import Board
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2

# from solver import Solver
from time import sleep


class MineSweeper:
    def __init__(self, size, prob):
        self.size, self.prob = size, prob
        self.board = Board(size, prob)
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        os.environ["SDL_VIDEODRIVER"] = "dummy"

        self.sizeScreen = 400, 400
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (self.sizeScreen[0] / size[1], self.sizeScreen[1] / size[0])
        self.loadPictures()
        self.running = True
        self.step = 0

        # 押せるマスのリスト list<x: int, y: int>
        self.unrevealed_piece = self.board.getUnrevealedPieces()
        # self.solver = Solver(self.board)

    def reset(self):
        self.board = Board(self.size, self.prob)
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        self.screen = pygame.display.set_mode(self.sizeScreen)
        self.pieceSize = (
            self.sizeScreen[0] / self.size[1],
            self.sizeScreen[1] / self.size[0],
        )
        self.step = 0
        self.unrevealed_piece = self.board.getUnrevealedPieces()

    def loadPictures(self):
        self.images = {}
        imagesDirectory = "minesweeper/images"
        for fileName in os.listdir(imagesDirectory):
            if not fileName.endswith(".png"):
                continue
            path = imagesDirectory + r"/" + fileName
            img = pygame.image.load(path)
            img = img.convert()
            img = pygame.transform.scale(
                img, (int(self.pieceSize[0]), int(self.pieceSize[1]))
            )
            self.images[fileName.split(".")[0]] = img

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and not (
                    self.board.getWon() or self.board.getLost()
                ):
                    rightClick = pygame.mouse.get_pressed(num_buttons=3)[2]
                    self.handleClick(pygame.mouse.get_pos(), rightClick)
                # if event.type == pygame.KEYDOWN:
                #     self.solver.move()
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            if self.board.getWon():
                self.win()
                running = False
        pygame.quit()

    def play_step(self, index):
        """play_step
        play action
        return type:
        (
        unrevealed_piece: list<int, int>
        board_won: boolean
        board_lost: boolean
        step: int
        reward: int
        )
        """
        self.step += 1
        if self.board.getPiece(index).getClicked():
            return (
                self.unrevealed_piece,
                self.board.getWon(),
                self.board.lost,
                self.step,
                0,
            )
        self.handleClick(index, False)
        self.unrevealed_piece = self.board.getUnrevealedPieces()
        self.screen.fill((0, 0, 0))
        self.draw()
        pygame.display.flip()

        reward = 1 if self.board.won else (-1 if self.board.lost else 0)

        return (
            self.unrevealed_piece,
            self.board.getWon(),
            self.board.lost,
            self.step,
            reward,
        )

    def draw(self):
        topLeft = (0, 0)
        for row in self.board.getBoard():
            for piece in row:
                rect = pygame.Rect(topLeft, self.pieceSize)
                image = self.images[self.getImageString(piece)]
                self.screen.blit(image, topLeft)
                topLeft = topLeft[0] + self.pieceSize[0], topLeft[1]
            topLeft = (0, topLeft[1] + self.pieceSize[1])

    def getImageString(self, piece):
        if piece.getClicked():
            return (
                str(piece.getNumAround())
                if not piece.getHasBomb()
                else "bomb-at-clicked-block"
            )
        if self.board.getLost():
            if piece.getHasBomb():
                return "unclicked-bomb"
            return "wrong-flag" if piece.getFlagged() else "empty-block"
        return "flag" if piece.getFlagged() else "empty-block"

    def handleClick(self, index, flag):
        self.board.handleClick(self.board.getPiece(index), flag)

    def win(self):
        pass

    def get_screen(self, w, h):
        string_image = pygame.image.tostring(self.screen, "RGB")
        surface = pygame.image.fromstring(
            string_image, (self.sizeScreen[0], self.sizeScreen[1]), "RGB"
        )
        screen_image_array = pygame.surfarray.array3d(surface)

        # rotate image by 90 degree and flip to adjust
        screen_image_array = np.rot90(screen_image_array, 3)
        screen_image_array = np.fliplr(screen_image_array)

        # convert color image to greyscale image
        # original image's shape: (800, 800, 3)
        screen_image_array = np.dot(
            screen_image_array[..., :3], [0.2989, 0.5870, 0.1140]
        )

        # resize
        screen_image_array = cv2.resize(screen_image_array, (w, h))

        return screen_image_array


if __name__ == "__main__":
    import random

    w = 6
    h = 6
    game = MineSweeper([w, h], 0.1)
    while True:
        random.shuffle(game.unrevealed_piece)
        index = game.unrevealed_piece[0]
        choice, win, lost, step, reward = game.play_step(index)
        print("win:{} lost:{} step:{} reward:{}".format(win, lost, step, reward))
        # print(np.ravel(screen).shape)

        # skip game when lost at first step
        if step == 1 and lost:
            pygame.quit()
            game = MineSweeper([w, h], 0.1)
            continue

        if win or lost:
            pygame.quit()
            game = MineSweeper([w, h], 0.1)

        # plt.imshow(screen)
        plt.show()
