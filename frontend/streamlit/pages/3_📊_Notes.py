"""
Grades Management Page - EduTrack IA
Handles grade entry, visualization, and filtering
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from typing import List, Dict, Optional

from frontend.shared.styles.theme import apply_theme, get_colors, apply_card_style
from frontend.streamlit.components.grade_chart import render_grade_chart, render_grade_distribution
from frontend.streamlit.utils.helpers import (
    validate_grade,
    calculate_average,
    get_grade_statistics,
    format_grade
)

# Page configuration
st.set_page_config(
    page_title="Gestion des Notes - EduTrack IA",
    page_icon="📊",
    layout="wide"
)

# Apply theme
apply_theme()
colors = get_colors()

# Initialize session state
if 'grades' not in st.session_state:
    st.session_state.grades = []

if 'students' not in st.session_state:
    st.session_state.students = [
        {"id": 1, "name": "Alice Dupont"},
        {"id": 2, "name": "Bob Martin"},
        {"id": 3, "name": "Claire Dubois"},
        {"id": 4, "name": "David Lefebvre"},
        {"id": 5, "name": "Emma Rousseau"}
    ]

if 'competencies' not in st.session_state:
    st.session_state.competencies = [
        {"id": 1, "name": "Mathématiques", "subject": "Mathématiques"},
        {"id": 2, "name": "Algèbre", "subject": "Mathématiques"},
        {"id": 3, "name": "Géométrie", "subject": "Mathématiques"},
        {"id": 4, "name": "Grammaire", "subject": "Français"},
        {"id": 5, "name": "Littérature", "subject": "Français"},
        {"id": 6, "name": "Physique", "subject": "Sciences"},
        {"id": 7, "name": "Chimie", "subject": "Sciences"},
        {"id": 8, "name": "Histoire", "subject": "Histoire-Géo"},
        {"id": 9, "name": "Géographie", "subject": "Histoire-Géo"}
    ]

# Evaluation types
EVALUATION_TYPES = [
    "Contrôle continu",
    "Devoir sur table",
    "Examen",
    "Oral",
    "Projet",
    "TP/TD",
    "Quiz"
]

# Helper functions
def add_grade(student_id: int, competency_id: int, value: float, 
              eval_type: str, eval_date: date, comment: str = ""):
    """Add a new grade to session state"""
    grade = {
        "id": len(st.session_state.grades) + 1,
        "student_id": student_id,
        "competency_id": competency_id,
        "value": value,
        "evaluation_type": eval_type,
        "date": eval_date,
        "comment": comment,
        "created_at": datetime.now()
    }
    st.session_state.grades.append(grade)
    return True

def get_student_name(student_id: int) -> str:
    """Get student name by ID"""
    student = next((s for s in st.session_state.students if s["id"] == student_id), None)
    return student["name"] if student else "Unknown"

def get_competency_name(competency_id: int) -> str:
    """Get competency name by ID"""
    comp = next((c for c in st.session_state.competencies if c["id"] == competency_id), None)
    return comp["name"] if comp else "Unknown"

def get_subject_name(competency_id: int) -> str:
    """Get subject name by competency ID"""
    comp = next((c for c in st.session_state.competencies if c["id"] == competency_id), None)
    return comp["subject"] if comp else "Unknown"

def filter_grades(student_id: Optional[int] = None, 
                 subject: Optional[str] = None,
                 date_range: Optional[tuple] = None) -> List[Dict]:
    """Filter grades based on criteria"""
    filtered = st.session_state.grades.copy()
    
    if student_id:
        filtered = [g for g in filtered if g["student_id"] == student_id]
    
    if subject:
        subject_comp_ids = [c["id"] for c in st.session_state.competencies if c["subject"] == subject]
        filtered = [g for g in filtered if g["competency_id"] in subject_comp_ids]
    
    if date_range and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = [g for g in filtered if start_date <= g["date"] <= end_date]
    
    return filtered

# Header
st.title("📊 Gestion des Notes")
st.markdown("Saisie et suivi des notes des élèves")
st.divider()

# Main layout
col1, col2 = st.columns([1, 2])

with col1:
    # Grade entry form
    st.subheader("Nouvelle Note")
    
    with st.form("grade_entry_form", clear_on_submit=True):
        # Student selection
        student_names = {s["id"]: s["name"] for s in st.session_state.students}
        selected_student = st.selectbox(
            "Élève *",
            options=list(student_names.keys()),
            format_func=lambda x: student_names[x],
            key="student_select"
        )
        
        # Competency selection
        competency_options = {c["id"]: f"{c['name']} ({c['subject']})" 
                             for c in st.session_state.competencies}
        selected_competency = st.selectbox(
            "Compétence *",
            options=list(competency_options.keys()),
            format_func=lambda x: competency_options[x],
            key="competency_select"
        )
        
        # Grade value
        grade_value = st.number_input(
            "Note (0-20) *",
            min_value=0.0,
            max_value=20.0,
            value=10.0,
            step=0.5,
            format="%.1f",
            key="grade_value"
        )
        
        # Evaluation type
        eval_type = st.selectbox(
            "Type d'évaluation *",
            options=EVALUATION_TYPES,
            key="eval_type"
        )
        
        # Date picker
        eval_date = st.date_input(
            "Date *",
            value=date.today(),
            max_value=date.today(),
            key="eval_date"
        )
        
        # Optional comment
        comment = st.text_area(
            "Commentaire (optionnel)",
            max_chars=200,
            key="comment"
        )
        
        # Submit button
        submitted = st.form_submit_button("➕ Ajouter la Note", use_container_width=True)
        
        if submitted:
            # Validate grade
            is_valid, error_message = validate_grade(grade_value)
            
            if is_valid:
                # Add grade
                success = add_grade(
                    student_id=selected_student,
                    competency_id=selected_competency,
                    value=grade_value,
                    eval_type=eval_type,
                    eval_date=eval_date,
                    comment=comment
                )
                
                if success:
                    st.success(f"✅ Note ajoutée avec succès pour {get_student_name(selected_student)}")
                    st.rerun()
            else:
                st.error(f"❌ {error_message}")
    
    # Statistics card
    if st.session_state.grades:
        st.divider()
        st.subheader("📈 Statistiques")
        
        with apply_card_style():
            all_grades = [g["value"] for g in st.session_state.grades]
            stats = get_grade_statistics(all_grades)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Moyenne Générale", f"{stats['mean']:.2f}/20")
                st.metric("Note Min", f"{stats['min']:.1f}/20")
            with col_b:
                st.metric("Total Notes", stats['count'])
                st.metric("Note Max", f"{stats['max']:.1f}/20")

with col2:
    # Filters section
    st.subheader("🔍 Filtres")
    
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        # Student filter
        student_filter_options = {"all": "Tous les élèves"}
        student_filter_options.update({s["id"]: s["name"] for s in st.session_state.students})
        selected_student_filter = st.selectbox(
            "Élève",
            options=list(student_filter_options.keys()),
            format_func=lambda x: student_filter_options[x],
            key="student_filter"
        )
    
    with filter_col2:
        # Subject filter
        subjects = list(set(c["subject"] for c in st.session_state.competencies))
        subject_filter = st.selectbox(
            "Matière",
            options=["Toutes"] + subjects,
            key="subject_filter"
        )
    
    with filter_col3:
        # Date range filter
        use_date_filter = st.checkbox("Filtrer par date", key="use_date_filter")
    
    if use_date_filter:
        date_col1, date_col2 = st.columns(2)
        with date_col1:
            start_date = st.date_input(
                "Date début",
                value=date.today().replace(day=1),
                key="start_date"
            )
        with date_col2:
            end_date = st.date_input(
                "Date fin",
                value=date.today(),
                key="end_date"
            )
        date_range = (start_date, end_date)
    else:
        date_range = None
    
    # Apply filters
    filtered_grades = filter_grades(
        student_id=selected_student_filter if selected_student_filter != "all" else None,
        subject=subject_filter if subject_filter != "Toutes" else None,
        date_range=date_range
    )
    
    st.divider()
    
    # Recent grades table
    st.subheader(f"📋 Notes Récentes ({len(filtered_grades)})")
    
    if filtered_grades:
        # Prepare data for display
        grades_data = []
        for grade in sorted(filtered_grades, key=lambda x: x["date"], reverse=True):
            grades_data.append({
                "Date": grade["date"].strftime("%d/%m/%Y"),
                "Élève": get_student_name(grade["student_id"]),
                "Matière": get_subject_name(grade["competency_id"]),
                "Compétence": get_competency_name(grade["competency_id"]),
                "Note": format_grade(grade["value"]),
                "Type": grade["evaluation_type"],
                "Commentaire": grade.get("comment", "")[:30] + "..." if len(grade.get("comment", "")) > 30 else grade.get("comment", "")
            })
        
        df_grades = pd.DataFrame(grades_data)
        
        # Display with grade chart component
        render_grade_chart(df_grades)
        
        # Download button
        csv = df_grades.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Télécharger CSV",
            data=csv,
            file_name=f"notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
    else:
        st.info("Aucune note trouvée avec ces filtres.")
    
    # Grade distribution histogram
    if filtered_grades:
        st.divider()
        st.subheader("📊 Distribution des Notes")
        
        # Use the grade_chart component
        grade_values = [g["value"] for g in filtered_grades]
        render_grade_distribution(grade_values)
        
        # Additional analysis
        with st.expander("📈 Analyse Détaillée"):
            analysis_col1, analysis_col2 = st.columns(2)
            
            with analysis_col1:
                # By subject
                st.markdown("**Par Matière**")
                subject_grades = {}
                for grade in filtered_grades:
                    subject = get_subject_name(grade["competency_id"])
                    if subject not in subject_grades:
                        subject_grades[subject] = []
                    subject_grades[subject].append(grade["value"])
                
                for subject, grades in subject_grades.items():
                    avg = calculate_average(grades)
                    st.metric(subject, f"{avg:.2f}/20", f"{len(grades)} notes")
            
            with analysis_col2:
                # By evaluation type
                st.markdown("**Par Type d'Évaluation**")
                type_grades = {}
                for grade in filtered_grades:
                    eval_type = grade["evaluation_type"]
                    if eval_type not in type_grades:
                        type_grades[eval_type] = []
                    type_grades[eval_type].append(grade["value"])
                
                for eval_type, grades in type_grades.items():
                    avg = calculate_average(grades)
                    st.metric(eval_type, f"{avg:.2f}/20", f"{len(grades)} notes")

# Footer
st.divider()
st.caption(f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
