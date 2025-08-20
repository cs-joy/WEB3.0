from pydantic import BaseModel, Field
from typing import Optional, List, Tuple
from datetime import datetime
from enum import Enum

class ResponseStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class ResponseQuality(str, Enum):
    POOR = "poor"
    FAIR = "fair"
    GOOD = "good"
    EXCELLENT = "excellent"

class ResponseBase(BaseModel):
    """Base model for response data"""
    query_id: Optional[int] = Field(None, description="ID of the original query")
    tx_hash: Optional[str] = Field(None, description="Transaction hash of the response")
    ipfs_cid: str = Field(..., description="IPFS CID of the stored response")
    model_used: str = Field(..., description="LLM model used for generation")
    tokens_used: Optional[int] = Field(None, description="Number of tokens used")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")

class ResponseCreate(ResponseBase):
    """Model for creating a new response"""
    query_text: str = Field(..., description="Original query text")
    response_text: str = Field(..., description="Generated response text")
    retrieved_chunks: List[Tuple[str, float]] = Field(
        default_factory=list, 
        description="List of retrieved chunks with similarity scores"
    )

class ResponseUpdate(BaseModel):
    """Model for updating response metadata"""
    status: Optional[ResponseStatus] = None
    quality_score: Optional[float] = Field(None, ge=0, le=1, description="Quality score between 0 and 1")
    quality_rating: Optional[ResponseQuality] = None
    user_feedback: Optional[str] = Field(None, max_length=500, description="User feedback on response")
    is_verified: Optional[bool] = Field(False, description="Whether response has been verified")

class ResponseInDB(ResponseBase):
    """Complete response model for database storage"""
    id: int = Field(..., description="Unique response ID")
    query_text: str = Field(..., description="Original query text")
    response_text: str = Field(..., description="Generated response text")
    retrieved_chunks: List[Tuple[str, float]] = Field(
        default_factory=list, 
        description="List of retrieved chunks with similarity scores"
    )
    status: ResponseStatus = Field(ResponseStatus.PENDING, description="Current status of the response")
    quality_score: Optional[float] = Field(None, ge=0, le=1, description="Quality score between 0 and 1")
    quality_rating: Optional[ResponseQuality] = None
    user_feedback: Optional[str] = Field(None, max_length=500, description="User feedback on response")
    is_verified: bool = Field(False, description="Whether response has been verified")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    class Config:
        orm_mode = True
        use_enum_values = True

class ResponsePublic(ResponseInDB):
    """Public-facing response model (excludes sensitive/internal fields)"""
    class Config:
        fields = {
            'retrieved_chunks': {'exclude': True},
            'quality_score': {'exclude': True},
            'is_verified': {'exclude': True}
        }

class ResponseQualityMetrics(BaseModel):
    """Model for response quality assessment metrics"""
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance to query")
    accuracy_score: float = Field(..., ge=0, le=1, description="Factual accuracy")
    coherence_score: float = Field(..., ge=0, le=1, description="Response coherence")
    completeness_score: float = Field(..., ge=0, le=1, description="Answer completeness")
    overall_score: float = Field(..., ge=0, le=1, description="Overall quality score")

class ResponseFeedback(BaseModel):
    """Model for user feedback on responses"""
    response_id: int = Field(..., description="ID of the response being rated")
    rating: int = Field(..., ge=1, le=5, description="User rating (1-5 stars)")
    feedback_text: Optional[str] = Field(None, max_length=1000, description="Detailed feedback")
    helpful: Optional[bool] = Field(None, description="Whether the response was helpful")

class ResponseStats(BaseModel):
    """Model for response statistics"""
    total_responses: int = Field(0, description="Total number of responses generated")
    average_processing_time: float = Field(0.0, description="Average processing time in seconds")
    average_quality_score: float = Field(0.0, description="Average quality score")
    responses_by_status: dict = Field(default_factory=dict, description="Count of responses by status")
    responses_by_model: dict = Field(default_factory=dict, description="Count of responses by model used")

class BatchResponse(BaseModel):
    """Model for batch response operations"""
    responses: List[ResponsePublic] = Field(..., description="List of responses")
    total_count: int = Field(..., description="Total number of responses")
    page: int = Field(..., description="Current page number")
    total_pages: int = Field(..., description="Total number of pages")

# Utility functions for response handling
def calculate_quality_score(metrics: ResponseQualityMetrics) -> float:
    """Calculate overall quality score from individual metrics"""
    weights = {
        'relevance_score': 0.3,
        'accuracy_score': 0.4,
        'coherence_score': 0.2,
        'completeness_score': 0.1
    }
    
    return (
        metrics.relevance_score * weights['relevance_score'] +
        metrics.accuracy_score * weights['accuracy_score'] +
        metrics.coherence_score * weights['coherence_score'] +
        metrics.completeness_score * weights['completeness_score']
    )

def get_quality_rating(score: float) -> ResponseQuality:
    """Convert quality score to rating category"""
    if score >= 0.8:
        return ResponseQuality.EXCELLENT
    elif score >= 0.6:
        return ResponseQuality.GOOD
    elif score >= 0.4:
        return ResponseQuality.FAIR
    else:
        return ResponseQuality.POOR

def validate_response_text(response_text: str, max_length: int = 10000) -> bool:
    """Validate response text meets requirements"""
    if not response_text or not response_text.strip():
        return False
    if len(response_text) > max_length:
        return False
    return True
