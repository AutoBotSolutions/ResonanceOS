import argparse
from resonance_os.api.hr_server import SimpleRequest, hr_generate

def main():
    parser = argparse.ArgumentParser(description="Human-Resonant CLI")
    parser.add_argument("--prompt", type=str, required=True)
    parser.add_argument("--tenant", type=str, default=None)
    parser.add_argument("--profile", type=str, default=None)
    args = parser.parse_args()

    req = SimpleRequest(prompt=args.prompt, tenant=args.tenant, profile_name=args.profile)
    resp = hr_generate(req)
    print("=== Generated Human-Resonant Article ===")
    print(resp.article)
    print("=== HRV Feedback ===")
    print(resp.hrv_feedback)

if __name__ == "__main__":
    main()
