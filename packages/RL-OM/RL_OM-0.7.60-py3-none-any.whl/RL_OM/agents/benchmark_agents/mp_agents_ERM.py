# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/agents/benchmark_agents/03_ERM_agents_multi_period_heuristic.ipynb.

# %% auto 0
__all__ = ['FakePolicy', 'NewsvendorData', 'LinearModel', 'MLP', 'SGDBase', 'LERMsgdAgent_MP', 'MLPsgdAgent']

# %% ../../../nbs/agents/benchmark_agents/03_ERM_agents_multi_period_heuristic.ipynb 4
# General libraries:
import numpy as np
from scipy.stats import norm
from tqdm import trange

# Torch
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

# Mushroom libraries
from mushroom_rl.core import Agent

# %% ../../../nbs/agents/benchmark_agents/03_ERM_agents_multi_period_heuristic.ipynb 6
class FakePolicy():
    def reset(*args, **kwargs):
        pass

class NewsvendorData(Dataset):

    def __init__(self, x, y):
        # create torch tensors
        self.x=torch.from_numpy(x)
        self.y=torch.from_numpy(y)
        
        # convert to torch float32
        self.x=self.x.float()
        self.y=self.y.float()

        self.n_samples=y.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

class LinearModel(nn.Module):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.l1=nn.Linear(input_size, output_size)

    def forward(self, x):
        out=self.l1(x)
        return out

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, num_hidden_layers=3, drop_prob=0.0):
        super().__init__()

        # List of layers
        layers = []

        # Input layer
        layers.append(nn.Linear(input_size, hidden_size))
        layers.append(nn.ReLU())
        layers.append(nn.Dropout(p=drop_prob))

        # Hidden layers
        for _ in range(num_hidden_layers-1): 
            layers.append(nn.Linear(hidden_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(p=drop_prob))

        # Output layer
        layers.append(nn.Linear(hidden_size, output_size))

        # Combine layers
        self.model = nn.Sequential(*layers)

    def forward(self, x):
        return self.model(x)

    
class SGDBase(Agent):

    def __init__(self, input_size, hidden_size=64, output_size=1, learning_rate=0.01, num_hidden_layers=3, drop_prob=0.0, l2_reg=0.0):
        if self.model_type=="Linear":
            #super(LinearModel, self).__init__(input_size, output_size)
            self.model=LinearModel(input_size, output_size)
        elif self.model_type=="MLP":
            self.model=MLP(input_size, hidden_size, output_size, num_hidden_layers=num_hidden_layers, drop_prob=drop_prob)
            #super(MLP, self).__init__(input_size, hidden_size, output_size)
        
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=l2_reg)
        self.criterion = nn.MSELoss()


    def fit(self, X_train, y_train, cu, co, batch_size=64, learning_rate=0.01, device="cpu"):
        
        if y_train.ndim == 1:
            y_train = y.reshape(-1, 1)
        
        dataset_train=NewsvendorData(X_train, y_train)
        
        n_features = X_train.shape[1]
        n_outputs = y_train.shape[1]

        self.model.to(device)

        train_loader=DataLoader(dataset=dataset_train, batch_size=batch_size, shuffle=True)

        self.model.train()

        for i, (feat, labels) in enumerate(train_loader):

                feat=feat.to(device)
                labels=labels.to(device)

                outputs=self.model(feat)
                loss = torch.mean(SGDBase.pinball_loss(cu, co, labels, outputs))

                #backward
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        self.model.eval()

        return self.model

    def predict(self, X):
        self.model.eval()
        with torch.no_grad():
            X=torch.from_numpy(X)
            X=X.float()
            output=self.model(X)
            output=output.numpy()

        return output

    def train(self):
        self.model.train()
    
    def eval(self):
        self.model.eval()   
    
    ### Helper functions

    @staticmethod
    def max_or_zero(data):
        length=data.shape[0]
        value, _ = torch.max(torch.cat((data,torch.zeros(size=(length,1))),dim=1), dim=1, out=None)
        return value

    @staticmethod
    def pinball_loss(cu, co, demand, order_quantity):

        cu = torch.tensor(cu, dtype=torch.float32)
        co = torch.tensor(co, dtype=torch.float32)

        underage=cu*SGDBase.max_or_zero(demand-order_quantity)
        overage=co*SGDBase.max_or_zero(order_quantity-demand)
        loss=underage+overage
        return loss

class LERMsgdAgent_MP(SGDBase):
    def __init__(self,
                    input_size,
                    output_size,
                    cu,
                    co,
                    l,
                    batch_size=128,
                    learning_rate=0.01,
                    device="cpu",
                    agent_name = "LERM"
                    ):
        self.name=agent_name
        self.model_type="Linear"
        self.cu = cu
        self.co = co
        self.device = device
        self.batch_size=batch_size
        self.learning_rate=learning_rate
        self.device=device
        self.lead_time = l
        self.num_products = l.shape[0]
        self.max_lead_time = l.max()
        self.num_features = input_size[0] - self.num_products - self.num_products*self.max_lead_time

        self.policy=FakePolicy()
        self._postprocessors = list()
        self._preprocessors = list()
        self.train_directly=True
        self.train_mode = "epochs"

        # Note that the agent currently only works for vector inputs
        super().__init__(input_size=self.num_features, hidden_size=None, output_size=output_size, learning_rate=learning_rate)

    def fit_epoch(self, features_train, demand_train):

        demand_aggregated = np.zeros((demand_train.shape[0]-self.max_lead_time, demand_train.shape[1]))

        for i in range(demand_train.shape[1]):
            for j in range(demand_aggregated.shape[0]):
                demand_aggregated[j,i] = np.sum(demand_train[j:j+self.lead_time[i]+1,i])

        super().fit(features_train, demand_aggregated, cu=self.cu, co=self.co, batch_size=self.batch_size, learning_rate=self.learning_rate, device=self.device)

    def draw_action(self, X):

        inventory = X[self.num_features:self.num_features+self.num_products]
        pipeline = np.zeros((self.num_products, self.max_lead_time))
        for i in range(self.num_products):
            pipeline[i,:] = X[self.num_features+self.num_products+i*self.max_lead_time:self.num_features+self.num_products+(i+1)*self.max_lead_time]

        # print("pipeline: ", pipeline)
        # print("inventory: ", inventory)

        virtual_inventory_position = np.sum(pipeline, axis=1)

        total_inventory_position = inventory + virtual_inventory_position

        X = X[:self.num_features]
        
        q = super().predict(X)

        # print("gross order: ", q)

        q = q - total_inventory_position
        # print("total inventory: ", total_inventory_position)

        q = np.maximum(q, 0)
        # print("new order: ", q)

        return q

class MLPsgdAgent(SGDBase):
    def __init__(self,
                    input_size,
                    output_size,
                    cu,
                    co,
                    hidden_size=64,
                    batch_size=128,
                    learning_rate=0.01,
                    device="cpu",
                    agent_name = "DLNV",
                    num_hidden_layers=3,
                    drop_prob=0.0,
                    l2_reg=0.0,
                    ): 
        
        self.name=agent_name
        self.model_type="MLP"
        self.cu = cu
        self.co = co
        self.device = device
        self.hidden_size = hidden_size
        self.batch_size=batch_size
        self.learning_rate=learning_rate
        self.device=device

        self.policy=FakePolicy()
        self._postprocessors = list()
        self._preprocessors = list()
        self.train_directly=True
        self.train_mode = "epochs"

        super().__init__(input_size=input_size, hidden_size=hidden_size, output_size=output_size, learning_rate=learning_rate, num_hidden_layers=num_hidden_layers, drop_prob=drop_prob, l2_reg=l2_reg)

    def fit_epoch(self, features_train, demand_train):
        super().fit(features_train, demand_train, cu=self.cu, co=self.co, batch_size=self.batch_size, learning_rate=self.learning_rate, device=self.device)

    def draw_action(self, X):
        return super().predict(X)

