"""
AFRO-GENOMICS Research Platform
Backend API - Pydantic Schemas

Request/response schemas with validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, List, Any
from datetime import datetime
from enum import Enum


# ==================== ENUMS ====================

class UserRoleEnum(str, Enum):
    LAB_ADMIN = "Lab Admin"
    RESEARCHER = "Researcher"
    LAB_TECHNICIAN = "Lab Technician"
    OBSERVER = "Observer"


class SampleStatusEnum(str, Enum):
    RECEIVED = "Received"
    PROCESSING = "Processing"
    RESULTS_AVAILABLE = "Results Available"
    ARCHIVED = "Archived"


class ConsentStatusEnum(str, Enum):
    ACTIVE = "Active"
    WITHDRAWN = "Withdrawn"
    EXPIRED = "Expired"


# ==================== AUTH SCHEMAS ====================

class LoginRequest(BaseModel):
    """Login request with MFA code"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    mfa_code: Optional[str] = None


class LoginResponse(BaseModel):
    """Login response with tokens"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: str
    user: "UserResponse"


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


# ==================== USER SCHEMAS ====================

class UserCreate(BaseModel):
    """Create new user"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRoleEnum
    institution_id: str


class UserResponse(BaseModel):
    """User response (safe to return)"""
    id: str
    email: str
    role: UserRoleEnum
    institution_id: str
    mfa_enabled: bool
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== INSTITUTION SCHEMAS ====================

class InstitutionCreate(BaseModel):
    """Create institution"""
    name: str
    country: str
    irb_approval_number: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    data_retention_months: int = 60


class InstitutionResponse(BaseModel):
    """Institution response"""
    id: str
    name: str
    country: str
    irb_approval_number: Optional[str]
    contact_person: Optional[str]
    data_retention_months: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== CONSENT SCHEMAS ====================

class PermittedUses(BaseModel):
    """Consent permitted uses"""
    research: bool = True
    publication: bool = True
    secondary_research: bool = True
    third_party_sharing: bool = False


class ConsentRecordCreate(BaseModel):
    """Create consent record"""
    user_id: str
    consent_version: str
    data_retention_period: str
    permitted_uses: PermittedUses
    irb_reference: Optional[str] = None


class ConsentRecordResponse(BaseModel):
    """Consent record response"""
    id: str
    user_id: str
    consent_version: str
    signed_at: datetime
    data_retention_period: str
    permitted_uses: Dict[str, bool]
    withdrawal_status: ConsentStatusEnum
    irb_reference: Optional[str]

    class Config:
        from_attributes = True


class ConsentWithdrawRequest(BaseModel):
    """Request consent withdrawal"""
    consent_id: str
    reason: Optional[str] = None


class ConsentWithdrawResponse(BaseModel):
    """Consent withdrawal response"""
    consent_id: str
    withdrawal_status: ConsentStatusEnum
    deletion_scheduled_for: datetime


# ==================== SAMPLE SCHEMAS ====================

class SampleCreate(BaseModel):
    """Upload sample metadata"""
    sample_id: str = Field(..., min_length=5, max_length=50)
    participant_id: Optional[str] = None
    consent_id: str
    notes: Optional[str] = None


class SampleResponse(BaseModel):
    """Sample response"""
    id: str
    sample_id: str
    participant_id: Optional[str]
    user_id: str
    institution_id: str
    status: SampleStatusEnum
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class SampleListResponse(BaseModel):
    """Paginated sample list"""
    samples: List[SampleResponse]
    total: int
    limit: int
    offset: int


# ==================== ANCESTRY RESULT SCHEMAS ====================

class ConfidenceInterval(BaseModel):
    """Confidence interval representation"""
    lower: float = Field(..., ge=0, le=100)
    upper: float = Field(..., ge=0, le=100)
    unit: str = "percentage"


class PopulationEstimate(BaseModel):
    """Population ancestry estimate"""
    population_group: str
    percentage: float = Field(..., ge=0, le=100)
    confidence_interval: ConfidenceInterval
    sample_size_reference: int
    reference_dataset: str


class AncestryResultsResponse(BaseModel):
    """Ancestry results for a sample"""
    sample_id: str
    primary_populations: List[PopulationEstimate]
    methodology: str
    limitations: str
    confidence_note: str


# ==================== HEALTH MARKER SCHEMAS ====================

class HealthMarkerResponse(BaseModel):
    """Health marker (gene variant) response"""
    gene: str
    variant: str
    phenotype: str
    genotype: str
    clinical_significance: Optional[str] = None
    population_frequency: Optional[Dict[str, str]] = None
    disclaimer: str

    class Config:
        from_attributes = True


# ==================== FULL RESULTS SCHEMAS ====================

class SampleResultsResponse(BaseModel):
    """Complete results for a sample (ancestry + health markers)"""
    sample_id: str
    sample_status: SampleStatusEnum
    results_computed_at: datetime
    
    disclaimer: str = (
        "Results are for research use only. Not diagnostic. "
        "Consult medical professionals for clinical interpretation."
    )
    
    ancestry: AncestryResultsResponse
    health_markers: List[HealthMarkerResponse]


# ==================== AUDIT LOG SCHEMAS ====================

class AuditLogResponse(BaseModel):
    """Audit log entry"""
    id: str
    user_id: str
    user_email: Optional[str] = None
    action: str
    resource_accessed: Optional[str] = None
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Paginated audit log"""
    logs: List[AuditLogResponse]
    total: int
    limit: int
    offset: int


# ==================== DATA EXPORT SCHEMAS ====================

class DataExportRequest(BaseModel):
    """Request data export with justification"""
    sample_ids: List[str]
    export_format: str = "JSON"  # JSON, CSV, VCF
    justification: str = Field(..., min_length=50)
    export_scope: str = "metadata_and_results"  # metadata_only, metadata_and_results


class DataExportResponse(BaseModel):
    """Data export response"""
    export_id: str
    status: str  # Pending Review, Approved, Completed
    requested_at: datetime
    estimated_completion: Optional[datetime] = None
    notification_email: str


# ==================== ERROR SCHEMAS ====================

class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Update forward references
LoginResponse.update_forward_refs()
