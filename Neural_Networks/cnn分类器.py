#!/usr/bin/env python
# coding: utf-8


import torch
import torchvision
import torchvision.transforms as transforms
from tqdm import tqdm


transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
     ]
)

# 训练数据集
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                        download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=16,
                                          shuffle=True, num_workers=0)

# 测试数据集
testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                       download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=16,
                                         shuffle=False, num_workers=0)



import matplotlib.pyplot as plt
import numpy as np

#get_ipython().run_line_magic('matplotlib', 'inline')

'''
def imshow(img):
    # 输入数据: torch.tensor [c, h, w]
    img = img / 2 + 0.5
    nping = img.numpy()
    nping = np.transpose(nping, (1, 2, 0))  # [h,w,c]
    plt.imshow(nping)


dataiter = iter(trainloader)  # 随机加载一个mini batch
images, labels = dataiter.next()

imshow(torchvision.utils.make_grid(images))'''


import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self):  # 定义神经网络结构, 输入数据 3x32x32
        super(Net, self).__init__()
        # 第一层（卷积层）
        self.conv1 = nn.Conv2d(3, 6, 3)  # 输入频道3， 输出频道6， 卷积3x3
        # 第二层（卷积层）
        self.conv2 = nn.Conv2d(6, 16, 3)  # 输入频道6， 输出频道16， 卷积3x3
        # 第三层（全连接层）
        self.fc1 = nn.Linear(16 * 28 * 28, 512)  # 输入维度16x28x28=12544，输出维度 512
        # 第四层（全连接层）
        self.fc2 = nn.Linear(512, 64)  # 输入维度512， 输出维度64
        # 第五层（全连接层）
        self.fc3 = nn.Linear(64, 10)  # 输入维度64， 输出维度10

    def forward(self, x):  # 定义数据流向
        x = self.conv1(x)
        x = F.relu(x)

        x = self.conv2(x)
        x = F.relu(x)

        x = x.view(-1, 16 * 28 * 28)
        x = self.fc1(x)
        x = F.relu(x)

        x = self.fc2(x)
        x = F.relu(x)

        x = self.fc3(x)

        return x


net = Net()
print(net)

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.0001, momentum=0.9)


train_loss_hist = []
test_loss_hist = []

for epoch in tqdm(range(20)):
    # 训练
    net.train()
    running_loss = 0.0
    for i, data in enumerate(trainloader,start=0):
        images, labels = data
        outputs = net(images)
        loss = criterion(outputs, labels)  # 计算损失

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (i % 1000 == 0):
            print('Epoch: %d,Step: %d,Loss: %.3f' % (epoch, i, loss.item()))

        running_loss += loss.item()
        if (i % 250 == 0):  # 每250 mini batch 测试一次
            correct = 0.0
            total = 0.0

            net.eval()
            with torch.no_grad():
                for test_data in testloader:
                    test_images, test_labels = test_data
                    test_outputs = net(test_images)
                    test_loss = criterion(test_outputs, test_labels)

            train_loss_hist.append(running_loss / 250)
            test_loss_hist.append(test_loss.item())
            running_loss = 0.0


plt.figure()
#plt.plot(temp)
plt.plot(test_loss_hist)
plt.legend(('train loss', 'test loss'))
plt.title('Train/Test Loss')
plt.xlabel('# mini batch *250')
plt.ylabel('Loss')
