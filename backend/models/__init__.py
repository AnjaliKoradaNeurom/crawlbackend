"""
Data models and schemas for the website analyzer
"""

from .schemas import (
   CrawlabilityFeatures,
   AIAnalysisResult, 
   Recommendation,
   PriorityLevel,
   Priority,  # Backward compatibility alias
   AnalysisResult,
   ValidationResult,
   GoogleSearchResult,
   URLVerificationResult,
   HealthCheckResult
)

__all__ = [
   'CrawlabilityFeatures',
   'AIAnalysisResult', 
   'Recommendation',
   'PriorityLevel',
   'Priority',  # Backward compatibility
   'AnalysisResult',
   'ValidationResult',
   'GoogleSearchResult',
   'URLVerificationResult',
   'HealthCheckResult'
]
