# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../nbs/agents/benchmark_agents/01_basic_NV_agents.ipynb.

# %% auto 0
__all__ = ['FakePolicy', 'RandomAgent', 'ParametricAgent']

# %% ../../../nbs/agents/benchmark_agents/01_basic_NV_agents.ipynb 4
# General libraries:
import numpy as np
from scipy.stats import norm

# Mushroom libraries
from mushroom_rl.core import Agent

# %% ../../../nbs/agents/benchmark_agents/01_basic_NV_agents.ipynb 6
class FakePolicy():
    def reset():
        pass

class RandomAgent(Agent):
    def __init__(self, num_products, min_action=0, max_action=1, name="Random"):
        self.num_products = num_products
        self.min_action = min_action
        self.max_action = max_action
        self._preprocessors = list()
        self._postprocessors = list()
        self.name = name
        self.policy = FakePolicy # needed for interface with MushroomRL
        self.train_directly = True
        self.train_mode = "direct"

    def draw_action(self, *args, **kwargs):
        action = np.random.rand(self.num_products)
        for postprocessor in self.postprocessors:
            action = postprocessor(action)
        return action
    
    def fit(self, *args, **kwargs):
        pass

    # def add_postprocessor(self, postprocessor):
    #     self.postprocessors.append(postprocessor)

class FakePolicy():
    def reset():
        pass

class ParametricAgent(Agent):
    def __init__(self, num_products, cu, co, name="Parametric"):
        self.num_products = num_products
        self._preprocessors = list()
        self._postprocessors = list()
        self.name = name
        self.policy = FakePolicy # needed for interface with MushroomRL
        self.train_directly = True
        self.train_mode="direct"
        self.action = np.zeros(num_products)
        self.sl = (cu/(co+cu))
        

    def fit(self, features, demand, mask=None):
        
        if mask is not None:
            
            assert demand.shape == mask.shape

            demand_relevant = demand[mask.astype(bool)]
            demand = demand_relevant
            print("test masking first")
            assert 1==2

        mean=demand.mean(axis=0)
        st=demand.std(axis=0)
        F_minus_1=norm.ppf(self.sl)
        self.action=mean+st*F_minus_1

    def draw_action(self, *args, **kwargs):
        return self.action
