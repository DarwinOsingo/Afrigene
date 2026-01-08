"""
AFRO-GENOMICS Research Platform
Mock Data Generation

Generates realistic mock data for demo purposes
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from auth import get_password_hash
from models import (
    User, Institution, ConsentRecord, Sample, AncestryResult, HealthMarker,
    UserRole, SampleStatus, ConsentWithdrawalStatus
)
import uuid


def generate_mock_data(db: Session):
    """Generate comprehensive mock dataset for demonstration"""
    
    # ==================== INSTITUTIONS ====================
    
    institutions = [
        {
            "name": "Kenyatta National Hospital",
            "country": "Kenya",
            "irb_approval": "KNH-IRB-2024-156",
            "contact": "Dr. Jane Kimani",
            "email": "j.kimani@knh.org",
        },
        {
            "name": "College of Medicine, Makerere University",
            "country": "Uganda",
            "irb_approval": "COMU-IRB-2024-089",
            "contact": "Prof. William Kasomo",
            "email": "w.kasomo@makerere.ac.ug",
        },
        {
            "name": "University of Lagos Medical Research Centre",
            "country": "Nigeria",
            "irb_approval": "UNILAG-IRB-2024-203",
            "contact": "Dr. Oluwaseun Adeyemi",
            "email": "oadeyemi@unilag.edu.ng",
        },
        {
            "name": "University of Addis Ababa Institute of Genetics",
            "country": "Ethiopia",
            "irb_approval": "UOAA-IRB-2024-067",
            "contact": "Dr. Desta Hailu",
            "email": "d.hailu@addisababa.edu.et",
        },
        {
            "name": "Stellenbosch University Medical School",
            "country": "South Africa",
            "irb_approval": "SUN-IRB-2024-134",
            "contact": "Prof. Thabo Mthembu",
            "email": "t.mthembu@sun.ac.za",
        },
    ]
    
    inst_objects = {}
    for inst in institutions:
        institution = Institution(
            id=f"inst_{uuid.uuid4().hex[:8]}",
            name=inst["name"],
            country=inst["country"],
            irb_approval_number=inst["irb_approval"],
            contact_person=inst["contact"],
            contact_email=inst["email"],
            data_retention_months=60
        )
        db.add(institution)
        inst_objects[inst["name"]] = institution
    
    db.commit()
    
    # ==================== USERS ====================
    
    users_data = [
        {
            "email": "jane.kimani@knh.org",
            "name": "Jane Kimani",
            "role": UserRole.LAB_ADMIN,
            "institution": "Kenyatta National Hospital"
        },
        {
            "email": "david.kipchoge@knh.org",
            "name": "David Kipchoge",
            "role": UserRole.RESEARCHER,
            "institution": "Kenyatta National Hospital"
        },
        {
            "email": "moses.owuor@knh.org",
            "name": "Moses Owuor",
            "role": UserRole.LAB_TECHNICIAN,
            "institution": "Kenyatta National Hospital"
        },
        {
            "email": "william.kasomo@makerere.ac.ug",
            "name": "William Kasomo",
            "role": UserRole.LAB_ADMIN,
            "institution": "College of Medicine, Makerere University"
        },
        {
            "email": "oluwaseun.adeyemi@unilag.edu.ng",
            "name": "Oluwaseun Adeyemi",
            "role": UserRole.RESEARCHER,
            "institution": "University of Lagos Medical Research Centre"
        },
        {
            "email": "desta.hailu@addisababa.edu.et",
            "name": "Desta Hailu",
            "role": UserRole.RESEARCHER,
            "institution": "University of Addis Ababa Institute of Genetics"
        },
        {
            "email": "thabo.mthembu@sun.ac.za",
            "name": "Thabo Mthembu",
            "role": UserRole.LAB_ADMIN,
            "institution": "Stellenbosch University Medical School"
        },
    ]
    
    user_objects = {}
    for user_data in users_data:
        user = User(
            id=f"usr_{uuid.uuid4().hex[:8]}",
            email=user_data["email"],
            hashed_password=get_password_hash("demo_password_123"),
            role=user_data["role"],
            institution_id=inst_objects[user_data["institution"]].id,
            mfa_enabled=False,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=180)
        )
        db.add(user)
        user_objects[user_data["email"]] = user
    
    db.commit()
    
    # ==================== CONSENT RECORDS ====================
    
    consent_versions = [
        {
            "version": "v2.1",
            "retention": "60 months",
            "permitted": {
                "research": True,
                "publication": True,
                "secondary_research": True,
                "third_party_sharing": False
            }
        }
    ]
    
    consent_objects = {}
    for user_email, user in user_objects.items():
        for consent_version in consent_versions:
            consent = ConsentRecord(
                id=f"con_{uuid.uuid4().hex[:8]}",
                user_id=user.id,
                consent_version=consent_version["version"],
                data_retention_period=consent_version["retention"],
                permitted_uses=consent_version["permitted"],
                withdrawal_status=ConsentWithdrawalStatus.ACTIVE,
                irb_reference=f"IRB-2024-{uuid.uuid4().hex[:5].upper()}",
                signed_at=datetime.utcnow() - timedelta(days=120)
            )
            db.add(consent)
            consent_objects[f"{user_email}_{consent_version['version']}"] = consent
    
    db.commit()
    
    # ==================== SAMPLES ====================
    
    sample_configs = [
        {
            "user": "jane.kimani@knh.org",
            "sample_id": "KEN-2024-00523",
            "participant_id": "P20240523",
            "population_hint": "Kikuyu",
        },
        {
            "user": "jane.kimani@knh.org",
            "sample_id": "KEN-2024-00524",
            "participant_id": "P20240524",
            "population_hint": "Luhya",
        },
        {
            "user": "david.kipchoge@knh.org",
            "sample_id": "KEN-2024-00525",
            "participant_id": "P20240525",
            "population_hint": "Maasai",
        },
        {
            "user": "william.kasomo@makerere.ac.ug",
            "sample_id": "UGA-2024-00234",
            "participant_id": "P20240234",
            "population_hint": "Luganda",
        },
        {
            "user": "oluwaseun.adeyemi@unilag.edu.ng",
            "sample_id": "NGA-2024-01245",
            "participant_id": "P20240245",
            "population_hint": "Yoruba",
        },
        {
            "user": "oluwaseun.adeyemi@unilag.edu.ng",
            "sample_id": "NGA-2024-01246",
            "participant_id": "P20240246",
            "population_hint": "Igbo",
        },
        {
            "user": "desta.hailu@addisababa.edu.et",
            "sample_id": "ETH-2024-00567",
            "participant_id": "P20240567",
            "population_hint": "Amhara",
        },
        {
            "user": "thabo.mthembu@sun.ac.za",
            "sample_id": "ZAF-2024-00892",
            "participant_id": "P20240892",
            "population_hint": "Zulu",
        },
    ]
    
    samples = []
    for config in sample_configs:
        user = user_objects[config["user"]]
        consent = list(consent_objects.values())[0]  # Use first consent
        
        sample = Sample(
            id=f"smp_{uuid.uuid4().hex[:8]}",
            sample_id=config["sample_id"],
            participant_id=config["participant_id"],
            user_id=user.id,
            institution_id=user.institution_id,
            consent_id=consent.id,
            status=SampleStatus.RESULTS_AVAILABLE,
            uploaded_at=datetime.utcnow() - timedelta(days=30),
            processed_at=datetime.utcnow() - timedelta(days=25),
            notes=f"Sample from {config['population_hint']} population cohort"
        )
        db.add(sample)
        samples.append((sample, config["population_hint"]))
    
    db.commit()
    
    # ==================== ANCESTRY RESULTS ====================
    
    ancestry_profiles = {
        "Kikuyu": [
            ("Bantu", 92, 87, 96),
            ("Nilotic", 7, 3, 12),
            ("North African", 1, 0, 5)
        ],
        "Luhya": [
            ("Bantu", 88, 82, 93),
            ("Nilotic", 10, 5, 16),
            ("North African", 2, 0, 6)
        ],
        "Maasai": [
            ("Nilotic", 78, 71, 85),
            ("Bantu", 18, 12, 24),
            ("Cushitic", 4, 1, 9)
        ],
        "Luganda": [
            ("Bantu", 85, 79, 90),
            ("Nilotic", 12, 7, 19),
            ("North African", 3, 1, 8)
        ],
        "Yoruba": [
            ("Bantu", 42, 35, 49),
            ("West African", 56, 48, 63),
            ("North African", 2, 0, 6)
        ],
        "Igbo": [
            ("Bantu", 38, 31, 45),
            ("West African", 60, 52, 67),
            ("North African", 2, 0, 6)
        ],
        "Amhara": [
            ("Afroasiatic", 65, 58, 71),
            ("North African", 25, 18, 32),
            ("Nilotic", 10, 5, 16)
        ],
        "Zulu": [
            ("Bantu", 96, 93, 98),
            ("Nilotic", 3, 1, 6),
            ("North African", 1, 0, 3)
        ],
    }
    
    for sample, pop_hint in samples:
        profiles = ancestry_profiles.get(pop_hint, ancestry_profiles["Kikuyu"])
        
        for pop_group, pct, lower, upper in profiles:
            result = AncestryResult(
                id=f"anc_{uuid.uuid4().hex[:8]}",
                sample_id=sample.id,
                population_group=pop_group,
                percentage=pct,
                confidence_interval_lower=lower,
                confidence_interval_upper=upper,
                reference_dataset="1KG-African-2023",
                reference_sample_size=2847,
                methodology_version="PCA v2.1",
                computed_at=sample.processed_at
            )
            db.add(result)
    
    db.commit()
    
    # ==================== HEALTH MARKERS ====================
    
    health_marker_templates = [
        {
            "gene": "LCT",
            "variant": "rs4988235",
            "chromosome": "chr2",
            "position": 136594750,
            "genotypes": ["C/C", "C/T", "T/T"],
            "phenotypes": ["Lactase Persistent", "Intermediate", "Lactose Intolerant"],
            "significance": "Lactose tolerance phenotype",
            "frequencies": {"East African": "0.70", "West African": "0.05", "North African": "0.02"}
        },
        {
            "gene": "HBB",
            "variant": "rs334",
            "chromosome": "chr11",
            "position": 5248232,
            "genotypes": ["A/A", "A/S", "S/S"],
            "phenotypes": ["Normal", "Sickle Cell Trait (AS)", "Sickle Cell Disease"],
            "significance": "Sickle cell disease; potential malarial resistance",
            "frequencies": {"East African": "0.18", "West African": "0.25", "North African": "0.02"}
        },
        {
            "gene": "G6PD",
            "variant": "rs1050829",
            "chromosome": "chrX",
            "position": 154519747,
            "genotypes": ["A/A", "A/G", "G/G"],
            "phenotypes": ["Deficiency", "Intermediate", "Normal"],
            "significance": "G6PD deficiency; hemolysis risk with triggers",
            "frequencies": {"East African": "0.08", "West African": "0.15", "North African": "0.10"}
        },
        {
            "gene": "DUFFY",
            "variant": "rs2814778",
            "chromosome": "chr1",
            "position": 159235043,
            "genotypes": ["A/A", "A/-", "-/-"],
            "phenotypes": ["Duffy Positive", "Intermediate", "Duffy Negative (P. vivax resistant)"],
            "significance": "Plasmodium vivax malaria resistance",
            "frequencies": {"East African": "0.88", "West African": "0.92", "North African": "0.40"}
        },
    ]
    
    for sample, pop_hint in samples:
        # Select genotypes based on population frequency
        selected_markers = []
        for template in health_marker_templates:
            freqs = template["frequencies"]
            
            # Simple logic: higher frequency populations get more positive markers
            if pop_hint in ["Kikuyu", "Luhya", "Luganda", "Zulu", "Igbo"]:  # Bantu-heavy
                if template["gene"] == "LCT":
                    selected_markers.append((template, "C/T", "Intermediate"))
                elif template["gene"] == "HBB":
                    selected_markers.append((template, "A/S", "Sickle Cell Trait (AS)"))
                elif template["gene"] == "G6PD":
                    selected_markers.append((template, "A/A", "Deficiency"))
                elif template["gene"] == "DUFFY":
                    selected_markers.append((template, "-/-", "Duffy Negative (P. vivax resistant)"))
            
            elif pop_hint in ["Yoruba"]:  # West African
                if template["gene"] == "LCT":
                    selected_markers.append((template, "T/T", "Lactose Intolerant"))
                elif template["gene"] == "HBB":
                    selected_markers.append((template, "A/S", "Sickle Cell Trait (AS)"))
                elif template["gene"] == "G6PD":
                    selected_markers.append((template, "A/G", "Intermediate"))
                elif template["gene"] == "DUFFY":
                    selected_markers.append((template, "-/-", "Duffy Negative (P. vivax resistant)"))
            
            elif pop_hint in ["Maasai"]:  # Nilotic
                if template["gene"] == "LCT":
                    selected_markers.append((template, "C/T", "Intermediate"))
                elif template["gene"] == "HBB":
                    selected_markers.append((template, "A/A", "Normal"))
                elif template["gene"] == "G6PD":
                    selected_markers.append((template, "A/A", "Deficiency"))
                elif template["gene"] == "DUFFY":
                    selected_markers.append((template, "-/-", "Duffy Negative (P. vivax resistant)"))
            
            elif pop_hint in ["Amhara"]:  # Afroasiatic
                if template["gene"] == "LCT":
                    selected_markers.append((template, "C/T", "Intermediate"))
                elif template["gene"] == "HBB":
                    selected_markers.append((template, "A/A", "Normal"))
                elif template["gene"] == "G6PD":
                    selected_markers.append((template, "A/G", "Intermediate"))
                elif template["gene"] == "DUFFY":
                    selected_markers.append((template, "A/-", "Intermediate"))
        
        for template, genotype, phenotype in selected_markers:
            marker = HealthMarker(
                id=f"hlth_{uuid.uuid4().hex[:8]}",
                sample_id=sample.id,
                gene_name=template["gene"],
                variant_rsid=template["variant"],
                chromosome=template["chromosome"],
                position=template["position"],
                genotype=genotype,
                phenotype=phenotype,
                clinical_significance=template["significance"],
                population_frequency=template["frequencies"],
                disclaimer="For research use only. Not diagnostic. Phenotype prediction has error rates. Consult genetic counselor for clinical interpretation.",
                computed_at=sample.processed_at
            )
            db.add(marker)
    
    db.commit()
    
    print(f"✓ Created {len(inst_objects)} institutions")
    print(f"✓ Created {len(user_objects)} users")
    print(f"✓ Created {len(consent_objects)} consent records")
    print(f"✓ Created {len(samples)} samples with results")
