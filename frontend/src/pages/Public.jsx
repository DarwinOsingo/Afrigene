import React from 'react';
import { Link } from 'react-router-dom';

export const HomePage = () => (
  <div className="space-y-12">
    {/* Hero Section */}
    <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-16 px-6 rounded-lg">
      <h1 className="text-4xl font-bold mb-4">AFRO-GENOMICS Research Platform</h1>
      <p className="text-xl text-blue-100 max-w-2xl mb-6">
        Advancing genomic research within and across African populations through ethical, 
        transparent, and scientifically rigorous methodologies.
      </p>
      <div className="flex gap-4">
        <Link 
          to="/lab/login"
          className="bg-white text-blue-600 font-semibold px-6 py-3 rounded hover:bg-blue-50"
        >
          Lab Access Portal
        </Link>
        <Link 
          to="/science"
          className="bg-blue-500 text-white font-semibold px-6 py-3 rounded hover:bg-blue-400"
        >
          Learn More
        </Link>
      </div>
    </div>

    {/* Mission Statement */}
    <div className="max-w-3xl">
      <h2 className="text-2xl font-bold mb-4 text-gray-900">Our Mission</h2>
      <p className="text-lg text-gray-700 mb-4">
        We are dedicated to advancing genomic research within and across African populations 
        through an ethical, transparent, and scientifically rigorous platform that centers 
        data sovereignty and community benefit.
      </p>
      <p className="text-lg text-gray-700">
        <strong>This is NOT ancestry entertainment.</strong> We focus on advancing population 
        genetics research with rigorous scientific methods, transparent limitations, and 
        unwavering commitment to African data sovereignty.
      </p>
    </div>

    {/* Key Principles */}
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-xl font-bold text-blue-900 mb-3">🔬 Scientific Rigor</h3>
        <p className="text-gray-700">
          Evidence-based population genetics with confidence intervals, peer-reviewed methodology, 
          and transparent limitations.
        </p>
      </div>

      <div className="bg-green-50 border border-green-200 rounded-lg p-6">
        <h3 className="text-xl font-bold text-green-900 mb-3">🛡️ Data Sovereignty</h3>
        <p className="text-gray-700">
          African data remains under African stewardship. No third-party sales. No data monetization. 
          Community benefit aligned.
        </p>
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
        <h3 className="text-xl font-bold text-amber-900 mb-3">✓ Ethical Transparency</h3>
        <p className="text-gray-700">
          Informed consent processes. IRB oversight. Complete audit trails. User control over data 
          and explicit withdrawal rights.
        </p>
      </div>

      <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h3 className="text-xl font-bold text-purple-900 mb-3">🌍 Cultural Respect</h3>
        <p className="text-gray-700">
          African genetic diversity treated as a research priority, not a novelty. Scholarly framing. 
          Community-centered governance.
        </p>
      </div>
    </div>

    {/* Research Focus */}
    <div>
      <h2 className="text-2xl font-bold mb-4 text-gray-900">Research Focus: African Population Genetics</h2>
      <p className="text-gray-700 mb-4">
        We specialize in genomic research across diverse African populations:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Nilotic Populations</h4>
          <p className="text-sm text-gray-700">Dinka, Nuer, Maasai, Samburu</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Bantu Populations</h4>
          <p className="text-sm text-gray-700">Luhya, Kikuyu, Zulu, Igbo, Xhosa</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Cushitic Populations</h4>
          <p className="text-sm text-gray-700">Somali, Oromo, Afar</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Afroasiatic & West African</h4>
          <p className="text-sm text-gray-700">Hausa, Berber, Yoruba, Akan, Mandinka</p>
        </div>
      </div>
    </div>

    {/* Institutional Partnerships */}
    <div>
      <h2 className="text-2xl font-bold mb-4 text-gray-900">Partner Institutions</h2>
      <p className="text-gray-700 mb-6">
        We work with leading medical genetics laboratories and research universities across Africa.
      </p>
      <Link 
        to="/lab-partnerships"
        className="text-blue-600 hover:underline font-semibold"
      >
        View partnership opportunities →
      </Link>
    </div>

    {/* CTA */}
    <div className="bg-gray-900 text-white rounded-lg p-8 text-center">
      <h3 className="text-2xl font-bold mb-4">Ready to Participate in African Genomic Research?</h3>
      <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
        Contact us for information about institutional partnerships, research collaborations, 
        and funding opportunities.
      </p>
      <a 
        href="mailto:research@afro-genomics.example.com"
        className="bg-blue-600 text-white font-semibold px-6 py-3 rounded hover:bg-blue-700 inline-block"
      >
        Get in Touch
      </a>
    </div>
  </div>
);

export const ScienceMethodology = () => (
  <div className="space-y-8 max-w-4xl">
    <h1 className="text-3xl font-bold text-gray-900">Scientific Methodology</h1>

    <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
      <h2 className="text-2xl font-bold text-blue-900 mb-4">Population Genetics Framework</h2>
      <p className="text-gray-700 mb-4">
        Our ancestry inference is based on Principal Component Analysis (PCA) and admixture modeling, 
        calibrated against reference populations from the 1000 Genomes Project (1KG) African panel and 
        other peer-reviewed genomic databases.
      </p>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Reference Populations</h3>
      <p className="text-gray-700 mb-4">
        We utilize reference samples from well-characterized African populations:
      </p>
      <table className="w-full border-collapse">
        <thead>
          <tr className="bg-gray-100 border-b-2 border-gray-300">
            <th className="text-left p-3 font-semibold text-gray-900">Population</th>
            <th className="text-left p-3 font-semibold text-gray-900">Sample Size (1KG)</th>
            <th className="text-left p-3 font-semibold text-gray-900">Geographic Region</th>
          </tr>
        </thead>
        <tbody>
          {[
            ['Luhya (LWK)', 99, 'Kenya'],
            ['Yoruba (YRI)', 88, 'Nigeria'],
            ['Esan (ESN)', 99, 'Nigeria'],
            ['Gambian Mandinka (GWD)', 113, 'Gambia'],
            ['Mende (MSL)', 85, 'Sierra Leone'],
            ['Maasai (MAS)', 84, 'Kenya/Tanzania'],
            ['Kikuyu (KHV)', 124, 'Kenya'],
            ['Zulu (ZUL)', 107, 'South Africa'],
            ['Temne (TSI)', 91, 'Sierra Leone'],
          ].map(([pop, size, region]) => (
            <tr key={pop} className="border-b border-gray-200 hover:bg-gray-50">
              <td className="p-3 font-mono text-sm text-gray-900">{pop}</td>
              <td className="p-3 text-gray-700">{size.toLocaleString()}</td>
              <td className="p-3 text-gray-700">{region}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p className="text-sm text-gray-600 mt-4">
        <span className="font-semibold">Total reference samples:</span> ~2,847 individuals from African populations
      </p>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Health-Relevant Genetic Markers</h3>
      <p className="text-gray-700 mb-4">
        We report on genetic variants with established phenotypic associations and population-specific 
        relevance. <strong>All health markers are for research use only and not diagnostic.</strong>
      </p>

      <div className="space-y-4">
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Lactose Persistence (LCT gene)</h4>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Variant:</strong> rs4988235 (C-13910T)
          </p>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Phenotype:</strong> Ability to digest milk into adulthood
          </p>
          <p className="text-sm text-gray-700">
            <strong>Population Frequency:</strong> High in East African pastoral populations 
            (~70% in Maasai/Samburu), rare in West African populations (~5% Yoruba)
          </p>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Sickle Cell (HBB gene)</h4>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Variant:</strong> rs334 (E6V)
          </p>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Phenotype:</strong> Sickle cell trait (heterozygous) confers malaria resistance benefit
          </p>
          <p className="text-sm text-gray-700">
            <strong>Population Frequency:</strong> 18-25% carrier frequency across sub-Saharan Africa
          </p>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">G6PD Deficiency (G6PD gene)</h4>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Variant:</strong> rs1050829
          </p>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Phenotype:</strong> Deficiency affecting red blood cell metabolism
          </p>
          <p className="text-sm text-gray-700">
            <strong>Population Frequency:</strong> 8-15% across African populations
          </p>
        </div>

        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Duffy Antigen (DARC gene)</h4>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Variant:</strong> rs2814778
          </p>
          <p className="text-sm text-gray-700 mb-2">
            <strong>Phenotype:</strong> Duffy-negative phenotype confers malaria (P. vivax) resistance
          </p>
          <p className="text-sm text-gray-700">
            <strong>Population Frequency:</strong> ~90% in sub-Saharan Africa
          </p>
        </div>
      </div>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Statistical Methods</h3>
      <ul className="list-disc list-inside space-y-2 text-gray-700">
        <li><strong>Ancestry Inference:</strong> Principal Component Analysis (PCA) with ADMIXTURE-style modeling</li>
        <li><strong>Confidence Intervals:</strong> 95% CI calculated via bootstrap resampling of reference populations</li>
        <li><strong>Phenotype Prediction:</strong> Association with reference genotype-phenotype data</li>
        <li><strong>Population Frequency:</strong> Allele frequency from 1KG and dbSNP databases</li>
        <li><strong>Quality Control:</strong> Sample call rate {'>'}95%, Hardy-Weinberg equilibrium testing</li>
      </ul>
    </div>

    <div className="bg-amber-50 border-l-4 border-amber-400 p-4 rounded">
      <h4 className="font-semibold text-amber-900 mb-2">Important Limitations</h4>
      <ul className="list-disc list-inside space-y-2 text-sm text-amber-800">
        <li>Confidence intervals reflect uncertainty in reference datasets; actual uncertainty may vary</li>
        <li>Limited representation of some rare or recently-diverged populations</li>
        <li>Ancestry inference assumes relatively recent divergence; older admixture may not be detected</li>
        <li>Phenotype predictions have error rates and should not be used for clinical decision-making</li>
        <li>Population frequency data subject to ascertainment bias in source datasets</li>
      </ul>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Key References (Illustrative)</h3>
      <ul className="space-y-2 text-gray-700">
        <li>• 1000 Genomes Project Consortium. (2015). "A global reference for human genetic variation." Nature, 526(7571).</li>
        <li>• Campbell, M.C., & Tishkoff, S.A. (2010). "African genetic diversity." Nature Reviews Genetics, 11(5).</li>
        <li>• Novembre, J., et al. (2008). "Genes mirror geography within Europe." Nature, 456(7218).</li>
        <li>• Enattah, N.S., et al. (2008). "Independent introduction of two lactase-persistence alleles into human populations." Nature Genetics, 40(3).</li>
      </ul>
    </div>
  </div>
);

export const ResearchEthics = () => (
  <div className="space-y-8 max-w-4xl">
    <h1 className="text-3xl font-bold text-gray-900">Research Ethics & Data Governance</h1>

    <div className="bg-green-50 border border-green-200 rounded-lg p-6">
      <h2 className="text-2xl font-bold text-green-900 mb-4">Our Ethical Framework</h2>
      <p className="text-gray-700">
        AFRO-GENOMICS is committed to the highest standards of research ethics, informed consent, 
        and data protection. We operate under principles of transparency, participant autonomy, and 
        community benefit.
      </p>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Informed Consent Process</h3>
      <p className="text-gray-700 mb-4">
        All research participants provide <strong>explicit, versioned consent</strong> for their genomic data use:
      </p>
      <div className="space-y-3 bg-gray-50 p-4 rounded border border-gray-200">
        <p className="text-sm text-gray-700"><strong>Step 1:</strong> Comprehensive consent document explaining study aims, data uses, and limitations</p>
        <p className="text-sm text-gray-700"><strong>Step 2:</strong> Opportunity for questions and discussion with research team</p>
        <p className="text-sm text-gray-700"><strong>Step 3:</strong> Informed, voluntary consent signature with witness</p>
        <p className="text-sm text-gray-700"><strong>Step 4:</strong> Institutional Review Board (IRB) approval prior to data collection</p>
        <p className="text-sm text-gray-700"><strong>Step 5:</strong> Ongoing right to withdraw consent without penalty</p>
      </div>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Data Sovereignty Principles</h3>
      <p className="text-gray-700 mb-4">
        African data must remain under African control and stewardship:
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">✓ Data Ownership</h4>
          <p className="text-sm text-gray-700">
            Participating individuals and institutions retain ownership of their data
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">✗ No Resale</h4>
          <p className="text-sm text-gray-700">
            Data never sold to commercial entities or third parties
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">✓ Local Control</h4>
          <p className="text-sm text-gray-700">
            Data governance decisions made by institutional and community partners
          </p>
        </div>
        <div className="bg-blue-50 p-4 rounded border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">✓ Community Benefit</h4>
          <p className="text-sm text-gray-700">
            Research benefits flow back to participating communities
          </p>
        </div>
      </div>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Data Protection & Privacy</h3>
      <p className="text-gray-700 mb-4">
        We implement security and privacy controls aligned with international best practices:
      </p>
      <ul className="list-disc list-inside space-y-2 text-gray-700 mb-4">
        <li><strong>Data Minimization:</strong> Collect only population and health genetics; no identifying information stored with genomic data</li>
        <li><strong>Encryption:</strong> AES-256 encryption at rest, TLS 1.3 in transit</li>
        <li><strong>Access Control:</strong> Role-based access control (RBAC) with principle of least privilege</li>
        <li><strong>Audit Logging:</strong> Complete audit trail of all data access and modifications</li>
        <li><strong>Secure Infrastructure:</strong> ISO 27001-aligned security practices</li>
        <li><strong>Regular Security Reviews:</strong> Periodic penetration testing and code security audits</li>
      </ul>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">User Rights</h3>
      <div className="space-y-4">
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Right to Access</h4>
          <p className="text-sm text-gray-700">Participants can request and review their genomic data and results at any time</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Right to Withdraw</h4>
          <p className="text-sm text-gray-700">Participants may withdraw consent and request complete data deletion without explanation or penalty</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Right to Rectification</h4>
          <p className="text-sm text-gray-700">Participants can request correction of inaccurate data</p>
        </div>
        <div className="bg-gray-50 p-4 rounded border border-gray-200">
          <h4 className="font-semibold text-gray-900 mb-2">Right to Data Portability</h4>
          <p className="text-sm text-gray-700">Participants can request export of their data in standard formats</p>
        </div>
      </div>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Data Retention & Deletion</h3>
      <p className="text-gray-700 mb-4">
        Data retention periods are defined in the consent document and can vary by study:
      </p>
      <ul className="list-disc list-inside space-y-2 text-gray-700 mb-4">
        <li>Default retention: 5 years (60 months) from date of collection</li>
        <li>Extended retention possible with explicit consent and IRB approval</li>
        <li>Upon withdrawal or retention expiration: data permanently deleted from all systems within 7 days</li>
        <li>Data deletion verified and documented with cryptographic assurance</li>
      </ul>
    </div>

    <div>
      <h3 className="text-2xl font-bold text-gray-900 mb-4">Regulatory Compliance</h3>
      <p className="text-gray-700 mb-4">
        This platform incorporates privacy and research ethics principles from:
      </p>
      <ul className="list-disc list-inside space-y-1 text-gray-700">
        <li>GDPR (EU General Data Protection Regulation)</li>
        <li>HIPAA (US Health Insurance Portability and Accountability Act)</li>
        <li>APTA (African Personal Data Protection Act)</li>
        <li>UNESCO Recommendation on Science and Scientific Researchers (2017)</li>
        <li>WHO Ethical Guidance on Global Genomic Data Sharing</li>
        <li>National/regional IRB and ethics committee requirements</li>
      </ul>
    </div>

    <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
      <h4 className="font-semibold text-red-900 mb-2">⚠️ Disclaimer</h4>
      <p className="text-sm text-red-800">
        This design document describes ethical principles and best practices. It is NOT a substitute for 
        comprehensive legal review, institutional ethics approval, or regulatory certification. Any actual 
        deployment requires explicit IRB approval, regulatory review, and data protection authority registration.
      </p>
    </div>
  </div>
);
