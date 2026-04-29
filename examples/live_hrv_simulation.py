import sys
sys.path.append('.')  # ensure resonance_os is importable

import numpy as np
import matplotlib.pyplot as plt
from resonance_os.generation.human_resonant_writer import HumanResonantWriter
from resonance_os.profiles.multi_tenant_hr_profiles import HRVProfileManager
from resonance_os.evolution.hr_rl_trainer import HRWritingEnv, train_hr_ppo

# --------------------------
# 1. Setup multi-tenant profiles
# --------------------------
profile_manager = HRVProfileManager("./profiles/hr_profiles")
tenant = "default"
profile_name = "brand_identity_v1"

# Load HRV target vector for this tenant
target_hrv = profile_manager.load_profile(tenant, profile_name)
print(f"Loaded HRV profile for tenant '{tenant}' profile '{profile_name}': {target_hrv}")

# --------------------------
# 2. Initialize human-resonant writer
# --------------------------
writer = HumanResonantWriter()

# --------------------------
# 3. Generate human-resonant article
# --------------------------
prompt = "Write a futuristic AI article integrating multi-agent resonance"
article = writer.generate(prompt)
paragraphs = article.split('.')
print("=== Generated Article ===\n")
for p in paragraphs:
    if p.strip():
        print(f"- {p.strip()}.")

# --------------------------
# 4. Simulate HRF feedback per paragraph
# --------------------------
hrv_feedback = np.random.rand(len(paragraphs), len(target_hrv))
print("\n=== Simulated HRV Feedback ===")
print(hrv_feedback)

# --------------------------
# 5. Plot HRV feedback per paragraph
# --------------------------
plt.figure(figsize=(10,6))
for i in range(len(target_hrv)):
    plt.plot(hrv_feedback[:, i], label=f'HRV Dim {i}')
plt.title('HRV Feedback per Paragraph')
plt.xlabel('Paragraph Index')
plt.ylabel('HRV Score')
plt.legend()
plt.show()

# --------------------------
# 6. Optional: Train HR-PPO to maximize resonance
# --------------------------
env = HRWritingEnv(hrv_dim=len(target_hrv))
model = train_hr_ppo(env, timesteps=2000)
print("✅ HR-PPO Model trained for resonance optimization")
