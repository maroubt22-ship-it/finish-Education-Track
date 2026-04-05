# frontend/streamlit/components/student_card.py
"""
Student card component for displaying student information
"""

import streamlit as st
from frontend.shared.styles.theme import COLORS


def display_student_card(student, average=None, trend=None):
    """
    Display a styled student information card
    
    Args:
        student: Student dictionary/Series with student data
        average: Optional average grade
        trend: Optional trend indicator
    """
    trend_emoji = {"amélioration": "📈", "stable": "➡️", "régression": "📉"}.get(trend, "")
    trend_color = {
        "amélioration": COLORS["success"],
        "stable": COLORS["info"],
        "régression": COLORS["danger"]
    }.get(trend, COLORS["info"])
    
    card_html = f"""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-top: 3px solid {COLORS['primary']};">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <h3 style="margin: 0; color: {COLORS['dark']};">
                    {student['first_name']} {student['last_name']}
                </h3>
                <p style="color: #6B7280; margin: 0.5rem 0;">
                    📚 {student['class_name']}
                </p>
                <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0.25rem 0;">
                    📞 {student['parent_phone']}
                </p>
                <p style="color: #9CA3AF; font-size: 0.9rem; margin: 0.25rem 0;">
                    📧 {student['parent_email']}
                </p>
            </div>
            <div style="text-align: right;">
    """
    
    if average is not None:
        avg_color = COLORS['success'] if average >= 14 else COLORS['warning'] if average >= 10 else COLORS['danger']
        card_html += f"""
                <div style="background: {avg_color}; color: white; padding: 0.75rem 1.25rem; 
                            border-radius: 10px; margin-bottom: 0.5rem;">
                    <div style="font-size: 1.5rem; font-weight: bold;">{average}/20</div>
                    <div style="font-size: 0.8rem;">Moyenne</div>
                </div>
        """
    
    if trend:
        card_html += f"""
                <div style="color: {trend_color}; font-weight: bold; font-size: 0.9rem;">
                    {trend_emoji} {trend.capitalize()}
                </div>
        """
    
    card_html += """
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def display_compact_student_list(students_df, grades_df=None):
    """
    Display a compact list of student cards
    
    Args:
        students_df: DataFrame with students
        grades_df: Optional DataFrame with grades for averages
    """
    for idx, student in students_df.iterrows():
        average = None
        trend = None
        
        if grades_df is not None:
            student_grades = grades_df[grades_df['student_id'] == student['id']]
            if len(student_grades) > 0:
                average = round(student_grades['value'].mean(), 2)
                
                # Simple trend calculation
                if len(student_grades) >= 4:
                    mid = len(student_grades) // 2
                    prev_avg = student_grades.iloc[:mid]['value'].mean()
                    recent_avg = student_grades.iloc[mid:]['value'].mean()
                    diff = recent_avg - prev_avg
                    
                    if diff > 2:
                        trend = "amélioration"
                    elif diff < -2:
                        trend = "régression"
                    else:
                        trend = "stable"
        
        display_student_card(student, average, trend)
        st.markdown("<br>", unsafe_allow_html=True)
