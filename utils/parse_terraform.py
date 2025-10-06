import hcl2
import json

def parse_terraform(file_path):
    with open(file_path, 'r') as f:
        data = hcl2.load(f)
    return data

if __name__ == "__main__":
    print(json.dumps(parse_terraform("../samples/s3_public.tf"), indent=2))
