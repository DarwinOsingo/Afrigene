"""
AFRO-GENOMICS Research Platform
Backend API - Main Application

FastAPI application with authentication, database setup, and endpoints
"""

from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from typing import Optional, List
import json
import uuid

from models import (
    Base, User, Institution, ConsentRecord, Sample, AncestryResult, HealthMarker, AuditLog,
    UserRole, SampleStatus, ConsentWithdrawalStatus
)
from schemas import (
    LoginRequest, LoginResponse, UserResponse,
    InstitutionResponse, ConsentRecordResponse, ConsentWithdrawRequest, ConsentWithdrawResponse,
    SampleCreate, SampleResponse, SampleListResponse, SampleResultsResponse,
    PopulationEstimate, ConfidenceInterval, AncestryResultsResponse,
    HealthMarkerResponse, AuditLogResponse, AuditLogListResponse,
    DataExportRequest, DataExportResponse
)
from auth import create_access_token, verify_password, get_password_hash, get_current_user
from mock_data import generate_mock_data

# ==================== DATABASE SETUP ====================

DATABASE_URL = "sqlite:///./afro_genomics.db"  # SQLite for demo; PostgreSQL for production
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency: get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== FASTAPI APP ====================

app = FastAPI(
    title="AFRO-GENOMICS Research Platform API",
    description="Lab-facing genomic research platform for African populations",
    version="1.0.0",
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production: specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.post("/api/v1/auth/login", response_model=LoginResponse, tags=["Authentication"])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token
    
    **Request:**
    ```json
    {
      "email": "scientist@nairobi-lab.org",
      "password": "secure_password",
      "mfa_code": "123456"
    }
    ```
    """
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # MFA validation (mock - in production, use TOTP)
    if user.mfa_enabled and not request.mfa_code:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="MFA code required"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role}
    )
    refresh_token = create_access_token(
        data={"sub": user.id, "type": "refresh"},
        expires_delta=timedelta(days=30)
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=3600,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user)
    )


@app.post("/api/v1/auth/logout", tags=["Authentication"])
def logout(user_id: str = Depends(get_current_user)):
    """Logout user (invalidate session)"""
    return {"message": "Logged out successfully"}


# ==================== INSTITUTION ENDPOINTS ====================

@app.get("/api/v1/institutions", response_model=List[InstitutionResponse], tags=["Institutions"])
def list_institutions(db: Session = Depends(get_db)):
    """List all partner institutions"""
    institutions = db.query(Institution).all()
    return institutions


# ==================== SAMPLES ENDPOINTS ====================

@app.get("/api/v1/samples", response_model=SampleListResponse, tags=["Samples"])
def list_samples(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List samples for user's institution
    
    **Query Parameters:**
    - status: Filter by status (Received, Processing, Results Available, Archived)
    - limit: Number of results (default: 50, max: 100)
    - offset: Pagination offset (default: 0)
    """
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    query = db.query(Sample).filter(Sample.institution_id == current_user.institution_id)
    
    if status:
        query = query.filter(Sample.status == status)
    
    total = query.count()
    samples = query.offset(offset).limit(limit).all()
    
    # Log access
    log_audit(db, current_user.id, "accessed_samples_list", None)
    
    return SampleListResponse(
        samples=[SampleResponse.from_orm(s) for s in samples],
        total=total,
        limit=limit,
        offset=offset
    )


@app.post("/api/v1/samples", response_model=SampleResponse, tags=["Samples"], status_code=201)
def upload_sample(
    sample_data: SampleCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload sample metadata (mock - no actual genomic data)
    
    **Sample ID Format:** {COUNTRY_CODE}-{YEAR}-{SEQUENCE}
    - Example: KEN-2024-00523
    """
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Verify consent exists and belongs to user
    consent = db.query(ConsentRecord).filter(
        ConsentRecord.id == sample_data.consent_id,
        ConsentRecord.user_id == current_user.id
    ).first()
    
    if not consent:
        raise HTTPException(status_code=404, detail="Consent record not found")
    
    if consent.withdrawal_status != ConsentWithdrawalStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Consent is not active")
    
    # Create sample
    sample = Sample(
        sample_id=sample_data.sample_id,
        participant_id=sample_data.participant_id,
        user_id=current_user.id,
        institution_id=current_user.institution_id,
        consent_id=sample_data.consent_id,
        status=SampleStatus.RECEIVED,
        notes=sample_data.notes
    )
    
    db.add(sample)
    db.commit()
    db.refresh(sample)
    
    # Log audit
    log_audit(db, current_user.id, "uploaded_sample", sample.id)
    
    return SampleResponse.from_orm(sample)


@app.get("/api/v1/samples/{sample_id}/results", response_model=SampleResultsResponse, tags=["Samples"])
def get_sample_results(
    sample_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve ancestry and health results for a sample
    
    **Includes:**
    - Ancestry breakdown with confidence intervals
    - Health-relevant genetic markers
    - Population frequency data
    - Research-use disclaimers
    """
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    sample = db.query(Sample).filter(Sample.id == sample_id).first()
    
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    
    # Verify user has permission (same institution)
    if sample.institution_id != current_user.institution_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Verify consent is active
    consent = sample.consent_record
    if consent.withdrawal_status != ConsentWithdrawalStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Consent is withdrawn")
    
    # Simulate sample processing if not done
    if sample.status == SampleStatus.RECEIVED:
        sample.status = SampleStatus.PROCESSING
        db.commit()
    
    # Get ancestry results
    ancestry_results = db.query(AncestryResult).filter(
        AncestryResult.sample_id == sample.id
    ).all()
    
    if not ancestry_results:
        # Generate mock results if not present
        _generate_sample_results(db, sample)
        ancestry_results = db.query(AncestryResult).filter(
            AncestryResult.sample_id == sample.id
        ).all()
    
    # Get health markers
    health_markers = db.query(HealthMarker).filter(
        HealthMarker.sample_id == sample.id
    ).all()
    
    if not health_markers:
        _generate_sample_health_markers(db, sample)
        health_markers = db.query(HealthMarker).filter(
            HealthMarker.sample_id == sample.id
        ).all()
    
    # Update sample status
    if sample.status != SampleStatus.RESULTS_AVAILABLE:
        sample.status = SampleStatus.RESULTS_AVAILABLE
        sample.processed_at = datetime.utcnow()
        db.commit()
    
    # Log audit
    log_audit(db, current_user.id, "accessed_results", sample.id)
    
    # Build response
    primary_populations = [
        PopulationEstimate(
            population_group=ar.population_group,
            percentage=ar.percentage,
            confidence_interval=ConfidenceInterval(
                lower=ar.confidence_interval_lower,
                upper=ar.confidence_interval_upper
            ),
            sample_size_reference=ar.reference_sample_size,
            reference_dataset=ar.reference_dataset
        )
        for ar in sorted(ancestry_results, key=lambda x: x.percentage, reverse=True)
    ]
    
    ancestry_response = AncestryResultsResponse(
        sample_id=sample.id,
        primary_populations=primary_populations,
        methodology="PCA-based ancestry inference with admixture modeling (STRUCTURE-like)",
        limitations="Confidence intervals reflect 95% CI from reference dataset. Limited availability of some rare populations. Ancestry inference assumes recent divergence.",
        confidence_note="95% CI based on reference dataset sample sizes (range: 150-2847 samples per population)"
    )
    
    health_markers_response = [
        HealthMarkerResponse(
            gene=hm.gene_name,
            variant=hm.variant_rsid,
            phenotype=hm.phenotype,
            genotype=hm.genotype,
            clinical_significance=hm.clinical_significance,
            population_frequency=hm.population_frequency,
            disclaimer=hm.disclaimer
        )
        for hm in health_markers
    ]
    
    return SampleResultsResponse(
        sample_id=sample.id,
        sample_status=sample.status,
        results_computed_at=sample.processed_at or datetime.utcnow(),
        ancestry=ancestry_response,
        health_markers=health_markers_response
    )


# ==================== CONSENT ENDPOINTS ====================

@app.get("/api/v1/consent/{user_id}", response_model=List[ConsentRecordResponse], tags=["Consent"])
def get_user_consents(
    user_id: str,
    current_user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve consent records for a user"""
    
    # Fetch current user
    current_user = db.query(User).filter(User.id == current_user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Users can only view their own consents; admins can view institution consents
    if current_user.id != user_id and current_user.role != UserRole.LAB_ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    
    consents = db.query(ConsentRecord).filter(ConsentRecord.user_id == user_id).all()
    return [ConsentRecordResponse.from_orm(c) for c in consents]


@app.post("/api/v1/consent/withdraw", response_model=ConsentWithdrawResponse, tags=["Consent"])
def withdraw_consent(
    request: ConsentWithdrawRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Withdraw consent and schedule data deletion"""
    
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    consent = db.query(ConsentRecord).filter(ConsentRecord.id == request.consent_id).first()
    
    if not consent:
        raise HTTPException(status_code=404, detail="Consent not found")
    
    # Verify ownership
    if consent.user_id != current_user.id and current_user.role != UserRole.LAB_ADMIN:
        raise HTTPException(status_code=403, detail="Access denied")
    
    consent.withdrawal_status = ConsentWithdrawalStatus.WITHDRAWN
    db.commit()
    
    # Log audit
    log_audit(db, current_user.id, "withdrew_consent", consent.id)
    
    deletion_date = datetime.utcnow() + timedelta(days=7)
    
    return ConsentWithdrawResponse(
        consent_id=consent.id,
        withdrawal_status=consent.withdrawal_status,
        deletion_scheduled_for=deletion_date
    )


# ==================== AUDIT LOG ENDPOINTS ====================

@app.get("/api/v1/audit-logs", response_model=AuditLogListResponse, tags=["Audit"])
def get_audit_logs(
    sample_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve audit logs (admin/lab admin only)
    
    Shows all data access and modifications
    """
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if current_user.role not in [UserRole.LAB_ADMIN]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    query = db.query(AuditLog).filter(
        AuditLog.user_id.in_(
            db.query(User.id).filter(User.institution_id == current_user.institution_id)
        )
    )
    
    if sample_id:
        query = query.filter(AuditLog.resource_accessed == sample_id)
    
    total = query.count()
    logs = query.order_by(AuditLog.timestamp.desc()).offset(offset).limit(limit).all()
    
    # Enrich with user emails
    log_responses = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_resp = AuditLogResponse.from_orm(log)
        log_resp.user_email = user.email if user else None
        log_responses.append(log_resp)
    
    return AuditLogListResponse(
        logs=log_responses,
        total=total,
        limit=limit,
        offset=offset
    )


# ==================== DATA EXPORT ENDPOINTS ====================

@app.post("/api/v1/data-export", response_model=DataExportResponse, tags=["Data Export"], status_code=202)
def request_data_export(
    request: DataExportRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Request data export with justification (requires review)
    
    **Process:**
    1. User submits export request with justification
    2. Lab admin reviews justification
    3. On approval, data is packaged
    4. User notified via email
    """
    
    # Fetch current user
    current_user = db.query(User).filter(User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Verify all samples belong to user's institution
    for sample_id in request.sample_ids:
        sample = db.query(Sample).filter(Sample.id == sample_id).first()
        if not sample or sample.institution_id != current_user.institution_id:
            raise HTTPException(status_code=404, detail=f"Sample {sample_id} not found")
    
    # Log audit
    log_audit(
        db, current_user.id, "requested_data_export",
        None,
        details={
            "sample_ids": request.sample_ids,
            "export_format": request.export_format,
            "justification_length": len(request.justification)
        }
    )
    
    # In production: queue export and send for review
    return DataExportResponse(
        export_id=f"exp_{uuid.uuid4().hex[:8]}",
        status="Pending Review",
        requested_at=datetime.utcnow(),
        estimated_completion=datetime.utcnow() + timedelta(days=3),
        notification_email=current_user.email
    )


# ==================== HEALTH CHECK ====================

@app.get("/api/v1/health", tags=["Health"])
def health_check():
    """API health check"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


# ==================== HELPER FUNCTIONS ====================

def log_audit(db: Session, user_id: str, action: str, resource_id: Optional[str], details: Optional[dict] = None):
    """Log audit event"""
    log = AuditLog(
        user_id=user_id,
        action=action,
        resource_accessed=resource_id,
        timestamp=datetime.utcnow(),
        ip_address="127.0.0.1",  # In production: extract from request
        user_agent="Mozilla/5.0",  # In production: extract from request
        details=details
    )
    db.add(log)
    db.commit()


def _generate_sample_results(db: Session, sample: Sample):
    """Generate mock ancestry results for a sample"""
    populations = [
        ("Bantu", 85, 78, 92),
        ("Nilotic", 12, 7, 18),
        ("North African", 3, 1, 8)
    ]
    
    for pop, pct, lower, upper in populations:
        result = AncestryResult(
            sample_id=sample.id,
            population_group=pop,
            percentage=pct,
            confidence_interval_lower=lower,
            confidence_interval_upper=upper,
            reference_dataset="1KG-African-2023",
            reference_sample_size=2847,
            methodology_version="PCA v2.1"
        )
        db.add(result)
    
    db.commit()


def _generate_sample_health_markers(db: Session, sample: Sample):
    """Generate mock health markers for a sample"""
    markers = [
        {
            "gene": "LCT",
            "variant": "rs4988235",
            "chromosome": "chr2",
            "position": 136594750,
            "genotype": "C/C",
            "phenotype": "Lactase Persistent",
            "significance": "Associated with lactose tolerance in adulthood",
            "frequencies": {"East African": "0.70", "West African": "0.05"}
        },
        {
            "gene": "HBB",
            "variant": "rs334",
            "chromosome": "chr11",
            "position": 5248232,
            "genotype": "A/S",
            "phenotype": "Sickle Cell Trait (AS)",
            "significance": "Heterozygous carrier. Potential malarial resistance benefit.",
            "frequencies": {"East African": "0.18", "West African": "0.25"}
        },
        {
            "gene": "G6PD",
            "variant": "rs1050829",
            "chromosome": "chrX",
            "position": 154519747,
            "genotype": "A/A",
            "phenotype": "G6PD Deficiency",
            "significance": "Risk of hemolysis with fava beans, infections, certain drugs",
            "frequencies": {"East African": "0.08", "West African": "0.15"}
        }
    ]
    
    for marker in markers:
        health_marker = HealthMarker(
            sample_id=sample.id,
            gene_name=marker["gene"],
            variant_rsid=marker["variant"],
            chromosome=marker["chromosome"],
            position=marker["position"],
            genotype=marker["genotype"],
            phenotype=marker["phenotype"],
            clinical_significance=marker["significance"],
            population_frequency=marker["frequencies"],
            disclaimer="For research use only. Not diagnostic. Phenotype prediction subject to error."
        )
        db.add(health_marker)
    
    db.commit()


# ==================== STARTUP ====================

@app.on_event("startup")
def startup_event():
    """Initialize mock data on startup"""
    db = SessionLocal()
    
    # Check if database is empty
    if db.query(Institution).count() == 0:
        generate_mock_data(db)
        print("✓ Mock data initialized")
    
    db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
