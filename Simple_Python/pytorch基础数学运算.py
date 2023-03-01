#!/usr/bin/env python
# coding: utf-8

# In[1]:


import torch


# In[2]:


#定义向量
vector = torch.tensor([1,2,3,4])
print('Vector:\t\t', vector)
print('Vector Shape:\t', vector.shape)


# In[3]:


#定义矩阵
matrix = torch.tensor([[1,2],[3,4]])
print('Matrix:\n', matrix)
print('Matirx Shape:\n', matrix.shape)


# In[4]:


#定义张量
tensor = torch.tensor([[[1,2],[3,4]],[[1,2],[3,4]]])
print('Tensor:\n', tensor)
print('Tensor Shape:\n', tensor.shape)


# In[ ]:




