"""
utils/assessment_questions.py
Returns topic-relevant assessment questions based on module title keywords.
"""

# ── QUESTION BANK ──────────────────────────────────────────────────────────
# Format: list of {q, opts: [4 options], correct: int (0-indexed)}

QUESTION_BANK = {

    # ── CYBERSECURITY ────────────────────────────────────────────────────────
    "introduction cybersecurity": [
        {"q": "What is the CIA triad in cybersecurity?",
         "opts": ["Confidentiality, Integrity, Availability", "Control, Inspection, Access", "Cipher, Intrusion, Audit", "Code, Integrity, Architecture"], "correct": 0},
        {"q": "Which type of attack tricks users into revealing credentials?",
         "opts": ["DoS attack", "Phishing", "SQL injection", "Buffer overflow"], "correct": 1},
        {"q": "What does a vulnerability scanner do?",
         "opts": ["Blocks all traffic", "Identifies security weaknesses in systems", "Encrypts data", "Monitors user activity"], "correct": 1},
        {"q": "What is the purpose of multi-factor authentication (MFA)?",
         "opts": ["Speed up login", "Add extra verification layers beyond passwords", "Remove the need for passwords", "Encrypt the database"], "correct": 1},
    ],
    "network security": [
        {"q": "What does a firewall primarily do?",
         "opts": ["Speed up the network", "Monitor and filter incoming/outgoing traffic", "Encrypt all data", "Assign IP addresses"], "correct": 1},
        {"q": "What is a DMZ in network security?",
         "opts": ["A dangerous malware zone", "A subnet that exposes external-facing services", "A type of VPN", "A DoS attack method"], "correct": 1},
        {"q": "Which protocol is used to securely manage network devices remotely?",
         "opts": ["Telnet", "FTP", "SSH", "HTTP"], "correct": 2},
        {"q": "What is an IDS (Intrusion Detection System)?",
         "opts": ["A firewall replacement", "A system that monitors for malicious activity", "A VPN service", "An authentication server"], "correct": 1},
    ],
    "ethical hacking penetration": [
        {"q": "What is the first phase of a penetration test?",
         "opts": ["Exploitation", "Reconnaissance", "Reporting", "Post-exploitation"], "correct": 1},
        {"q": "Which tool is commonly used for network scanning in pen testing?",
         "opts": ["Wireshark", "Nmap", "Burp Suite", "Metasploit"], "correct": 1},
        {"q": "What does 'CVE' stand for?",
         "opts": ["Common Vulnerability Exposure", "Cyber Vulnerability Engine", "Common Vulnerabilities and Exposures", "Controlled Vulnerability Exploit"], "correct": 2},
        {"q": "What is privilege escalation?",
         "opts": ["Increasing network bandwidth", "Gaining higher access rights than intended", "Brute forcing passwords", "Scanning open ports"], "correct": 1},
    ],
    "web application security": [
        {"q": "What does XSS stand for in web security?",
         "opts": ["Extra Style Sheet", "Cross-Site Scripting", "External Source Script", "Cross-Server Security"], "correct": 1},
        {"q": "Which OWASP Top 10 item involves improper access control?",
         "opts": ["Injection", "Broken Access Control", "Security Misconfiguration", "Insecure Deserialization"], "correct": 1},
        {"q": "What is a CSRF attack?",
         "opts": ["Intercepting network packets", "Forcing a user to execute unwanted actions on a trusted site", "Injecting SQL queries", "Cracking passwords"], "correct": 1},
        {"q": "How does parameterized query prevent SQL injection?",
         "opts": ["By encrypting the database", "By separating code from user input data", "By blocking all input fields", "By logging all queries"], "correct": 1},
    ],
    "malware analysis": [
        {"q": "What is static malware analysis?",
         "opts": ["Running malware in a sandbox", "Examining malware without executing it", "Monitoring network traffic", "Blocking malware signatures"], "correct": 1},
        {"q": "What is a rootkit?",
         "opts": ["An antivirus tool", "Malware that hides its presence on a system", "A network scanner", "A firewall rule set"], "correct": 1},
        {"q": "Which tool is used for dynamic malware analysis?",
         "opts": ["IDA Pro", "Cuckoo Sandbox", "Wireshark", "Nessus"], "correct": 1},
        {"q": "What does ransomware typically do?",
         "opts": ["Steals passwords silently", "Encrypts files and demands payment", "Slows down the network", "Creates fake accounts"], "correct": 1},
    ],
    "cryptography": [
        {"q": "What is the difference between symmetric and asymmetric encryption?",
         "opts": ["Symmetric uses two keys; asymmetric uses one", "Symmetric uses one shared key; asymmetric uses a key pair", "They are the same", "Symmetric is stronger than asymmetric"], "correct": 1},
        {"q": "What does a hash function produce?",
         "opts": ["An encrypted message", "A fixed-length digest of input data", "A digital signature", "A public key"], "correct": 1},
        {"q": "What is the purpose of TLS?",
         "opts": ["Speed up web traffic", "Encrypt communication between client and server", "Assign domain names", "Block malicious traffic"], "correct": 1},
        {"q": "What is a digital certificate used for?",
         "opts": ["Storing passwords", "Verifying the identity of a public key owner", "Encrypting files locally", "Generating random numbers"], "correct": 1},
    ],

    # ── DATA SCIENCE ─────────────────────────────────────────────────────────
    "python data science": [
        {"q": "Which Python library provides the DataFrame data structure?",
         "opts": ["NumPy", "Pandas", "Matplotlib", "SciPy"], "correct": 1},
        {"q": "What does `df.dropna()` do in Pandas?",
         "opts": ["Drops duplicate rows", "Removes rows with missing values", "Resets the index", "Sorts the DataFrame"], "correct": 1},
        {"q": "What is NumPy primarily used for?",
         "opts": ["Web development", "Numerical computation with arrays", "Database management", "File I/O operations"], "correct": 1},
        {"q": "What does vectorization mean in NumPy?",
         "opts": ["Converting text to numbers", "Applying operations to entire arrays without loops", "Normalizing data", "Creating visualizations"], "correct": 1},
    ],
    "data analysis visualization": [
        {"q": "What type of plot is best for showing data distribution?",
         "opts": ["Bar chart", "Histogram", "Scatter plot", "Pie chart"], "correct": 1},
        {"q": "What does correlation measure?",
         "opts": ["The difference between two variables", "The linear relationship between two variables", "The mean of a dataset", "The outliers in data"], "correct": 1},
        {"q": "What is an outlier in a dataset?",
         "opts": ["The most common value", "A data point significantly different from others", "The median value", "A missing value"], "correct": 1},
        {"q": "What does EDA stand for?",
         "opts": ["Enhanced Data Architecture", "Exploratory Data Analysis", "External Data Aggregation", "Evaluated Data Algorithm"], "correct": 1},
    ],
    "machine learning": [
        {"q": "What is the difference between supervised and unsupervised learning?",
         "opts": ["Speed of training", "Supervised uses labeled data; unsupervised finds patterns without labels", "Supervised is always better", "Unsupervised uses more data"], "correct": 1},
        {"q": "What is overfitting?",
         "opts": ["Model is too simple", "Model learns training data too well and fails on new data", "Model has too many features removed", "Model trains too slowly"], "correct": 1},
        {"q": "What is cross-validation used for?",
         "opts": ["Training faster", "Estimating model performance on unseen data", "Feature selection", "Reducing dimensionality"], "correct": 1},
        {"q": "What does a confusion matrix show?",
         "opts": ["Training loss over epochs", "True vs predicted classification results", "Feature importance", "Correlation between features"], "correct": 1},
    ],
    "deep learning neural": [
        {"q": "What is the role of an activation function in a neural network?",
         "opts": ["Initialize weights", "Introduce non-linearity into the network", "Normalize input data", "Select features"], "correct": 1},
        {"q": "What does backpropagation do?",
         "opts": ["Generates predictions", "Calculates gradients to update network weights", "Normalizes batch data", "Adds layers to the network"], "correct": 1},
        {"q": "What is dropout in deep learning?",
         "opts": ["Removing input features", "Randomly deactivating neurons during training to reduce overfitting", "Reducing learning rate", "Removing outliers"], "correct": 1},
        {"q": "What type of neural network is best suited for image recognition?",
         "opts": ["RNN", "CNN (Convolutional Neural Network)", "Autoencoder", "Transformer"], "correct": 1},
    ],
    "natural language processing": [
        {"q": "What is tokenization in NLP?",
         "opts": ["Encrypting text", "Splitting text into words or subwords", "Translating text", "Compressing text files"], "correct": 1},
        {"q": "What does TF-IDF measure?",
         "opts": ["Text formatting", "How important a word is in a document relative to a corpus", "Translation frequency", "Typing speed"], "correct": 1},
        {"q": "What is the purpose of word embeddings like Word2Vec?",
         "opts": ["Encrypt words", "Represent words as dense numerical vectors capturing meaning", "Count word frequency", "Remove stop words"], "correct": 1},
        {"q": "What is the attention mechanism in transformers?",
         "opts": ["A memory management technique", "A method to weigh the importance of different tokens", "A dropout technique", "A normalization method"], "correct": 1},
    ],

    # ── WEB DEVELOPMENT ──────────────────────────────────────────────────────
    "html css": [
        {"q": "What does the CSS `box-model` consist of?",
         "opts": ["Color, font, border", "Content, padding, border, margin", "Width, height, position", "Display, visibility, overflow"], "correct": 1},
        {"q": "What is the purpose of semantic HTML tags like `<article>` and `<section>`?",
         "opts": ["Add styling", "Provide meaning and structure to content", "Speed up page load", "Create animations"], "correct": 1},
        {"q": "What does CSS Flexbox primarily help with?",
         "opts": ["Animations", "One-dimensional layout alignment", "Typography", "Color gradients"], "correct": 1},
        {"q": "What is responsive design?",
         "opts": ["Fast-loading websites", "Design that adapts to different screen sizes", "Interactive animations", "Dark mode support"], "correct": 1},
    ],
    "javascript": [
        {"q": "What is the difference between `let` and `var` in JavaScript?",
         "opts": ["No difference", "`let` has block scope; `var` has function scope", "`var` is newer than `let`", "`let` is only for numbers"], "correct": 1},
        {"q": "What does `async/await` do in JavaScript?",
         "opts": ["Makes code run faster", "Handles asynchronous operations in a synchronous-like syntax", "Creates threads", "Replaces callbacks entirely"], "correct": 1},
        {"q": "What is the DOM?",
         "opts": ["A JavaScript framework", "Document Object Model — a tree representation of the HTML page", "A CSS preprocessor", "A server-side language"], "correct": 1},
        {"q": "What does the `Promise` object represent?",
         "opts": ["A guaranteed function return", "A value that may be available now, later, or never", "A class constructor", "A loop structure"], "correct": 1},
    ],
    "react": [
        {"q": "What is a React component?",
         "opts": ["A CSS class", "A reusable UI building block", "A database model", "A server route"], "correct": 1},
        {"q": "What does `useState` hook do?",
         "opts": ["Fetches data from an API", "Adds local state to a functional component", "Manages routing", "Connects to a database"], "correct": 1},
        {"q": "What is the virtual DOM in React?",
         "opts": ["A hidden HTML element", "A lightweight in-memory representation of the real DOM", "A CSS framework", "A server-side renderer"], "correct": 1},
        {"q": "What is the purpose of `useEffect`?",
         "opts": ["Style components", "Handle side effects like API calls and subscriptions", "Create animations", "Define routes"], "correct": 1},
    ],
    "node express backend": [
        {"q": "What is Node.js?",
         "opts": ["A front-end framework", "A JavaScript runtime built on Chrome's V8 engine", "A database system", "A CSS preprocessor"], "correct": 1},
        {"q": "What is middleware in Express.js?",
         "opts": ["A database connector", "A function that processes requests before reaching route handlers", "A frontend library", "A template engine"], "correct": 1},
        {"q": "What does REST stand for?",
         "opts": ["Remote Execution Service Technology", "Representational State Transfer", "Reliable Endpoint Service Transfer", "Resource Execution Syntax Tree"], "correct": 1},
        {"q": "What HTTP method is typically used to update a resource?",
         "opts": ["GET", "POST", "PUT/PATCH", "DELETE"], "correct": 2},
    ],

    # ── CLOUD COMPUTING ──────────────────────────────────────────────────────
    "cloud computing concepts": [
        {"q": "What is the difference between IaaS and PaaS?",
         "opts": ["No difference", "IaaS provides infrastructure; PaaS provides a development platform", "PaaS provides hardware; IaaS provides software", "They are the same service"], "correct": 1},
        {"q": "What is cloud elasticity?",
         "opts": ["Data encryption in the cloud", "Ability to scale resources up or down on demand", "Cloud backup frequency", "Network latency management"], "correct": 1},
        {"q": "What is a hybrid cloud?",
         "opts": ["A very fast cloud", "A combination of public and private cloud environments", "A cloud for mobile apps only", "A free cloud service"], "correct": 1},
        {"q": "What is the main benefit of cloud computing over on-premise?",
         "opts": ["Always faster", "Reduced upfront capital expenditure and on-demand scalability", "More secure always", "No internet required"], "correct": 1},
    ],
    "aws": [
        {"q": "What is Amazon EC2?",
         "opts": ["A database service", "A virtual server in the AWS cloud", "A storage bucket", "A DNS service"], "correct": 1},
        {"q": "What is Amazon S3 used for?",
         "opts": ["Running virtual machines", "Object storage for files and data", "Managing DNS", "Load balancing"], "correct": 1},
        {"q": "What is AWS Lambda?",
         "opts": ["A database service", "A serverless compute service that runs code on demand", "A VPN service", "A monitoring tool"], "correct": 1},
        {"q": "What is an AWS VPC?",
         "opts": ["A storage service", "A virtual private cloud — isolated network environment in AWS", "A compute instance type", "A CDN service"], "correct": 1},
    ],
    "docker kubernetes": [
        {"q": "What is a Docker container?",
         "opts": ["A virtual machine", "A lightweight isolated environment with app and dependencies", "A cloud server", "A database instance"], "correct": 1},
        {"q": "What is the purpose of a Dockerfile?",
         "opts": ["Store container data", "Define instructions to build a Docker image", "Monitor container health", "Connect containers to networks"], "correct": 1},
        {"q": "What does Kubernetes orchestrate?",
         "opts": ["Virtual machines", "Containers across multiple hosts", "Database clusters", "Network packets"], "correct": 1},
        {"q": "What is a Kubernetes Pod?",
         "opts": ["A storage volume", "The smallest deployable unit containing one or more containers", "A load balancer", "A configuration file"], "correct": 1},
    ],
    "devops": [
        {"q": "What is CI/CD?",
         "opts": ["Cloud Infrastructure/Cloud Deployment", "Continuous Integration/Continuous Delivery", "Code Inspection/Code Distribution", "Container Images/Container Deployment"], "correct": 1},
        {"q": "What is Infrastructure as Code (IaC)?",
         "opts": ["Writing code inside cloud consoles", "Managing infrastructure through machine-readable configuration files", "A monitoring technique", "A deployment strategy"], "correct": 1},
        {"q": "What is the purpose of a load balancer?",
         "opts": ["Encrypt traffic", "Distribute incoming traffic across multiple servers", "Back up data", "Scan for vulnerabilities"], "correct": 1},
        {"q": "What does monitoring in DevOps involve?",
         "opts": ["Writing tests", "Tracking application performance, logs, and alerts in real time", "Code reviews", "Database backups"], "correct": 1},
    ],

    # ── PROGRAMMING ─────────────────────────────────────────────────────────
    "programming fundamentals python": [
        {"q": "What is a function in programming?",
         "opts": ["A variable type", "A reusable block of code that performs a specific task", "A loop structure", "A class definition"], "correct": 1},
        {"q": "What is the difference between a list and a tuple in Python?",
         "opts": ["No difference", "Lists are mutable; tuples are immutable", "Tuples hold more data", "Lists are faster"], "correct": 1},
        {"q": "What does `OOP` stand for?",
         "opts": ["Open Operational Process", "Object Oriented Programming", "Optimized Output Protocol", "Online Object Processing"], "correct": 1},
        {"q": "What is a dictionary in Python?",
         "opts": ["An ordered list", "A key-value pair data structure", "A class method", "A loop iterator"], "correct": 1},
    ],
    "data structures algorithms": [
        {"q": "What is the time complexity of binary search?",
         "opts": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "correct": 1},
        {"q": "What data structure does a queue follow?",
         "opts": ["LIFO", "FIFO (First In First Out)", "Random access", "Priority-based"], "correct": 1},
        {"q": "What is a hash table?",
         "opts": ["A sorted array", "A data structure that maps keys to values using a hash function", "A type of tree", "A linked list variant"], "correct": 1},
        {"q": "What is dynamic programming?",
         "opts": ["Programming with dynamic typing", "Breaking problems into overlapping subproblems and caching solutions", "Using dynamic libraries", "Runtime code generation"], "correct": 1},
    ],
    "system design": [
        {"q": "What is horizontal scaling?",
         "opts": ["Making a single server more powerful", "Adding more servers to distribute load", "Increasing database storage", "Upgrading network speed"], "correct": 1},
        {"q": "What is a CDN?",
         "opts": ["A database type", "A network of servers that delivers content from locations close to users", "A coding language", "A security protocol"], "correct": 1},
        {"q": "What is database sharding?",
         "opts": ["Encrypting database tables", "Splitting a database into smaller pieces distributed across servers", "Creating database backups", "Indexing large tables"], "correct": 1},
        {"q": "What is the CAP theorem?",
         "opts": ["A security model", "A distributed system can only guarantee 2 of: Consistency, Availability, Partition tolerance", "A network protocol", "A caching strategy"], "correct": 1},
    ],
    "software engineering": [
        {"q": "What does the SOLID principle stand for?",
         "opts": ["A security framework", "5 design principles: Single responsibility, Open/closed, Liskov, Interface, Dependency", "A testing methodology", "A deployment strategy"], "correct": 1},
        {"q": "What is a design pattern?",
         "opts": ["A UI template", "A reusable solution to a commonly occurring software design problem", "A coding style guide", "A database schema"], "correct": 1},
        {"q": "What is the purpose of unit testing?",
         "opts": ["Test the full application end to end", "Test individual components/functions in isolation", "Test performance under load", "Test UI interactions"], "correct": 1},
        {"q": "What is technical debt?",
         "opts": ["Cost of cloud services", "Cost of shortcuts taken in development that need future rework", "Software licensing fees", "Database storage cost"], "correct": 1},
    ],

    # ── DEFAULT (fallback) ────────────────────────────────────────────────────
    "default": [
        {"q": "What was the main concept covered in this module?",
         "opts": ["Theory only", "Practical skills only", "Both theoretical concepts and practical application", "Neither"], "correct": 2},
        {"q": "Which learning approach best describes this module?",
         "opts": ["Memorization", "Critical thinking and application", "Observation only", "Trial and error without guidance"], "correct": 1},
        {"q": "What is the best way to retain knowledge from this module?",
         "opts": ["Read once and move on", "Practice applying concepts regularly", "Memorize all terms", "Skip to the next module"], "correct": 1},
        {"q": "How does this module connect to your overall learning goal?",
         "opts": ["It is unrelated", "It builds a foundational or advanced skill in your domain", "It covers a different domain entirely", "It only covers theory"], "correct": 1},
    ],
}


def get_questions_for_module(module_title: str, module_domain: str = '', n: int = 4) -> list:
    """
    Return topic-relevant assessment questions for a module.
    Matches module title keywords against the question bank.
    Falls back to domain-level, then default questions.
    """
    title_lower = module_title.lower()
    domain_lower = (module_domain or '').lower().replace('_', ' ')

    # Try to find a matching question set by scanning title keywords
    best_key = None
    best_score = 0

    for key in QUESTION_BANK:
        if key == 'default':
            continue
        keywords = key.split()
        score = sum(1 for kw in keywords if kw in title_lower)
        if score > best_score:
            best_score = score
            best_key = key

    # If no title match, try domain
    if best_score == 0:
        for key in QUESTION_BANK:
            if key == 'default':
                continue
            keywords = key.split()
            score = sum(1 for kw in keywords if kw in domain_lower)
            if score > best_score:
                best_score = score
                best_key = key

    questions = QUESTION_BANK.get(best_key or 'default', QUESTION_BANK['default'])

    import random
    selected = random.sample(questions, min(n, len(questions)))
    return selected