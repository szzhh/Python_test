from collections import namedtuple
import datetime
import os, time
import numpy as np

import gym
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data.sampler import BatchSampler, SubsetRandomSampler
from tensorboardX import SummaryWriter
#########################################
# 请补充第59，104，109，113，114，116行代码
#########################################
if torch.cuda.is_available():
    device = torch.device("cuda:0")
print(device)

# Hyper-parameters
seed = 1              # 随机因子
render = True    #是否显示图形化界面
num_episodes = 2000   # 训练周期
env = gym.make('MountainCar-v0').unwrapped
num_state = env.observation_space.shape[0]
num_action = env.action_space.n
torch.manual_seed(seed)
#env.seed(seed)

Transition = namedtuple('Transition', ['state', 'action', 'reward', 'next_state'])


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(num_state, 100)
        self.fc2 = nn.Linear(100, num_action)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        action_prob = self.fc2(x)
        return action_prob


class DQN():
    capacity = 10000
    learning_rate = 1e-3    # 学习率
    memory_count = 0
    batch_size = 256
    gamma = 0.999          # 折扣因子
    update_count = 0

    def __init__(self):
        super(DQN, self).__init__()
        self.target_net, self.act_net = Net(), Net()
        self.target_net.to(device)
        self.act_net.to(device)
        self.memory = [None] * self.capacity
        self.optimizer = optim.Adam(self.act_net.parameters(), self.learning_rate)
        self.loss_func = nn.MSELoss()
        self.loss_func = self.loss_func.to(device)
        now_time = datetime.datetime.now().strftime('%Y%m%d_%H%M')
        self.writer = SummaryWriter('./logs_gamma/1_999/')

    def select_action(self, state):
        state = torch.tensor(state, dtype=torch.float).unsqueeze(0).to(device)
        # 请补充第59行代码，主网络以环境状态作为输入
        value = self.act_net(state)
        action_max_value, index = torch.max(value, 1)
        action = index.item()
        if np.random.rand(1) >= 0.9:  # epslion greedy
            action = np.random.choice(range(num_action), 1).item()
        return action

    def store_transition(self, transition):
        index = self.memory_count % self.capacity
        self.memory[index] = transition
        self.memory_count += 1
        return self.memory_count >= self.capacity

    def update(self):
        if self.memory_count >= self.capacity:
            state = torch.tensor(np.array([t.state for t in self.memory])).float().to(device)
            action = torch.LongTensor(np.array([t.action for t in self.memory])).view(-1, 1).long().to(device)
            reward = torch.tensor(np.array([t.reward for t in self.memory])).float().to(device)
            next_state = torch.tensor(np.array([t.next_state for t in self.memory])).float().to(device)

            # reward = (reward - reward.mean()) / (reward.std() + 1e-7)
            with torch.no_grad():
                target_v = reward + self.gamma * self.target_net(next_state).max(1)[0]

            # Update...
            for index in BatchSampler(SubsetRandomSampler(range(len(self.memory))), batch_size=self.batch_size,
                                    drop_last=False):
                v = (self.act_net(state).gather(1, action))[index]
                loss = self.loss_func(target_v[index].unsqueeze(1), (self.act_net(state).gather(1, action))[index])
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                self.writer.add_scalar('loss/value_loss', loss, self.update_count)
                self.update_count += 1
                if self.update_count % 100 == 0:
                    self.target_net.load_state_dict(self.act_net.state_dict())
        else:
            print("Memory Buff is too less")


def main():
    agent = DQN()
    for i_ep in range(num_episodes):
        re = 0
        # 请补充第104行代码，在每一个训练周期伊始，需对环境初始化
        state = env.reset(seed=seed)
        if render: env.render()
        for t in range(1000):
            action = agent.select_action(state)
            # 请补充第109行代码，智能体动作作用于环境，环境返回新的状态和奖励
            next_state, reward, done, info = env.step(action)
            re += reward
            if render: env.render()
            # 请补充第113和第114行代码，储存状态转移样本：旧状态、动作、奖励、新状态
            transition = Transition(state, action, reward, next_state)
            agent.store_transition(transition)
            # 请补充第116行代码，更新环境状态
            state = next_state
            if done or t >= 999:
                agent.writer.add_scalar('live/finish_step', t + 1, global_step=i_ep)
                agent.writer.add_scalar('live/training_reward', re, global_step=i_ep)
                agent.update()
                if i_ep % 10 == 0:
                    print("episodes {}, step is {} ".format(i_ep, t))
                break


if __name__ == '__main__':
    starttime = time.time()
    main()
    endtime = time.time()
    print('Time:', round(endtime-starttime, 2), 'secs')
