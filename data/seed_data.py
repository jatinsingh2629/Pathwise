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


# ── RESOURCE SEED DATA ───────────────────────────────────────────────────────
# Each entry is keyed by a substring that must appear in the module title.
# The seeder matches modules by scanning their title for these substrings.

RESOURCE_TEMPLATES = [
    # ── CYBERSECURITY ────────────────────────────────────────────────────────
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Introduction",
        "resources": [
            {"title": "Cybersecurity for Beginners – Full Course",
             "description": "A comprehensive beginner-friendly video course covering core cybersecurity concepts, threat landscapes, and basic defenses.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=U_P23SqJaDc",
             "duration_min": 120, "difficulty": "beginner", "provider": "YouTube", "rating": 4.7},
            {"title": "What is Cybersecurity? – IBM Think",
             "description": "Concise IBM article explaining cybersecurity fundamentals, key terminology, and why it matters for every organization.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://www.ibm.com/topics/cybersecurity",
             "duration_min": 15, "difficulty": "beginner", "provider": "IBM", "rating": 4.5},
            {"title": "TryHackMe – Pre-Security Learning Path",
             "description": "Hands-on browser-based labs covering networking, Linux, and web fundamentals — no setup required.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://tryhackme.com/path/outline/presecurity",
             "duration_min": 180, "difficulty": "beginner", "provider": "TryHackMe", "rating": 4.9},
            {"title": "NIST Cybersecurity Framework Overview",
             "description": "Official NIST documentation introducing the Cybersecurity Framework used by organizations worldwide.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://www.nist.gov/cyberframework",
             "duration_min": 30, "difficulty": "beginner", "provider": "NIST", "rating": 4.6},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Network Security",
        "resources": [
            {"title": "Network Security Tutorial – Professor Messer",
             "description": "Free CompTIA Security+ video series covering network security protocols, firewalls, IDS/IPS, and VPNs.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-plus-course/",
             "duration_min": 90, "difficulty": "beginner", "provider": "Professor Messer", "rating": 4.8},
            {"title": "TCP/IP and Network Security – Medium",
             "description": "In-depth article series on TCP/IP stack vulnerabilities, packet analysis, and network hardening techniques.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://medium.com/tag/network-security",
             "duration_min": 25, "difficulty": "beginner", "provider": "Medium", "rating": 4.4},
            {"title": "Wireshark Network Analysis Lab",
             "description": "Hands-on Wireshark lab: capture and analyze real network traffic to identify anomalies and common attacks.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://tryhackme.com/room/wireshark101",
             "duration_min": 120, "difficulty": "beginner", "provider": "TryHackMe", "rating": 4.7},
            {"title": "Cisco Networking Academy – Network Security",
             "description": "Free Cisco course covering firewall configuration, VPN setup, and intrusion prevention systems.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.netacad.com/courses/cybersecurity",
             "duration_min": 240, "difficulty": "intermediate", "provider": "Cisco NetAcad", "rating": 4.6},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Ethical Hacking",
        "resources": [
            {"title": "Metasploit Framework Tutorial – Full Course",
             "description": "Complete Metasploit tutorial covering exploitation, post-exploitation, and reporting for penetration testers.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=8lR27r8Y_ik",
             "duration_min": 45, "difficulty": "intermediate", "provider": "YouTube", "rating": 4.8},
            {"title": "Penetration Testing Guide – Medium",
             "description": "Step-by-step penetration testing methodology covering reconnaissance, scanning, exploitation, and reporting.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://medium.com/@cybersecurity/penetration-testing-guide",
             "duration_min": 20, "difficulty": "intermediate", "provider": "Medium", "rating": 4.5},
            {"title": "DVWA – Damn Vulnerable Web Application Lab",
             "description": "Set up and attack DVWA to practice SQL injection, XSS, CSRF, and file inclusion in a safe environment.",
             "resource_type": "project", "learning_style": "labs",
             "url": "https://github.com/digininja/DVWA",
             "duration_min": 180, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.9},
            {"title": "Kali Linux Revealed – Hands-on Course",
             "description": "Official Kali Linux course covering tool usage, scripting, and real-world penetration testing scenarios.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.kali.org/docs/introduction/",
             "duration_min": 120, "difficulty": "intermediate", "provider": "Offensive Security", "rating": 4.7},
            {"title": "OWASP Testing Guide v4.2",
             "description": "The definitive reference for web application security testing — methodology, checklists, and tool recommendations.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://owasp.org/www-project-web-security-testing-guide/",
             "duration_min": 60, "difficulty": "intermediate", "provider": "OWASP", "rating": 4.8},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Web Application Security",
        "resources": [
            {"title": "OWASP Top 10 Explained – Video Series",
             "description": "Video walkthrough of each OWASP Top 10 vulnerability with live demos and mitigation strategies.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=rWHvp7rUka8",
             "duration_min": 60, "difficulty": "intermediate", "provider": "YouTube", "rating": 4.8},
            {"title": "PortSwigger Web Security Academy",
             "description": "Free interactive labs covering SQL injection, XSS, CSRF, SSRF, and more — built by the creators of Burp Suite.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://portswigger.net/web-security",
             "duration_min": 300, "difficulty": "intermediate", "provider": "PortSwigger", "rating": 5.0},
            {"title": "Secure Coding Practices – OWASP Cheat Sheet",
             "description": "Comprehensive cheat sheet series covering secure coding patterns for common web vulnerabilities.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://cheatsheetseries.owasp.org/",
             "duration_min": 40, "difficulty": "intermediate", "provider": "OWASP", "rating": 4.7},
            {"title": "Build a Vulnerable Flask App and Fix It",
             "description": "GitHub project: intentionally vulnerable Python/Flask app with guided exercises to identify and patch each flaw.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/we45/Vulnerable-Flask-App",
             "duration_min": 240, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.6},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Malware",
        "resources": [
            {"title": "Malware Analysis Fundamentals – ANY.RUN Blog",
             "description": "Detailed article series on static and dynamic malware analysis techniques using industry-standard tools.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://any.run/cybersecurity-blog/malware-analysis-fundamentals/",
             "duration_min": 35, "difficulty": "advanced", "provider": "ANY.RUN", "rating": 4.7},
            {"title": "Reverse Engineering Malware – Full Course",
             "description": "Video course covering IDA Pro, Ghidra, and x86 assembly for reverse engineering real malware samples.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=9vKG8-TnawY",
             "duration_min": 90, "difficulty": "advanced", "provider": "YouTube", "rating": 4.8},
            {"title": "Malware Analysis Lab Setup – GitHub",
             "description": "Complete guide and scripts to build an isolated malware analysis lab with FlareVM and REMnux.",
             "resource_type": "project", "learning_style": "labs",
             "url": "https://github.com/mandiant/flare-vm",
             "duration_min": 180, "difficulty": "advanced", "provider": "GitHub / Mandiant", "rating": 4.9},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "SOC",
        "resources": [
            {"title": "SOC Analyst Training – TryHackMe SOC Level 1",
             "description": "Structured learning path covering SIEM, log analysis, threat intelligence, and incident response for SOC analysts.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://tryhackme.com/path/outline/soclevel1",
             "duration_min": 480, "difficulty": "intermediate", "provider": "TryHackMe", "rating": 4.9},
            {"title": "Introduction to SIEM – Splunk Free Training",
             "description": "Official Splunk training covering data ingestion, search, dashboards, and alert creation for security operations.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.splunk.com/en_us/training/free-courses/splunk-fundamentals-1.html",
             "duration_min": 180, "difficulty": "intermediate", "provider": "Splunk", "rating": 4.7},
            {"title": "Incident Response Playbook – GitHub",
             "description": "Open-source collection of incident response playbooks covering ransomware, phishing, data breach, and more.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/certsocietegenerale/IRM",
             "duration_min": 120, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.6},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Cryptography",
        "resources": [
            {"title": "Cryptography I – Stanford (Coursera)",
             "description": "Dan Boneh's legendary cryptography course covering symmetric/asymmetric encryption, MACs, and digital signatures.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.coursera.org/learn/crypto",
             "duration_min": 300, "difficulty": "intermediate", "provider": "Coursera / Stanford", "rating": 4.9},
            {"title": "How TLS/SSL Works – Cloudflare Learning",
             "description": "Clear, illustrated explanation of TLS handshake, certificate chains, and PKI infrastructure.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://www.cloudflare.com/learning/ssl/what-is-ssl/",
             "duration_min": 20, "difficulty": "intermediate", "provider": "Cloudflare", "rating": 4.6},
            {"title": "CryptoPals Challenges",
             "description": "Hands-on cryptography challenges that teach real-world crypto attacks by breaking intentionally weak implementations.",
             "resource_type": "project", "learning_style": "labs",
             "url": "https://cryptopals.com/",
             "duration_min": 360, "difficulty": "advanced", "provider": "Cryptopals", "rating": 4.9},
        ]
    },
    {
        "match_domain": "cybersecurity",
        "match_title_contains": "Capstone",
        "resources": [
            {"title": "Build a Full Penetration Test Report – Template",
             "description": "Professional pentest report template with guidance on executive summary, findings, CVSS scoring, and remediation.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/hmaverickadams/TCM-Security-Sample-Pentest-Report",
             "duration_min": 240, "difficulty": "advanced", "provider": "GitHub / TCM Security", "rating": 4.8},
            {"title": "Hack The Box – Pro Labs",
             "description": "Enterprise-grade lab environments simulating real corporate networks for advanced penetration testing practice.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.hackthebox.com/hacker/pro-labs",
             "duration_min": 600, "difficulty": "advanced", "provider": "Hack The Box", "rating": 4.9},
            {"title": "Security Audit Methodology – SANS Reading Room",
             "description": "Comprehensive SANS whitepaper on conducting end-to-end security audits in enterprise environments.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://www.sans.org/reading-room/",
             "duration_min": 45, "difficulty": "advanced", "provider": "SANS Institute", "rating": 4.7},
        ]
    },

    # ── DATA SCIENCE ─────────────────────────────────────────────────────────
    {
        "match_domain": "data_science",
        "match_title_contains": "Python for Data Science",
        "resources": [
            {"title": "Python for Data Science – freeCodeCamp Full Course",
             "description": "4-hour beginner video covering Python, NumPy, Pandas, and Matplotlib with hands-on Jupyter notebooks.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=LHBE6Q9XlzI",
             "duration_min": 240, "difficulty": "beginner", "provider": "YouTube / freeCodeCamp", "rating": 4.8},
            {"title": "Pandas Documentation – Getting Started",
             "description": "Official Pandas documentation with tutorials, API reference, and worked examples for data manipulation.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://pandas.pydata.org/docs/getting_started/index.html",
             "duration_min": 30, "difficulty": "beginner", "provider": "Pandas", "rating": 4.6},
            {"title": "Kaggle Python Course",
             "description": "Free interactive Python course on Kaggle with exercises covering syntax, functions, lists, and data types.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.kaggle.com/learn/python",
             "duration_min": 180, "difficulty": "beginner", "provider": "Kaggle", "rating": 4.7},
            {"title": "NumPy Quickstart – Official Tutorial",
             "description": "Official NumPy tutorial covering array creation, indexing, broadcasting, and linear algebra operations.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://numpy.org/doc/stable/user/quickstart.html",
             "duration_min": 25, "difficulty": "beginner", "provider": "NumPy", "rating": 4.5},
        ]
    },
    {
        "match_domain": "data_science",
        "match_title_contains": "Data Analysis",
        "resources": [
            {"title": "Exploratory Data Analysis – Kaggle Course",
             "description": "Hands-on Kaggle course covering EDA techniques, missing data handling, and feature distributions.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.kaggle.com/learn/data-visualization",
             "duration_min": 180, "difficulty": "beginner", "provider": "Kaggle", "rating": 4.7},
            {"title": "Data Visualization with Python – Towards Data Science",
             "description": "Comprehensive article covering Matplotlib, Seaborn, and Plotly with real-world dataset examples.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://towardsdatascience.com/data-visualization-with-python",
             "duration_min": 25, "difficulty": "beginner", "provider": "Towards Data Science", "rating": 4.5},
            {"title": "EDA on Titanic Dataset – Kaggle Notebook",
             "description": "Classic EDA project notebook on the Titanic dataset — great starting point for data analysis practice.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://www.kaggle.com/code/startupsci/titanic-data-science-solutions",
             "duration_min": 120, "difficulty": "beginner", "provider": "Kaggle", "rating": 4.8},
            {"title": "Seaborn Tutorial – Official Documentation",
             "description": "Official Seaborn tutorial with gallery examples for statistical data visualization.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://seaborn.pydata.org/tutorial.html",
             "duration_min": 20, "difficulty": "beginner", "provider": "Seaborn", "rating": 4.4},
        ]
    },
    {
        "match_domain": "data_science",
        "match_title_contains": "Machine Learning",
        "resources": [
            {"title": "Machine Learning – Andrew Ng (Coursera)",
             "description": "The world's most popular ML course covering supervised learning, neural networks, and best practices.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.coursera.org/specializations/machine-learning-introduction",
             "duration_min": 600, "difficulty": "intermediate", "provider": "Coursera / DeepLearning.AI", "rating": 4.9},
            {"title": "Scikit-learn User Guide",
             "description": "Official scikit-learn documentation covering all estimators, pipelines, model selection, and evaluation metrics.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://scikit-learn.org/stable/user_guide.html",
             "duration_min": 60, "difficulty": "intermediate", "provider": "scikit-learn", "rating": 4.7},
            {"title": "Kaggle ML Competitions – Beginner Track",
             "description": "Participate in beginner Kaggle competitions to apply ML algorithms on real datasets with community notebooks.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://www.kaggle.com/competitions?hostSegment=playground",
             "duration_min": 360, "difficulty": "intermediate", "provider": "Kaggle", "rating": 4.8},
            {"title": "Hands-On Machine Learning – Code Examples",
             "description": "GitHub repository with all code examples from Aurélien Géron's 'Hands-On ML with Scikit-Learn & TensorFlow'.",
             "resource_type": "code_example", "learning_style": "labs",
             "url": "https://github.com/ageron/handson-ml3",
             "duration_min": 240, "difficulty": "intermediate", "provider": "GitHub / O'Reilly", "rating": 4.9},
        ]
    },
    {
        "match_domain": "data_science",
        "match_title_contains": "Deep Learning",
        "resources": [
            {"title": "Deep Learning Specialization – Andrew Ng",
             "description": "Five-course specialization covering neural networks, CNNs, RNNs, and transformers with TensorFlow.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.coursera.org/specializations/deep-learning",
             "duration_min": 900, "difficulty": "advanced", "provider": "Coursera / DeepLearning.AI", "rating": 4.9},
            {"title": "PyTorch Tutorials – Official",
             "description": "Official PyTorch tutorials covering tensors, autograd, neural networks, and computer vision.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://pytorch.org/tutorials/",
             "duration_min": 120, "difficulty": "advanced", "provider": "PyTorch", "rating": 4.7},
            {"title": "Fast.ai Practical Deep Learning for Coders",
             "description": "Top-down practical course using fast.ai library — build state-of-the-art models from lesson one.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://course.fast.ai/",
             "duration_min": 600, "difficulty": "advanced", "provider": "fast.ai", "rating": 4.9},
            {"title": "Build a CNN from Scratch – GitHub",
             "description": "Step-by-step project implementing a convolutional neural network from scratch in NumPy and PyTorch.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/vzhou842/cnn-from-scratch",
             "duration_min": 180, "difficulty": "advanced", "provider": "GitHub", "rating": 4.7},
        ]
    },
    {
        "match_domain": "data_science",
        "match_title_contains": "Natural Language",
        "resources": [
            {"title": "NLP with Transformers – Hugging Face Course",
             "description": "Free Hugging Face course covering tokenization, fine-tuning BERT, and building NLP pipelines.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://huggingface.co/learn/nlp-course/",
             "duration_min": 480, "difficulty": "advanced", "provider": "Hugging Face", "rating": 4.9},
            {"title": "Illustrated BERT – Jay Alammar",
             "description": "Visually rich article explaining BERT's architecture, attention mechanism, and pre-training objectives.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://jalammar.github.io/illustrated-bert/",
             "duration_min": 30, "difficulty": "advanced", "provider": "Jay Alammar Blog", "rating": 4.9},
            {"title": "Text Classification with BERT – Kaggle Notebook",
             "description": "End-to-end Kaggle notebook fine-tuning BERT for sentiment analysis on the IMDB dataset.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://www.kaggle.com/code/harshjain123/bert-for-everyone-tutorial-implementation",
             "duration_min": 180, "difficulty": "advanced", "provider": "Kaggle", "rating": 4.7},
        ]
    },
    {
        "match_domain": "data_science",
        "match_title_contains": "Capstone",
        "resources": [
            {"title": "End-to-End ML Project – Towards Data Science",
             "description": "Complete walkthrough of a production ML pipeline: data collection, EDA, modeling, deployment, and monitoring.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://towardsdatascience.com/end-to-end-machine-learning-project",
             "duration_min": 40, "difficulty": "advanced", "provider": "Towards Data Science", "rating": 4.7},
            {"title": "Kaggle Featured Competition – Real-World Dataset",
             "description": "Compete in a Kaggle featured competition to build and deploy a full data science pipeline on real-world data.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://www.kaggle.com/competitions",
             "duration_min": 600, "difficulty": "advanced", "provider": "Kaggle", "rating": 4.8},
            {"title": "MLflow – Model Tracking & Deployment",
             "description": "Official MLflow documentation for experiment tracking, model registry, and deployment to production.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://mlflow.org/docs/latest/index.html",
             "duration_min": 60, "difficulty": "advanced", "provider": "MLflow", "rating": 4.6},
        ]
    },

    # ── WEB DEVELOPMENT ──────────────────────────────────────────────────────
    {
        "match_domain": "web_development",
        "match_title_contains": "HTML",
        "resources": [
            {"title": "HTML & CSS Full Course – freeCodeCamp",
             "description": "11-hour beginner video covering HTML5 structure, CSS3 styling, Flexbox, Grid, and responsive design.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=mU6anWqZJcc",
             "duration_min": 660, "difficulty": "beginner", "provider": "YouTube / freeCodeCamp", "rating": 4.8},
            {"title": "MDN Web Docs – HTML Basics",
             "description": "Mozilla's authoritative HTML reference covering elements, attributes, forms, and semantic markup.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
             "duration_min": 45, "difficulty": "beginner", "provider": "MDN Web Docs", "rating": 4.9},
            {"title": "freeCodeCamp – Responsive Web Design Certification",
             "description": "Interactive curriculum with 300 hours of hands-on HTML/CSS challenges and five certification projects.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
             "duration_min": 300, "difficulty": "beginner", "provider": "freeCodeCamp", "rating": 4.8},
            {"title": "Build a Personal Portfolio – GitHub Pages",
             "description": "Step-by-step project to build and deploy a personal portfolio site using HTML, CSS, and GitHub Pages.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://pages.github.com/",
             "duration_min": 180, "difficulty": "beginner", "provider": "GitHub", "rating": 4.6},
        ]
    },
    {
        "match_domain": "web_development",
        "match_title_contains": "JavaScript",
        "resources": [
            {"title": "JavaScript Full Course – Bro Code",
             "description": "Comprehensive JavaScript video covering variables, functions, DOM, events, async/await, and ES6+ features.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=lfmg-EJ8gm4",
             "duration_min": 480, "difficulty": "beginner", "provider": "YouTube", "rating": 4.8},
            {"title": "The Modern JavaScript Tutorial – javascript.info",
             "description": "The most comprehensive free JavaScript tutorial covering core language, browser APIs, and advanced patterns.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://javascript.info/",
             "duration_min": 60, "difficulty": "beginner", "provider": "javascript.info", "rating": 4.9},
            {"title": "JavaScript30 – 30 Day Vanilla JS Challenge",
             "description": "Build 30 projects in 30 days using only vanilla JavaScript — no frameworks, no libraries.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://javascript30.com/",
             "duration_min": 900, "difficulty": "beginner", "provider": "Wes Bos", "rating": 4.9},
            {"title": "Codecademy – Learn JavaScript",
             "description": "Interactive JavaScript course with in-browser coding exercises covering syntax through object-oriented programming.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.codecademy.com/learn/introduction-to-javascript",
             "duration_min": 300, "difficulty": "beginner", "provider": "Codecademy", "rating": 4.6},
        ]
    },
    {
        "match_domain": "web_development",
        "match_title_contains": "React",
        "resources": [
            {"title": "React – Official Tutorial: Tic-Tac-Toe",
             "description": "Official React tutorial building a tic-tac-toe game — covers components, state, props, and hooks.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://react.dev/learn/tutorial-tic-tac-toe",
             "duration_min": 90, "difficulty": "intermediate", "provider": "React Docs", "rating": 4.8},
            {"title": "React Full Course 2024 – Traversy Media",
             "description": "Complete React course covering hooks, context API, Redux Toolkit, React Router, and API integration.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=LDB4uaJ87e0",
             "duration_min": 300, "difficulty": "intermediate", "provider": "YouTube / Traversy Media", "rating": 4.8},
            {"title": "Build a Full-Stack React App – GitHub",
             "description": "Open-source project template: React frontend + Node/Express backend with authentication and CRUD operations.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/bradtraversy/mern-tutorial",
             "duration_min": 360, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.7},
            {"title": "Scrimba – Learn React for Free",
             "description": "Interactive React course with embedded code editor — learn by doing with 140+ coding challenges.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://scrimba.com/learn/learnreact",
             "duration_min": 480, "difficulty": "intermediate", "provider": "Scrimba", "rating": 4.8},
        ]
    },
    {
        "match_domain": "web_development",
        "match_title_contains": "Node",
        "resources": [
            {"title": "Node.js & Express – Traversy Media Crash Course",
             "description": "Fast-paced video covering Node.js fundamentals, Express routing, middleware, and REST API creation.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=fBNz5xF-Kx4",
             "duration_min": 90, "difficulty": "intermediate", "provider": "YouTube / Traversy Media", "rating": 4.7},
            {"title": "Node.js Official Documentation",
             "description": "Official Node.js docs covering the runtime, built-in modules, streams, events, and the HTTP module.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://nodejs.org/en/docs/",
             "duration_min": 45, "difficulty": "intermediate", "provider": "Node.js", "rating": 4.5},
            {"title": "REST API with Node, Express & MongoDB – GitHub",
             "description": "Complete REST API project with JWT authentication, CRUD operations, and MongoDB Atlas integration.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/bradtraversy/node_rest_api_mongodb",
             "duration_min": 240, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.7},
            {"title": "The Odin Project – NodeJS Path",
             "description": "Free full-stack curriculum covering Node, Express, databases, and deployment with hands-on projects.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/nodejs",
             "duration_min": 600, "difficulty": "intermediate", "provider": "The Odin Project", "rating": 4.9},
        ]
    },
    {
        "match_domain": "web_development",
        "match_title_contains": "Full Stack",
        "resources": [
            {"title": "MERN Stack Project – Full Tutorial",
             "description": "Build and deploy a complete MERN stack application with authentication, file uploads, and cloud deployment.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=7CqJlxBYj-M",
             "duration_min": 360, "difficulty": "advanced", "provider": "YouTube", "rating": 4.8},
            {"title": "Full Stack Open – University of Helsinki",
             "description": "Free university-level course covering React, Node, GraphQL, TypeScript, and CI/CD with real projects.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://fullstackopen.com/en/",
             "duration_min": 1200, "difficulty": "advanced", "provider": "University of Helsinki", "rating": 4.9},
            {"title": "Deploy MERN App to Railway – Guide",
             "description": "Step-by-step guide to deploying a full-stack MERN application to Railway with environment variables and databases.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://docs.railway.app/",
             "duration_min": 30, "difficulty": "advanced", "provider": "Railway Docs", "rating": 4.6},
        ]
    },

    # ── CLOUD COMPUTING ──────────────────────────────────────────────────────
    {
        "match_domain": "cloud_computing",
        "match_title_contains": "Cloud Computing Concepts",
        "resources": [
            {"title": "Cloud Computing Explained – IBM Technology",
             "description": "Clear video explanation of IaaS, PaaS, SaaS, public/private/hybrid cloud, and key cloud benefits.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=M988_fsOSWo",
             "duration_min": 20, "difficulty": "beginner", "provider": "YouTube / IBM", "rating": 4.7},
            {"title": "What is Cloud Computing? – AWS",
             "description": "AWS's comprehensive introduction to cloud computing concepts, service models, and deployment options.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://aws.amazon.com/what-is-cloud-computing/",
             "duration_min": 15, "difficulty": "beginner", "provider": "AWS", "rating": 4.5},
            {"title": "Google Cloud Skills Boost – Cloud Fundamentals",
             "description": "Hands-on Google Cloud labs covering core services, IAM, networking, and storage with free credits.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.cloudskillsboost.google/paths/11",
             "duration_min": 240, "difficulty": "beginner", "provider": "Google Cloud", "rating": 4.7},
        ]
    },
    {
        "match_domain": "cloud_computing",
        "match_title_contains": "AWS",
        "resources": [
            {"title": "AWS Solutions Architect – Full Course",
             "description": "Complete SAA-C03 exam prep video covering EC2, S3, VPC, Lambda, RDS, and CloudFormation.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=Ia-UEYYR44s",
             "duration_min": 600, "difficulty": "intermediate", "provider": "YouTube / freeCodeCamp", "rating": 4.8},
            {"title": "AWS Well-Architected Framework",
             "description": "Official AWS whitepaper covering the five pillars: operational excellence, security, reliability, performance, cost.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://aws.amazon.com/architecture/well-architected/",
             "duration_min": 60, "difficulty": "intermediate", "provider": "AWS", "rating": 4.7},
            {"title": "AWS Hands-On Labs – AWS Skill Builder",
             "description": "Official AWS lab environment with guided exercises for EC2, S3, Lambda, and VPC configuration.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://skillbuilder.aws/",
             "duration_min": 360, "difficulty": "intermediate", "provider": "AWS Skill Builder", "rating": 4.8},
            {"title": "Terraform AWS Infrastructure – GitHub",
             "description": "Production-ready Terraform modules for provisioning AWS infrastructure following best practices.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/terraform-aws-modules",
             "duration_min": 240, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.7},
        ]
    },
    {
        "match_domain": "cloud_computing",
        "match_title_contains": "Docker",
        "resources": [
            {"title": "Docker & Kubernetes Full Course – TechWorld with Nana",
             "description": "Comprehensive video covering Docker fundamentals, Kubernetes architecture, Helm, and production deployment.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
             "duration_min": 180, "difficulty": "intermediate", "provider": "YouTube / TechWorld with Nana", "rating": 4.9},
            {"title": "Docker Official Documentation – Get Started",
             "description": "Official Docker tutorial covering images, containers, volumes, networks, and Docker Compose.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://docs.docker.com/get-started/",
             "duration_min": 45, "difficulty": "intermediate", "provider": "Docker", "rating": 4.7},
            {"title": "Kubernetes the Hard Way – GitHub",
             "description": "Kelsey Hightower's famous guide to bootstrapping a Kubernetes cluster from scratch — the definitive learning project.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/kelseyhightower/kubernetes-the-hard-way",
             "duration_min": 480, "difficulty": "advanced", "provider": "GitHub", "rating": 4.9},
            {"title": "Play with Docker – Interactive Labs",
             "description": "Free browser-based Docker playground with guided labs — no local installation required.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://labs.play-with-docker.com/",
             "duration_min": 120, "difficulty": "intermediate", "provider": "Play with Docker", "rating": 4.6},
        ]
    },
    {
        "match_domain": "cloud_computing",
        "match_title_contains": "DevOps",
        "resources": [
            {"title": "DevOps Roadmap 2024 – TechWorld with Nana",
             "description": "Video overview of the complete DevOps toolchain: Git, CI/CD, Docker, Kubernetes, Terraform, and monitoring.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=9pZ2xmsSDdo",
             "duration_min": 60, "difficulty": "advanced", "provider": "YouTube / TechWorld with Nana", "rating": 4.8},
            {"title": "GitHub Actions – Official Documentation",
             "description": "Official GitHub Actions docs covering workflow syntax, triggers, jobs, secrets, and reusable workflows.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://docs.github.com/en/actions",
             "duration_min": 45, "difficulty": "advanced", "provider": "GitHub", "rating": 4.7},
            {"title": "Build a CI/CD Pipeline – GitHub Actions Project",
             "description": "End-to-end project: build, test, and deploy a containerized application using GitHub Actions and Railway.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/actions/starter-workflows",
             "duration_min": 300, "difficulty": "advanced", "provider": "GitHub", "rating": 4.7},
            {"title": "Terraform Getting Started – HashiCorp Learn",
             "description": "Official HashiCorp tutorial series for Terraform: write, plan, apply, and manage infrastructure as code.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://developer.hashicorp.com/terraform/tutorials",
             "duration_min": 240, "difficulty": "advanced", "provider": "HashiCorp", "rating": 4.8},
        ]
    },

    # ── PROGRAMMING ──────────────────────────────────────────────────────────
    {
        "match_domain": "programming",
        "match_title_contains": "Programming Fundamentals",
        "resources": [
            {"title": "Python for Everybody – Dr. Chuck (Coursera)",
             "description": "Beginner-friendly Python course covering variables, loops, functions, files, and web data.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.coursera.org/specializations/python",
             "duration_min": 480, "difficulty": "beginner", "provider": "Coursera / University of Michigan", "rating": 4.8},
            {"title": "Python Official Tutorial",
             "description": "Official Python documentation tutorial covering all language fundamentals with interactive examples.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://docs.python.org/3/tutorial/",
             "duration_min": 60, "difficulty": "beginner", "provider": "Python.org", "rating": 4.6},
            {"title": "Codecademy – Learn Python 3",
             "description": "Interactive Python course with 25 hours of in-browser coding exercises covering syntax through OOP.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.codecademy.com/learn/learn-python-3",
             "duration_min": 300, "difficulty": "beginner", "provider": "Codecademy", "rating": 4.7},
            {"title": "Automate the Boring Stuff – Free Book",
             "description": "Practical Python programming book with projects: web scraping, Excel automation, PDF manipulation, and more.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://automatetheboringstuff.com/",
             "duration_min": 120, "difficulty": "beginner", "provider": "Al Sweigart", "rating": 4.8},
        ]
    },
    {
        "match_domain": "programming",
        "match_title_contains": "Data Structures",
        "resources": [
            {"title": "Data Structures & Algorithms – freeCodeCamp",
             "description": "Complete video course covering arrays, linked lists, trees, graphs, sorting, and dynamic programming.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=8hly31xKli0",
             "duration_min": 480, "difficulty": "intermediate", "provider": "YouTube / freeCodeCamp", "rating": 4.8},
            {"title": "LeetCode – Top Interview 150",
             "description": "Curated set of 150 LeetCode problems covering all major DSA topics for technical interview preparation.",
             "resource_type": "project", "learning_style": "labs",
             "url": "https://leetcode.com/studyplan/top-interview-150/",
             "duration_min": 1200, "difficulty": "intermediate", "provider": "LeetCode", "rating": 4.9},
            {"title": "Big-O Cheat Sheet",
             "description": "Quick reference for time and space complexity of common data structures and sorting algorithms.",
             "resource_type": "documentation", "learning_style": "reading",
             "url": "https://www.bigocheatsheet.com/",
             "duration_min": 10, "difficulty": "intermediate", "provider": "Big-O Cheat Sheet", "rating": 4.7},
            {"title": "Visualgo – Algorithm Visualizations",
             "description": "Interactive visualizations of sorting, graph traversal, and data structure operations — great for visual learners.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://visualgo.net/en",
             "duration_min": 60, "difficulty": "intermediate", "provider": "Visualgo", "rating": 4.8},
        ]
    },
    {
        "match_domain": "programming",
        "match_title_contains": "System Design",
        "resources": [
            {"title": "System Design Interview – Alex Xu (Summary)",
             "description": "Video series summarizing key system design concepts: load balancing, caching, databases, and microservices.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=i7twT3x5yv8",
             "duration_min": 60, "difficulty": "advanced", "provider": "YouTube", "rating": 4.8},
            {"title": "System Design Primer – GitHub",
             "description": "The most starred system design resource on GitHub — covers scalability, CAP theorem, SQL vs NoSQL, and more.",
             "resource_type": "project", "learning_style": "reading",
             "url": "https://github.com/donnemartin/system-design-primer",
             "duration_min": 120, "difficulty": "advanced", "provider": "GitHub", "rating": 5.0},
            {"title": "Designing Data-Intensive Applications – Key Concepts",
             "description": "Article series summarizing DDIA chapters on replication, partitioning, transactions, and distributed systems.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://medium.com/tag/system-design",
             "duration_min": 45, "difficulty": "advanced", "provider": "Medium", "rating": 4.7},
            {"title": "Grokking System Design – Interactive",
             "description": "Interactive system design course with case studies: URL shortener, Twitter, Netflix, Uber, and more.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers",
             "duration_min": 480, "difficulty": "advanced", "provider": "Educative", "rating": 4.8},
        ]
    },
    {
        "match_domain": "programming",
        "match_title_contains": "Software Engineering",
        "resources": [
            {"title": "Clean Code – Key Principles Video",
             "description": "Video summary of Robert Martin's Clean Code principles: naming, functions, comments, and error handling.",
             "resource_type": "video", "learning_style": "video",
             "url": "https://www.youtube.com/watch?v=7EmboKQH8lM",
             "duration_min": 45, "difficulty": "intermediate", "provider": "YouTube", "rating": 4.7},
            {"title": "Refactoring Guru – Design Patterns",
             "description": "Beautifully illustrated guide to all 23 Gang of Four design patterns with real-world examples and code.",
             "resource_type": "article", "learning_style": "reading",
             "url": "https://refactoring.guru/design-patterns",
             "duration_min": 60, "difficulty": "intermediate", "provider": "Refactoring Guru", "rating": 4.9},
            {"title": "Git & GitHub – The Complete Guide",
             "description": "Comprehensive Git tutorial covering branching, merging, rebasing, pull requests, and team workflows.",
             "resource_type": "tutorial", "learning_style": "labs",
             "url": "https://www.atlassian.com/git/tutorials",
             "duration_min": 120, "difficulty": "intermediate", "provider": "Atlassian", "rating": 4.7},
            {"title": "Build a Well-Tested Python Project – GitHub",
             "description": "Sample project demonstrating pytest, coverage, CI with GitHub Actions, and clean architecture patterns.",
             "resource_type": "project", "learning_style": "project",
             "url": "https://github.com/navdeep-G/samplemod",
             "duration_min": 180, "difficulty": "intermediate", "provider": "GitHub", "rating": 4.5},
        ]
    },
]


def _seed_resources(db, Module, Resource):
    """
    Seed curated resources for each module based on domain + title matching.
    Called after modules are committed so module IDs are available.
    """
    if Resource.query.count() > 0:
        logger.info("Resources already seeded. Skipping.")
        return

    logger.info("🌱 Seeding resources...")
    resource_count = 0

    for template in RESOURCE_TEMPLATES:
        domain = template["match_domain"]
        title_fragment = template["match_title_contains"]

        # Find all modules that match domain and title substring
        matching_modules = Module.query.filter(
            Module.domain == domain,
            Module.title.contains(title_fragment)
        ).all()

        for module in matching_modules:
            for res_data in template["resources"]:
                resource = Resource(
                    module_id=module.id,
                    title=res_data["title"],
                    description=res_data["description"],
                    resource_type=res_data["resource_type"],
                    learning_style=res_data["learning_style"],
                    url=res_data["url"],
                    duration_min=res_data.get("duration_min"),
                    difficulty=res_data.get("difficulty", "beginner"),
                    provider=res_data.get("provider"),
                    rating=res_data.get("rating", 4.0),
                    is_external=True,
                )
                db.session.add(resource)
                resource_count += 1

    db.session.commit()
    logger.info(f"✅ Seeded {resource_count} resources across {Module.query.count()} modules")


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

        # ── Seed Resources ────────────────────────────────────────────────────
        from models.resource import Resource
        _seed_resources(db, Module, Resource)

        logger.info("🎉 Database seeding complete!")
