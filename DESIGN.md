# AFRO-GENOMICS RESEARCH PLATFORM
## System Architecture & Design Document

**Platform Version:** 1.0 (Prototype)  
**Date:** January 2026  
**Status:** Reference Design & Mockup (NOT Production-Ready)

---

## EXECUTIVE SUMMARY

**AFRO-GENOMICS** is a lab-facing research portal designed to support African genomic research with scientific rigor, ethical transparency, and data sovereignty as foundational principles.

### Key Differentiators
- **Scientific focus:** Population genetics research, not ancestry entertainment
- **Data sovereignty:** No third-party data sales; African data remains under African stewardship
- **Academic rigor:** Confidence intervals, reference datasets, peer-reviewed methodology
- **Institutional trust:** IRB-style consent, audit logging, transparent limitations
- **Cultural respect:** Treats African genetic diversity as a research priority

⚠️ **IMPORTANT:** This is a **design mockup** suitable for institutional presentation. It uses simulated data and demonstrates architectural principles. It is **NOT** medically validated, **NOT** clinically deployed, and **NOT** HIPAA/GDPR compliant without additional regulatory work.

---

## MISSION & SCOPE

### Mission Statement
To advance genomic research within and across African populations through an ethical, transparent, and scientifically rigorous platform that centers data sovereignty and community benefit.

### Target Users
1. **Medical genetics laboratories** (national health systems)
2. **University research institutions** (anthropology, population genetics)
3. **Research partners** (international collaborators with local agreements)
4. **Ethics review bodies** (IRB, research committees)

### NOT Intended For
- Direct-to-consumer ancestry testing
- Ancestry entertainment marketing
- Data monetization or resale
- Medical diagnosis (research use only)

---

## SYSTEM ARCHITECTURE

### High-Level Architecture Diagram (Textual)

```
┌─────────────────────────────────────────────────────────────────┐
│                    USERS & INSTITUTIONS                          │
├─────────────────────────────────────────────────────────────────┤
│ Lab Technicians | Scientists | Admins | Ethics Reviewers        │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTPS/TLS 1.3
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│               FRONTEND (React + Tailwind)                         │
├─────────────────────────────────────────────────────────────────┤
│ • Public pages (marketing/education)                             │
│ • Lab portal (authentication + dashboard)                        │
│ • Results visualization & reports                               │
│ • Consent & permissions management                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │ REST API (JSON)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│         BACKEND API (FastAPI + Python 3.10+)                     │
├─────────────────────────────────────────────────────────────────┤
│ • Authentication & RBAC                                          │
│ • Consent management                                             │
│ • Sample processing workflow                                    │
│ • Results aggregation                                           │
│ • Audit logging                                                 │
│ • Data access controls                                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │ ORM (SQLAlchemy)
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│     DATABASE (PostgreSQL + Encrypted Storage)                    │
├─────────────────────────────────────────────────────────────────┤
│ • Users & roles (with MFA metadata)                              │
│ • Consent records (IRB-linked)                                  │
│ • Sample metadata (status tracking)                             │
│ • Ancestry results (with CI intervals)                          │
│ • Health markers (gene/variant annotations)                     │
│ • Audit logs (access tracking)                                 │
│ • Raw genomic files (S3-compatible, encrypted)                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## DATABASE SCHEMA

### Schema Overview & Relationships

```
users (PK: id)
├── email (unique)
├── hashed_password
├── role (Lab Admin | Researcher | Lab Technician | Observer)
├── institution_id (FK)
├── mfa_enabled, mfa_secret
├── created_at, last_login
└── is_active

institutions (PK: id)
├── name
├── country
├── contact_person
├── irb_approval_number
└── data_retention_months

samples (PK: id)
├── sample_id (e.g., "KEN-2024-00523")
├── user_id (FK) -- lab owner
├── institution_id (FK)
├── consent_id (FK)
├── status (Received | Processing | Results Available | Archived)
├── uploaded_at, processed_at
└── notes

consent_records (PK: id)
├── user_id (FK)
├── consent_version (e.g., "v2.1")
├── signed_at (timestamp)
├── data_retention_period (e.g., 5 years)
├── permitted_uses (JSON: research, publication, secondary_research)
├── withdrawal_status (Active | Withdrawn)
└── irb_reference

ancestry_results (PK: id)
├── sample_id (FK)
├── population_group (Luhya | Yoruba | Maasai | etc.)
├── percentage (float, 0-100)
├── confidence_interval_lower (e.g., 78)
├── confidence_interval_upper (e.g., 92)
├── reference_dataset (e.g., "1KG-African-2023")
├── methodology_version
└── computed_at

health_markers (PK: id)
├── sample_id (FK)
├── gene_name (LCT | HBB | G6PD | etc.)
├── variant_rsid
├── genotype (0/0 | 0/1 | 1/1)
├── phenotype (Lactase Persistent | Carrier | Resistant)
├── clinical_significance
├── population_frequency (JSON)
└── disclaimer ("For research use only")

audit_logs (PK: id)
├── user_id (FK)
├── action (accessed_results | exported_data | modified_consent)
├── resource_accessed (sample_id | consent_id)
├── timestamp
├── ip_address
└── user_agent
```

---

## API ENDPOINTS SPECIFICATION

### Base URL
```
https://api.afro-genomics.example.com/api/v1
```

### Authentication

#### POST /auth/login
**Purpose:** Authenticate lab user  
**Request:**
```json
{
  "email": "scientist@nairobi-lab.org",
  "password": "secure_password",
  "mfa_code": "123456"
}
```
**Response (200 OK):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600,
  "user": {
    "id": "usr_12345",
    "email": "scientist@nairobi-lab.org",
    "role": "Researcher",
    "institution": "Nairobi Medical Lab"
  }
}
```

#### POST /auth/logout
**Purpose:** Invalidate session  
**Headers:** `Authorization: Bearer <token>`

#### POST /auth/refresh
**Purpose:** Refresh expired token  
**Request:**
```json
{
  "refresh_token": "..."
}
```

---

### Samples Management

#### GET /samples
**Purpose:** List all samples for authenticated user's institution  
**Query Parameters:**
- `status` (optional): Received, Processing, Results Available
- `limit` (default: 50)
- `offset` (default: 0)

**Response (200 OK):**
```json
{
  "samples": [
    {
      "id": "smp_98765",
      "sample_id": "KEN-2024-00523",
      "status": "Results Available",
      "uploaded_at": "2025-11-15T10:30:00Z",
      "processed_at": "2025-11-18T14:22:00Z",
      "institution": "Kenyatta National Hospital",
      "consent_status": "Active"
    }
  ],
  "total": 145,
  "limit": 50,
  "offset": 0
}
```

#### GET /samples/{sample_id}/results
**Purpose:** Retrieve ancestry and health results  
**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "sample_id": "KEN-2024-00523",
  "sample_status": "Results Available",
  "results_computed_at": "2025-11-18T14:22:00Z",
  "disclaimer": "Results are for research use only. Not diagnostic. Consult medical professionals for clinical interpretation.",
  
  "ancestry": {
    "primary_populations": [
      {
        "population_group": "Bantu",
        "percentage": 85,
        "confidence_interval": {
          "lower": 78,
          "upper": 92
        },
        "sample_size_reference": 2847,
        "reference_dataset": "1KG-African-2023"
      },
      {
        "population_group": "Nilotic",
        "percentage": 12,
        "confidence_interval": {
          "lower": 7,
          "upper": 18
        },
        "sample_size_reference": 2847,
        "reference_dataset": "1KG-African-2023"
      }
    ],
    "methodology": "PCA-based ancestry inference with admixture modeling",
    "limitations": "Confidence intervals reflect 95% CI from reference dataset. Limited availability of some rare populations."
  },
  
  "health_markers": [
    {
      "gene": "LCT",
      "variant": "rs4988235",
      "phenotype": "Lactase Persistent",
      "genotype": "C/C",
      "clinical_significance": "Associated with lactose tolerance in adulthood",
      "population_frequency": {
        "East African": "0.70",
        "West African": "0.05"
      },
      "disclaimer": "For research use only. Phenotype prediction has error rates."
    },
    {
      "gene": "HBB",
      "variant": "rs334",
      "phenotype": "Sickle Cell Trait (AS)",
      "genotype": "A/S",
      "clinical_significance": "Heterozygous carrier. Potential malarial resistance benefit.",
      "population_frequency": {
        "East African": "0.18",
        "West African": "0.25"
      },
      "disclaimer": "Carrier status does not indicate disease. Genetic counseling recommended."
    }
  ]
}
```

#### POST /samples/upload
**Purpose:** Upload sample metadata (mock - no real genomic data)  
**Headers:** `Authorization: Bearer <token>`, `Content-Type: application/json`

**Request:**
```json
{
  "sample_id": "KEN-2024-00524",
  "participant_id": "part_9876",
  "consent_id": "con_5432",
  "notes": "Samples from Kikuyu population study cohort"
}
```

**Response (201 Created):**
```json
{
  "id": "smp_98766",
  "sample_id": "KEN-2024-00524",
  "status": "Received",
  "uploaded_at": "2025-12-01T09:15:00Z"
}
```

---

### Consent & Permissions

#### GET /consent/{user_id}
**Purpose:** Retrieve consent records for user  
**Headers:** `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "consents": [
    {
      "id": "con_5432",
      "consent_version": "v2.1",
      "signed_at": "2025-10-20T11:30:00Z",
      "data_retention_period": "60 months",
      "permitted_uses": {
        "research": true,
        "publication": true,
        "secondary_research": true,
        "third_party_sharing": false
      },
      "irb_reference": "IRB-2024-00156",
      "withdrawal_status": "Active"
    }
  ]
}
```

#### POST /consent/withdraw
**Purpose:** Withdraw consent and request data deletion  
**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "consent_id": "con_5432",
  "reason": "User-requested withdrawal"
}
```

**Response (200 OK):**
```json
{
  "consent_id": "con_5432",
  "withdrawal_status": "Withdrawn",
  "deletion_scheduled_for": "2025-12-08T00:00:00Z"
}
```

---

### Data Access & Audit

#### GET /audit-logs
**Purpose:** Retrieve access logs for institutional oversight  
**Headers:** `Authorization: Bearer <token>`  
**Query Parameters:** `sample_id`, `start_date`, `end_date`

**Response (200 OK):**
```json
{
  "logs": [
    {
      "id": "log_12345",
      "user_id": "usr_12345",
      "user_email": "scientist@nairobi-lab.org",
      "action": "accessed_results",
      "resource_accessed": "smp_98765",
      "timestamp": "2025-11-20T14:30:00Z",
      "ip_address": "197.254.x.x",
      "user_agent": "Mozilla/5.0..."
    }
  ],
  "total": 342
}
```

#### POST /data-export
**Purpose:** Request data export with justification  
**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "sample_ids": ["smp_98765", "smp_98766"],
  "export_format": "JSON",
  "justification": "Comparative population genetics analysis for publication in Nature Genetics",
  "export_scope": "metadata_and_results"
}
```

**Response (202 Accepted):**
```json
{
  "export_id": "exp_54321",
  "status": "Pending Review",
  "estimated_completion": "2025-12-05T00:00:00Z",
  "notification_email": "scientist@nairobi-lab.org"
}
```

---

### Health System Integration

#### GET /institutions
**Purpose:** List partner institutions  

**Response (200 OK):**
```json
{
  "institutions": [
    {
      "id": "inst_001",
      "name": "Kenyatta National Hospital",
      "country": "Kenya",
      "irb_approval_number": "KNH-IRB-2024-156",
      "contact_person": "Dr. Jane Kimani",
      "data_retention_months": 60
    }
  ]
}
```

---

## FRONTEND ARCHITECTURE

### Page Structure & Navigation

```
Public Pages:
├── /
│   └── HomePage (Mission, statistics, partnerships)
├── /science
│   └── ScienceMethodology (Populations, reference datasets, limitations)
├── /research-ethics
│   └── ResearchEthics (Consent, data sovereignty, IRB process)
├── /populations
│   └── PopulationsPage (Migration history, timelines, scholarly context)
├── /lab-partnerships
│   └── LabPartnerships (Integration workflow, technical requirements)
├── /pricing
│   └── Pricing (Institutional tiers, funding options)

Lab Portal:
├── /lab/login
│   └── LoginPage (Email, password, MFA)
├── /lab/dashboard
│   └── Dashboard (Sample overview, status counts, recent activity)
├── /lab/samples
│   └── SamplesList (Filterable table, bulk actions)
├── /lab/samples/:id
│   └── SampleDetail (Results, health markers, audit trail)
├── /lab/consent
│   └── ConsentManagement (Active consents, withdrawal option)
├── /lab/settings
│   └── Settings (User preferences, permissions)

Admin Pages:
├── /admin/users
│   └── UserManagement (Role assignment, institution access)
├── /admin/audit
│   └── AuditLog (Access tracking, export history)
```

### Component Hierarchy

```
App
├── Router (React Router v6)
├── PublicLayout
│   ├── Navbar (logo, links, login button)
│   ├── Page (dynamic)
│   └── Footer (links, legal, contact)
└── LabLayout (protected)
    ├── SideNav (navigation, logout)
    ├── Header (user info, breadcrumbs)
    ├── MainContent (page)
    └── MobileMenu
```

### Key UI Components

- `DataTable`: Searchable, sortable sample lists
- `ConfidenceInterval`: Visual representation of ancestry ranges
- `HealthMarkerCard`: Gene variant information with disclaimers
- `ConsentBanner`: Persistent reminder of research-only status
- `AuditLog`: Formatted access tracking
- `PopulationChart`: PCA/ancestry visualization

---

## SECURITY MODEL

### Authentication & Authorization

**Method:** JWT Token-Based  
**Flow:**
1. User authenticates with email + password + MFA code
2. Backend validates credentials against hashed DB records
3. Backend generates JWT token (RS256 signing, HS256 verification)
4. Token includes: user_id, role, institution_id, expiration (1 hour)
5. Refresh tokens allow 30-day session extension
6. All requests require Authorization header

**Role-Based Access Control (RBAC):**

| Role | Capabilities |
|------|--------------|
| Lab Admin | Create users, manage institution samples, view audit logs, set permissions |
| Researcher | View samples, export results, publish data |
| Lab Technician | Upload samples, track processing status |
| Observer | Read-only access to assigned samples |

### Data Security

**At Rest:**
- Passwords: bcrypt (cost=12)
- Sensitive fields: AES-256 encryption in PostgreSQL
- Genomic files: Encrypted S3 with KMS keys
- Database backups: Encrypted, stored geographically distributed

**In Transit:**
- All APIs: TLS 1.3 minimum
- HSTS headers enforced
- No unencrypted HTTP fallback

**Access Control:**
- Principle of least privilege (each user sees only their institution's data)
- Granular consent tracking (user must have affirmative consent to access sample)
- Audit every data access (timestamp, user, IP, action)

### Compliance Principles

This design incorporates privacy principles similar to GDPR/HIPAA/APTA (African Personal Data Protection Act):

| Principle | Implementation |
|-----------|-----------------|
| Data Minimization | Only collect population & health genetics; no identifying information |
| Purpose Limitation | Results used only for stated research purpose |
| Consent | Explicit, versioned, withdrawal-enabled consent records |
| Transparency | Privacy policy, methodology, limitations clearly stated |
| Right to Deletion | Users can withdraw and request data expungement |
| Data Sovereignty | No third-party sales; data remains under institutional control |
| Audit Trail | Complete logging of access and modifications |
| Encryption | All sensitive data encrypted at rest and in transit |

⚠️ **CRITICAL DISCLAIMER:** This design demonstrates principles but is NOT a substitute for legal review, regulatory certification, or institutional audit.

---

## MOCK DATA SPECIFICATIONS

### African Population Groups Represented

**Nilotic Populations:**
- Dinka (South Sudan)
- Nuer (South Sudan, Ethiopia)
- Maasai (Kenya, Tanzania)
- Samburu (Kenya)

**Bantu Populations:**
- Luhya (Kenya)
- Kikuyu (Kenya)
- Zulu (South Africa)
- Igbo (Nigeria)
- Xhosa (South Africa)

**Cushitic Populations:**
- Somali (Somalia, Kenya, Ethiopia)
- Oromo (Ethiopia)
- Afar (Ethiopia, Djibouti, Eritrea)

**Afroasiatic Populations:**
- Hausa (Nigeria, Niger)
- Berber/Amazigh (North Africa)
- Amhara (Ethiopia)

**West African Populations:**
- Yoruba (Nigeria)
- Akan (Ghana, Côte d'Ivoire)
- Mandinka (Senegal, Mali)

### Ancestry Result Examples

```json
{
  "sample_id": "KEN-2024-00523",
  "ancestry": {
    "primary": [
      {
        "population": "Bantu",
        "percentage": 85,
        "ci_lower": 78,
        "ci_upper": 92
      },
      {
        "population": "Nilotic",
        "percentage": 12,
        "ci_lower": 7,
        "ci_upper": 18
      },
      {
        "population": "North African",
        "percentage": 3,
        "ci_lower": 1,
        "ci_upper": 8
      }
    ],
    "confidence": "95% CI based on 2847 reference samples from 1KG-African-2023"
  }
}
```

### Health Marker Examples

```
LCT (Lactase):
  Genotype: C/C (Lactase Persistent)
  Frequency: 70% in East Africa, 5% in West Africa
  Phenotype: Can digest milk into adulthood
  Disclaimer: Phenotype predicted; actual persistence varies individually

HBB (Hemoglobin Beta):
  Genotype: A/S (Sickle Cell Trait)
  Frequency: 18% in East Africa, 25% in West Africa
  Phenotype: Carrier; potential malarial resistance
  Disclaimer: Carrier does not indicate disease; genetic counseling recommended

G6PD (Glucose-6-Phosphate Dehydrogenase):
  Genotype: A/A (Deficient)
  Frequency: 8% in East Africa, 15% in West Africa
  Phenotype: Deficiency; hemolytic risk with fava beans, infections, certain drugs
  Disclaimer: Not diagnostic; clinical confirmation required before treatment decisions

DUFFY (Duffy Antigen):
  Genotype: -/-  (Duffy Negative)
  Frequency: 90% in sub-Saharan Africa
  Phenotype: Resistant to Plasmodium vivax malaria
  Disclaimer: Phenotype prediction; actual resistance depends on other factors
```

### Sample Data Format

```
Sample ID Format: {COUNTRY_CODE}-{YEAR}-{SEQUENCE}
Examples:
  KEN-2024-00523  (Kenya)
  NGA-2024-01245  (Nigeria)
  ZAF-2024-00892  (South Africa)
  ETH-2024-00567  (Ethiopia)
  GHA-2024-00234  (Ghana)

Consent Versions:
  v1.0 - Initial consent form (2023)
  v2.0 - Added secondary research clause (2024-06)
  v2.1 - Clarified data retention periods (2024-10) [CURRENT]

IRB Reference Format:
  {INSTITUTION_CODE}-IRB-{YEAR}-{SEQUENCE}
  Examples:
    KNH-IRB-2024-156   (Kenyatta National Hospital)
    UGMC-IRB-2024-089  (Uganda Medical Center)
    CBH-IRB-2023-203   (Cape Biomedical Hub)
```

---

## DEPLOYMENT & INFRASTRUCTURE

### Development Environment

```
Local Development:
├── Frontend: npm run dev (localhost:3000)
├── Backend: uvicorn main:app --reload (localhost:8000)
├── Database: PostgreSQL in Docker (localhost:5432)
└── Mock S3: minio container (localhost:9000)

Docker Compose Setup:
- FastAPI service
- PostgreSQL database
- Redis (for session management)
- Nginx (reverse proxy)
```

### Production Architecture (Notional)

```
AWS Deployment (Example):
├── Frontend: CloudFront + S3 (static hosting)
├── Backend: ECS Fargate (containerized FastAPI)
├── Database: RDS PostgreSQL (multi-AZ, automated backups)
├── Secrets: AWS Secrets Manager (credentials, API keys)
├── Storage: S3 (encrypted genomic files)
├── Logging: CloudWatch (audit logs, application logs)
└── Monitoring: CloudWatch Alarms, X-Ray tracing
```

---

## NEXT STEPS FOR PRODUCTION

1. **Legal & Regulatory Review**
   - GDPR, HIPAA, APTA compliance assessment
   - Institutional Review Board (IRB) approval
   - Data Protection Authority registration

2. **Security Hardening**
   - Penetration testing
   - Code review by security experts
   - ISO 27001 certification pursuit

3. **Data Partnership Agreements**
   - Formal MOUs with institutions
   - Data sovereignty clauses
   - Benefit-sharing frameworks

4. **Genomic Data Integration**
   - Actual VCF pipeline implementation
   - Alignment with reference datasets (1KG, gnomAD, etc.)
   - Population genetics quality control

5. **Clinical Validation**
   - Accuracy assessment of ancestry inference
   - Health marker phenotype concordance
   - Confidence interval calibration

6. **Scaling & Performance**
   - Load testing with realistic throughput
   - Database query optimization
   - Caching strategy implementation

7. **Community Engagement**
   - Indigenous consent frameworks
   - Community advisory boards
   - Benefit-sharing governance

---

## GLOSSARY & REFERENCES

**Key Terms:**

- **Admixture:** The blending of DNA from two or more distinct populations
- **CI (Confidence Interval):** Range indicating uncertainty in estimate (e.g., ±8%)
- **PCA (Principal Component Analysis):** Statistical method to identify population structure
- **VCF (Variant Call Format):** Standard file format for genomic variants
- **Phenotype:** Observable traits resulting from genotype + environment
- **Genotype:** Genetic composition (e.g., A/A, A/T, T/T)

**Cited Methodologies (Mock References):**
- 1000 Genomes Project - Phase 3 (2015)
- International HapMap Consortium (2010)
- Human Genome Diversity Project (HGDP)
- Population Reference Sequences for African Genomes (Mock Database)

**Regulatory Frameworks Considered:**
- EU General Data Protection Regulation (GDPR)
- US Health Insurance Portability and Accountability Act (HIPAA)
- African Union Personal Data Protection Act (APTA)
- UNESCO Recommendation on Science and Scientific Researchers (2017)

---

## CONTACT & GOVERNANCE

**Platform Governance:** Academic consortium (notional)  
**Data Protection Officer:** [Designated]  
**Ethics Oversight:** Independent Ethics Committee  
**Questions:** [research@afro-genomics.example.com](mailto:research@afro-genomics.example.com)

**DISCLAIMER:** This document describes a design prototype. All data is simulated. No medical claims are made. This is not certified for clinical use. Institutional review and additional regulatory work are required before any deployment.

---

**End of Design Document**
