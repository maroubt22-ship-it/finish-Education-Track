# frontend/streamlit/utils/helpers.py
"""
Utility functions for EduTrack IA Streamlit application
"""

import pandas as pd
import numpy as np
from datetime import datetime
import locale

# Try to set French locale for date formatting
try:
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'French_France.1252')
    except:
        pass  # Fallback to default locale


def format_date(date_str, format_type="short"):
    """
    Format date string to French format
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        format_type: "short" (DD/MM/YYYY) or "long" (DD mois YYYY)
    
    Returns:
        Formatted date string
    """
    try:
        if isinstance(date_str, str):
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        else:
            date_obj = date_str
        
        if format_type == "short":
            return date_obj.strftime("%d/%m/%Y")
        elif format_type == "long":
            months_fr = {
                1: "janvier", 2: "février", 3: "mars", 4: "avril",
                5: "mai", 6: "juin", 7: "juillet", 8: "août",
                9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
            }
            return f"{date_obj.day} {months_fr[date_obj.month]} {date_obj.year}"
        else:
            return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str


def calculate_average(grades_series):
    """
    Calculate average grade
    
    Args:
        grades_series: Series or list of grade values
    
    Returns:
        Average grade rounded to 2 decimals
    """
    if len(grades_series) == 0:
        return 0.0
    return round(np.mean(grades_series), 2)


def calculate_trend(grades_df, period_days=90):
    """
    Calculate grade trend comparing recent vs previous period
    
    Args:
        grades_df: DataFrame with 'evaluation_date' and 'value' columns
        period_days: Number of days for each period (default: 90)
    
    Returns:
        Dictionary with trend info: {
            'trend': 'amélioration'|'stable'|'régression',
            'trend_value': float,
            'recent_avg': float,
            'previous_avg': float
        }
    """
    if len(grades_df) < 4:
        return {
            'trend': 'stable',
            'trend_value': 0.0,
            'recent_avg': 0.0,
            'previous_avg': 0.0
        }
    
    # Sort by date
    grades_sorted = grades_df.sort_values('evaluation_date')
    
    # Split into two periods
    mid_point = len(grades_sorted) // 2
    previous_grades = grades_sorted.iloc[:mid_point]['value']
    recent_grades = grades_sorted.iloc[mid_point:]['value']
    
    previous_avg = calculate_average(previous_grades)
    recent_avg = calculate_average(recent_grades)
    trend_value = recent_avg - previous_avg
    
    # Classify trend
    if trend_value > 2:
        trend = "amélioration"
    elif trend_value < -2:
        trend = "régression"
    else:
        trend = "stable"
    
    return {
        'trend': trend,
        'trend_value': round(trend_value, 2),
        'recent_avg': round(recent_avg, 2),
        'previous_avg': round(previous_avg, 2)
    }


def classify_grade(value):
    """
    Classify grade into mastery level
    
    Args:
        value: Grade value (0-20)
    
    Returns:
        Dictionary with classification info: {
            'level': 'maîtrisée'|'en cours'|'à renforcer',
            'color': str,
            'emoji': str
        }
    """
    if value >= 14:
        return {
            'level': 'maîtrisée',
            'color': 'green',
            'emoji': '🟢'
        }
    elif value >= 10:
        return {
            'level': 'en cours',
            'color': 'orange',
            'emoji': '🟡'
        }
    else:
        return {
            'level': 'à renforcer',
            'color': 'red',
            'emoji': '🔴'
        }


def get_mention(average):
    """
    Get academic mention based on average grade
    
    Args:
        average: Average grade (0-20)
    
    Returns:
        Mention string
    """
    if average >= 16:
        return "Très Bien"
    elif average >= 14:
        return "Bien"
    elif average >= 12:
        return "Assez Bien"
    elif average >= 10:
        return "Passable"
    else:
        return "Insuffisant"


def calculate_competency_stats(grades_df, competencies_df):
    """
    Calculate statistics for each competency
    
    Args:
        grades_df: DataFrame with student grades
        competencies_df: DataFrame with competencies
    
    Returns:
        DataFrame with competency statistics
    """
    stats = []
    
    for _, comp in competencies_df.iterrows():
        comp_grades = grades_df[grades_df['competency_id'] == comp['id']]
        
        if len(comp_grades) > 0:
            avg = calculate_average(comp_grades['value'])
            classification = classify_grade(avg)
            
            stats.append({
                'competency_id': comp['id'],
                'competency_name': comp['name'],
                'subject': comp['subject'],
                'average': avg,
                'level': classification['level'],
                'emoji': classification['emoji'],
                'count': len(comp_grades),
                'min': comp_grades['value'].min(),
                'max': comp_grades['value'].max()
            })
    
    return pd.DataFrame(stats)


def filter_students(students_df, search_term="", class_filter=None, status_filter="active"):
    """
    Filter students based on search and filter criteria
    
    Args:
        students_df: DataFrame with students
        search_term: Search string for name filtering
        class_filter: Class name filter (or None for all)
        status_filter: "active", "inactive", or "all"
    
    Returns:
        Filtered DataFrame
    """
    filtered = students_df.copy()
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered = filtered[
            filtered['first_name'].str.lower().str.contains(search_term) |
            filtered['last_name'].str.lower().str.contains(search_term)
        ]
    
    # Apply class filter
    if class_filter and class_filter != "Toutes les classes":
        filtered = filtered[filtered['class_name'] == class_filter]
    
    # Apply status filter
    if status_filter == "active":
        filtered = filtered[filtered['is_active'] == True]
    elif status_filter == "inactive":
        filtered = filtered[filtered['is_active'] == False]
    # "all" shows everything
    
    return filtered


def get_student_summary(student_id, students_df, grades_df):
    """
    Get comprehensive summary for a student
    
    Args:
        student_id: Student ID
        students_df: Students DataFrame
        grades_df: Grades DataFrame
    
    Returns:
        Dictionary with student summary
    """
    student = students_df[students_df['id'] == student_id].iloc[0]
    student_grades = grades_df[grades_df['student_id'] == student_id]
    
    if len(student_grades) == 0:
        return {
            'student': student,
            'average': 0.0,
            'total_grades': 0,
            'trend': 'stable',
            'classification': classify_grade(0),
            'mention': 'Aucune note'
        }
    
    average = calculate_average(student_grades['value'])
    trend_info = calculate_trend(student_grades)
    classification = classify_grade(average)
    mention = get_mention(average)
    
    return {
        'student': student,
        'average': average,
        'total_grades': len(student_grades),
        'trend': trend_info['trend'],
        'trend_value': trend_info['trend_value'],
        'classification': classification,
        'mention': mention,
        'recent_avg': trend_info['recent_avg'],
        'previous_avg': trend_info['previous_avg']
    }


def generate_report_text(student_summary, observations, competency_stats):
    """
    Generate formatted report text
    
    Args:
        student_summary: Student summary dictionary
        observations: List of recent observations
        competency_stats: DataFrame with competency statistics
    
    Returns:
        Formatted report text
    """
    student = student_summary['student']
    
    # Header
    report = f"📋 RAPPORT DE PROGRESSION – {student['first_name']} {student['last_name']}\n"
    report += f"Date : {format_date(datetime.now().strftime('%Y-%m-%d'), 'long')}\n"
    report += f"Classe : {student['class_name']}\n\n"
    
    # Section 1: Competencies worked on
    report += "1. COMPÉTENCES TRAVAILLÉES\n"
    report += "-" * 50 + "\n"
    if len(competency_stats) > 0:
        for _, comp in competency_stats.head(5).iterrows():
            report += f"   • {comp['competency_name']} ({comp['subject']}) - Moyenne: {comp['average']}/20\n"
    else:
        report += "   Aucune compétence évaluée pour cette période.\n"
    report += "\n"
    
    # Section 2: Progress achieved
    report += "2. PROGRÈS RÉALISÉS\n"
    report += "-" * 50 + "\n"
    if student_summary['trend'] == 'amélioration':
        report += f"   Excellente progression constatée ! La moyenne est passée de {student_summary['previous_avg']}/20 "
        report += f"à {student_summary['recent_avg']}/20 (+{student_summary['trend_value']:.1f} points).\n"
        report += "   L'élève montre une amélioration continue et une bonne assimilation des concepts.\n"
    elif student_summary['trend'] == 'stable':
        report += f"   Performance stable maintenue autour de {student_summary['average']}/20.\n"
        report += "   L'élève consolide ses acquis de manière régulière.\n"
    else:
        report += f"   Une attention particulière est nécessaire. La moyenne a légèrement baissé.\n"
    report += "\n"
    
    # Section 3: Areas to improve
    report += "3. POINTS À AMÉLIORER\n"
    report += "-" * 50 + "\n"
    weak_comps = competency_stats[competency_stats['average'] < 10] if len(competency_stats) > 0 else pd.DataFrame()
    if len(weak_comps) > 0:
        for _, comp in weak_comps.iterrows():
            report += f"   • {comp['competency_name']} : renforcement nécessaire (moyenne: {comp['average']}/20)\n"
    else:
        report += "   Continuer les efforts actuels pour maintenir le bon niveau.\n"
    report += "\n"
    
    # Section 4: Teacher observations
    report += "4. OBSERVATIONS DE L'ENSEIGNANT\n"
    report += "-" * 50 + "\n"
    if len(observations) > 0:
        for obs in observations[:3]:
            report += f"   • {obs['content']}\n"
    else:
        report += "   Aucune observation particulière pour cette période.\n"
    report += "\n"
    
    # Section 5: Recommendations
    report += "5. RECOMMANDATIONS\n"
    report += "-" * 50 + "\n"
    if student_summary['average'] >= 14:
        report += "   • Continuer sur cette excellente lancée\n"
        report += "   • Approfondir les sujets avancés pour aller plus loin\n"
    elif student_summary['average'] >= 10:
        report += "   • Réviser régulièrement les concepts fondamentaux\n"
        report += "   • Pratiquer davantage d'exercices pour gagner en assurance\n"
    else:
        report += "   • Revoir les bases avec attention\n"
        report += "   • Prévoir des séances de soutien supplémentaires\n"
        report += "   • Encourager la participation active en classe\n"
    
    return report


def prepare_radar_data(competency_stats):
    """
    Prepare data for radar chart visualization
    
    Args:
        competency_stats: DataFrame with competency statistics
    
    Returns:
        Dictionary with radar chart data
    """
    if len(competency_stats) == 0:
        return {'subjects': [], 'values': []}
    
    # Aggregate by subject
    subject_stats = competency_stats.groupby('subject')['average'].mean().reset_index()
    subject_stats = subject_stats.sort_values('average', ascending=False).head(8)  # Max 8 for readability
    
    return {
        'subjects': subject_stats['subject'].tolist(),
        'values': subject_stats['average'].tolist()
    }


def validate_grade(value):
    """
    Validate grade value
    
    Args:
        value: Grade value
    
    Returns:
        Tuple (is_valid, error_message)
    """
    try:
        val = float(value)
        if val < 0 or val > 20:
            return False, "La note doit être entre 0 et 20"
        return True, ""
    except:
        return False, "La note doit être un nombre valide"
