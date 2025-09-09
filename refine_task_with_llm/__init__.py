# __init__.py
from __future__ import annotations

import json
from typing import List, Optional, Dict, Any

from llmatch_messages import llmatch
from langchain_llm7 import ChatLLM7
from langchain_core.language_models import BaseChatModel


def refine_task_with_llm(
    llm: BaseChatModel | None,
    custom_text: str,
    *,
    project_name: Optional[str] = None,
    audience: Optional[str] = "senior engineer",
    include_examples: bool = True,
    verbose: bool = False,
) -> dict:
    """
    Refine an unstructured user brief into a strict, implementation-ready task description.

    - llm: Optional LLM instance. If None, a deterministic ChatLLM7 is instantiated.
    - custom_text: Raw user brief to refine.
    - project_name: Optional project name to include in the prompt.
    - audience: Intended audience for the refined task.
    - include_examples: Whether to include example usage block in the output.
    - verbose: If True, pass verbose to llmatch for debugging.

    Returns:
        A dict parsed from the JSON produced by the LLM within BEGIN_JSON / END_JSON markers.

    Raises:
        RuntimeError: If extraction or JSON parsing fails.
    """
    # 1. LLM handling
    if llm is None:
        try:
            llm = ChatLLM7(temperature=0)  # type: ignore[call-arg]
        except TypeError:
            llm = ChatLLM7()  # type: ignore[assignment]

    assert llm is not None

    # 2. Prompting - Build system message
    system_message = {
        "role": "system",
        "content": (
            "You are a precise task refiner for software engineers. "
            "Output only JSON wrapped between BEGIN_JSON and END_JSON markers. "
            "Use exactly the schema provided. Do not add extra top-level keys. "
            "Be concrete; avoid placeholders and vague language."
        ),
    }

    # 2. Prompting - Build human message
    # Verbose, verbatim JSON schema description included in the human prompt
    verbatim_schema = """{
  "title": "Generate setup.py from source summary",
  "objective": "Produce a valid setup.py for packaging based on provided repo metadata.",
  "context": "The tool must run offline during CI. No network calls.",
  "inputs": [
    {"name": "custom_text", "type": "str", "constraints": "Non-empty"},
    {"name": "author", "type": "Optional[str]", "constraints": "If provided, valid email in author_email"}
  ],
  "outputs": [
    {"name": "setup_py", "type": "str", "validation": "Parsable Python; contains setup(...)"}
  ],
  "acceptance_criteria": [
    "Output contains only a single JSON object (no prose).",
    "Fields match the schema exactly.",
    "Each acceptance criterion is concrete and testable."
  ],
  "steps": [
    "Parse metadata from input.",
    "Assemble setup() fields deterministically.",
    "Return the file content as a string."
  ],
  "non_functional_requirements": [
    "Deterministic: same input → same output.",
    "No network calls.",
    "Run under Python 3.11+."
  ],
  "edge_cases": [
    "Missing optional metadata.",
    "Extra whitespace in input.",
    "Non-ASCII characters in author name."
  ],
  "out_of_scope": [
    "Writing to disk.",
    "Uploading to PyPI."
  ],
  "examples": [
    {"input_brief": "Minimal lib", "expected_keys": ["title","objective","acceptance_criteria"]}
  ]
}"""

    human_content_parts: List[str] = [
        f"Raw input (custom_text): {custom_text}",
    ]
    if project_name:
        human_content_parts.append(f"Project name: {project_name}")
    if audience:
        human_content_parts.append(f"Audience: {audience}")
    human_content_parts.append(f"Include examples: {str(include_examples).lower()}")
    human_content_parts.append("JSON schema (verbatim):")
    human_content_parts.append(verbatim_schema)
    human_content_parts.append('Final instruction: "Return only one JSON object, strictly between the markers."')

    human_message = {"role": "user", "content": "\n".join(human_content_parts)}

    # 3. Extraction
    pattern = r"(?s)BEGIN_JSON\s*(\{.*\})\s*END_JSON"
    response = llmatch(
        llm=llm,
        messages=[system_message, human_message],
        pattern=pattern,
        verbose=verbose,
    )

    # Normalize capture
    captured = response["extracted_data"][0]

    if not isinstance(captured, str):
        raise RuntimeError("LLM did not return valid JSON string between markers.")

    try:
        data = json.loads(captured)
    except Exception as e:
        raise RuntimeError("Invalid JSON from LLM.") from e

    return data