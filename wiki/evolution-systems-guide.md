# Evolution Systems Guide - ResonanceOS v6

## Overview

The Evolution Systems module provides reinforcement learning capabilities for ResonanceOS v6, enabling the system to improve content generation quality through iterative learning from human feedback. This module implements HR-RL (Human-Resonance Reinforcement Learning) training and reward modeling for adaptive content generation.

## System Architecture

```
Evolution Systems
├── hr_rl_trainer.py (RL Training Environment)
└── resonance_reward_model.py (Reward Model)
```

## System Components

### 1. HR RL Trainer (`hr_rl_trainer.py`)

Implements a reinforcement learning environment for training content generation policies using human resonance as the reward signal.

#### Architecture

```python
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
```

#### Environment Details

**Observation Space**: 8-dimensional continuous space
- Represents current HRV state
- Range: [0.0, 1.0] for each dimension
- Corresponds to HRV dimensions

**Action Space**: 8-dimensional continuous space
- Represents HRV adjustments to make
- Range: [0.0, 1.0] for each dimension
- Actions modify the HRV state

**Reward**: Human resonance score
- Range: [0.0, 1.0]
- Higher values indicate better human resonance
- Computed from actual human feedback in production

#### Training Function

```python
def train_hr_ppo(env: HRWritingEnv, timesteps=10000):
    """Train PPO model on HR writing environment"""
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=timesteps)
    return model
```

#### Dependencies

- `stable_baselines3`: Reinforcement learning algorithms (PPO)
- `gym`: OpenAI Gym environment interface
- `numpy`: Numerical computations

#### Usage Example

```python
from resonance_os.evolution.hr_rl_trainer import HRWritingEnv, train_hr_ppo

# Create environment
env = HRWritingEnv(hrv_dim=8)

# Train model
model = train_hr_ppo(env, timesteps=10000)

# Use trained model for generation
obs = env.reset()
action, _ = model.predict(obs)
print(f"Recommended HRV adjustment: {action}")
```

### 2. Resonance Reward Model (`resonance_reward_model.py`)

Predicts human resonance scores for generated content to serve as the reward signal for reinforcement learning.

#### Purpose

- Provide reward signal for RL training
- Predict human engagement and emotional response
- Guide content generation improvements

#### Architecture (Placeholder)

Current implementation is a placeholder. Production deployment requires:

- Training on engagement data
- Integration with ML frameworks
- Multi-dimensional output
- Real-time inference

#### Expected Interface

```python
class ResonanceRewardModel:
    def predict(self, text: str, target_hrv: List[float]) -> float:
        """
        Predict human resonance score for text.
        
        Args:
            text: Generated content to evaluate
            target_hrv: Target HRV vector for comparison
        
        Returns:
            Resonance score between 0.0 and 1.0
        """
        pass
```

## Integration Points

The Evolution Systems module integrates with:

- **Generation Systems**: Uses generation pipeline for environment simulation
- **Core Systems**: Uses HRV dimensions for state/action spaces
- **Profile Systems**: Uses profiles for target HRV specification
- **Similarity Systems**: Measures HRV alignment for reward computation

## Training Workflow

### 1. Environment Setup

```python
from resonance_os.evolution.hr_rl_trainer import HRWritingEnv

# Create environment
env = HRWritingEnv(hrv_dim=8)

# Verify spaces
print(f"Observation space: {env.observation_space}")
print(f"Action space: {env.action_space}")
```

### 2. Model Training

```python
from resonance_os.evolution.hr_rl_trainer import train_hr_ppo

# Train PPO model
model = train_hr_ppo(env, timesteps=50000)

# Save model
model.save("hr_ppo_model")
```

### 3. Model Evaluation

```python
# Load trained model
model = PPO.load("hr_ppo_model")

# Test on new observation
obs = env.reset()
action, _ = model.predict(obs)
print(f"Predicted HRV adjustment: {action}")
```

### 4. Integration with Generation

```python
from resonance_os.generation.human_resonant_writer import HumanResonantWriter

writer = HumanResonantWriter()

# Use RL model to guide HRV selection
obs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]  # Current state
action, _ = model.predict(obs)
target_hrv = action  # Use RL-recommended HRV

# Generate with RL-guided HRV
# (Integration depends on generation pipeline modifications)
```

## Advanced Usage

### Custom Reward Function

```python
class CustomHRWritingEnv(HRWritingEnv):
    def step(self, action):
        # Custom reward calculation
        obs = self._get_observation(action)
        reward = self._calculate_reward(obs, action)
        done = False
        info = {}
        return obs, reward, done, info
    
    def _calculate_reward(self, obs, action):
        # Custom reward logic
        # Could incorporate engagement metrics, HRV alignment, etc.
        return reward
```

### Multi-Objective Training

```python
# Train with different HRV targets
for profile_name in ["professional", "creative", "technical"]:
    profile = load_profile(profile_name)
    target_hrv = profile["target_hrv"]
    
    env = HRWritingEnv(hrv_dim=8)
    env.set_target_hrv(target_hrv)
    
    model = train_hr_ppo(env, timesteps=10000)
    model.save(f"hr_ppo_{profile_name}")
```

## Performance Considerations

- **Training time**: RL training can be time-consuming (hours to days)
- **Memory**: PPO requires significant memory for replay buffer
- **Sample efficiency**: PPO is relatively sample-efficient
- **Inference**: Trained models are fast for inference

## Best Practices

1. **Start with simulation**: Use placeholder environment before real deployment
2. **Monitor training**: Track reward curves and convergence
3. **Regular evaluation**: Evaluate on held-out test data
4. **Hyperparameter tuning**: Experiment with learning rates, batch sizes
5. **Model versioning**: Track model versions and performance

## Common Issues

**Issue**: Training instability
**Solution**: Adjust learning rate, clip range, or entropy coefficient

**Issue**: Slow convergence
**Solution**: Increase timesteps or adjust network architecture

**Issue**: Poor reward signal
**Solution**: Improve reward model with better training data

**Issue**: Overfitting
**Solution**: Use regularization or reduce model capacity

## Future Enhancements

- **Real reward integration**: Connect to actual human feedback
- **Multi-agent training**: Train multiple agents for different styles
- **Curriculum learning**: Start with simple tasks, increase complexity
- **Transfer learning**: Pre-train on related tasks
- **Online learning**: Continual learning from live feedback
- **Hierarchical RL**: Hierarchical policy for complex generation

## Deployment

### Training Pipeline

```python
# train_rl.py
from resonance_os.evolution.hr_rl_trainer import HRWritingEnv, train_hr_ppo

def main():
    env = HRWritingEnv(hrv_dim=8)
    model = train_hr_ppo(env, timesteps=100000)
    model.save("models/hr_ppo_final")

if __name__ == "__main__":
    main()
```

### Inference Pipeline

```python
# inference.py
from stable_baselines3 import PPO
from resonance_os.evolution.hr_rl_trainer import HRWritingEnv

def main():
    model = PPO.load("models/hr_ppo_final")
    env = HRWritingEnv(hrv_dim=8)
    
    obs = env.reset()
    action, _ = model.predict(obs)
    print(f"Recommended HRV: {action}")

if __name__ == "__main__":
    main()
```

## Dependencies Installation

```bash
pip install stable-baselines3 gym numpy
```

## Troubleshooting

**Issue**: Import errors for stable_baselines3
**Solution**: Install with `pip install stable-baselines3`

**Issue**: Gym compatibility issues
**Solution**: Ensure compatible gym version: `pip install gym==0.21.0`

**Issue**: Training crashes
**Solution**: Check GPU availability and memory requirements

## References

- [Generation Systems Guide](./generation-systems-guide.md)
- [Core Systems Guide](./core-systems-guide.md)
- [Profile Systems Guide](./profile-systems-guide.md)
