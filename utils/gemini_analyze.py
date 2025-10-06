import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("⚠️ Missing GEMINI_API_KEY in .env file")

genai.configure(api_key=api_key)

def analyze_with_gemini(terraform_json, checkov_findings):
    prompt = f"""
    You are an AWS security expert.
    Analyze the following Terraform configuration for potential misconfigurations.
    Provide a summary of risks and remediation advice.

    Terraform config (parsed JSON):
    {terraform_json}

    Static analysis findings:
    {checkov_findings}
    """

    model = genai.GenerativeModel("gemini-2.5-pro")
    # models = genai.list_models()
    # for model in models:
    #     print(f"{model.name}")
    response = model.generate_content(prompt)
    return response.text
