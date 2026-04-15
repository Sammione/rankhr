import json
from ranking_logic import rank_cvs, detect_role_type

print("=" * 80)
print("TESTING ROLE-AWARE RANKING SYSTEM")
print("=" * 80)

# ============ TEST 1: Tech Role (Frontend Engineer) ============
print("\n" + "=" * 80)
print("TEST 1: Frontend Engineer (Tech Role)")
print("=" * 80)

tech_jd = """Role: Frontend Engineer
Level: Intern
Employment Type: FullTime
Work Style: Remote
Location: Lagos state, NG
Summary: A Frontend Engineer is responsible for building and maintaining user-facing features of web applications. They translate UI/UX designs into responsive, interactive, and high-performance interfaces using modern web technologies such as HTML, CSS, and JavaScript frameworks like React, Vue, or Angular.
Requirements: Strong proficiency in HTML, CSS, and JavaScript (ES6+). Experience with modern frameworks/libraries such as React, Next.js, Vue, or Angular. Familiarity with responsive design and cross-browser compatibility. Experience integrating RESTful APIs and working with backend services. Knowledge of state management tools (e.g., Redux, Context API, Zustand). Understanding of version control systems such as Git."""

tech_cvs = [
    {
        "id": "tech-1",
        "name": "Alice Johnson",
        "text": """Applicant: Alice Johnson
Skills: React, JavaScript, TypeScript, HTML, CSS, Next.js, Redux, Git, REST APIs
Experience: 3 years as Frontend Developer at TechCorp. Built responsive web applications using React and TypeScript. Implemented state management with Redux. Collaborated with backend team to integrate RESTful APIs."""
    },
    {
        "id": "tech-2",
        "name": "Bob Smith",
        "text": """Applicant: Bob Smith
Skills: Python, Django, PostgreSQL, Docker, AWS, Git
Experience: 5 years as Backend Developer. Built RESTful APIs using Django. Deployed applications on AWS using Docker and Kubernetes."""
    },
    {
        "id": "tech-3",
        "name": "Carol White",
        "text": """Applicant: Carol White
Skills: Marketing, Sales, Business Development, CRM, Salesforce, Customer Service
Experience: 4 years in Marketing and Sales. Managed marketing campaigns and client relations. Expert in Salesforce CRM and lead generation."""
    },
    {
        "id": "tech-4",
        "name": "David Lee",
        "text": """Applicant: David Lee
Skills: Vue.js, JavaScript, HTML, CSS, Git, Agile, Unit Testing
Experience: 2 years as Frontend Developer. Built user interfaces using Vue.js. Wrote unit tests and followed Agile methodologies."""
    }
]

print(f"\nDetected Role Type: {detect_role_type(tech_jd)}")
tech_results = rank_cvs(tech_jd, tech_cvs)

print("\nRanking Results:")
for i, result in enumerate(tech_results, 1):
    print(f"{i}. {result['name']} (ID: {result['applicant_id']})")
    print(f"   Score: {result['score']}% - {result['match_level']}")
    print(f"   Role Type: {result['role_type']}")

print("\nEXPECTED: Frontend developers (Alice, David) should rank highest")
print("EXPECTED: Backend developer (Bob) should rank lower")
print("EXPECTED: Marketing candidate (Carol) should rank lowest (penalized)")

# ============ TEST 2: Business Role (Marketing Manager) ============
print("\n" + "=" * 80)
print("TEST 2: Marketing Manager (Business Role)")
print("=" * 80)

business_jd = """Role: Marketing Manager
Level: Senior
Employment Type: FullTime
Work Style: Hybrid
Location: New York, NY
Summary: We are looking for an experienced Marketing Manager to lead our marketing team. The ideal candidate will have strong experience in digital marketing, brand management, campaign management, and analytics.
Requirements: 5+ years of marketing experience. Expertise in digital marketing, SEO, content marketing, social media marketing, and Google Analytics. Experience with campaign management and brand strategy. Strong analytical skills and data-driven mindset."""

business_cvs = [
    {
        "id": "biz-1",
        "name": "Eve Davis",
        "text": """Applicant: Eve Davis
Skills: Marketing, Digital Marketing, SEO, Google Analytics, Social Media, Content Marketing, Brand Management, Campaign Management
Experience: 6 years as Marketing Manager. Led digital marketing campaigns with 200% ROI. Expert in SEO and Google Analytics. Managed brand strategy and social media presence."""
    },
    {
        "id": "biz-2",
        "name": "Frank Miller",
        "text": """Applicant: Frank Miller
Skills: React, JavaScript, Python, Node.js, Git, Docker, AWS
Experience: 5 years as Full Stack Developer. Built web applications using React and Node.js. Deployed on AWS using Docker."""
    },
    {
        "id": "biz-3",
        "name": "Grace Wilson",
        "text": """Applicant: Grace Wilson
Skills: Sales, Business Development, CRM, Salesforce, Negotiation, Client Relations, Lead Generation
Experience: 4 years in Sales and Business Development. Exceeded sales targets by 150%. Expert in Salesforce and client negotiations."""
    },
    {
        "id": "biz-4",
        "name": "Henry Brown",
        "text": """Applicant: Henry Brown
Skills: Accounting, Finance, Financial Analysis, Budgeting, Excel, ERP, SAP
Experience: 7 years as Financial Analyst. Managed budgets and financial reporting. Expert in Excel, SAP, and ERP systems."""
    }
]

print(f"\nDetected Role Type: {detect_role_type(business_jd)}")
business_results = rank_cvs(business_jd, business_cvs)

print("\nRanking Results:")
for i, result in enumerate(business_results, 1):
    print(f"{i}. {result['name']} (ID: {result['applicant_id']})")
    print(f"   Score: {result['score']}% - {result['match_level']}")
    print(f"   Role Type: {result['role_type']}")

print("\nEXPECTED: Marketing expert (Eve) should rank highest")
print("EXPECTED: Sales candidate (Grace) and Finance candidate (Henry) should rank lower")
print("EXPECTED: Developer (Frank) should rank lowest (penalized for tech skills)")

# ============ TEST 3: Creative Role (UI/UX Designer) ============
print("\n" + "=" * 80)
print("TEST 3: UI/UX Designer (Creative Role)")
print("=" * 80)

creative_jd = """Role: UI/UX Designer
Level: Mid-Level
Employment Type: FullTime
Work Style: On-site
Location: San Francisco, CA
Summary: We are seeking a talented UI/UX Designer to create beautiful and functional user interfaces. The ideal candidate will have strong skills in visual design, prototyping, and user research.
Requirements: Proficiency in Figma, Sketch, Adobe Creative Suite. Strong portfolio demonstrating UI design and UX design skills. Experience with prototyping and user testing. Understanding of design systems and responsive design principles."""

creative_cvs = [
    {
        "id": "creative-1",
        "name": "Ivy Chen",
        "text": """Applicant: Ivy Chen
Skills: Figma, Sketch, Adobe Creative Suite, UI Design, UX Design, Prototyping, Visual Design, User Research
Experience: 4 years as UI/UX Designer. Created design systems and prototypes in Figma. Conducted user research and usability testing. Strong visual design portfolio."""
    },
    {
        "id": "creative-2",
        "name": "Jack Taylor",
        "text": """Applicant: Jack Taylor
Skills: Video Editing, Photography, Adobe Premiere Pro, After Effects, Content Creation, Storytelling
Experience: 3 years as Video Producer. Created video content and motion graphics. Expert in Premiere Pro and After Effects."""
    },
    {
        "id": "creative-3",
        "name": "Karen Anderson",
        "text": """Applicant: Karen Anderson
Skills: Python, Java, JavaScript, React, Node.js, Git, Docker, AWS, Agile
Experience: 5 years as Software Engineer. Built web applications using React and Node.js. Deployed on AWS using Docker and Kubernetes."""
    },
    {
        "id": "creative-4",
        "name": "Leo Martinez",
        "text": """Applicant: Leo Martinez
Skills: Graphic Design, Illustrator, Photoshop, InDesign, Branding, Visual Design, Adobe Creative Suite
Experience: 6 years as Graphic Designer. Created brand identities and marketing materials. Expert in Adobe Creative Suite."""
    }
]

print(f"\nDetected Role Type: {detect_role_type(creative_jd)}")
creative_results = rank_cvs(creative_jd, creative_cvs)

print("\nRanking Results:")
for i, result in enumerate(creative_results, 1):
    print(f"{i}. {result['name']} (ID: {result['applicant_id']})")
    print(f"   Score: {result['score']}% - {result['match_level']}")
    print(f"   Role Type: {result['role_type']}")

print("\nEXPECTED: UI/UX Designer (Ivy) should rank highest")
print("EXPECTED: Graphic Designer (Leo) should rank high (related skills)")
print("EXPECTED: Video Producer (Jack) should rank moderate")
print("EXPECTED: Software Engineer (Karen) should rank lowest (penalized for tech skills)")

# ============ SUMMARY ============
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print("The system now supports ranking for different role types:")
print("- Tech roles (Engineer, Developer, etc.)")
print("- Business roles (Manager, Analyst, Marketing, Sales, HR, Finance)")
print("- Creative roles (Designer, Content Creator, etc.)")
print("\nThe AI automatically detects the role type from the JD and:")
print("1. Uses appropriate skill matching for that role type")
print("2. Penalizes irrelevant skills (e.g., tech skills for business roles)")
print("3. Works dynamically with any JD and CV combination")