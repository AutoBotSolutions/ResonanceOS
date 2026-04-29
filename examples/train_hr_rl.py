from resonance_os.evolution.hr_rl_trainer import HRWritingEnv, train_hr_ppo

env = HRWritingEnv(hrv_dim=8)
model = train_hr_ppo(env, timesteps=5000)
print("HR-PPO model trained successfully")
