import time
import torch
import random
import numpy as np
from collections import deque
from game import TargetGameAI, Eye_predict, Eye_real
from vision import Face
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.8
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(45, 135, 2)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, face):
        face.see()
        li = [[i.x, i.y, i.z] for i in face.points_list]
        end_li = [x for l in li for x in l]          
        return np.array(end_li)

    def remember(self, state, action,reward, next_state, done):
        self.memory.append((state, action,reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions,rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions,rewards, next_states, dones)

    def train_short_memory(self, state, action,reward, next_state, done):
        self.trainer.train_step(state, action,reward, next_state, done)

    def get_action(self, state):
        self.epsilon = 5 - self.n_games
        final_move = [960,540]
        # if False:
        if random.randint(0,200) < self.epsilon:
            move = [random.randint(-48,48), random.randint(-54,54)]            
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # move = torch.argmax(prediction).item()
            move = [prediction[0].item() * 1, prediction[1].item() * 1]
        
        final_move[0] += move[0] 
        final_move[1] += move[1] 
        print(final_move)
        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = -5000
    agent = Agent()
    face = Face()
    game = TargetGameAI()
    while True:

        state_old = agent.get_state(face)

        final_move = agent.get_action(state_old)

        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(face)

        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            time.sleep(1)
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record', record)
            
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()

    