# frontend/shared/data/mock_data.py
"""
Mock data generators for EduTrack IA
Generates realistic Moroccan educational data for demo purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path

# Moroccan student names (mix of Arabic and French influenced names)
FIRST_NAMES = [
    "Youssef", "Fatima", "Mohamed", "Aisha", "Hassan", "Zineb", "Omar", "Salma",
    "Amine", "Nour", "Karim", "Leila", "Adam", "Sarah", "Mehdi", "Amina",
    "Hamza", "Khadija", "Rayan", "Meryem", "Imane", "Ayoub", "Hiba", "Bilal",
    "Yasmine", "Othmane", "Sofia", "Ismail", "Dounia", "Zakaria"
]

LAST_NAMES = [
    "Alami", "Benali", "Chakir", "Dahbi", "El Fassi", "Fahmi", "Ghazi", "Hilal",
    "Idrissi", "Jalil", "Kabbaj", "Lamrani", "Mansouri", "Naciri", "Ouazzani",
    "Qadiri", "Rachidi", "Saidi", "Tazi", "Wahbi", "Yacoubi", "Zarrouki"
]

# Moroccan educational system classes
CLASSES = [
    "1ère année collège", "2ème année collège", "3ème année collège",
    "Tronc Commun", "1ère Bac Sciences", "1ère Bac Lettres",
    "2ème Bac Sciences Math", "2ème Bac Sciences Physiques", "2ème Bac Lettres"
]

# Subjects by category
SUBJECTS = {
    "Sciences": ["Mathématiques", "Physique-Chimie", "SVT"],
    "Langues": ["Arabe", "Français", "Anglais"],
    "Humanités": ["Histoire-Géographie", "Philosophie", "Éducation Islamique"],
    "Techniques": ["Informatique", "Sciences de l'Ingénieur"]
}

# Competencies by subject
COMPETENCIES = {
    "Mathématiques": [
        "Algèbre - Résolution d'équations",
        "Géométrie - Théorèmes et démonstrations",
        "Analyse - Dérivées et primitives",
        "Statistiques et probabilités"
    ],
    "Physique-Chimie": [
        "Mécanique - Lois du mouvement",
        "Électricité - Circuits et lois",
        "Chimie - Réactions et équilibres",
        "Optique et ondes"
    ],
    "SVT": [
        "Biologie cellulaire",
        "Génétique et hérédité",
        "Écologie et environnement",
        "Physiologie humaine"
    ],
    "Arabe": [
        "Compréhension de texte",
        "Expression écrite",
        "Grammaire et conjugaison",
        "Littérature arabe"
    ],
    "Français": [
        "Compréhension de texte",
        "Expression écrite",
        "Grammaire et orthographe",
        "Littérature française"
    ],
    "Anglais": [
        "Reading comprehension",
        "Writing skills",
        "Grammar and vocabulary",
        "Oral communication"
    ],
    "Histoire-Géographie": [
        "Histoire contemporaine",
        "Géographie économique",
        "Analyse de documents",
        "Méthodologie dissertation"
    ],
    "Philosophie": [
        "Problématisation",
        "Argumentation",
        "Analyse conceptuelle",
        "Dissertation philosophique"
    ],
    "Éducation Islamique": [
        "Compréhension des textes religieux",
        "Éthique et morale",
        "Histoire islamique",
        "Culture religieuse"
    ],
    "Informatique": [
        "Algorithmique",
        "Programmation Python",
        "Bases de données",
        "Réseaux et Internet"
    ]
}

# Evaluation types
EVALUATION_TYPES = ["contrôle", "test blanc", "exercice", "devoir maison"]

# Observation categories
OBSERVATION_CATEGORIES = ["comportement", "progrès", "difficulté"]


def generate_students(n=50):
    """Generate mock student data"""
    students = []
    
    for i in range(n):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        class_name = random.choice(CLASSES)
        
        # Generate birth date based on class level
        if "collège" in class_name:
            age = random.randint(12, 15)
        else:
            age = random.randint(15, 18)
        
        birth_date = datetime.now() - timedelta(days=age*365 + random.randint(0, 364))
        
        # Generate parent phone (Moroccan format)
        parent_phone = f"+212 6{random.randint(10000000, 99999999)}"
        parent_email = f"{first_name.lower()}.parent@gmail.com"
        
        students.append({
            "id": f"STU{i+1:04d}",
            "first_name": first_name,
            "last_name": last_name,
            "class_name": class_name,
            "date_of_birth": birth_date.strftime("%Y-%m-%d"),
            "parent_phone": parent_phone,
            "parent_email": parent_email,
            "is_active": random.choice([True] * 19 + [False]),  # 95% active
            "created_at": (datetime.now() - timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return pd.DataFrame(students)


def generate_competencies():
    """Generate competency framework"""
    competencies = []
    comp_id = 1
    
    for subject, comps in COMPETENCIES.items():
        # Determine subject category
        category = None
        for cat, subjects in SUBJECTS.items():
            if subject in subjects:
                category = cat
                break
        
        for comp_name in comps:
            competencies.append({
                "id": f"COMP{comp_id:04d}",
                "name": comp_name,
                "subject": subject,
                "category": category,
                "level": random.choice(["Fondamental", "Intermédiaire", "Avancé"]),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            comp_id += 1
    
    return pd.DataFrame(competencies)


def generate_grades(students_df, competencies_df, grades_per_student=20):
    """Generate mock grades for students"""
    grades = []
    grade_id = 1
    
    for _, student in students_df.iterrows():
        # Determine student performance profile
        profile = random.choices(
            ["excellent", "good", "average", "struggling", "improving", "declining"],
            weights=[0.1, 0.25, 0.35, 0.15, 0.10, 0.05]
        )[0]
        
        # Base grade depends on profile
        base_grades = {
            "excellent": (16, 20),
            "good": (14, 17),
            "average": (10, 14),
            "struggling": (5, 10),
            "improving": (8, 16),  # wide range
            "declining": (6, 14)   # wide range
        }
        
        min_grade, max_grade = base_grades[profile]
        
        # Generate grades over time
        for i in range(grades_per_student):
            competency = competencies_df.sample(1).iloc[0]
            
            # Calculate grade with some randomness
            if profile == "improving":
                # Grades improve over time
                trend_factor = (i / grades_per_student) * 8  # up to +8 points
                base_value = min_grade + trend_factor
            elif profile == "declining":
                # Grades decline over time
                trend_factor = (i / grades_per_student) * -6  # up to -6 points
                base_value = max_grade + trend_factor
            else:
                base_value = random.uniform(min_grade, max_grade)
            
            # Add small random variation
            value = base_value + random.uniform(-1.5, 1.5)
            value = max(0, min(20, value))  # Clamp to 0-20
            value = round(value * 2) / 2  # Round to nearest 0.5
            
            # Generate evaluation date (last 6 months)
            eval_date = datetime.now() - timedelta(days=random.randint(1, 180))
            
            grades.append({
                "id": f"GRD{grade_id:05d}",
                "student_id": student["id"],
                "competency_id": competency["id"],
                "competency_name": competency["name"],
                "subject": competency["subject"],
                "value": value,
                "evaluation_type": random.choice(EVALUATION_TYPES),
                "evaluation_date": eval_date.strftime("%Y-%m-%d"),
                "created_at": eval_date.strftime("%Y-%m-%d %H:%M:%S")
            })
            grade_id += 1
    
    df = pd.DataFrame(grades)
    # Sort by evaluation date
    df = df.sort_values("evaluation_date")
    return df


def generate_observations(students_df, n_per_student=3):
    """Generate teacher observations"""
    observations = []
    obs_id = 1
    
    # Templates for observations
    obs_templates = {
        "comportement": [
            "Élève très attentif et participatif en classe.",
            "Manque parfois de concentration, facilement distrait.",
            "Excellent comportement, toujours respectueux.",
            "A besoin d'encouragements pour participer activement.",
            "Très motivé, pose des questions pertinentes."
        ],
        "progrès": [
            "Progrès remarquables depuis le début du trimestre.",
            "Amélioration constante de la méthodologie.",
            "Excellente évolution dans la compréhension des concepts.",
            "Progrès lents mais réguliers, persévérant.",
            "A bien assimilé les derniers chapitres."
        ],
        "difficulté": [
            "Difficultés persistantes en résolution de problèmes.",
            "Besoin de renforcement sur les bases.",
            "Manque de rigueur dans la rédaction.",
            "Problèmes de méthode à corriger.",
            "Lacunes importantes à combler rapidement."
        ]
    }
    
    teacher_names = ["M. Alaoui", "Mme Benjelloun", "M. Chraibi", "Mme Douiri", "M. El Alami"]
    
    for _, student in students_df.iterrows():
        for _ in range(n_per_student):
            category = random.choice(OBSERVATION_CATEGORIES)
            content = random.choice(obs_templates[category])
            obs_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            observations.append({
                "id": f"OBS{obs_id:05d}",
                "student_id": student["id"],
                "teacher_name": random.choice(teacher_names),
                "content": content,
                "category": category,
                "observation_date": obs_date.strftime("%Y-%m-%d"),
                "created_at": obs_date.strftime("%Y-%m-%d %H:%M:%S")
            })
            obs_id += 1
    
    return pd.DataFrame(observations)


def generate_reports(students_df):
    """Generate sample report data"""
    reports = []
    report_id = 1
    
    for _, student in students_df.iterrows():
        # Generate 2-3 reports per student
        for i in range(random.randint(2, 3)):
            report_date = datetime.now() - timedelta(days=random.randint(7, 120))
            
            reports.append({
                "id": f"RPT{report_id:05d}",
                "student_id": student["id"],
                "student_name": f"{student['first_name']} {student['last_name']}",
                "generated_date": report_date.strftime("%Y-%m-%d"),
                "period": f"Séance du {report_date.strftime('%d/%m/%Y')}",
                "status": "sent"
            })
            report_id += 1
    
    return pd.DataFrame(reports)


def classify_grade(value):
    """Classify grade into mastery levels"""
    if value >= 14:
        return {"level": "maîtrisée", "color": "green", "emoji": "🟢"}
    elif value >= 10:
        return {"level": "en cours", "color": "orange", "emoji": "🟡"}
    else:
        return {"level": "à renforcer", "color": "red", "emoji": "🔴"}


def calculate_trend(grades_series):
    """Calculate grade trend (recent vs previous period)"""
    if len(grades_series) < 4:
        return "stable"
    
    mid_point = len(grades_series) // 2
    previous_avg = grades_series[:mid_point].mean()
    recent_avg = grades_series[mid_point:].mean()
    
    trend_value = recent_avg - previous_avg
    
    if trend_value > 2:
        return "amélioration"
    elif trend_value < -2:
        return "régression"
    else:
        return "stable"


def _load_samples_data():
    """Load CSV samples when available and normalize required columns."""
    samples_dir = Path(__file__).resolve().parent / "samples"
    students_path = samples_dir / "students.csv"
    grades_path = samples_dir / "grades.csv"
    competencies_path = samples_dir / "competencies.csv"

    if not (
        students_path.exists()
        and grades_path.exists()
        and competencies_path.exists()
    ):
        return None

    students = pd.read_csv(students_path)
    grades = pd.read_csv(grades_path)
    competencies = pd.read_csv(competencies_path)

    # Ensure downstream pages have expected columns.
    if "is_active" not in students.columns:
        students["is_active"] = True
    if "created_at" not in students.columns:
        students["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if "created_at" not in grades.columns:
        grades["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if "evaluation_date" in grades.columns:
        grades["evaluation_date"] = pd.to_datetime(
            grades["evaluation_date"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    if "created_at" not in competencies.columns:
        competencies["created_at"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    observations = generate_observations(students)
    reports = generate_reports(students)

    return {
        "students": students,
        "competencies": competencies,
        "grades": grades,
        "observations": observations,
        "reports": reports,
    }


def get_all_mock_data(prefer_samples=True):
    """Return app data, preferring CSV samples when available."""
    if prefer_samples:
        sample_data = _load_samples_data()
        if sample_data is not None:
            return sample_data

    students = generate_students(50)
    competencies = generate_competencies()
    grades = generate_grades(students, competencies)
    observations = generate_observations(students)
    reports = generate_reports(students)

    return {
        "students": students,
        "competencies": competencies,
        "grades": grades,
        "observations": observations,
        "reports": reports,
    }


_DATA_CACHE = None


def _ensure_data_cache():
    """Load demo data once per process so IDs stay consistent across calls."""
    global _DATA_CACHE
    if _DATA_CACHE is None:
        _DATA_CACHE = get_all_mock_data()
    return _DATA_CACHE


def get_students():
    """Return student records formatted for parent-view pages."""
    students_df = _ensure_data_cache()["students"]
    return [
        {
            "id": row["id"],
            "nom": row["last_name"],
            "prenom": row["first_name"],
            "classe": row["class_name"],
            "date_naissance": row["date_of_birth"],
            "telephone_parent": row["parent_phone"],
            "email_parent": row["parent_email"],
        }
        for _, row in students_df.iterrows()
    ]


def get_evaluations_for_student(student_id):
    """Return evaluations for a student with French keys used in parent pages."""
    grades_df = _ensure_data_cache()["grades"]
    student_grades = grades_df[grades_df["student_id"] == student_id].copy()
    student_grades = student_grades.sort_values("evaluation_date")

    return [
        {
            "id": row["id"],
            "date": row["evaluation_date"],
            "note": float(row["value"]),
            "matiere": row["subject"],
            "competence": row["competency_name"],
            "type": row["evaluation_type"],
        }
        for _, row in student_grades.iterrows()
    ]


def get_student_stats(student_id):
    """Compute compact student stats for parent dashboard widgets."""
    evaluations = get_evaluations_for_student(student_id)
    if not evaluations:
        return {"moyenne_generale": 0.0, "tendance": "stable", "evolution": 0.0}

    notes = pd.Series([e["note"] for e in evaluations])
    trend = calculate_trend(notes)

    if len(notes) >= 6:
        evolution = float(notes.iloc[-3:].mean() - notes.iloc[-6:-3].mean())
    elif len(notes) >= 2:
        evolution = float(notes.iloc[-1] - notes.iloc[0])
    else:
        evolution = 0.0

    return {
        "moyenne_generale": float(notes.mean()),
        "tendance": trend,
        "evolution": round(evolution, 2),
    }


def get_student_competencies(student_id):
    """Aggregate competency mastery levels for parent competency page."""
    grades_df = _ensure_data_cache()["grades"]
    student_grades = grades_df[grades_df["student_id"] == student_id].copy()
    if student_grades.empty:
        return []

    agg = (
        student_grades.groupby(["subject", "competency_name"], as_index=False)["value"]
        .mean()
        .sort_values(["subject", "competency_name"])
    )

    return [
        {
            "matiere": row["subject"],
            "competence": row["competency_name"],
            "niveau": round(float(row["value"]), 2),
        }
        for _, row in agg.iterrows()
    ]


if __name__ == "__main__":
    # Test data generation
    data = get_all_mock_data()
    
    print("✅ Generated Mock Data:")
    print(f"   - {len(data['students'])} students")
    print(f"   - {len(data['competencies'])} competencies")
    print(f"   - {len(data['grades'])} grades")
    print(f"   - {len(data['observations'])} observations")
    print(f"   - {len(data['reports'])} reports")
    
    # Show sample student
    print("\n📋 Sample Student:")
    print(data['students'].head(1).T)
    
    # Show grade distribution
    print("\n📊 Grade Distribution:")
    print(data['grades']['value'].describe())
