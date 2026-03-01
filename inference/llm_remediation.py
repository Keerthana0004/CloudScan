"""
LLM Remediation Module
Calls the Gemini API to generate remediation advice for flagged Terraform resources.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# ── Gemini API Setup ──────────────────────────────────────────────────────────
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "⚠️  Missing GEMINI_API_KEY. "
        "Create a .env file in the project root with:\n"
        "  GEMINI_API_KEY=your_key_here"
    )

genai.configure(api_key=api_key)

# Risk-level labels used in the prompt
RISK_LABELS = {0: "Safe", 1: "Low", 2: "Medium", 3: "High/Critical"}

# ── If you have a finetuned model, put its ID here ────────────────────────────
# Example: "tunedModels/terraform-remediation-abc123"
# Set to None to use the base Gemini model
FINETUNED_MODEL_ID = os.getenv("GEMINI_FINETUNED_MODEL", None)


def _build_prompt(flagged_resources, terraform_source=None):
    """
    Build a structured prompt for the LLM listing every flagged resource
    together with the original Terraform source file (if available).
    """
    resource_blocks = []
    for i, res in enumerate(flagged_resources, 1):
        risk_label = RISK_LABELS.get(res["predicted_risk"], "Unknown")
        block = (
            f"### Flagged Resource #{i}\n"
            f"- **Resource Type:** {res['resource_type']}\n"
            f"- **Resource ID:** {res['node_id']}\n"
            f"- **Predicted Risk Level:** {risk_label} ({res['predicted_risk']})\n"
            f"- **Configuration:**\n```json\n{json.dumps(res['config'], indent=2, default=str)}\n```"
        )
        resource_blocks.append(block)

    flagged_section = "\n\n".join(resource_blocks)

    source_section = ""
    if terraform_source:
        source_section = (
            "\n\n## Original Terraform Source\n"
            f"```hcl\n{terraform_source}\n```"
        )

    prompt = f"""You are an expert AWS cloud security engineer specializing in Terraform Infrastructure-as-Code.

An AI model (RGCN graph neural network) has analyzed a Terraform configuration and flagged the following resources as potentially misconfigured or insecure.

For EACH flagged resource below:
1. Explain what the security risk or misconfiguration is.
2. Explain the potential impact if left unaddressed.
3. Provide the corrected Terraform code block as a remediation.

{flagged_section}
{source_section}

Please provide your remediation in clear, structured format with corrected Terraform HCL code blocks."""

    return prompt


def generate_remediation(flagged_resources, terraform_source=None):
    """
    Generate remediation advice for a list of flagged Terraform resources.

    Parameters
    ----------
    flagged_resources : list[dict]
        Each dict must contain:
          - node_id       : str   (e.g. "main.tf::aws_s3_bucket.my_bucket")
          - resource_type : str   (e.g. "aws_s3_bucket")
          - predicted_risk: int   (1, 2, or 3)
          - config        : dict  (the parsed resource configuration)
    terraform_source : str, optional
        The raw .tf file contents for additional context.

    Returns
    -------
    str
        The LLM-generated remediation text.
    """
    if not flagged_resources:
        return "✅ No resources were flagged — no remediation needed."

    prompt = _build_prompt(flagged_resources, terraform_source)

    # Use finetuned model if available, otherwise fall back to base
    model_name = FINETUNED_MODEL_ID if FINETUNED_MODEL_ID else "gemini-2.0-flash"
    
    print(f"🤖 Calling Gemini ({model_name}) for remediation...")
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text


# ── Standalone test ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Quick smoke test with a dummy flagged resource
    sample = [
        {
            "node_id": "main.tf::aws_s3_bucket.public_bucket",
            "resource_type": "aws_s3_bucket",
            "predicted_risk": 3,
            "config": {
                "bucket": "my-public-data",
                "acl": "public-read",
            },
        }
    ]
    result = generate_remediation(sample)
    print("\n── Remediation Output ──")
    print(result)
