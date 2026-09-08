import torch
import torch.nn as nn

class FNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(4, 16)
        self.fc2 = nn.Linear(16,8)
        self.fc3 = nn.Linear(8,3)
        
        self.relu = nn.ReLu()
    
    def forwar(self, x):
        x = self.relu(self.fc1)
        x = self.relu(self.fc2)
        x = self.fc3(x)
        
        return x
model =FNN()