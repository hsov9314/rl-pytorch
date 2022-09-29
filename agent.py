from time import sleep
import time
import torch
import random
import numpy as np
from collections import deque
import cv2

# from game import SnakeGameAI, Direction, Point
from minesweeper.game import MineSweeper
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 400
LR = 0.0001


class Agent:
    def __init__(self, image_w, image_h, board_w, board_h):
        self.n_games = 0
        self.won_count = 0
        self.epsilon = 0.5  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(image_w * image_h, 256, board_w * board_h)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.board_w, self.board_h = board_w, board_h
        self.image_w, self.image_h = image_w, image_h

    def ms_get_state(self, game):
        screen = game.get_screen(self.image_w, self.image_h)
        screen = np.ravel(screen)
        return screen

    def remember(self, state, action, reward, next_state, done):
        self.memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, next_state, done in mini_sample:
        #     self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def ms_get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        # self.epsilon *= 0.9997
        final_move = np.zeros(self.board_h * self.board_w)

        if np.random.choice([True, False], p=[self.epsilon, 1 - self.epsilon]):
            move = random.randint(0, self.board_h * self.board_w) - 1
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        final_move = final_move.astype(np.int64)
        # print(final_move.dtype)
        return final_move

    def ms_mock_get_action(self, game):
        random.shuffle(game.unrevealed_piece)
        index = game.unrevealed_piece[0]
        return index

    def convert_index_to_vector(self, index, row, col):
        arr = np.zeros(row * col)
        arr_index = index[1] * col + index[0]
        arr[arr_index] = 1
        return arr

    def convert_vector_to_index(self, vector, row, col):
        vec_index = (vector == 1).nonzero()[0][0]
        index = [vec_index % row, vec_index // row]
        return index


def train():
    plot_scores = []

    image_w, image_h = 84, 84
    board_w, board_h = 6, 6
    mine_rate = 0.1
    agent = Agent(image_w=image_w, image_h=image_h, board_w=board_w, board_h=board_h)
    game = MineSweeper([board_w, board_h], mine_rate)
    while True:
        # get old state
        # state_old = agent.get_state(game)
        state_old = agent.ms_get_state(game)

        # get move
        # final_move = agent.get_action(state_old)
        # final_move = agent.ms_mock_get_action(game)
        final_move = agent.ms_get_action(state_old)
        index = agent.convert_vector_to_index(final_move, agent.board_h, agent.board_w)

        # perform move and get new state
        # reward, done, score = game.play_step(final_move)
        _, won, lost, _, reward = game.play_step(index)
        done = won or lost

        state_new = agent.ms_get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            if won:
                agent.won_count += 1
            agent.train_long_memory()

            # if score > record:
            #     record = score
            #     agent.model.save()
            # if won:
            #     agent.model.save()

            print(
                "n={}: win_rate={}".format(
                    agent.n_games, agent.won_count / agent.n_games
                )
            )
            # print("Game", agent.n_games, "Score", score, "Record:", record)
            # print(agent.won_count)
            # print(agent.n_games)
            plot_scores.append(agent.won_count / agent.n_games)
            # total_score += score
            # mean_score = total_score / agent.n_games
            # plot_mean_scores.append(mean_score)
            if agent.n_games % 100 == 0:
                plot(plot_scores, agent.n_games)


if __name__ == "__main__":
    train()
