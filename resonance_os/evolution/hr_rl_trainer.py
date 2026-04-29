from stable_baselines3 import PPO
from gym import Env
from gym.spaces import Box
import numpy as np

class HRWritingEnv(Env):
    """Simulated environment where reward = human resonance score"""
    def __init__(self, hrv_dim=8):
        super().__init__()
        self.observation_space = Box(low=0, high=1, shape=(hrv_dim,))
        self.action_space = Box(low=0, high=1, shape=(hrv_dim,))

    def reset(self):
        return np.random.rand(self.observation_space.shape[0])

    def step(self, action):
        reward = float(np.random.rand())  # placeholder for real HR reward
        done = False
        return np.random.rand(self.observation_space.shape[0]), reward, done, {}

def train_hr_ppo(env: HRWritingEnv, timesteps=10000):
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)
    return model
