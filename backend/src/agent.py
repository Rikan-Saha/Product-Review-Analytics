import os
import json
import re

from typing import TypedDict, List, Dict

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from langgraph.graph import StateGraph, END

# =====================================================
# ENVIRONMENT
# =====================================================

load_dotenv()

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4.1-mini"
)

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0
)

# =====================================================
# STATE
# =====================================================

class RecommendationState(TypedDict):
    cluster_summaries: str
    recommendations: List[Dict]
    final_output: List[Dict]

# =====================================================
# JSON PARSER
# =====================================================

def extract_json(text):

    text = text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)

    try:
        return json.loads(text)

    except Exception:

        match = re.search(
            r"(\[.*\]|\{.*\})",
            text,
            re.DOTALL
        )

        if match:
            return json.loads(match.group())

        raise ValueError("Unable to parse JSON")

# =====================================================
# SAFE LLM CALL
# =====================================================

def safe_llm_call(prompt):

    try:

        response = llm.invoke(
            [HumanMessage(content=prompt)]
        )

        return {
            "success": True,
            "data": extract_json(response.content)
        }

    except Exception as e:

        print(f"LLM Error: {e}")

        return {
            "success": False,
            "error": str(e)
        }

# =====================================================
# FALLBACK RECOMMENDATION
# =====================================================

def fallback_recommendation_agent():

    return [
        {
            "title": "Continue Monitoring Customer Feedback",
            "customer_problem": "No significant issue detected",
            "proposed_solution": "Monitor future reviews",
            "expected_impact": "Maintain customer satisfaction",
            "priority_score": 5,
            "implementation_complexity": "Low",
            "category": "Support",
            "customer_satisfaction_impact": "Medium",
            "retention_impact": "Medium",
            "revenue_impact": "Low",
            "business_value_score": 50,
            "supported_by_reviews": True,
            "confidence_score": 0.60,
            "validation_status": "Fallback Generated"
        }
    ]

# =====================================================
# AGENT 1
# RECOMMENDATION GENERATION
# =====================================================

def recommendation_agent(state):

    cluster_summaries = state["cluster_summaries"]

    prompt = f"""
You are a Principal Product Manager.

Analyze these customer review clusters:

{cluster_summaries}

Generate top 5 product improvement recommendations.

Return ONLY JSON.

[
  {{
    "title":"",
    "customer_problem":"",
    "proposed_solution":"",
    "expected_impact":"",
    "priority_score":1,
    "implementation_complexity":"",
    "category":""
  }}
]
"""

    result = safe_llm_call(prompt)

    if not result["success"]:
        return {
            "recommendations": fallback_recommendation_agent()
        }

    recommendations = result["data"]

    if isinstance(recommendations, dict):
        recommendations = recommendations.get(
            "recommendations",
            []
        )

    return {
        "recommendations": recommendations
    }

# =====================================================
# AGENT 2
# BUSINESS IMPACT
# =====================================================

def business_impact_agent(state):

    recommendations = state["recommendations"]

    prompt = f"""
You are a Product Strategy Consultant.

Recommendations:

{json.dumps(recommendations, indent=2)}

For each recommendation provide:

[
  {{
    "customer_satisfaction_impact":"High",
    "retention_impact":"Medium",
    "revenue_impact":"Medium",
    "business_value_score":90
  }}
]

Return ONLY JSON.
"""

    result = safe_llm_call(prompt)

    if not result["success"]:
        return {
            "recommendations": recommendations
        }

    impacts = result["data"]

    if isinstance(impacts, dict):

        if "recommendations" in impacts:
            impacts = impacts["recommendations"]

        elif "impacts" in impacts:
            impacts = impacts["impacts"]

        else:
            impacts = [impacts]

    if not isinstance(impacts, list):
        impacts = []

    for rec, impact in zip(
        recommendations,
        impacts
    ):
        rec.update(impact)

    return {
        "recommendations": recommendations
    }

# =====================================================
# AGENT 3
# VALIDATION
# =====================================================

def validation_agent(state):

    cluster_summaries = state["cluster_summaries"]

    recommendations = state["recommendations"]

    prompt = f"""
You are a Product Governance Reviewer.

Customer Reviews:

{cluster_summaries}

Recommendations:

{json.dumps(recommendations, indent=2)}

For each recommendation provide:

[
  {{
    "supported_by_reviews": true,
    "confidence_score": 0.90,
    "validation_status": "Approved"
  }}
]

Return ONLY JSON.
"""

    result = safe_llm_call(prompt)

    if not result["success"]:
        return {
            "final_output": recommendations
        }

    validations = result["data"]

    if isinstance(validations, dict):

        if "validations" in validations:
            validations = validations["validations"]

        elif "recommendations" in validations:
            validations = validations["recommendations"]

        else:
            validations = [validations]

    if not isinstance(validations, list):
        validations = []

    for rec, validation in zip(
        recommendations,
        validations
    ):
        rec.update(validation)

    return {
        "final_output": recommendations
    }

# =====================================================
# LANGGRAPH WORKFLOW
# =====================================================

builder = StateGraph(
    RecommendationState
)

builder.add_node(
    "recommendation_agent",
    recommendation_agent
)

builder.add_node(
    "business_impact_agent",
    business_impact_agent
)

builder.add_node(
    "validation_agent",
    validation_agent
)

builder.set_entry_point(
    "recommendation_agent"
)

builder.add_edge(
    "recommendation_agent",
    "business_impact_agent"
)

builder.add_edge(
    "business_impact_agent",
    "validation_agent"
)

builder.add_edge(
    "validation_agent",
    END
)

graph = builder.compile()

# =====================================================
# PUBLIC FUNCTION
# =====================================================

def propose_improvements(cluster_summaries):

    try:

        result = graph.invoke(
            {
                "cluster_summaries": cluster_summaries,
                "recommendations": [],
                "final_output": []
            }
        )

        return result["final_output"]

    except Exception as e:

        print(f"Workflow Error: {e}")

        return fallback_recommendation_agent()