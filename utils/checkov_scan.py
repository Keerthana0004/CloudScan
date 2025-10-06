import subprocess
import json

def run_checkov_scan(file_path):
    cmd = ["checkov", "-f", file_path, "--output", "json"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        findings = json.loads(result.stdout)
    except json.JSONDecodeError:
        findings = {}
    return findings

if __name__ == "__main__":
    output = run_checkov_scan("../samples/s3_public.tf")
    print(json.dumps(output, indent=2))
