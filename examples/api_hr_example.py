import requests
resp = requests.post(
    "http://127.0.0.1:8000/hr_generate",
    json={"prompt":"Write an AI article on human resonance tone"}
)
data = resp.json()
print(data["article"])
print(data["hrv_feedback"])
