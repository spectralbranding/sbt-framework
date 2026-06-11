"""Cross-LLM consistency demonstration for the sbt-framework MethodsX article, Section 2.6.

Runs the Module 1 (Brand Decomposition) prompt across three LLM families (Claude, GPT, Gemini)
at temperature 0 on two canonical brands, parses each model's per-dimension strength (0-5) and
SIGNAL SIGNATURE (percentages on Delta^7), and reports cross-model agreement:
  - Fisher-Rao distance between the models' signature distributions (the article's simplex metric).
  - Spearman rank correlation of the 8 strength ratings (agreement on dimension ordering).

Keys read from env: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY.
Raw responses logged to cross_llm_run/<brand>_<model>.json for provenance.
"""

import os, re, json, itertools, math
import numpy as np
from scipy.stats import spearmanr

DIMS = [
    "semiotic",
    "narrative",
    "ideological",
    "experiential",
    "social",
    "economic",
    "cultural",
    "temporal",
]
BRANDS = ["Patagonia", "IKEA"]
OUT = os.path.join(os.path.dirname(__file__), "cross_llm_run")

SYSTEM = (
    "You are a brand analyst using Spectral Brand Theory (SBT). A brand is decomposed into signals across "
    "8 dimensions: SEMIOTIC (visual/auditory identity), NARRATIVE (stories/myths/temporal structure), "
    "IDEOLOGICAL (values/ethics/purpose), EXPERIENTIAL (touchpoints/product encounters), SOCIAL "
    "(community/status/belonging), ECONOMIC (price/value/financial), CULTURAL (aesthetic codes/taste/zeitgeist), "
    "TEMPORAL (heritage/evolution/era). For each dimension assess how actively the brand emits on it."
)
INSTR = (
    "Analyze the brand: {brand}. Then output ONLY a final fenced JSON code block (```json ... ```) with one key "
    "per dimension (lowercase: semiotic, narrative, ideological, experiential, social, economic, cultural, temporal). "
    "Each value is an object with 'strength' (integer 0-5, how actively the brand emits on that dimension) and "
    "'signature_percent' (number, the dimension's share of total emphasis). The eight signature_percent values MUST sum to 100."
)


def fisher_rao(w1, w2):
    w1 = np.asarray(w1, float)
    w2 = np.asarray(w2, float)
    w1 = w1 / w1.sum()
    w2 = w2 / w2.sum()
    return 2 * math.acos(min(1.0, float(np.sqrt(w1 * w2).sum())))


def parse(text):
    m = re.findall(r"\{[\s\S]*\}", text)
    if not m:
        return None
    obj = json.loads(m[-1])
    strength, sig = [], []
    for d in DIMS:
        v = obj.get(d) or obj.get(d.upper()) or {}
        strength.append(float(v.get("strength", 0)))
        sig.append(float(v.get("signature_percent", 0)))
    return strength, sig


def call_anthropic(brand):
    import anthropic

    c = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], timeout=120)
    r = c.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        temperature=0,
        system=SYSTEM,
        messages=[{"role": "user", "content": INSTR.format(brand=brand)}],
    )
    return "".join(b.text for b in r.content if getattr(b, "type", None) == "text")


def call_openai(brand):
    import openai

    c = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=120)
    r = c.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": INSTR.format(brand=brand)},
        ],
    )
    return r.choices[0].message.content


def call_gemini(brand):
    from google import genai
    from google.genai import types

    c = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    r = c.models.generate_content(
        model="gemini-2.5-pro",
        contents=SYSTEM + "\n\n" + INSTR.format(brand=brand),
        config=types.GenerateContentConfig(temperature=0),
    )
    return r.text


MODELS = {
    "claude-sonnet-4-6": call_anthropic,
    "gpt-4o": call_openai,
    "gemini-2.5-pro": call_gemini,
}

results = {}  # brand -> model -> (strength, sig)
for brand in BRANDS:
    results[brand] = {}
    for mname, fn in MODELS.items():
        try:
            txt = fn(brand)
            with open(os.path.join(OUT, f"{brand}_{mname}.json"), "w") as f:
                json.dump({"brand": brand, "model": mname, "raw": txt}, f, indent=2)
            p = parse(txt)
            if p:
                results[brand][mname] = p
                print(f"OK  {brand:10} {mname:18} strength={p[0]}")
            else:
                print(f"PARSE-FAIL {brand} {mname}")
        except Exception as e:
            print(f"ERR {brand} {mname}: {type(e).__name__}: {str(e)[:120]}")

print("\n=== Cross-model agreement ===")
all_fr, all_sp = [], []
for brand in BRANDS:
    ms = list(results[brand])
    if len(ms) < 2:
        print(f"{brand}: <2 models, skip")
        continue
    frs, sps = [], []
    for a, b in itertools.combinations(ms, 2):
        fr = fisher_rao(results[brand][a][1], results[brand][b][1])
        sp = spearmanr(results[brand][a][0], results[brand][b][0]).statistic
        frs.append(fr)
        sps.append(sp)
        print(
            f"  {brand:10} {a:16} vs {b:16}: Fisher-Rao(signature)={fr:.4f}  Spearman(strength)={sp:.3f}"
        )
    all_fr += frs
    all_sp += sps
    print(
        f"  {brand:10} mean Fisher-Rao={np.mean(frs):.4f}  mean Spearman={np.mean(sps):.3f}"
    )
if all_fr:
    print(
        f"\nOVERALL mean pairwise Fisher-Rao = {np.mean(all_fr):.4f} (range {min(all_fr):.4f}-{max(all_fr):.4f})"
    )
    print(
        f"OVERALL mean pairwise Spearman   = {np.mean(all_sp):.3f} (range {min(all_sp):.3f}-{max(all_sp):.3f})"
    )
