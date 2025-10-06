from utils.parse_terraform import parse_terraform
from utils.checkov_scan import run_checkov_scan
from utils.gemini_analyze import analyze_with_gemini
# from utils.build_graph import build_resource_graph, visualize_graph
import json

def main():
    tf_file = "samples/s3_public.tf"

    # Step 1: Parse Terraform
    tf_data = parse_terraform(tf_file)
    print("\n✅ Parsed Terraform Data:")
    print(json.dumps(tf_data, indent=2))

    # Step 2: Run Checkov
    findings = run_checkov_scan(tf_file)
    print("\n✅ Checkov Findings:")
    print(json.dumps(findings, indent=2))

    # # Step 3: Build Resource Graph
    # G = build_resource_graph(tf_data)
    # print("\n✅ Resource Graph:")
    # visualize_graph(G)

    # Step 4: Analyze with Gemini
    print("\n🤖 Gemini Analysis:")
    gemini_response = analyze_with_gemini(tf_data, findings)
    print(gemini_response)

if __name__ == "__main__":
    main()
