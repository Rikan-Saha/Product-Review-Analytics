# ## Currently, providing the non-AI solutions 

# def generate_recommendations(df):
#     recommendations = []

#     negative_reviews = df[df["sentiment"] == "negative"]["review"]

#     issues = {
#         "quality": ["bad quality", "poor quality", "thin"],
#         "packaging": ["damaged", "box", "packing"],
#         "broken": ["broken", "defect"],
#         "performance": ["not working", "slow", "leaking"]
#     }

#     found_issues = {key: 0 for key in issues}

#     for review in negative_reviews:
#         for issue, keywords in issues.items():
#             if any(word in review for word in keywords):
#                 found_issues[issue] += 1

#     # Generate smart recommendations
#     if found_issues["quality"] > 0:
#         recommendations.append("Improve product quality and material durability")

#     if found_issues["packaging"] > 0:
#         recommendations.append("Enhance packaging to prevent damage during delivery")

#     if found_issues["broken"] > 0:
#         recommendations.append("Improve quality checks to avoid defective items")

#     if found_issues["performance"] > 0:
#         recommendations.append("Improve product performance and reliability")

#     if not recommendations:
#         recommendations.append("Overall product feedback is positive. Maintain quality.")

#     return recommendations

import os
import json
import re
import time
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple

import openai  # Assumes the legacy openai package; if you use the new SDK, see note below.

PROMPT_TEMPLATE = """
You are a product improvement assistant. Given cluster summaries, list top 5 actionable product improvements, prioritized, each with a one-line rationale.

Cluster summaries:
{cluster_summaries}

Return a JSON array of items: [{{"action":"...","rationale":"...","priority":1}}]
"""

# ---------------------------
# Utilities
# ---------------------------

def _configure_openai_for_azure(key: str, base: str, deployment: str, api_version: str = "2023-05-15"):
    openai.api_type = "azure"
    openai.api_key = key
    openai.api_base = base
    openai.api_version = api_version
    return deployment

def _try_parse_json(text: str) -> Any:
    """
    Attempt to extract and parse a JSON array/dict from a possibly messy LLM response.
    - Strips code fences
    - Finds first JSON array/dict via regex
    """
    def _strip_fences(s: str) -> str:
        s = s.strip()
        if s.startswith("```"):
            s = re.sub(r"^```(?:json)?", "", s, flags=re.IGNORECASE).strip()
        if s.endswith("```"):
            s = s[: s.rfind("```")].strip()
        return s

    s = _strip_fences(text)

    # Quick path
    try:
        return json.loads(s)
    except Exception:
        pass

    # Try to locate first JSON array or object in the text
    m = re.search(r"(\[.*\]|\{.*\})", s, flags=re.DOTALL)
    if m:
        candidate = m.group(1)
        try:
            return json.loads(candidate)
        except Exception:
            pass

    raise ValueError("Could not parse JSON from model output")

# ---------------------------
# Offline heuristic generator
# ---------------------------

_SEVERITY_KEYWORDS = {
    "crash": 4, "outage": 4, "data loss": 5, "security": 5, "breach": 5, "leak": 5,
    "fail": 3, "failure": 3, "error": 3, "bug": 3, "latency": 3, "slow": 2, "timeout": 3,
    "broken": 3, "corrupt": 4, "freeze": 3, "hang": 3, "infinite loop": 4
}
_IMPACT_KEYWORDS = {
    "payment": 4, "checkout": 4, "login": 4, "onboarding": 3, "signup": 3, "billing": 4,
    "export": 2, "reporting": 2, "notifications": 2, "search": 2, "sync": 3, "mobile": 3
}
_RECENCY_KEYWORDS = {"latest": 1, "new release": 1, "recent": 1, "v2.": 1, "v3.": 1, "today": 1}

_STOPWORDS = set("""
a an the and or but if while to for of on in with by from at as is are was were be been being this that these those
""".split())

def _tokenize_lines(text: str) -> List[str]:
    lines = [ln.strip("•-* \t") for ln in text.splitlines()]
    return [ln for ln in lines if ln]

def _score_line(line: str) -> int:
    s = line.lower()
    score = 0
    for k, w in _SEVERITY_KEYWORDS.items():
        if k in s:
            score += w
    for k, w in _IMPACT_KEYWORDS.items():
        if k in s:
            score += w
    for k, w in _RECENCY_KEYWORDS.items():
        if k in s:
            score += w
    # length heuristic (not too short, not too long)
    n = len(s.split())
    if 5 <= n <= 25:
        score += 1
    return score

def _normalize_action_phrase(s: str) -> str:
    s = s.strip().rstrip(".")
    s_low = s.lower()
    # Map common complaint patterns -> action verbs
    replacements = [
        (r"(login|authentication|auth).*fail", "Improve login reliability"),
        (r"(payment|checkout).*fail", "Fix checkout/payment failures"),
        (r"(crash|freeze|hang)", "Fix app stability issues"),
        (r"(latency|slow|timeout|performance)", "Reduce latency and improve performance"),
        (r"(onboarding|signup|registration)", "Streamline onboarding flow"),
        (r"(security|breach|leak|vuln)", "Address security vulnerabilities"),
        (r"(report|export)", "Stabilize reporting/export workflows"),
        (r"(sync|synchronization)", "Improve data sync reliability"),
        (r"(mobile|iOS|android)", "Fix critical mobile issues"),
        (r"(search)", "Improve search relevance and speed"),
    ]
    for pat, action in replacements:
        if re.search(pat, s_low):
            return action

    # Fallback: compress to a clear imperative starting with a verb
    # Keep nouns and verbs only (very rough)
    cleaned = re.sub(r"[^a-zA-Z0-9 ]+", " ", s).strip()
    words = [w for w in cleaned.split() if w.lower() not in _STOPWORDS]
    if not words:
        words = ["issue"]
    # Start with a generic verb
    return "Improve " + " ".join(words[:6])

def _group_similar(lines_scored: List[Tuple[str, int]]) -> Dict[str, Dict[str, Any]]:
    """
    Bucket lines that map to the same normalized action. Aggregate score & examples.
    """
    buckets: Dict[str, Dict[str, Any]] = {}
    for line, score in lines_scored:
        action = _normalize_action_phrase(line)
        b = buckets.setdefault(action, {"action": action, "score": 0, "examples": [], "count": 0})
        b["score"] += score
        b["count"] += 1
        if len(b["examples"]) < 3:
            b["examples"].append(line)
    return buckets

def _rank_to_priorities(items: List[Dict[str, Any]]) -> List[int]:
    """
    Convert rank (0..n-1) to priority scale (1 is highest). Ties handled by order.
    """
    return list(range(1, len(items) + 1))

def _offline_improvement_proposals(cluster_summaries: str) -> List[Dict[str, Any]]:
    lines = _tokenize_lines(cluster_summaries)
    if not lines:
        return [{"action": "Clarify user pain points", "rationale": "No cluster summaries provided.", "priority": 1}]

    scored = [(ln, _score_line(ln)) for ln in lines]
    # Boost frequently repeated problems
    freq = Counter([re.sub(r"\s+", " ", ln.lower()).strip() for ln in lines])
    scored = [(ln, sc + min(3, freq[re.sub(r'\s+', ' ', ln.lower()).strip()])) for ln, sc in scored]

    buckets = _group_similar(scored)
    ranked = sorted(buckets.values(), key=lambda x: (x["score"], x["count"]), reverse=True)

    # Compose final list with rationales
    top = ranked[:5]
    priorities = _rank_to_priorities(top)

    results = []
    for i, item in enumerate(top):
        examples = "; ".join(item["examples"])
        rationale = f"High impact and severity indicated by {item['count']} related reports (e.g., {examples})."
        results.append({"action": item["action"], "rationale": rationale, "priority": priorities[i]})
    return results

# ---------------------------
# Main entry
# ---------------------------
import json
from dotenv import load_dotenv
from openai import OpenAI

# --------------------------------------------------
# Load Environment Variables
# --------------------------------------------------

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))
print("OPENAI_MODEL:", os.getenv("OPENAI_MODEL"))

client = OpenAI(api_key=OPENAI_API_KEY)
def propose_improvements(cluster_summaries: str):

    system_prompt = """
    You are a Principal Product Manager.

    Your job is to analyze customer review clusters
    and identify the most valuable product improvements.

    Consider:

    - Customer pain points
    - Complaint frequency
    - Business impact
    - User experience impact
    - Product reliability
    - Ease of implementation

    Prioritize recommendations according to impact.

    Return ONLY valid JSON.
    """

    user_prompt = f"""
    Analyze the following customer review clusters.

    Customer Review Clusters:

    {cluster_summaries}

    Generate the TOP 5 product improvement recommendations.

    Return JSON in the following format:

    [
      {{
        "title": "",
        "customer_problem": "",
        "proposed_solution": "",
        "expected_impact": "",
        "priority_score": 1,
        "implementation_complexity": "",
        "category": ""
      }}
    ]

    Categories:

    - UX
    - Feature
    - Performance
    - Reliability
    - Support

    Rules:

    1. Return ONLY JSON.
    2. No markdown.
    3. No explanation outside JSON.
    """

    try:

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )

        result = response.output_text

        return json.loads(result)

    except Exception as e:

        print(f"OpenAI Error: {e}")

        return [{
            "title": "OpenAI API Failure",
            "customer_problem": str(e),
            "proposed_solution": "Check API configuration",
            "expected_impact": "Restore AI recommendations",
            "priority_score": 10,
            "implementation_complexity": "Low",
            "category": "Support"
        }]