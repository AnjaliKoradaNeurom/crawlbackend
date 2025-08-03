"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class PriorityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

# Create alias for backward compatibility
Priority = PriorityLevel

class Recommendation(BaseModel):
    priority: PriorityLevel
    title: str
    message: str
    impact_score: Optional[int] = Field(default=5, ge=1, le=10)
    code_snippet: Optional[str] = None
    doc_link: Optional[str] = None

class CrawlabilityFeatures(BaseModel):
    # Configure to allow model_ fields
    model_config = ConfigDict(protected_namespaces=())
    
    # Basic URL and response info
    url: str
    status_code: int
    
    # SSL and security
    https_enabled: bool
    ssl_certificate_valid: bool
    
    # Content metrics
    html_size: int
    word_count: int
    page_load_time: float
    
    # SEO elements
    title_tag_present: bool = False
    title_length: int = 0
    meta_description_present: bool = False
    meta_description_length: int = 0
    
    # Heading structure
    h1_count: int = 0
    h1_text: str = ""
    h2_count: int = 0
    h3_count: int = 0
    
    # Links
    internal_links_count: int = 0
    external_links_count: int = 0
    
    # Images
    images_count: int = 0
    images_with_alt_count: int = 0
    
    # Scripts and resources
    external_scripts_count: int = 0
    external_stylesheets_count: int = 0
    
    # Advanced SEO
    canonical_tag_present: bool = False
    robots_txt_exists: bool = False
    robots_txt_blocks_crawling: bool = False
    sitemap_exists: bool = False
    
    # Mobile and accessibility
    mobile_friendly: bool = False
    viewport_configured: bool = False
    lazy_loading_images: int = 0
    
    # Meta and structured data
    meta_robots_noindex: bool = False
    structured_data_present: bool = False
    open_graph_present: bool = False
    open_graph_tags_count: int = 0
    twitter_cards_present: bool = False
    
    # Technical elements
    favicon_present: bool = False
    lang_attribute_present: bool = False
    charset_declared: bool = False
    
    # Code quality
    inline_css_count: int = 0
    inline_js_count: int = 0
    deprecated_html_tags: int = 0
    
    # Performance and optimization
    broken_links_count: int = 0
    redirect_chains: int = 0
    compression_enabled: bool = False
    minified_resources: int = 0
    cache_headers_present: bool = False
    
    # Security
    security_headers_count: int = 0
    mixed_content_issues: int = 0
    
    # Calculated scores
    accessibility_score: float = 0.0
    performance_score: float = 0.0
    seo_score: float = 0.0
    
    # Additional features for extensibility
    raw_features: Dict[str, Any] = {}

class AIAnalysisResult(BaseModel):
    score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    label: str
    recommendations: List[Recommendation]
    category_scores: Dict[str, float] = {}
    analysis_method: str = "rule_based"
    ai_explanation: Optional[str] = None

class AnalysisRequest(BaseModel):
    url: HttpUrl
    include_lighthouse: bool = False
    deep_crawl: bool = False

class DetailedRecommendation(BaseModel):
    title: str
    description: str
    impact: str
    effort: str
    priority: str
    resources: List[str] = []

class AuditDetails(BaseModel):
    status: str = Field(description="pass, fail, or warning")
    details: str
    recommendations: List[DetailedRecommendation] = []

class AnalysisResult(BaseModel):
    # Configure to allow model_ fields
    model_config = ConfigDict(protected_namespaces=())
    
    # Existing fields (unchanged for backward compatibility)
    url: str
    timestamp: str
    crawlability_score: float = Field(ge=0, le=100)
    confidence: float = Field(ge=0, le=1)
    label: str
    features: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    
    # NEW: Individual scores for enhanced SEO analysis (all optional for backward compatibility)
    individual_crawlability_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual crawlability score")
    individual_indexability_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual indexability score")
    individual_site_structure_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual site structure score")
    individual_robots_txt_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual robots.txt score")
    individual_canonical_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual canonical score")
    individual_core_web_vitals_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual Core Web Vitals score")
    individual_mobile_friendliness_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual mobile friendliness score")
    individual_https_security_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual HTTPS security score")
    individual_broken_links_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual broken links score")
    individual_meta_tags_schema_score: Optional[float] = Field(default=None, ge=0, le=100, description="Individual meta tags and schema score")
    
    # Existing detailed audit sections (unchanged)
    crawlability_details: Optional[AuditDetails] = None
    indexability_details: Optional[AuditDetails] = None
    site_structure_details: Optional[AuditDetails] = None
    robots_txt_details: Optional[AuditDetails] = None
    canonical_issues_details: Optional[AuditDetails] = None
    core_web_vitals_details: Optional[AuditDetails] = None
    mobile_friendliness_details: Optional[AuditDetails] = None
    https_security_details: Optional[AuditDetails] = None
    broken_links_details: Optional[AuditDetails] = None
    meta_tags_headers_schema_details: Optional[AuditDetails] = None
    
    # Existing fields (unchanged)
    analysis_time: float
    model_version: str
    backend_status: str = "online"

class BatchAnalysisRequest(BaseModel):
    urls: List[HttpUrl] = Field(min_length=1, max_length=100)
    include_lighthouse: bool = False

class BatchAnalysisResult(BaseModel):
    batch_id: str
    status: str  # "processing", "completed", "failed"
    total_urls: int
    processed: int = 0
    failed: int = 0
    results: List[AnalysisResult] = []
    started_at: datetime
    completed_at: Optional[datetime] = None

class ValidationResult(BaseModel):
    is_valid: bool
    normalized_url: Optional[str] = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    redirect_chain: Optional[List[str]] = None

class GoogleSearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    position: int

class URLVerificationResult(BaseModel):
    is_real: bool
    is_indexed: bool
    search_results: List[GoogleSearchResult] = []
    verification_method: str
    confidence: float = Field(ge=0, le=1)

class HealthCheckResult(BaseModel):
    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: str
    version: str
    components: Dict[str, bool]
    system_info: Dict[str, Any] = {}
