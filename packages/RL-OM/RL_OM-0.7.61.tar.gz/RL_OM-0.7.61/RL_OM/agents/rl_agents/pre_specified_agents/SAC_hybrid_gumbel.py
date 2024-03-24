# AUTOGENERATED! DO NOT EDIT! File to edit: ../../../../nbs/agents/rl_agents/pre_specified_agents/21_SAC_hybrid_gumbel.ipynb.

# %% auto 0
__all__ = ['SACHybridGumbel', 'SACHybridGumbelReversed', 'SACHybridGumbelSeparate']

# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/21_SAC_hybrid_gumbel.ipynb 4
# General libraries
import numpy as np

# Torch
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# Networks
from ...networks.critics import CriticNetworkStateAction
from ...networks.actors import ActorNetwork

# Algorithms
from ..sac_hybrid import SAC_hybrid
from ..sac_hybrid_separate import SAC_hybrid_separate
from ..sac_hybrid_reversed import SAC_hybrid_reversed

from mushroom_rl.core.serialization import Serializable

# Processors
from ...processors.processors import  OneHotHybridtoContinuous


# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/21_SAC_hybrid_gumbel.ipynb 5
class SACHybridGumbel():

    """
    Soft Actor Critic (SAC) agent with hybrid Gaussian-Gumbel policy.
    ! Currently works only for binary discrete actions.

    Args:
        mdp_info (MDPInfo): Contains relevant information about the environment.
        learning_rate_actor (float): Learning rate for the actor.
        learning_rate_critic (float): Learning rate for the critic.
        learning_rate_alpha (float): Learning rate for the temperature parameter.
        initial_replay_size (int): Number of transitions to save in the replay buffer during startup.
        max_replay_size (int): Maximum number of transitions to save in the replay buffer.
        batch_size (int): Number of transitions to sample each time experience is replayed.
        n_features (int): Number of features for the hidden layers of the networks.
        n_features_discrete (int): Number of features for the hidden layers of the discrete network. If set to None will use the same as n_features.
        warmup_transitions (int): Number of transitions to replay before starting to update the networks.
        lr_alpha (float): Learning rate for the temperature parameter.
        tau (float): Parameter for the soft update of the target networks.
        optimizer (torch.optim): Optimizer to use for the networks.
        squeeze_output (bool): Whether to squeeze the output of the actor network or not.
        use_cuda (bool): Whether to use CUDA or not. If True and not available, it will use CPU.
        agent_name (str): Name of the agent. If set to None will use some default name.

    """

    def __init__(
            self,
            mdp_info,
            learning_rate_actor = 3e-4,
            learning_rate_critic = None,
            learning_rate_alpha = 3e-4,
            initial_replay_size = 64,
            max_replay_size = 50000,
            batch_size = 64,
            n_features = 64,
            n_features_discrete = None,
            warmup_transitions = 100,
            lr_alpha = 3e-4,
            tau = 0.005,
            target_entropy = None,
            optimizer = optim.Adam,
            squeeze_output = True,
            use_cuda = True,
            agent_name = None):
        
        use_cuda = use_cuda and torch.cuda.is_available()

        actor_input_shape = mdp_info.observation_space.shape
        actor_output_shape = (mdp_info.action_space.shape[0],)
        actor_discrete_input_shape = (mdp_info.observation_space.shape[0] + mdp_info.action_space.shape[0],)
        actor_discrete_output_shape = (2,) # Currently hardcoded for binary discrete actions

        if learning_rate_critic is None:
            learning_rate_critic = learning_rate_actor


        actor_mu_params = dict(network=ActorNetwork,
                                n_features=n_features,
                                input_shape=actor_input_shape,
                                output_shape=actor_output_shape,
                                use_cuda=use_cuda)

        actor_sigma_params = dict(network=ActorNetwork,
                                    n_features=n_features,
                                    input_shape=actor_input_shape,
                                    output_shape=actor_output_shape,
                                    use_cuda=use_cuda)
        
        actor_discrete_params = dict(network=ActorNetwork,
                                    n_features=n_features if n_features_discrete is None else n_features_discrete,
                                    input_shape=actor_discrete_input_shape,
                                    output_shape=actor_discrete_output_shape,
                                    use_cuda=use_cuda)
        
        actor_optimizer = {'class': optimizer,
                    'params': {'lr': learning_rate_alpha}} 
        
        critic_input_shape = (actor_input_shape[0] + actor_output_shape[0]*3,)
        critic_params = dict(network=CriticNetworkStateAction,
                        optimizer={'class': optim.Adam,
                                'params': {'lr': learning_rate_critic}}, 
                        loss=F.mse_loss,
                        n_features=n_features,
                        input_shape=critic_input_shape,
                        output_shape=(1,),
                        squeeze_output=squeeze_output,
                        use_cuda=use_cuda)

        self.agent = SAC_hybrid(mdp_info, actor_mu_params, actor_sigma_params,
                actor_discrete_params, actor_optimizer, critic_params, batch_size, initial_replay_size,
                max_replay_size, warmup_transitions, tau, lr_alpha,
                critic_fit_params=None)
        
        if agent_name is None:
            self.agent.name = 'SAC_hybrid_gumbel'
        else:
            self.agent.name = agent_name

        self.agent.add_postprocessor(OneHotHybridtoContinuous(mdp_info.action_space.shape[0]))

    def __getattr__(self, attr):
        return getattr(self.agent, attr)



# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/21_SAC_hybrid_gumbel.ipynb 6
class SACHybridGumbelReversed():

    """
    Soft Actor Critic (SAC) agent with hybrid Gaussian-Gumbel policy. The order of the actor
    Networks is reversed in comparison to the original implementation (SACHybridGumbel)
    ! Currently works only for binary discrete actions.

   Args:
        mdp_info (MDPInfo): Contains relevant information about the environment.
        learning_rate_actor (float): Learning rate for the actor.
        learning_rate_critic (float): Learning rate for the critic.
        learning_rate_alpha (float): Learning rate for the temperature parameter.
        initial_replay_size (int): Number of transitions to save in the replay buffer during startup.
        max_replay_size (int): Maximum number of transitions to save in the replay buffer.
        batch_size (int): Number of transitions to sample each time experience is replayed.
        n_features (int): Number of features for the hidden layers of the networks.
        n_features_discrete (int): Number of features for the hidden layers of the discrete network. If set to None will use the same as n_features.
        warmup_transitions (int): Number of transitions to replay before starting to update the networks.
        lr_alpha (float): Learning rate for the temperature parameter.
        tau (float): Parameter for the soft update of the target networks.
        optimizer (torch.optim): Optimizer to use for the networks.
        use_cuda (bool): Whether to use CUDA or not. If True and not available, it will use CPU.
        agent_name (str): Name of the agent. If set to None will use some default name.

    """

    def __init__(
            self,
            mdp_info,
            learning_rate_actor = 3e-4,
            learning_rate_critic = None,
            learning_rate_alpha = 3e-4,
            initial_replay_size = 64,
            max_replay_size = 50000,
            batch_size = 64,
            n_features = 64,
            n_features_discrete = None,
            warmup_transitions = 100,
            lr_alpha = 3e-4,
            tau = 0.005,
            target_entropy = None,
            optimizer = optim.Adam,
            squeeze_output = True,
            use_cuda = True,
            agent_name = None):
        
        use_cuda = use_cuda and torch.cuda.is_available()

        actor_input_shape = mdp_info.observation_space.shape
        actor_output_shape = (mdp_info.action_space.shape[0],)
        actor_continuous_input_shape = (actor_input_shape[0]+2,)
        actor_discrete_output_shape = (2,) # Currently hardcoded for binary discrete actions

        if learning_rate_critic is None:
            learning_rate_critic = learning_rate_actor

        # Changer here: Now there is an additional input representing the taken discrete action
        actor_mu_params = dict(network=ActorNetwork,
                                n_features=n_features,
                                input_shape=actor_continuous_input_shape , # Currently hardcoded for binary discrete actions
                                output_shape=actor_output_shape,
                                use_cuda=use_cuda)

        # Changer here: Now there is an additional input representing the taken discrete action
        actor_sigma_params = dict(network=ActorNetwork,
                                    n_features=n_features,
                                    input_shape=actor_continuous_input_shape , # Currently hardcoded for binary discrete actions
                                    output_shape=actor_output_shape,
                                    use_cuda=use_cuda)
        
        # Change here: Only state as input for discrete network. Same as for sepearate agent
        actor_discrete_params = dict(network=ActorNetwork,
                            n_features = n_features if n_features_discrete is None else n_features_discrete,
                            input_shape=actor_input_shape,
                            output_shape=actor_discrete_output_shape,
                            use_cuda=use_cuda)
        
        actor_optimizer = {'class': optimizer,
                    'params': {'lr': learning_rate_alpha}} 
        
        critic_input_shape = (actor_input_shape[0] + actor_output_shape[0]*3,)
        critic_params = dict(network=CriticNetworkStateAction,
                        optimizer={'class': optim.Adam,
                                'params': {'lr': learning_rate_critic}}, 
                        loss=F.mse_loss,
                        n_features=n_features,
                        input_shape=critic_input_shape,
                        output_shape=(1,),
                        squeeze_output=squeeze_output,
                        use_cuda=use_cuda)

        # Change here: Use reversed SAC algorithm
        self.agent = SAC_hybrid_reversed(mdp_info, actor_mu_params, actor_sigma_params,
                actor_discrete_params, actor_optimizer, critic_params, batch_size, initial_replay_size,
                max_replay_size, warmup_transitions, tau, lr_alpha,
                critic_fit_params=None)
        
        # Change here: Different default name
        if agent_name is None:
            self.agent.name = 'SAC_hybrid_gumbel_reversed'
        else:
            self.agent.name = agent_name

        self.agent.add_postprocessor(OneHotHybridtoContinuous(mdp_info.action_space.shape[0]))

    def __getattr__(self, attr):
        return getattr(self.agent, attr)

# %% ../../../../nbs/agents/rl_agents/pre_specified_agents/21_SAC_hybrid_gumbel.ipynb 7
class SACHybridGumbelSeparate():

    """
    Soft Actor Critic (SAC) agent with hybrid Gaussian-Gumbel policy. The contiuous and discrete
    Actor networks are independent, different from the original implementation (SACHybridGumbel)
    ! Currently works only for binary discrete actions.

   Args:
        mdp_info (MDPInfo): Contains relevant information about the environment.
        learning_rate_actor (float): Learning rate for the actor.
        learning_rate_critic (float): Learning rate for the critic.
        learning_rate_alpha (float): Learning rate for the temperature parameter.
        initial_replay_size (int): Number of transitions to save in the replay buffer during startup.
        max_replay_size (int): Maximum number of transitions to save in the replay buffer.
        batch_size (int): Number of transitions to sample each time experience is replayed.
        n_features (int): Number of features for the hidden layers of the networks.
        n_features_discrete (int): Number of features for the hidden layers of the discrete network. If set to None will use the same as n_features.
        warmup_transitions (int): Number of transitions to replay before starting to update the networks.
        lr_alpha (float): Learning rate for the temperature parameter.
        tau (float): Parameter for the soft update of the target networks.
        optimizer (torch.optim): Optimizer to use for the networks.
        use_cuda (bool): Whether to use CUDA or not. If True and not available, it will use CPU.
        agent_name (str): Name of the agent. If set to None will use some default name.

    """

    def __init__(
            self,
            mdp_info,
            learning_rate_actor = 3e-4,
            learning_rate_critic = None,
            learning_rate_alpha = 3e-4,
            initial_replay_size = 64,
            max_replay_size = 50000,
            batch_size = 64,
            n_features = 64,
            n_features_discrete = None,
            warmup_transitions = 100,
            lr_alpha = 3e-4,
            tau = 0.005,
            target_entropy = None,
            optimizer = optim.Adam,
            squeeze_output = True,
            use_cuda = True,
            agent_name = None):
        
        use_cuda = use_cuda and torch.cuda.is_available()

        actor_input_shape = mdp_info.observation_space.shape
        actor_output_shape = (mdp_info.action_space.shape[0],)
        actor_discrete_output_shape = (2,) # Currently hardcoded for binary discrete actions

        if learning_rate_critic is None:
            learning_rate_critic = learning_rate_actor

        actor_mu_params = dict(network=ActorNetwork,
                                n_features=n_features,
                                input_shape=actor_input_shape,
                                output_shape=actor_output_shape,
                                use_cuda=use_cuda)

        actor_sigma_params = dict(network=ActorNetwork,
                                    n_features=n_features,
                                    input_shape=actor_input_shape,
                                    output_shape=actor_output_shape,
                                    use_cuda=use_cuda)
        
        # Change here: Only state as input for discrete network. Same as for reversed agent
        actor_discrete_params = dict(network=ActorNetwork,
                            n_features=n_features if n_features_discrete is None else n_features_discrete,
                            input_shape=actor_input_shape,
                            output_shape=actor_discrete_output_shape,
                            use_cuda=use_cuda)
        
        actor_optimizer = {'class': optimizer,
                    'params': {'lr': learning_rate_alpha}} 
        
        critic_input_shape = (actor_input_shape[0] + actor_output_shape[0]*3,) # Currently hardcoded for binary discrete actions
        critic_params = dict(network=CriticNetworkStateAction,
                        optimizer={'class': optim.Adam,
                                'params': {'lr': learning_rate_critic}}, 
                        loss=F.mse_loss,
                        n_features=n_features,
                        input_shape=critic_input_shape,
                        output_shape=(1,),
                        squeeze_output=squeeze_output,
                        use_cuda=use_cuda)

        # Change here: Use separate SAC algorithm
        self.agent = SAC_hybrid_separate(mdp_info, actor_mu_params, actor_sigma_params,
                actor_discrete_params, actor_optimizer, critic_params, batch_size, initial_replay_size,
                max_replay_size, warmup_transitions, tau, lr_alpha,
                critic_fit_params=None)
        
        # Change here: Different default name
        if agent_name is None:
            self.agent.name = 'SAC_hybrid_gumbel_separate'
        else:
            self.agent.name = agent_name

        self.agent.add_postprocessor(OneHotHybridtoContinuous(mdp_info.action_space.shape[0]))

    def __getattr__(self, attr):
        return getattr(self.agent, attr)
