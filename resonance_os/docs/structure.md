resonance_os_v6/
│
├── resonance_os/
│   ├── core/
│   │   ├── hrv_constants.py
│   │   └── hrv_types.py
│   │
│   ├── profiling/
│   │   └── hrv_extractor.py
│   │
│   ├── generation/
│   │   ├── planner_layer.py
│   │   ├── sentence_layer.py
│   │   ├── refiner_layer.py
│   │   ├── human_resonant_writer.py
│   │   └── hrf_model.py
│   │
│   ├── evolution/
│   │   ├── resonance_reward_model.py
│   │   └── hr_rl_trainer.py
│   │
│   ├── profiles/
│   │   └── multi_tenant_hr_profiles.py
│   │
│   ├── api/
│   │   └── hr_server.py
│   │
│   ├── cli/
│   │   └── hr_main.py
│   │
│   ├── utils/
│   │   ├── hrv_utils.py
│   │   └── text_emotion_tools.py
│   │
│   └── integrations/
│       └── aurora_hr_adapter.py
│
├── notebooks/
│   └── resonance_os_v6_dev.ipynb
│
├── examples/
│   ├── train_hr_rl.py
│   ├── cli_hr_example.py
│   └── api_hr_example.py
│
├── tests/
│   ├── test_hrv_extractor.py
│   ├── test_hrf_model.py
│   └── test_human_resonant_writer.py
│
├── pyproject.toml
├── .env
├── Dockerfile
└── docker-compose.yml
