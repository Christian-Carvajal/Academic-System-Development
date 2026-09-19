"""
curriculum_catalog.py
Pre-configured curriculum catalog containing official 3rd-Year Computer Science
courses from the College of Computer Studies (UPHSD Molino).
Enables zero-manual-typing automated 1-click syllabus generation.
"""
from typing import Dict, List, Any, Optional

CURRICULUM_SUBJECTS: Dict[str, Dict[str, Any]] = {
    "BSCS 3112": {
        "course_code": "BSCS 3112",
        "course_title": "Artificial Intelligence",
        "semester": "3rd Year, 1st Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "CS 3110 (Data Structures and Algorithms)",
        "icon": "🤖",
        "category": "Core Specialization",
        "course_description": (
            "Foundational and modern principles of artificial intelligence, including intelligent agents, "
            "state-space search heuristics (A*, Minimax), knowledge representation, first-order logic, "
            "probabilistic reasoning, machine learning pipelines, deep neural networks, computer vision, "
            "natural language processing, and ethical considerations in autonomous systems."
        ),
        "target_pos": [
            "PLO 1 (Analyze complex computing problems and apply principles of computing)",
            "PLO 2 (Design, implement, and evaluate computing-based solutions)",
            "PLO 3 (Communicate effectively in a variety of professional contexts)",
            "PLO 5 (Apply computer science theory and software development fundamentals)"
        ]
    },
    "BSCS 3108": {
        "course_code": "BSCS 3108",
        "course_title": "Automata Theory and Formal Languages",
        "semester": "3rd Year, 1st Sem",
        "credit_units": 3,
        "lecture_hours": 3,
        "lab_hours": 0,
        "prerequisites": "CS 2106 (Discrete Mathematics)",
        "icon": "⚙️",
        "category": "Theoretical Computer Science",
        "course_description": (
            "Rigorous theoretical exploration of computational models and formal grammars, covering regular "
            "expressions, deterministic and non-deterministic finite automata (DFA/NFA), context-free grammars, "
            "pushdown automata, Turing machines, decidability, the Halting problem, and the Chomsky hierarchy."
        ),
        "target_pos": [
            "PLO 1 (Analyze complex computing problems and apply principles of computing)",
            "PLO 5 (Apply computer science theory and software development fundamentals)"
        ]
    },
    "BSCS 3109": {
        "course_code": "BSCS 3109",
        "course_title": "Operating System Configuration and Use",
        "semester": "3rd Year, 1st Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "CS 2108 (Computer Architecture and Organization)",
        "icon": "🖥️",
        "category": "Systems Infrastructure",
        "course_description": (
            "Comprehensive study of operating system architectures and system configuration, encompassing "
            "process scheduling, multithreading, concurrency synchronization, deadlock avoidance, memory "
            "virtualization, paging, file system structures, device management, and hands-on Linux/Unix shell administration."
        ),
        "target_pos": [
            "PLO 1 (Analyze complex computing problems)",
            "PLO 2 (Design, implement, and evaluate computing-based solutions)",
            "PLO 5 (Apply systems theory and software development fundamentals)"
        ]
    },
    "BSCS 3110": {
        "course_code": "BSCS 3110",
        "course_title": "Information Assurance and Security",
        "semester": "3rd Year, 1st Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "CS 2207 (Data Communications and Networking)",
        "icon": "🔒",
        "category": "Cybersecurity & Governance",
        "course_description": (
            "Core principles of cybersecurity and information assurance, focusing on the CIA triad "
            "(Confidentiality, Integrity, Availability), symmetric and asymmetric cryptography, public key "
            "infrastructure (PKI), secure network architectures, threat modeling, vulnerability assessment, "
            "intrusion detection systems, and institutional security governance."
        ),
        "target_pos": [
            "PLO 1 (Analyze computing problems and apply cybersecurity fundamentals)",
            "PLO 4 (Recognize professional responsibilities and make informed judgments in computing practice)",
            "PLO 5 (Apply security theory to system design)"
        ]
    },
    "BSCS 3111": {
        "course_code": "BSCS 3111",
        "course_title": "Data Mining",
        "semester": "3rd Year, 1st Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "CS 3112 (Database Systems 1)",
        "icon": "📊",
        "category": "Data Science & Analytics",
        "course_description": (
            "Principles, algorithms, and applications of knowledge discovery in databases (KDD), including "
            "data cleaning and preprocessing, exploratory data analysis, ETL pipelines, association rule mining "
            "(Apriori, FP-Growth), classification algorithms (Decision Trees, Naive Bayes, SVM), clustering "
            "techniques (K-Means, DBSCAN), and evaluation metrics."
        ),
        "target_pos": [
            "PLO 1 (Apply principles of computing and mathematics to data analysis)",
            "PLO 2 (Design and implement analytical data-driven models)",
            "PLO 5 (Apply computer science theory to large-scale data extraction)"
        ]
    },
    "BSCS 3213": {
        "course_code": "BSCS 3213",
        "course_title": "Software Engineering",
        "semester": "3rd Year, 2nd Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "CS 3110 (Data Structures and Algorithms)",
        "icon": "🏗️",
        "category": "Software Architecture",
        "course_description": (
            "Systematic engineering methodologies for software development, covering SDLC models, Agile/Scrum "
            "frameworks, requirements engineering, object-oriented analysis and design with UML, architectural patterns, "
            "unit and integration testing, continuous integration and deployment (CI/CD), and software project management."
        ),
        "target_pos": [
            "PLO 2 (Design, implement, and evaluate computing-based solutions)",
            "PLO 3 (Communicate effectively in professional development teams)",
            "PLO 5 (Apply software development fundamentals and engineering best practices)"
        ]
    },
    "BSCS 3214": {
        "course_code": "BSCS 3214",
        "course_title": "Data Visualization",
        "semester": "3rd Year, 2nd Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "BSCS 3111 (Data Mining)",
        "icon": "📈",
        "category": "Visual Analytics",
        "course_description": (
            "Theories and hands-on practices of visual data analytics and graphical storytelling, including "
            "visual perception cognition, the Grammar of Graphics, interactive dashboard construction, "
            "exploratory plotting with modern tools (Plotly, D3.js, Seaborn), multidimensional and geospatial "
            "visualization, and effective communication of data insights."
        ),
        "target_pos": [
            "PLO 2 (Design and implement visual computing interfaces)",
            "PLO 3 (Communicate complex quantitative findings effectively)",
            "PLO 5 (Apply computer science theory and visual representation standards)"
        ]
    },
    "BSCS 3215": {
        "course_code": "BSCS 3215",
        "course_title": "Parallel and Distributed Computing",
        "semester": "3rd Year, 2nd Sem",
        "credit_units": 3,
        "lecture_hours": 2,
        "lab_hours": 3,
        "prerequisites": "BSCS 3109 (Operating System Configuration and Use)",
        "icon": "⚡",
        "category": "High-Performance Computing",
        "course_description": (
            "Foundational principles and architectures of concurrent, parallel, and distributed computing systems. "
            "Topics encompass Flynn's taxonomy, shared-memory programming (OpenMP/pthreads), distributed-memory "
            "message passing (MPI), massively parallel GPU programming (CUDA), distributed consensus algorithms, "
            "cloud cluster parallelism, and performance scalability metrics."
        ),
        "target_pos": [
            "PLO 1 (Analyze complex computing problems and evaluate parallel algorithm scalability)",
            "PLO 2 (Design and implement high-performance parallel solutions)",
            "PLO 5 (Apply computer science theory and distributed computing fundamentals)"
        ]
    }
}


def get_all_subjects() -> List[Dict[str, Any]]:
    """Returns a list of all 8 official curriculum subjects."""
    return list(CURRICULUM_SUBJECTS.values())


def get_subject(course_code: str) -> Optional[Dict[str, Any]]:
    """Finds and returns subject metadata by course code (case-insensitive & whitespace tolerant)."""
    norm = course_code.strip().upper().replace("_", " ").replace("-", " ")
    for code, data in CURRICULUM_SUBJECTS.items():
        if code.upper() == norm:
            return data
    # Partial match
    for code, data in CURRICULUM_SUBJECTS.items():
        if norm in code.upper() or code.upper() in norm:
            return data
    return None
