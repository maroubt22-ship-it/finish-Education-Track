# frontend/streamlit/components/alert_banner.py
"""
Alert banner component for notifications and warnings
"""

import streamlit as st
from frontend.shared.styles.theme import COLORS


def display_alert(message, alert_type="info", icon=None):
    """
    Display styled alert banner
    
    Args:
        message: Alert message text
        alert_type: "success", "warning", "danger", or "info"
        icon: Optional emoji icon
    """
    type_config = {
        "success": {
            "bg_color": "#D1FAE5",
            "border_color": COLORS["success"],
            "text_color": "#065F46",
            "default_icon": "✅"
        },
        "warning": {
            "bg_color": "#FEF3C7",
            "border_color": COLORS["warning"],
            "text_color": "#92400E",
            "default_icon": "⚠️"
        },
        "danger": {
            "bg_color": "#FEE2E2",
            "border_color": COLORS["danger"],
            "text_color": "#991B1B",
            "default_icon": "❌"
        },
        "info": {
            "bg_color": "#DBEAFE",
            "border_color": COLORS["info"],
            "text_color": "#1E40AF",
            "default_icon": "ℹ️"
        }
    }
    
    config = type_config.get(alert_type, type_config["info"])
    display_icon = icon if icon else config["default_icon"]
    
    alert_html = f"""
    <div style="background-color: {config['bg_color']}; 
                padding: 1rem 1.5rem; 
                border-radius: 8px; 
                border-left: 4px solid {config['border_color']};
                color: {config['text_color']};
                margin: 1rem 0;
                display: flex;
                align-items: center;
                gap: 0.75rem;">
        <span style="font-size: 1.5rem;">{display_icon}</span>
        <span style="flex: 1;">{message}</span>
    </div>
    """
    
    st.markdown(alert_html, unsafe_allow_html=True)


def display_student_alerts(students_df, grades_df):
    """
    Display alerts for students requiring attention
    
    Args:
        students_df: DataFrame with students
        grades_df: DataFrame with grades
    """
    alerts = []
    
    for _, student in students_df.iterrows():
        student_grades = grades_df[grades_df['student_id'] == student['id']]
        
        if len(student_grades) >= 4:
            # Check for declining trend
            mid = len(student_grades) // 2
            prev_avg = student_grades.iloc[:mid]['value'].mean()
            recent_avg = student_grades.iloc[mid:]['value'].mean()
            
            if recent_avg - prev_avg < -2:
                alerts.append({
                    'type': 'danger',
                    'student': f"{student['first_name']} {student['last_name']}",
                    'message': f"Régression détectée (moyenne passée de {prev_avg:.1f} à {recent_avg:.1f})",
                    'class': student['class_name']
                })
            
            # Check for very low average
            if recent_avg < 8:
                alerts.append({
                    'type': 'warning',
                    'student': f"{student['first_name']} {student['last_name']}",
                    'message': f"Moyenne très faible ({recent_avg:.1f}/20) - soutien recommandé",
                    'class': student['class_name']
                })
    
    if len(alerts) == 0:
        display_alert("Aucune alerte - Tous les élèves progressent normalement !", "success", "🎉")
    else:
        st.markdown("### 🚨 Alertes - Élèves nécessitant une attention")
        for alert in alerts:
            message = f"**{alert['student']}** ({alert['class']}) : {alert['message']}"
            display_alert(message, alert['type'])


def display_success_message(message, icon="✅"):
    """Display success message"""
    display_alert(message, "success", icon)


def display_warning_message(message, icon="⚠️"):
    """Display warning message"""
    display_alert(message, "warning", icon)


def display_error_message(message, icon="❌"):
    """Display error message"""
    display_alert(message, "danger", icon)


def display_info_message(message, icon="ℹ️"):
    """Display info message"""
    display_alert(message, "info", icon)
