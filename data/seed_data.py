"""
data/seed_data.py - Sample Dataset Loader & Database Seeder.

Loads synthetic learner profiles (AI-Powered Personalized Learning Dataset)
and Coursera course metadata into the database.
"""

import json
import logging
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# ── COURSERA-STYLE COURSES & MODULES ────────────────────────────────────────

SAMPLE_COURSES = [
    # ── CYBERSECURITY ────────────────────────────────────────────────────────
    {"title": "Introduction to Cybersecurity", "category": "cybersecurity", "difficulty": "beginner",
     "duration_hrs": 8, "format_type": "video", "provider": "Coursera",
     "description": "Foundational cybersecurity concepts, threats, and defenses.",
     "rating": 4.7, "enrolled_count": 125000},
    {"title": "Network Security Fundamentals", "category": "cybersecurity", "difficulty": "beginner",
     "duration_hrs": 10, "format_type": "theory", "provider": "Coursera",
     "description": "TCP/IP, firewalls, IDS/IPS, VPNs and network protocols.",
     "rating": 4.5, "enrolled_count": 89000},
    {"title": "Ethical Hacking & Penetration Testing", "category": "cybersecurity", "difficulty": "intermediate",
     "duration_hrs": 20, "format_type": "labs", "provider": "Coursera",
     "description": "Hands-on penetration testing with Kali Linux, Metasploit, Nmap.",
     "rating": 4.8, "enrolled_count": 203000},
    {"title": "Web Application Security", "category": "cybersecurity", "difficulty": "intermediate",
     "duration_hrs": 15, "format_type": "labs", "provider": "Coursera",
     "description": "OWASP Top 10, SQL injection, XSS, CSRF, and secure coding.",
     "rating": 4.6, "enrolled_count": 76000},
    {"title": "Advanced Malware Analysis", "category": "cybersecurity", "difficulty": "advanced",
     "duration_hrs": 25, "format_type": "labs", "provider": "Coursera",
     "description": "Static and dynamic malware analysis, reverse engineering.",
     "rating": 4.9, "enrolled_count": 42000},
    {"title": "Security Operations Center (SOC) Analyst", "category": "cybersecurity", "difficulty": "intermediate",
     "duration_hrs": 18, "format_type": "mixed", "provider": "Coursera",
     "description": "SIEM tools, incident response, threat hunting, log analysis.",
     "rating": 4.7, "enrolled_count": 61000},
    {"title": "Cryptography & PKI", "category": "cybersecurity", "difficulty": "intermediate",
     "duration_hrs": 12, "format_type": "theory", "provider": "Coursera",
     "description": "Symmetric/asymmetric encryption, certificates, TLS/SSL.",
     "rating": 4.4, "enrolled_count": 55000},
    {"title": "Cybersecurity Capstone Project", "category": "cybersecurity", "difficulty": "advanced",
     "duration_hrs": 30, "format_type": "project", "provider": "Coursera",
     "description": "End-to-end security audit and penetration test on a live environment.",
     "rating": 4.8, "enrolled_count": 28000},

    # ── DATA SCIENCE ─────────────────────────────────────────────────────────
    {"title": "Python for Data Science Basics", "category": "data_science", "difficulty": "beginner",
     "duration_hrs": 12, "format_type": "video", "provider": "Coursera",
     "description": "Python fundamentals, NumPy, Pandas for data manipulation.",
     "rating": 4.8, "enrolled_count": 310000},
    {"title": "Data Analysis & Visualization", "category": "data_science", "difficulty": "beginner",
     "duration_hrs": 10, "format_type": "labs", "provider": "Coursera",
     "description": "EDA with Pandas, Matplotlib, Seaborn, Plotly.",
     "rating": 4.6, "enrolled_count": 195000},
    {"title": "Machine Learning Foundations", "category": "data_science", "difficulty": "intermediate",
     "duration_hrs": 20, "format_type": "theory", "provider": "Coursera",
     "description": "Supervised/unsupervised learning, model evaluation, scikit-learn.",
     "rating": 4.9, "enrolled_count": 450000},
    {"title": "Deep Learning & Neural Networks", "category": "data_science", "difficulty": "advanced",
     "duration_hrs": 28, "format_type": "labs", "provider": "Coursera",
     "description": "CNNs, RNNs, LSTMs, transformers with TensorFlow/PyTorch.",
     "rating": 4.9, "enrolled_count": 280000},
    {"title": "Natural Language Processing", "category": "data_science", "difficulty": "advanced",
     "duration_hrs": 22, "format_type": "labs", "provider": "Coursera",
     "description": "Text preprocessing, sentiment analysis, transformers, BERT.",
     "rating": 4.8, "enrolled_count": 165000},
    {"title": "Data Science Capstone Project", "category": "data_science", "difficulty": "advanced",
     "duration_hrs": 35, "format_type": "project", "provider": "Coursera",
     "description": "Build and deploy a full data science pipeline on real-world data.",
     "rating": 4.7, "enrolled_count": 98000},

    # ── WEB DEVELOPMENT ──────────────────────────────────────────────────────
    {"title": "HTML & CSS Fundamentals", "category": "web_development", "difficulty": "beginner",
     "duration_hrs": 8, "format_type": "labs", "provider": "Coursera",
     "description": "Structure, style, and layout with HTML5 and CSS3.",
     "rating": 4.7, "enrolled_count": 420000},
    {"title": "JavaScript: From Basics to ES6+", "category": "web_development", "difficulty": "beginner",
     "duration_hrs": 14, "format_type": "video", "provider": "Coursera",
     "description": "Core JS, DOM manipulation, async/await, modules.",
     "rating": 4.8, "enrolled_count": 380000},
    {"title": "React.js Complete Guide", "category": "web_development", "difficulty": "intermediate",
     "duration_hrs": 22, "format_type": "labs", "provider": "Coursera",
     "description": "React hooks, context, Redux, routing, and API integration.",
     "rating": 4.9, "enrolled_count": 290000},
    {"title": "Node.js & Express Backend", "category": "web_development", "difficulty": "intermediate",
     "duration_hrs": 18, "format_type": "labs", "provider": "Coursera",
     "description": "REST APIs, authentication, MongoDB with Node/Express.",
     "rating": 4.7, "enrolled_count": 210000},
    {"title": "Full Stack Web Development Project", "category": "web_development", "difficulty": "advanced",
     "duration_hrs": 40, "format_type": "project", "provider": "Coursera",
     "description": "Build and deploy a full-stack application with MERN stack.",
     "rating": 4.8, "enrolled_count": 155000},

    # ── CLOUD COMPUTING ──────────────────────────────────────────────────────
    {"title": "Cloud Computing Concepts", "category": "cloud_computing", "difficulty": "beginner",
     "duration_hrs": 10, "format_type": "theory", "provider": "Coursera",
     "description": "IaaS, PaaS, SaaS, cloud service models and deployment.",
     "rating": 4.5, "enrolled_count": 175000},
    {"title": "AWS Solutions Architect", "category": "cloud_computing", "difficulty": "intermediate",
     "duration_hrs": 25, "format_type": "labs", "provider": "Coursera",
     "description": "EC2, S3, VPC, Lambda, RDS, CloudFormation.",
     "rating": 4.8, "enrolled_count": 320000},
    {"title": "Docker & Kubernetes", "category": "cloud_computing", "difficulty": "intermediate",
     "duration_hrs": 20, "format_type": "labs", "provider": "Coursera",
     "description": "Containerization, orchestration, Helm, service mesh.",
     "rating": 4.9, "enrolled_count": 245000},
    {"title": "DevOps & CI/CD Pipelines", "category": "cloud_computing", "difficulty": "advanced",
     "duration_hrs": 22, "format_type": "project", "provider": "Coursera",
     "description": "Jenkins, GitHub Actions, Terraform, monitoring, SRE.",
     "rating": 4.7, "enrolled_count": 187000},

    # ── PROGRAMMING ─────────────────────────────────────────────────────────
    {"title": "Programming Fundamentals with Python", "category": "programming", "difficulty": "beginner",
     "duration_hrs": 12, "format_type": "video", "provider": "Coursera",
     "description": "Variables, loops, functions, OOP basics in Python.",
     "rating": 4.8, "enrolled_count": 520000},
    {"title": "Data Structures & Algorithms", "category": "programming", "difficulty": "intermediate",
     "duration_hrs": 24, "format_type": "theory", "provider": "Coursera",
     "description": "Arrays, trees, graphs, sorting, dynamic programming.",
     "rating": 4.7, "enrolled_count": 310000},
    {"title": "System Design Interview Prep", "category": "programming", "difficulty": "advanced",
     "duration_hrs": 20, "format_type": "theory", "provider": "Coursera",
     "description": "Scalability, load balancing, caching, databases, design patterns.",
     "rating": 4.9, "enrolled_count": 195000},
    {"title": "Software Engineering Best Practices", "category": "programming", "difficulty": "intermediate",
     "duration_hrs": 15, "format_type": "mixed", "provider": "Coursera",
     "description": "Clean code, SOLID, design patterns, testing, Git.",
     "rating": 4.6, "enrolled_count": 145000},
]

# ── MODULES (per course — 3-5 modules each) ──────────────────────────────────

def generate_modules_for_course(course_id: int, course: dict) -> list:
    """Generate 3-5 modules for a given course."""
    domain = course['category']
    difficulty = course['difficulty']
    fmt = course['format_type']
    base_title = course['title']

    module_templates = {
        'beginner': [
            {"suffix": "101 - Introduction & Overview", "type": "video", "duration_min": 45},
            {"suffix": "Core Concepts & Terminology", "type": "reading", "duration_min": 60},
            {"suffix": "Hands-on Basics", "type": fmt if fmt != 'theory' else 'labs', "duration_min": 90},
            {"suffix": "Practice Exercises", "type": "labs", "duration_min": 60},
        ],
        'intermediate': [
            {"suffix": "Deep Dive: Core Techniques", "type": "video", "duration_min": 60},
            {"suffix": "Lab: Practical Implementation", "type": "labs", "duration_min": 120},
            {"suffix": "Advanced Concepts", "type": "theory", "duration_min": 75},
            {"suffix": "Mini Project", "type": "project", "duration_min": 180},
            {"suffix": "Assessment & Review", "type": "quiz", "duration_min": 30},
        ],
        'advanced': [
            {"suffix": "Expert Techniques", "type": "theory", "duration_min": 90},
            {"suffix": "Advanced Lab Workshop", "type": "labs", "duration_min": 150},
            {"suffix": "Real-world Case Study", "type": "video", "duration_min": 60},
            {"suffix": "Capstone Lab", "type": "project", "duration_min": 240},
            {"suffix": "Final Assessment", "type": "quiz", "duration_min": 45},
        ],
    }

    templates = module_templates.get(difficulty, module_templates['intermediate'])
    modules = []
    assessment_pool = _get_assessment_questions(domain)

    for i, tmpl in enumerate(templates):
        title = f"{base_title}: {tmpl['suffix']}"
        mtype = tmpl.get('type', fmt)
        # Map format types
        type_map = {'reading': 'theory', 'text': 'theory', 'quiz': 'video'}
        mtype = type_map.get(mtype, mtype)

        modules.append({
            'course_id': course_id,
            'title': title,
            'description': f"Module {i+1} of {base_title}. Focus: {tmpl['suffix']}.",
            'module_type': mtype,
            'difficulty': difficulty,
            'duration_min': tmpl['duration_min'],
            'domain': domain,
            'tags': [domain, difficulty, mtype],
            'order_index': i,
            'assessment_questions': random.sample(assessment_pool, min(4, len(assessment_pool))),
        })

    return modules


def _get_assessment_questions(domain: str) -> list:
    """Return assessment questions per domain."""
    base = [
        {"q": "What was the main focus of this module?", "opts": ["Theory", "Practice", "Both theory and practice", "Neither"], "correct": 2},
        {"q": "Rate your confidence after this module:", "opts": ["Not confident", "Slightly confident", "Confident", "Very confident"], "correct": 2},
        {"q": "Which concept was most challenging?", "opts": ["Core concepts", "Practical application", "Terminology", "Nothing was challenging"], "correct": 1},
        {"q": "Would you recommend this module?", "opts": ["No", "Maybe", "Yes", "Absolutely"], "correct": 3},
    ]
    domain_specific = {
        "cybersecurity": {"q": "What is the primary goal of penetration testing?", "opts": ["Damage systems", "Find vulnerabilities before attackers do", "Install backdoors", "Bypass laws"], "correct": 1},
        "data_science": {"q": "What is the bias-variance tradeoff?", "opts": ["Speed vs accuracy", "Underfitting vs overfitting balance", "Data size vs model size", "Training vs testing split"], "correct": 1},
        "web_development": {"q": "What is the purpose of version control?", "opts": ["Speed up websites", "Track and manage code changes", "Host websites", "Encrypt data"], "correct": 1},
        "cloud_computing": {"q": "What is auto-scaling in cloud?", "opts": ["Manual server management", "Automatic resource adjustment based on demand", "Fixed server capacity", "One-time setup"], "correct": 1},
        "programming": {"q": "What is time complexity?", "opts": ["Actual execution time", "Measure of how runtime grows with input size", "Memory usage", "Code length"], "correct": 1},
    }
    questions = list(base)
    if domain in domain_specific:
        questions.append(domain_specific[domain])
    return questions


# ── SYNTHETIC LEARNER CASES ──────────────────────────────────────────────────

SYNTHETIC_CASES = [
    # Cybersecurity learners
    {"persona": "job_seeker", "learning_goal": "become a penetration tester and learn ethical hacking",
     "goal_domain": "cybersecurity", "skill_level": "beginner", "background": "tech",
     "memory_capacity": "medium", "learning_style": "labs", "quiz_score": 35,
     "prior_knowledge": "beginner", "completion_rate": 0.95, "avg_score": 78},
    {"persona": "professional", "learning_goal": "advance my network security skills for SOC analyst role",
     "goal_domain": "cybersecurity", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "mixed", "quiz_score": 65,
     "prior_knowledge": "intermediate", "completion_rate": 1.0, "avg_score": 85},
    {"persona": "college_student", "learning_goal": "learn cybersecurity fundamentals for my degree",
     "goal_domain": "cybersecurity", "skill_level": "beginner", "background": "tech",
     "memory_capacity": "short", "learning_style": "video", "quiz_score": 40,
     "prior_knowledge": "beginner", "completion_rate": 0.88, "avg_score": 72},
    {"persona": "explorer", "learning_goal": "understand how hackers attack systems out of curiosity",
     "goal_domain": "cybersecurity", "skill_level": "beginner", "background": "non_tech",
     "memory_capacity": "short", "learning_style": "video", "quiz_score": 30,
     "prior_knowledge": "beginner", "completion_rate": 0.75, "avg_score": 65},

    # Data Science learners
    {"persona": "professional", "learning_goal": "transition to data scientist from software engineer",
     "goal_domain": "data_science", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "project", "quiz_score": 72,
     "prior_knowledge": "intermediate", "completion_rate": 1.0, "avg_score": 88},
    {"persona": "college_student", "learning_goal": "learn machine learning and AI for my thesis",
     "goal_domain": "data_science", "skill_level": "beginner", "background": "tech",
     "memory_capacity": "medium", "learning_style": "theory", "quiz_score": 55,
     "prior_knowledge": "intermediate", "completion_rate": 0.92, "avg_score": 81},
    {"persona": "job_seeker", "learning_goal": "become a data analyst and get a job in data",
     "goal_domain": "data_science", "skill_level": "beginner", "background": "non_tech",
     "memory_capacity": "medium", "learning_style": "video", "quiz_score": 38,
     "prior_knowledge": "beginner", "completion_rate": 0.90, "avg_score": 74},
    {"persona": "explorer", "learning_goal": "understand deep learning and neural networks",
     "goal_domain": "data_science", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "labs", "quiz_score": 68,
     "prior_knowledge": "intermediate", "completion_rate": 0.85, "avg_score": 79},

    # Web Development learners
    {"persona": "job_seeker", "learning_goal": "become a full stack web developer",
     "goal_domain": "web_development", "skill_level": "beginner", "background": "non_tech",
     "memory_capacity": "medium", "learning_style": "labs", "quiz_score": 45,
     "prior_knowledge": "beginner", "completion_rate": 0.95, "avg_score": 77},
    {"persona": "college_student", "learning_goal": "build web apps with React and Node.js",
     "goal_domain": "web_development", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "medium", "learning_style": "project", "quiz_score": 62,
     "prior_knowledge": "intermediate", "completion_rate": 1.0, "avg_score": 83},
    {"persona": "professional", "learning_goal": "upgrade my frontend skills with modern frameworks",
     "goal_domain": "web_development", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "mixed", "quiz_score": 70,
     "prior_knowledge": "intermediate", "completion_rate": 0.97, "avg_score": 87},

    # Cloud Computing learners
    {"persona": "professional", "learning_goal": "get AWS certification and become cloud architect",
     "goal_domain": "cloud_computing", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "labs", "quiz_score": 78,
     "prior_knowledge": "intermediate", "completion_rate": 1.0, "avg_score": 91},
    {"persona": "job_seeker", "learning_goal": "learn DevOps and cloud deployment",
     "goal_domain": "cloud_computing", "skill_level": "beginner", "background": "tech",
     "memory_capacity": "medium", "learning_style": "video", "quiz_score": 48,
     "prior_knowledge": "beginner", "completion_rate": 0.88, "avg_score": 73},

    # Programming learners
    {"persona": "college_student", "learning_goal": "master data structures and algorithms for interviews",
     "goal_domain": "programming", "skill_level": "intermediate", "background": "tech",
     "memory_capacity": "long", "learning_style": "theory", "quiz_score": 68,
     "prior_knowledge": "intermediate", "completion_rate": 0.95, "avg_score": 82},
    {"persona": "explorer", "learning_goal": "learn programming from scratch with Python",
     "goal_domain": "programming", "skill_level": "beginner", "background": "non_tech",
     "memory_capacity": "short", "learning_style": "video", "quiz_score": 25,
     "prior_knowledge": "beginner", "completion_rate": 0.80, "avg_score": 68},
]


def seed_database(app, db, models):
    """
    Seed the database with courses, modules, and synthetic cases.
    Should be called once on app initialization if tables are empty.
    """
    from recommender.bert_model import bert_model

    with app.app_context():
        Course = models['Course']
        Module = models['Module']
        CaseBase = models['CaseBase']

        # Check if already seeded
        if Course.query.count() > 0:
            logger.info("Database already seeded. Skipping.")
            return

        logger.info("🌱 Seeding database with courses, modules, and cases...")

        # ── Seed Courses & Modules ────────────────────────────────────────────
        all_modules_by_domain = {}

        for course_data in SAMPLE_COURSES:
            course = Course(
                title=course_data['title'],
                provider=course_data['provider'],
                category=course_data['category'],
                difficulty=course_data['difficulty'],
                duration_hrs=course_data['duration_hrs'],
                format_type=course_data['format_type'],
                description=course_data['description'],
                rating=course_data['rating'],
                enrolled_count=course_data['enrolled_count'],
            )
            db.session.add(course)
            db.session.flush()  # Get the ID

            modules_data = generate_modules_for_course(course.id, course_data)
            domain = course_data['category']
            if domain not in all_modules_by_domain:
                all_modules_by_domain[domain] = []

            for mod_data in modules_data:
                module = Module(
                    course_id=course.id,
                    title=mod_data['title'],
                    description=mod_data['description'],
                    module_type=mod_data['module_type'],
                    difficulty=mod_data['difficulty'],
                    duration_min=mod_data['duration_min'],
                    domain=mod_data['domain'],
                    order_index=mod_data['order_index'],
                )
                module.set_tags(mod_data['tags'])
                module.set_assessment_questions(mod_data['assessment_questions'])
                db.session.add(module)
                db.session.flush()
                all_modules_by_domain[domain].append(module.id)

        db.session.commit()
        logger.info(f"✅ Seeded {Course.query.count()} courses and {Module.query.count()} modules")

        # ── Seed Synthetic Cases ──────────────────────────────────────────────
        for case_data in SYNTHETIC_CASES:
            domain = case_data['goal_domain']
            domain_module_ids = all_modules_by_domain.get(domain, [])

            # Select appropriate modules based on skill level
            skill = case_data['skill_level']
            all_mods = Module.query.filter_by(domain=domain).all()
            skill_mods = [m for m in all_mods if m.difficulty == skill]
            int_mods = [m for m in all_mods if m.difficulty == 'intermediate']
            selected = (skill_mods + int_mods)[:6] if skill != 'expert' else all_mods[:6]
            path_ids = [m.id for m in selected]

            if not path_ids:
                path_ids = domain_module_ids[:5]

            # Encode goal with BERT
            try:
                embedding = bert_model.encode_single(case_data['learning_goal'])
            except Exception:
                embedding = []

            case = CaseBase(
                persona=case_data['persona'],
                learning_goal=case_data['learning_goal'],
                goal_domain=case_data['goal_domain'],
                skill_level=case_data['skill_level'],
                background=case_data['background'],
                memory_capacity=case_data['memory_capacity'],
                learning_style=case_data['learning_style'],
                quiz_score=case_data['quiz_score'],
                prior_knowledge=case_data['prior_knowledge'],
                completion_rate=case_data['completion_rate'],
                avg_assessment_score=case_data['avg_score'],
                outcome_success=True,
                is_synthetic=True,
            )
            case.set_goal_embedding(embedding)
            case.set_path_module_ids(path_ids)
            db.session.add(case)

        db.session.commit()
        logger.info(f"✅ Seeded {CaseBase.query.count()} synthetic cases")
        logger.info("🎉 Database seeding complete!")
