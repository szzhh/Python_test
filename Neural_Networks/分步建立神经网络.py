import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self): #定义神经网络结构, 输入数据 1x32x32
        super(Net, self).__init__()
        # 第一层（卷积层）
        self.conv1 = nn.Conv2d(1,6,3) #输入频道1， 输出频道6， 卷积3x3
        # 第二层（卷积层）
        self.conv2 = nn.Conv2d(6,16,3) #输入频道6， 输出频道16， 卷积3x3
        # 第三层（全连接层）
        self.fc1 = nn.Linear(16*28*28, 512) #输入维度16x28x28=12544，输出维度 512
        # 第四层（全连接层）
        self.fc2 = nn.Linear(512, 64) #输入维度512， 输出维度64
        # 第五层（全连接层）
        self.fc3 = nn.Linear(64, 2) #输入维度64， 输出维度2
    
    def forward(self, x): #定义数据流向
        x = self.conv1(x)
        x = F.relu(x)
        
        x = self.conv2(x)
        x = F.relu(x)
        
        x = x.view(-1, 16*28*28)
        x = self.fc1(x)
        x = F.relu(x)
        
        x = self.fc2(x)
        x = F.relu(x)
        
        x = self.fc3(x)
        
        return x
        
net = Net()
print(net)


#生成随机输入
input_data = torch.randn(1,1,32,32) 
print(input_data)
print(input_data.size())

# 运行神经网络
out = net(input_data)
print(out)
print(out.size())

# 随机生成真实值
target = torch.randn(2)
target = target.view(1,-1)
print(target)


criterion = nn.L1Loss() # 定义损失函数
loss = criterion(out, target) # 计算损失
print(loss)


# 反向传递
net.zero_grad() #清零梯度
loss.backward() #自动计算梯度、反向传递

import torch.optim as optim

optimizer = optim.SGD(net.parameters(), lr=0.01)
optimizer.step()


out = net(input_data)
print(out)
print(out.size())
