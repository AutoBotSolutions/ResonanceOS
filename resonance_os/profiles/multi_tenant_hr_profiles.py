from pathlib import Path
import json
from typing import List

class HRVProfileManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_profile(self, tenant: str, profile_name: str, hrv_vector: List[float]):
        tenant_dir = self.base_dir / tenant
        tenant_dir.mkdir(exist_ok=True)
        path = tenant_dir / f"{profile_name}.json"
        with open(path, "w") as f:
            json.dump(hrv_vector, f)

    def load_profile(self, tenant: str, profile_name: str) -> List[float]:
        path = self.base_dir / tenant / f"{profile_name}.json"
        with open(path, "r") as f:
            return json.load(f)

    def list_profiles(self, tenant: str) -> List[str]:
        tenant_dir = self.base_dir / tenant
        return [p.stem for p in tenant_dir.glob("*.json")]
