import subprocess
subprocess.run([
    "python", "resonance_os/cli/hr_main.py",
    "--prompt", "Write a compelling AI article about resonance tone",
    "--tenant", "default",
    "--profile", "brand_identity_v1"
])
