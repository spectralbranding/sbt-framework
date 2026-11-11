"""The toolkit states one signal scale (1-10) in its templates, prompts and generator."""

import re
from pathlib import Path

import yaml

from spectral_branding.prompt_generator import generate_prism_b_prompt
from spectral_branding.validators._math import SIGNAL_MAX, SIGNAL_MIN

ROOT = Path(__file__).resolve().parents[1]
TEXT_FILES = sorted(
    [*(ROOT / "templates").glob("*.yaml"), *(ROOT / "prompts").glob("*.md")]
)
# A per-dimension rating on another range: "0-5", "1-5", "0 to 5", "4/5 stars".
OTHER_RANGE = re.compile(r"\b[01]\s*(?:-|–|to)\s*5\b|\b\d/5\b|\bstars?\b", re.I)


def _strength_values(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "strength" and isinstance(value, (int, float)):
                yield value  # numeric signal; categorical labels are not signals
            else:
                yield from _strength_values(value)
    elif isinstance(node, list):
        for item in node:
            yield from _strength_values(item)


def test_scale_constants():
    assert (SIGNAL_MIN, SIGNAL_MAX) == (1.0, 10.0)


def test_templates_and_prompts_state_no_other_signal_range():
    hits = [
        f"{path.relative_to(ROOT)}:{n}: {line.strip()}"
        for path in TEXT_FILES
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if OTHER_RANGE.search(line)
    ]
    assert hits == []


def test_template_strengths_lie_on_the_signal_scale():
    values = [
        value
        for path in (ROOT / "templates").glob("*.yaml")
        for value in _strength_values(yaml.safe_load(path.read_text(encoding="utf-8")))
    ]
    assert values, "expected strength values in the templates"
    assert all(SIGNAL_MIN <= float(v) <= SIGNAL_MAX for v in values)


def test_generated_prompt_asks_for_the_signal_scale():
    prompt = generate_prism_b_prompt("Patagonia")
    text = prompt["system"] + prompt["user"]
    assert f"<{SIGNAL_MIN:g}-{SIGNAL_MAX:g}>" in text
