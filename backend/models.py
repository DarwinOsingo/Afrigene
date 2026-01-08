"""
AFRO-GENOMICS Research Platform
Backend API - Database Models

This module defines the SQLAlchemy ORM models for:
- Users and authentication
- Consent records (IRB-linked)
- Sample metadata and tracking
- Ancestry results with confidence intervals
- Health markers and genetic variants
- Audit logging
"""

from datetime import datetime, timedelta
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text, Enum, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import uuid

Base = declarative_base()


class SampleStatus(str, enum.Enum):
    """Sample processing status"""
    RECEIVED = "Received"
    PROCESSING = "Processing"
    RESULTS_AVAILABLE = "Results Available"
    ARCHIVED = "Archived"


class UserRole(str, enum.Enum):
    """User roles for RBAC"""
    LAB_ADMIN = "Lab Admin"
    RESEARCHER = "Researcher"
    LAB_TECHNICIAN = "Lab Technician"
    OBSERVER = "Observer"


class ConsentWithdrawalStatus(str, enum.Enum):
    """Consent withdrawal status"""
    ACTIVE = "Active"
    WITHDRAWN = "Withdrawn"
    EXPIRED = "Expired"


class User(Base):
    """
    Lab users with role-based access control
    
    Fields:
        - email: Unique identifier (institutional email recommended)
        - hashed_password: bcrypt hash
        - role: Lab Admin | Researcher | Lab Technician | Observer
        - institution_id: Parent institution
        - mfa_enabled: Multi-factor authentication status
        - mfa_secret: Encrypted TOTP secret (if enabled)
    """
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    
    role = Column(Enum(UserRole), nullable=False, default=UserRole.RESEARCHER)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=False)
    
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)  # Encrypted TOTP secret
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="users")
    samples = relationship("Sample", back_populates="user")
    consent_records = relationship("ConsentRecord", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

    __table_args__ = (
        Index("idx_institution_email", "institution_id", "email"),
    )


class Institution(Base):
    """
    Partner institutions (labs, research centers, hospitals)
    
    Fields:
        - name: Institution name
        - country: Country of operation
        - irb_approval_number: IRB/Ethics committee reference
        - contact_person: Institutional contact
        - data_retention_months: Data retention policy
    """
    __tablename__ = "institutions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    country = Column(String(100), nullable=False)
    irb_approval_number = Column(String(100), nullable=True)
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    data_retention_months = Column(Integer, default=60)  # 5 years
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("User", back_populates="institution")
    samples = relationship("Sample", back_populates="institution")


class ConsentRecord(Base):
    """
    Informed consent documents (IRB-linked)
    
    Fields:
        - user_id: Consenting researcher/user
        - consent_version: Consent form version (v2.1, etc.)
        - signed_at: Timestamp of consent signature
        - data_retention_period: How long data retained
        - permitted_uses: JSON object defining allowed uses
        - withdrawal_status: Active | Withdrawn | Expired
        - irb_reference: Link to IRB approval
    """
    __tablename__ = "consent_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    consent_version = Column(String(20), nullable=False)  # e.g., "v2.1"
    
    signed_at = Column(DateTime, default=datetime.utcnow)
    data_retention_period = Column(String(50), nullable=False)  # "60 months", "5 years"
    
    # JSON object: {research: bool, publication: bool, secondary_research: bool, third_party_sharing: bool}
    permitted_uses = Column(JSON, nullable=False, default={
        "research": True,
        "publication": True,
        "secondary_research": True,
        "third_party_sharing": False
    })
    
    withdrawal_status = Column(Enum(ConsentWithdrawalStatus), default=ConsentWithdrawalStatus.ACTIVE)
    irb_reference = Column(String(100), nullable=True)
    
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="consent_records")
    samples = relationship("Sample", back_populates="consent_record")

    __table_args__ = (
        Index("idx_user_active_consent", "user_id", "withdrawal_status"),
    )


class Sample(Base):
    """
    Genomic sample metadata and tracking
    
    Fields:
        - sample_id: Lab-specific sample identifier (e.g., "KEN-2024-00523")
        - participant_id: De-identified participant (if applicable)
        - user_id: Lab user who uploaded
        - institution_id: Owning institution
        - consent_id: Linked consent record
        - status: Received | Processing | Results Available | Archived
        - uploaded_at: Upload timestamp
        - processed_at: Results computation timestamp
    """
    __tablename__ = "samples"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sample_id = Column(String(50), nullable=False, index=True)  # e.g., "KEN-2024-00523"
    participant_id = Column(String(50), nullable=True)  # De-identified if applicable
    
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=False)
    consent_id = Column(String(36), ForeignKey("consent_records.id"), nullable=False)
    
    status = Column(Enum(SampleStatus), default=SampleStatus.RECEIVED)
    
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="samples")
    institution = relationship("Institution", back_populates="samples")
    consent_record = relationship("ConsentRecord", back_populates="samples")
    ancestry_results = relationship("AncestryResult", back_populates="sample")
    health_markers = relationship("HealthMarker", back_populates="sample")

    __table_args__ = (
        Index("idx_institution_status", "institution_id", "status"),
        Index("idx_sample_id_institution", "sample_id", "institution_id"),
    )


class AncestryResult(Base):
    """
    Ancestry inference results with confidence intervals
    
    Fields:
        - sample_id: Parent sample
        - population_group: African population classification
        - percentage: Ancestry percentage (0-100)
        - confidence_interval_lower/upper: 95% CI bounds
        - reference_dataset: Dataset used for inference
        - methodology_version: Algorithm/method version
    """
    __tablename__ = "ancestry_results"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sample_id = Column(String(36), ForeignKey("samples.id"), nullable=False)
    
    population_group = Column(String(100), nullable=False)  # Luhya, Yoruba, Maasai, etc.
    percentage = Column(Float, nullable=False)  # 0-100
    confidence_interval_lower = Column(Float, nullable=False)  # e.g., 78
    confidence_interval_upper = Column(Float, nullable=False)  # e.g., 92
    
    reference_dataset = Column(String(100), nullable=False)  # e.g., "1KG-African-2023"
    reference_sample_size = Column(Integer, nullable=False)
    methodology_version = Column(String(50), nullable=False)
    
    computed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sample = relationship("Sample", back_populates="ancestry_results")


class HealthMarker(Base):
    """
    Health-relevant genetic markers (non-diagnostic, research-use only)
    
    Fields:
        - sample_id: Parent sample
        - gene_name: Gene symbol (LCT, HBB, G6PD, etc.)
        - variant_rsid: dbSNP identifier
        - genotype: Diploid genotype (0/0, 0/1, 1/1)
        - phenotype: Inferred phenotype
        - clinical_significance: ACMG classification (mock)
        - population_frequency: JSON object of pop frequencies
    """
    __tablename__ = "health_markers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sample_id = Column(String(36), ForeignKey("samples.id"), nullable=False)
    
    gene_name = Column(String(50), nullable=False)  # LCT, HBB, G6PD, DUFFY, etc.
    variant_rsid = Column(String(20), nullable=False)  # rs334, rs4988235, etc.
    chromosome = Column(String(5), nullable=True)  # chr2, chr11, etc.
    position = Column(Integer, nullable=True)
    
    genotype = Column(String(10), nullable=False)  # 0/0, 0/1, 1/1
    phenotype = Column(String(255), nullable=False)  # Lactase Persistent, Carrier, etc.
    
    clinical_significance = Column(String(255), nullable=True)
    
    # JSON: {"East African": "0.70", "West African": "0.05"}
    population_frequency = Column(JSON, nullable=True)
    
    disclaimer = Column(Text, nullable=False, default="For research use only. Not diagnostic.")
    
    computed_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    sample = relationship("Sample", back_populates="health_markers")


class AuditLog(Base):
    """
    Complete audit trail of data access and modifications
    
    Fields:
        - user_id: User performing action
        - action: accessed_results | exported_data | modified_consent | etc.
        - resource_accessed: sample_id | consent_id | user_id
        - timestamp: When action occurred
        - ip_address: Source IP (privacy-preserving format)
        - user_agent: Browser/client identifier
    """
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    action = Column(String(100), nullable=False)  # accessed_results, exported_data, etc.
    resource_accessed = Column(String(100), nullable=True)  # sample_id, consent_id, etc.
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    ip_address = Column(String(45), nullable=True)  # Supports IPv6
    user_agent = Column(String(500), nullable=True)
    
    details = Column(JSON, nullable=True)  # Additional context

    # Relationships
    user = relationship("User", back_populates="audit_logs")

    __table_args__ = (
        Index("idx_audit_user_timestamp", "user_id", "timestamp"),
        Index("idx_audit_resource", "resource_accessed", "timestamp"),
    )


# Index definitions for common queries
Index("idx_sample_upload_date", Sample.uploaded_at)
Index("idx_ancestry_population", AncestryResult.population_group)
Index("idx_health_gene", HealthMarker.gene_name)
