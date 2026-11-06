"""NVIDIA NIM client with guided_json (grammar-constrained) output.

PRD v1.2 §7.6: use `guided_json` (xgrammar backend) so the LLM can only
produce JSON matching schema/slide_schema.json. Downstream only needs
semantic validation (tags, zones) — no parse-retry loop.
"""

# TODO: implement generate_script(topic: str) -> dict
#   - Load system prompt from llm/system_prompt.txt
#   - Inject allow-lists (schema/allowlists.json) into prompt text
#   - POST to NVIDIA_BASE_URL/chat/completions with guided_json=schema
#   - Return parsed slide deck dict
