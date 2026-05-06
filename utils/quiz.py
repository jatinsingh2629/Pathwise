"""
utils/quiz.py - Domain-based quiz generator.
Generates 3-5 domain questions + 2-3 computer knowledge questions.
"""

import random
from typing import List, Dict, Any


# ── Computer Knowledge Questions (always included) ──────────────────────────
COMPUTER_KNOWLEDGE_QUESTIONS = [
    {
        "id": "ck1",
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Computer Personal Unit", "Central Program Utility", "Core Processing Unit"],
        "correct": 0,
        "type": "computer_knowledge"
    },
    {
        "id": "ck2",
        "question": "Which of the following is NOT a programming language?",
        "options": ["Python", "HTML", "Java", "Microsoft Word"],
        "correct": 3,
        "type": "computer_knowledge"
    },
    {
        "id": "ck3",
        "question": "What is the primary function of an operating system?",
        "options": ["Create documents", "Manage hardware and software resources", "Connect to the internet", "Store files only"],
        "correct": 1,
        "type": "computer_knowledge"
    },
    {
        "id": "ck4",
        "question": "What does RAM stand for?",
        "options": ["Read Access Memory", "Random Access Memory", "Real Application Memory", "Runtime Application Module"],
        "correct": 1,
        "type": "computer_knowledge"
    },
    {
        "id": "ck5",
        "question": "Which data structure uses LIFO (Last In, First Out)?",
        "options": ["Queue", "Stack", "Tree", "Graph"],
        "correct": 1,
        "type": "computer_knowledge"
    },
]

# ── Domain-Specific Question Banks ──────────────────────────────────────────
DOMAIN_QUESTIONS = {
    "cybersecurity": [
        {
            "id": "cy1",
            "question": "What does SQL injection attack target?",
            "options": ["Web browsers", "Database queries", "Network packets", "File systems"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cy2",
            "question": "What is the purpose of a firewall?",
            "options": ["Speed up internet", "Block unauthorized network access", "Encrypt files", "Manage passwords"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cy3",
            "question": "Which protocol is used for secure web communication?",
            "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
            "correct": 2,
            "type": "domain"
        },
        {
            "id": "cy4",
            "question": "What is a zero-day vulnerability?",
            "options": ["An old known bug", "A vulnerability with no available patch", "A network downtime", "A type of malware"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cy5",
            "question": "What does CIA triad stand for in security?",
            "options": ["Control, Integrity, Access", "Confidentiality, Integrity, Availability", "Computing, Intelligence, Analysis", "Cryptography, Intrusion, Audit"],
            "correct": 1,
            "type": "domain"
        },
    ],
    "data_science": [
        {
            "id": "ds1",
            "question": "Which Python library is primarily used for data manipulation?",
            "options": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "ds2",
            "question": "What is overfitting in machine learning?",
            "options": ["Model performs well on training and test data", "Model performs well on training but poor on test data", "Model is too simple", "Model has too little data"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "ds3",
            "question": "Which algorithm is used for classification problems?",
            "options": ["Linear regression", "K-means clustering", "Random forest", "PCA"],
            "correct": 2,
            "type": "domain"
        },
        {
            "id": "ds4",
            "question": "What does EDA stand for in data science?",
            "options": ["Enhanced Data Analysis", "Exploratory Data Analysis", "External Data Aggregation", "Evaluated Decision Algorithm"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "ds5",
            "question": "Which measure is best for skewed data distributions?",
            "options": ["Mean", "Standard deviation", "Median", "Variance"],
            "correct": 2,
            "type": "domain"
        },
    ],
    "web_development": [
        {
            "id": "wd1",
            "question": "What does HTML stand for?",
            "options": ["Hyper Text Markup Language", "High Text Machine Language", "Hyper Transfer Markup Language", "HTML Text Multiple Language"],
            "correct": 0,
            "type": "domain"
        },
        {
            "id": "wd2",
            "question": "Which CSS property controls element spacing inside the border?",
            "options": ["margin", "padding", "border-spacing", "gap"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "wd3",
            "question": "What is the purpose of RESTful APIs?",
            "options": ["Style web pages", "Enable client-server communication", "Manage databases", "Compress files"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "wd4",
            "question": "Which JavaScript framework uses a virtual DOM?",
            "options": ["Angular", "Vue", "React", "Both B and C"],
            "correct": 3,
            "type": "domain"
        },
        {
            "id": "wd5",
            "question": "What does HTTP status code 404 mean?",
            "options": ["Server error", "Resource not found", "Unauthorized access", "Redirect"],
            "correct": 1,
            "type": "domain"
        },
    ],
    "cloud_computing": [
        {
            "id": "cc1",
            "question": "What is IaaS in cloud computing?",
            "options": ["Internet as a Service", "Infrastructure as a Service", "Integration as a Service", "Information as a Service"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cc2",
            "question": "Which AWS service provides serverless compute?",
            "options": ["EC2", "S3", "Lambda", "RDS"],
            "correct": 2,
            "type": "domain"
        },
        {
            "id": "cc3",
            "question": "What is containerization?",
            "options": ["Hardware virtualization", "Packaging apps with dependencies", "Cloud storage", "Network routing"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cc4",
            "question": "What does CI/CD stand for?",
            "options": ["Cloud Integration/Cloud Deployment", "Continuous Integration/Continuous Delivery", "Code Inspection/Code Delivery", "Container Infrastructure/Container Deployment"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "cc5",
            "question": "What is Kubernetes primarily used for?",
            "options": ["Database management", "Container orchestration", "File storage", "Network security"],
            "correct": 1,
            "type": "domain"
        },
    ],
    "programming": [
        {
            "id": "pr1",
            "question": "What is Big O notation used for?",
            "options": ["Measuring code length", "Describing algorithm complexity", "Counting bugs", "Memory allocation"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "pr2",
            "question": "What is recursion?",
            "options": ["A loop structure", "A function calling itself", "A type of variable", "A database query"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "pr3",
            "question": "What does OOP stand for?",
            "options": ["Open Operational Process", "Object Oriented Programming", "Optimized Output Protocol", "Online Object Processing"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "pr4",
            "question": "What is a binary search tree?",
            "options": ["A linear data structure", "A tree where left < root < right", "A tree with exactly 2 nodes", "A circular linked list"],
            "correct": 1,
            "type": "domain"
        },
        {
            "id": "pr5",
            "question": "Which sorting algorithm has average O(n log n) complexity?",
            "options": ["Bubble sort", "Selection sort", "Merge sort", "Insertion sort"],
            "correct": 2,
            "type": "domain"
        },
    ],
}

# Default questions for unknown domains
DEFAULT_DOMAIN_QUESTIONS = DOMAIN_QUESTIONS['programming']


def get_quiz_questions(domain: str, n_domain: int = 4, n_computer: int = 3) -> List[Dict[str, Any]]:
    """
    Generate a quiz for a given domain.

    Args:
        domain: The learner's classified domain
        n_domain: Number of domain-specific questions (3-5)
        n_computer: Number of computer knowledge questions (2-3)

    Returns:
        Shuffled list of quiz questions
    """
    # Get domain questions
    domain_pool = DOMAIN_QUESTIONS.get(domain, DEFAULT_DOMAIN_QUESTIONS)
    selected_domain = random.sample(domain_pool, min(n_domain, len(domain_pool)))

    # Get computer knowledge questions
    selected_computer = random.sample(COMPUTER_KNOWLEDGE_QUESTIONS, min(n_computer, len(COMPUTER_KNOWLEDGE_QUESTIONS)))

    all_questions = selected_domain + selected_computer

    # Shuffle options for each question (keeping track of correct answer)
    for q in all_questions:
        options = list(q['options'])
        correct_text = options[q['correct']]
        random.shuffle(options)
        q['options'] = options
        q['correct'] = options.index(correct_text)

    return all_questions


def calculate_quiz_score(questions: List[Dict], answers: Dict[str, int]) -> Dict[str, Any]:
    """
    Calculate quiz score from answers.

    Args:
        questions: List of question dicts
        answers: Dict of {question_id: selected_option_index}

    Returns:
        Dict with score (0-100), correct count, total, and classification
    """
    total = len(questions)
    correct = 0

    for q in questions:
        q_id = q['id']
        user_answer = answers.get(q_id)
        if user_answer is not None and int(user_answer) == q['correct']:
            correct += 1

    score = (correct / total * 100) if total > 0 else 0
    classification = 'intermediate' if score >= 50 else 'beginner'

    return {
        'score': round(score, 1),
        'correct': correct,
        'total': total,
        'classification': classification,
        'passed': score >= 50
    }
