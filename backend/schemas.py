from pydantic import BaseModel
from typing import List, Dict, Any

class Reviews(BaseModel):
    data: List[Dict[str, Any]]

class ClusterRequest(BaseModel):
    cleaned_data: List[Dict[str, Any]]
    num_clusters: int

class ClusterSummaryResponse(BaseModel):
    count: int
    top_terms: List[str]
    samples: List[str]
    sentiment_dist: Dict[str, float]

class ClusterSummarizerResponse(BaseModel):
    cluster_counts: Dict[int, int]
    summaries: Dict[int, ClusterSummaryResponse]

class ClusterSummary(BaseModel):
    count: int
    top_terms: List[str]
    samples: List[str]
    sentiment_dist: Dict[str, float] = {}

class ImprovementPlanRequest(BaseModel):
    summarization: Dict[int, ClusterSummary]