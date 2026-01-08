# AFRO-GENOMICS Research Platform

## Lab-Facing Genomic Research Platform for African Populations

A comprehensive design and working prototype for a clinically-oriented, ethically-grounded genomic research platform focused on African population genetics.

---

## 📋 Overview

**AFRO-GENOMICS** is a reference platform demonstration designed for presentation to:
- Medical genetics laboratories
- University research institutions  
- Funding bodies and ethics review boards
- African health ministries

**⚠️ IMPORTANT: This is a design mockup and working prototype, NOT a production-ready system.** All data is simulated. No actual genomic processing occurs. See [DESIGN.md](DESIGN.md) for comprehensive architecture documentation.

### Key Features

✅ **Scientific Rigor**
- Population genetics based on reference datasets (1000 Genomes)
- Confidence intervals for ancestry estimates
- Health-relevant genetic markers with disclaimers

✅ **Ethical Framework**
- Informed consent management (IRB-linked)
- Data sovereignty (no third-party resale)
- Complete audit trail of all data access
- Right to withdrawal with data deletion

✅ **Professional UI**
- Clinical/academic aesthetic (not consumer-oriented)
- Comprehensive data visualization
- Research-focused language and disclaimers
- RBAC (Role-Based Access Control)

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- FastAPI (Python 3.10+)
- SQLAlchemy ORM
- SQLite (demo) / PostgreSQL (production)
- JWT authentication

**Frontend:**
- React 18 with TypeScript
- React Router v6
- Tailwind CSS
- Recharts for data visualization
- Axios for API calls

### Directory Structure

```
anti/
├── DESIGN.md                     # Comprehensive design document
├── README.md                     # This file
├── backend/
│   ├── main.py                   # FastAPI application
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── schemas.py                # Pydantic request/response schemas
│   ├── auth.py                   # JWT auth and password hashing
│   ├── mock_data.py              # Mock data generation
│   └── requirements.txt           # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx               # Main React app with routing
    │   ├── main.jsx              # Entry point
    │   ├── index.css             # Global styles
    │   ├── context/
    │   │   └── AuthContext.jsx   # Authentication context
    │   ├── pages/
    │   │   ├── Public.jsx        # Home, Science, Ethics pages
    │   │   ├── Lab.jsx           # Login page
    │   │   └── Dashboard.jsx     # Lab dashboard and sample results
    │   └── components/
    │       ├── Common.jsx        # Shared UI components
    │       └── Results.jsx       # Results visualization
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── postcss.config.js
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Install Python dependencies:**

```bash
cd backend
pip install -r requirements.txt
```

2. **Run the FastAPI server:**

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**Interactive API docs:** `http://localhost:8000/api/v1/docs`

### Frontend Setup

1. **Install dependencies:**

```bash
cd frontend
npm install
```

2. **Start development server:**

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

### Demo Credentials

The system includes mock data with pre-configured demo accounts:

| Email | Role | Institution | Password |
|-------|------|-------------|----------|
| jane.kimani@knh.org | Lab Admin | Kenyatta National Hospital | demo_password_123 |
| david.kipchoge@knh.org | Researcher | Kenyatta National Hospital | demo_password_123 |
| moses.owuor@knh.org | Lab Technician | Kenyatta National Hospital | demo_password_123 |
| william.kasomo@makerere.ac.ug | Lab Admin | Makerere University | demo_password_123 |
| oluwaseun.adeyemi@unilag.edu.ng | Researcher | University of Lagos | demo_password_123 |
| desta.hailu@addisababa.edu.et | Researcher | University of Addis Ababa | demo_password_123 |
| thabo.mthembu@sun.ac.za | Lab Admin | Stellenbosch University | demo_password_123 |

---

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### Authentication
```
POST   /auth/login                 # User login
POST   /auth/logout                # User logout
POST   /auth/refresh               # Refresh token
```

#### Samples
```
GET    /samples                    # List samples (filtered, paginated)
POST   /samples                    # Upload sample metadata
GET    /samples/{sample_id}/results # Get ancestry + health results
```

#### Consent
```
GET    /consent/{user_id}          # Get consent records
POST   /consent/withdraw           # Withdraw consent
```

#### Audit
```
GET    /audit-logs                 # Get access audit trail (admin)
```

#### Data Export
```
POST   /data-export                # Request data export
```

Full OpenAPI documentation available at `/api/v1/docs`

---

## 🔐 Security Model

### Authentication
- **JWT tokens** (RS256 signing, 1-hour expiration)
- **Refresh tokens** (30-day expiration)
- **Password hashing** (bcrypt, cost=12)
- **Multi-factor authentication** (described, mockable)

### Authorization
- **Role-based access control (RBAC):**
  - Lab Admin: Full institutional access
  - Researcher: Sample viewing and export
  - Lab Technician: Sample upload and tracking
  - Observer: Read-only access

### Data Protection
- **Encryption at rest:** AES-256 (simulated)
- **Encryption in transit:** TLS 1.3
- **Audit logging:** All data access tracked with timestamp, user, IP, action
- **Access control:** Granular consent verification

### Compliance Principles
This design incorporates privacy principles from:
- GDPR (EU)
- HIPAA (US)
- APTA (African Personal Data Protection Act)
- UNESCO Scientific Integrity Recommendations

⚠️ **Disclaimer:** This is a design mockup. Full regulatory compliance requires institutional IRB approval, legal review, and regulatory certification.

---

## 📊 Mock Data

The system initializes with realistic mock data:

### Institutions (5)
- Kenyatta National Hospital (Kenya)
- College of Medicine, Makerere University (Uganda)
- University of Lagos Medical Research Centre (Nigeria)
- University of Addis Ababa Institute of Genetics (Ethiopia)
- Stellenbosch University Medical School (South Africa)

### Users (7)
- Lab administrators and researchers with realistic email addresses
- Password: `demo_password_123` (all accounts)

### Samples (8)
- With realistic sample IDs: `KEN-2024-00523`, `NGA-2024-01245`, etc.
- Processing status varies (Received, Processing, Results Available)
- Linked to consent records with IRB references

### Ancestry Results
- Population groups: Bantu, Nilotic, Cushitic, Afroasiatic, West African, North African
- Percentages with 95% confidence intervals
- Reference dataset: 1KG-African-2023 (mock)

### Health Markers
- LCT (Lactase Persistence)
- HBB (Sickle Cell)
- G6PD (G6PD Deficiency)
- DUFFY (Malaria Resistance)

---

## 🖥️ Frontend Pages

### Public Pages
- **/** - Home page with mission statement and key principles
- **/science** - Population genetics methodology with reference data
- **/research-ethics** - Informed consent, data sovereignty, user rights
- **/populations** - (Placeholder) Migration history and scholarly context
- **/lab-partnerships** - (Placeholder) Integration and partnership details
- **/pricing** - (Placeholder) Institutional pricing and funding options

### Lab Portal Pages
- **/lab/login** - Authentication with demo account selection
- **/lab/dashboard** - Sample overview with status statistics
- **/lab/samples/:id** - Sample results with ancestry charts and health markers
- **/lab/samples** - (Placeholder) Sample list and management
- **/lab/consent** - (Placeholder) Consent management interface
- **/lab/settings** - (Placeholder) User preferences
- **/lab/audit** - (Admin only) Access audit trail

---

## 📈 Results Visualization

### Ancestry Visualization
- **Bar chart:** Population percentages
- **Pie chart:** Ancestry distribution
- **Confidence intervals:** Visual ranges with uncertainty bounds
- **Reference context:** Sample sizes and reference dataset metadata

### Health Markers
- **Gene cards:** Variant details with population frequencies
- **Phenotype interpretation:** Clear, non-diagnostic descriptions
- **Population stratification:** Allele frequency by population
- **Research disclaimers:** Persistent warnings on clinical use

---

## 🧪 Testing the Platform

### Sample Workflow

1. **Login** (use any demo account)
2. **View Dashboard** - See sample statistics and status
3. **Click "View Results"** on a sample (preferably one with status "Results Available")
4. **Explore Results:**
   - Ancestry breakdown with confidence intervals
   - Health-relevant markers with disclaimers
   - Population frequency data
5. **Review Disclaimers** - Notice research-use-only language throughout

### Key Demo Features

- ✅ Role-based UI (Lab Admin has audit log access)
- ✅ Realistic sample IDs and population assignments
- ✅ Confidence interval visualization
- ✅ Multiple health markers with population frequencies
- ✅ Scientific methodology page with reference data
- ✅ Ethics and consent framework documentation
- ✅ Data access audit trail (Admin only)

---

## 🔮 Next Steps for Production

### Phase 1: Legal & Regulatory
- [ ] Institutional Review Board (IRB) approval
- [ ] Legal review (GDPR, HIPAA, APTA compliance)
- [ ] Data Protection Authority registration
- [ ] Institutional partnerships formalized (MOUs)

### Phase 2: Infrastructure
- [ ] PostgreSQL deployment (replace SQLite)
- [ ] AWS/GCP/Azure deployment (containerized)
- [ ] Encryption key management (HSM/KMS)
- [ ] Database backup and disaster recovery
- [ ] Security audits and penetration testing

### Phase 3: Genomic Integration
- [ ] VCF pipeline implementation (real genomic data)
- [ ] Alignment with reference genomes
- [ ] Population genetics QC
- [ ] Accuracy assessment and validation

### Phase 4: Institutional Scaling
- [ ] Multi-institution federation
- [ ] Sample barcode/tracking systems
- [ ] Lab information management system (LIMS) integration
- [ ] Automated result reporting

### Phase 5: Community & Governance
- [ ] Community advisory boards
- [ ] Benefit-sharing governance frameworks
- [ ] Indigenous consent protocols
- [ ] Public engagement and communication

---

## 📖 Design Documentation

Comprehensive design documentation is available in [DESIGN.md](DESIGN.md), including:

- **System Architecture** - Component diagrams and data flow
- **Database Schema** - Complete ERD and field descriptions
- **API Specification** - Full endpoint documentation with examples
- **Security Model** - Authentication, encryption, compliance framework
- **Mock Data Specifications** - Population groups, sample formats, ancestry profiles
- **Production Deployment** - Infrastructure recommendations
- **Regulatory Compliance** - GDPR, HIPAA, APTA principles

---

## 🤝 Contributing

This is a design reference and prototype. For institutional implementations:

1. Conduct comprehensive security audits
2. Obtain institutional IRB approval
3. Engage community advisory boards
4. Implement actual genomic pipelines
5. Establish formal data governance policies

---

## ⚠️ Disclaimers

### This is NOT Production-Ready

- All data is simulated and not real
- No actual genomic processing occurs
- No real medical claims are made
- Not clinically validated or certified
- No HIPAA, GDPR, or regulatory compliance guaranteed

### Research Use Only

This platform is designed as an educational and reference prototype for:
- Understanding lab-facing genomic platforms
- Demonstrating ethical research practices
- Showcasing data sovereignty principles
- Supporting institutional presentations and funding proposals

### No Medical Advice

Results and information provided by this platform are for research and educational purposes only. They are not diagnostic and do not constitute medical advice. Consult qualified healthcare providers for any health concerns.

---

## 📞 Contact

**Project:** AFRO-GENOMICS Research Platform  
**Email:** research@afro-genomics.example.com  
**License:** [Specify - e.g., Creative Commons Attribution]

---

## 📄 License

[Specify license - e.g., Creative Commons for design documentation]

---

**Last Updated:** January 2026  
**Version:** 1.0 (Reference Design & Prototype)

---

### Quick Links

- [Comprehensive Design Document](DESIGN.md)
- [API Documentation](http://localhost:8000/api/v1/docs) (when running)
- [Repository](https://github.com/yourusername/afro-genomics)

