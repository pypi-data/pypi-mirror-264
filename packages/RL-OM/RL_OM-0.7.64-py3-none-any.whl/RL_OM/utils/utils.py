# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/utils/01_utils.ipynb.

# %% auto 0
__all__ = ['combine_dict', 'convert_str_none_to_none', 'load_agent_function', 'merge_with_namespace',
           'delete_lag_window_from_config', 'get_git_revision_hash', 'get_version', 'init_pipeline',
           'prepare_hyperparameter_opt', 'prepare_lag_window', 'prepare_calculation_function',
           'get_actions_per_product', 'track_normalization', 'create_env_agent']

# %% ../../nbs/utils/01_utils.ipynb 4
# General libraries:
# import numpy as np
# import pickle
import yaml
# import os
# from tqdm import tqdm, trange
import wandb
import datetime
import torch
import pkg_resources
# import sys,traceback

# %% ../../nbs/utils/01_utils.ipynb 6
def combine_dict(dict1, dict2):

    """
    Combines two dictionaries. Raises error if there are overlapping keys.

    Args:
        dict1 (dict): First dictionary
        dict2 (dict): Second dictionary

    Returns:
        dict: Combined dictionary
    """

    overlapping_keys = set(dict1.keys()).intersection(set(dict2.keys()))
    if overlapping_keys:
        raise ValueError(f"Overlapping keys detected: {overlapping_keys}")
    return {**dict1, **dict2}

def convert_str_none_to_none(d):
    """Recursively convert all string "None" in a dictionary to Python's None."""
    for key, value in d.items():
        if value == "None":
            d[key] = None
        elif isinstance(value, dict):
            convert_str_none_to_none(value)
    return d

def load_agent_function(agent_name, agent_mapping):

    """
    Load an agent function based on agent_name.
    The function must be in the same folder as the main file that calls this function.

    Args:
        agent_name (str): Name of the agent
        agent_mapping (dict): Dictionary mapping agent names to agent functions

    Returns:    
        function: Agent function

    """

    if agent_name not in agent_mapping:
        raise ValueError(f"Unknown agent name: {agent_name}")

    module_name, function_name = agent_mapping[agent_name].rsplit('.', 1)
    module = __import__(module_name, fromlist=[function_name])
    create_agent = getattr(module, function_name)

    return create_agent.create_agent

def merge_with_namespace(target_dict, source_dict, target_dict_name):
    
    """
    Merge source_dict into target_dict, using the keys as namespaces.
    For example, if target_dict_name is "agent", the key "agent-epsilon" in source_dict will be merged into target_dict["epsilon"].
    The function is to merge hyperparameters from a config file with the default hyperparameters from the yaml files

    Args:
        target_dict (dict): Target dictionary
        source_dict (dict): Source dictionary
        target_dict_name (str): Name of the target dictionary

    Returns:
        dict: Merged dictionary


    """
    for namespaced_key, value in source_dict.items():
        keys = namespaced_key.split('-')

        if keys[0] != target_dict_name:
            continue

        keys = keys[1:]

        d = target_dict
    
        # Check if keys already exist in target_dict
        exists = True
        for key in keys:
            if key not in d:
                exists = False
                break
            if isinstance(d[key], dict):
                d = d[key]
                continue
            else:
                break

        # If all keys are present, overwrite the value
        if exists:
            prev = d[key]
            d[key] = value
            print(f"Overwriting in key {namespaced_key} value {prev} with value {value}")
        else:
            # exception if key is not present in target_dict
            print(f"Key {namespaced_key} not found in {target_dict_name}.")
            raise ValueError(f"Key {namespaced_key} not found in {target_dict_name}.")

    return target_dict

def delete_lag_window_from_config(config_agent):

    """
    Delete lag_window from config_agent.
    This is necessary to define lag_window per agent in yaml file,
    but the information is used by the environment, not the agent.
    Befor applying the agent it has to be removed.

    """

    for agent_param_name in config_agent.keys():
        if "lag_window" in config_agent[agent_param_name]:
            del config_agent[agent_param_name]["lag_window"]
        
def get_git_revision_hash(directory):
    """
    Get curret git hash of the repository (e.g., to be logged in wandb).
    """
    return subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory).decode('ascii').strip()

def get_version(library_name: str) -> str:
    """
    Get the version of a specified library.

    :param library_name: Name of the library
    :return: Version of the library
    """
    
    try:
        version = pkg_resources.get_distribution(library_name).version
        return version
    except pkg_resources.DistributionNotFound:
        print(f"Library '{library_name}' not found.")
        return "Not Installed"
    

# %% ../../nbs/utils/01_utils.ipynb 8
def init_pipeline(config_env, config_train, config_agent, project_name):

    torch.set_num_threads(1)

    try:
        sweep_config = wandb.config
    except:
        sweep_config = None

    # Get parames for env and training
    with open(config_env, "r") as f:
        config_env = yaml.safe_load(f)

    with open(config_train, "r") as f:
        config_train = yaml.safe_load(f)
    
    with open(config_agent, "r") as f:
        config_agent = yaml.safe_load(f)

    wandb.init(
        project=project_name,
        name = f"{project_name}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    )

    try:
        rl_om_directory = config_train["rl_om_directory"]
        rl_om_hash = get_git_revision_hash(rl_om_directory)
    except:
        rl_om_hash = get_version("RL_OM")
        
    try:
        mushroom_fork_directory = config_train["mushroom_fork_directory"]
        mushroom_fork_hash = get_git_revision_hash(mushroom_fork_directory)
    except:
        mushroom_fork_hash = get_version("mushroom_rl")

    success = False 
    for experiment_directory in config_train["experiment_directory"]:
        try:
            experiment_hash = get_git_revision_hash(experiment_directory)
            success = True
            break
        except:
            pass
    
    if not success:
        experiment_hash = None
    
    return config_env, config_train, config_agent, sweep_config, rl_om_hash, mushroom_fork_hash, experiment_hash

def prepare_hyperparameter_opt():
        
    if 'hyperparameter_opt' in wandb.config._items:
        hyperparameter_opt = wandb.config._items['hyperparameter_opt']
    else:
        hyperparameter_opt = None
    
    if hyperparameter_opt:
        num_datasets = wandb.config._items["num_datasets"]
        weight_final = wandb.config._items["weight_final"] 
        weight_best = wandb.config._items["weight_best"]
        eval_period = wandb.config._items["eval_period"]
        if "dataset_start" in wandb.config._items:
            dataset_start = wandb.config._items["dataset_start"]
        else:
            dataset_start=1
    else:
        num_datasets = None 
        weight_final = None 
        weight_best = None 
        eval_period = None
        dataset_start = None

    return hyperparameter_opt, num_datasets, weight_final, weight_best, eval_period, dataset_start
    
def prepare_lag_window(config_env, config_agent, agent_param_name):
    if "lag_window" in config_agent[agent_param_name]:
        lag_window = config_agent[agent_param_name]["lag_window"]
        config_env["lag_window"] = lag_window
        delete_lag_window_from_config(config_agent) 
    
    return config_env, config_agent

def prepare_calculation_function(config_env, config_agent, agent_param_name):
    # TODO: Check this functionn works properly
    if "calculation_function" in config_agent[agent_param_name]:
        print("overwriting calculation function")
        config_env["calculations"] = config_agent[agent_param_name]["calculation_function"]
        del config_agent[agent_param_name]["calculation_function"]

    return config_env, config_agent

def get_actions_per_product(config_agent, agent_param_name):
    if "actions_per_product" in config_agent[agent_param_name]:
        actions_per_product = config_agent[agent_param_name]["actions_per_product"]
        del config_agent[agent_param_name]["actions_per_product"]
    else:
        actions_per_product = 1
    
    return actions_per_product

def track_normalization(config_env):
    norm_features = config_env.get("normalize_features", False)
    norm_reward = config_env.get("env_kwargs", {}).get("normalize_reward", False)
    norm_limit_low = config_env["env_kwargs"]["order_limit_low"]
    norm_limit_high = config_env["env_kwargs"]["order_limit_high"]
    
    norm_features = 1 if norm_features else 0
    norm_reward  = 1 if norm_reward else 0

    wandb.config.update({"norm_features": norm_features, "norm_reward": norm_reward, "norm_limit_low": norm_limit_low, "norm_limit_high": norm_limit_high})

def create_env_agent(create_env, config_env, config_train, config_agent, hyperparameter_opt, num_datasets, dataset_start, actions_per_product):
    
    if hyperparameter_opt:

        mdp_train_l = list()
        mdp_val_l = list()
        agent_l= list()
        for i in range(dataset_start-1, dataset_start-1+num_datasets):
            print("creating list of validation sets, not test sets")
            mdp_train, mdp_val, _ = create_env(config_env, create_val=True, use_dataset = i+1, actions_per_product = actions_per_product)

            mdp_train_l.append(mdp_train)
            mdp_val_l.append(mdp_val)

            create_agent = load_agent_function(config_train["agent"], config_agent["AGENTS"])

            agent, agent_kwargs_agent_only = create_agent(mdp_train, config_agent, config_env["unit_size"])

            agent_l.append(agent)
        
        mdp_train = mdp_train_l
        mdp_val = mdp_val_l
        mdp_test = None
        agent = agent_l

    else:
        if config_train["TRAINING_PARAMS"]["early_stopping_patience"] > 0 or config_train["TRAINING_PARAMS"]["save_best"]:
            print("creating validation and test set")
            mdp_train, mdp_val, mdp_test = create_env(config_env, create_val=True, actions_per_product=actions_per_product) 
        else:
            print("creating only test set")
            mdp_train, mdp_test = create_env(config_env, actions_per_product=actions_per_product)
            mdp_val = None

        create_agent = load_agent_function(config_train["agent"], config_agent["AGENTS"])
        agent, agent_kwargs_agent_only = create_agent(mdp_train, config_agent, config_env["unit_size"])

    return create_agent, mdp_train, mdp_val, mdp_test, agent, agent_kwargs_agent_only
