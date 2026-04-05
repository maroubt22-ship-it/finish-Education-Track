"""
Analytics page for EduTrack IA
Displays student performance analysis, trends, and class insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

from frontend.shared.styles.theme import apply_theme, get_theme_colors
from frontend.streamlit.components.competency_radar import competency_radar
from frontend.streamlit.components.grade_chart import grade_chart
from frontend.streamlit.components.alert_banner import alert_banner
from frontend.streamlit.utils.helpers import calculate_trend, calculate_average, get_risk_level


def get_sample_students():
    """Generate sample student data"""
    return [
        {"id": 1, "name": "Alice Martin", "class": "3A"},
        {"id": 2, "name": "Bob Dubois", "class": "3A"},
        {"id": 3, "name": "Charlie Petit", "class": "3A"},
        {"id": 4, "name": "Diana Lambert", "class": "3B"},
        {"id": 5, "name": "Emma Rousseau", "class": "3B"},
        {"id": 6, "name": "Felix Bernard", "class": "3B"},
        {"id": 7, "name": "Grace Moreau", "class": "3A"},
        {"id": 8, "name": "Hugo Laurent", "class": "3A"},
    ]


def get_student_grades_history(student_id):
    """Generate sample grade history for a student"""
    np.random.seed(student_id)
    dates = pd.date_range(end=datetime.now(), periods=10, freq='W')
    
    # Generate grades with some trend
    base_grade = np.random.uniform(8, 15)
    trend = np.random.choice([-0.3, 0, 0.3])  # declining, stable, improving
    
    grades = []
    for i in range(10):
        grade = base_grade + trend * i + np.random.normal(0, 1.5)
        grade = np.clip(grade, 0, 20)
        grades.append(grade)
    
    return pd.DataFrame({
        'date': dates,
        'grade': grades,
        'subject': np.random.choice(['Mathématiques', 'Français', 'Sciences'], 10)
    })


def get_student_competencies(student_id):
    """Generate sample competency data for radar chart"""
    np.random.seed(student_id)
    return {
        'Raisonnement': np.random.uniform(8, 18),
        'Communication': np.random.uniform(8, 18),
        'Résolution': np.random.uniform(8, 18),
        'Créativité': np.random.uniform(8, 18),
        'Collaboration': np.random.uniform(8, 18),
        'Autonomie': np.random.uniform(8, 18),
    }


def get_class_heatmap_data():
    """Generate class competency heatmap data"""
    students = get_sample_students()
    competencies = ['Raisonnement', 'Communication', 'Résolution', 'Créativité', 'Collaboration', 'Autonomie']
    
    data = []
    for student in students:
        comp_data = get_student_competencies(student['id'])
        row = [student['name']] + [comp_data[comp] for comp in competencies]
        data.append(row)
    
    return pd.DataFrame(data, columns=['Étudiant'] + competencies)


def get_students_at_risk():
    """Get list of students who need attention"""
    students = get_sample_students()
    at_risk = []
    
    for student in students:
        avg_grade = calculate_average([g for g in get_student_grades_history(student['id'])['grade']])
        risk = get_risk_level(avg_grade)
        
        if risk in ['high', 'medium']:
            at_risk.append({
                'name': student['name'],
                'average': avg_grade,
                'risk': risk,
                'class': student['class']
            })
    
    return at_risk


def main():
    st.set_page_config(page_title="Analyses - EduTrack IA", page_icon="📈", layout="wide")
    
    # Apply theme
    apply_theme()
    colors = get_theme_colors()
    
    # 1. Title and header
    st.title("📈 Analyses Avancées")
    st.markdown("""
    Analyse approfondie des performances des étudiants, tendances et insights de classe.
    """)
    
    st.divider()
    
    # 2. Student selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        students = get_sample_students()
        student_names = {s['name']: s['id'] for s in students}
        selected_student_name = st.selectbox(
            "🎓 Sélectionner un étudiant",
            options=list(student_names.keys()),
            help="Choisissez un étudiant pour voir son analyse détaillée"
        )
        selected_student_id = student_names[selected_student_name]
    
    with col2:
        # Get student's class
        student_class = next(s['class'] for s in students if s['id'] == selected_student_id)
        st.metric("Classe", student_class)
    
    st.divider()
    
    # Student analysis section
    st.header(f"📊 Analyse de {selected_student_name}")
    
    # 3. Progress charts - Grade evolution over time
    st.subheader("📈 Évolution des Notes")
    
    grades_history = get_student_grades_history(selected_student_id)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_grade = calculate_average(grades_history['grade'].tolist())
        st.metric("Moyenne Générale", f"{avg_grade:.1f}/20")
    
    with col2:
        trend = calculate_trend(grades_history['grade'].tolist())
        trend_icon = "📈" if trend == "amélioration" else "📉" if trend == "régression" else "➡️"
        trend_color = "green" if trend == "amélioration" else "red" if trend == "régression" else "gray"
        st.metric("Tendance", trend.capitalize(), delta=trend_icon)
    
    with col3:
        latest_grade = grades_history['grade'].iloc[-1]
        previous_grade = grades_history['grade'].iloc[-2]
        delta = latest_grade - previous_grade
        st.metric("Dernière Note", f"{latest_grade:.1f}/20", f"{delta:+.1f}")
    
    # Grade evolution chart
    grade_chart(
        data=grades_history,
        title="Évolution des notes au fil du temps"
    )
    
    st.divider()
    
    # 4. Competency radar chart
    st.subheader("🎯 Profil de Compétences")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        competencies = get_student_competencies(selected_student_id)
        competency_radar(
            competencies=competencies,
            title=f"Radar des compétences - {selected_student_name}"
        )
    
    with col2:
        st.markdown("### Points Forts")
        sorted_comps = sorted(competencies.items(), key=lambda x: x[1], reverse=True)
        
        for i, (comp, score) in enumerate(sorted_comps[:3]):
            st.markdown(f"**{i+1}. {comp}**")
            st.progress(score / 20)
            st.caption(f"{score:.1f}/20")
        
        st.markdown("### Axes d'Amélioration")
        for i, (comp, score) in enumerate(sorted_comps[-3:]):
            st.markdown(f"**{comp}**")
            st.progress(score / 20)
            st.caption(f"{score:.1f}/20")
    
    st.divider()
    
    # 5. Class heatmap
    st.header("🗺️ Carte Thermique de Classe")
    st.markdown("Vue d'ensemble des compétences de tous les étudiants")
    
    heatmap_data = get_class_heatmap_data()
    
    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Prepare data for heatmap (exclude student names)
    heatmap_values = heatmap_data.iloc[:, 1:].values
    
    sns.heatmap(
        heatmap_values,
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        xticklabels=heatmap_data.columns[1:],
        yticklabels=heatmap_data['Étudiant'],
        cbar_kws={'label': 'Score /20'},
        vmin=0,
        vmax=20,
        ax=ax
    )
    
    ax.set_title('Compétences par Étudiant', fontsize=16, pad=20)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close()
    
    st.divider()
    
    # 6. Trend analysis with indicators
    st.header("📊 Analyse de Tendances")
    
    col1, col2, col3 = st.columns(3)
    
    students_data = []
    for student in students:
        grades = get_student_grades_history(student['id'])['grade'].tolist()
        avg = calculate_average(grades)
        trend = calculate_trend(grades)
        students_data.append({
            'name': student['name'],
            'average': avg,
            'trend': trend
        })
    
    # Count trends
    amelioration = sum(1 for s in students_data if s['trend'] == 'amélioration')
    stable = sum(1 for s in students_data if s['trend'] == 'stable')
    regression = sum(1 for s in students_data if s['trend'] == 'régression')
    
    with col1:
        st.metric(
            "📈 En Amélioration",
            amelioration,
            delta="Positif",
            delta_color="normal"
        )
        for s in students_data:
            if s['trend'] == 'amélioration':
                st.success(f"✓ {s['name']} ({s['average']:.1f}/20)")
    
    with col2:
        st.metric(
            "➡️ Stable",
            stable,
            delta="Neutre",
            delta_color="off"
        )
        for s in students_data:
            if s['trend'] == 'stable':
                st.info(f"• {s['name']} ({s['average']:.1f}/20)")
    
    with col3:
        st.metric(
            "📉 En Régression",
            regression,
            delta="Attention",
            delta_color="inverse"
        )
        for s in students_data:
            if s['trend'] == 'régression':
                st.warning(f"⚠ {s['name']} ({s['average']:.1f}/20)")
    
    st.divider()
    
    # 7. Alerts section - Students in difficulty
    st.header("🚨 Alertes et Suivi")
    st.markdown("Étudiants nécessitant une attention particulière")
    
    at_risk_students = get_students_at_risk()
    
    if at_risk_students:
        for student in at_risk_students:
            severity = "error" if student['risk'] == 'high' else "warning"
            message = f"**{student['name']}** (Classe {student['class']}) - Moyenne: {student['average']:.1f}/20"
            
            if student['risk'] == 'high':
                recommendation = "⚠️ Action immédiate requise - Entretien individuel recommandé"
            else:
                recommendation = "📋 Suivi renforcé recommandé"
            
            alert_banner(
                message=message,
                severity=severity,
                details=recommendation
            )
    else:
        st.success("✅ Aucun étudiant en difficulté détecté")
    
    st.divider()
    
    # Additional insights
    st.header("💡 Insights Complémentaires")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution des Moyennes")
        
        all_averages = [s['average'] for s in students_data]
        
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=all_averages,
            nbinsx=10,
            marker_color=colors.get('primary', '#1f77b4'),
            name='Étudiants'
        ))
        
        fig.update_layout(
            title="Répartition des moyennes de classe",
            xaxis_title="Moyenne /20",
            yaxis_title="Nombre d'étudiants",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Statistiques de Classe")
        
        class_avg = calculate_average(all_averages)
        class_min = min(all_averages)
        class_max = max(all_averages)
        class_std = np.std(all_averages)
        
        st.metric("Moyenne de Classe", f"{class_avg:.1f}/20")
        st.metric("Note Minimale", f"{class_min:.1f}/20")
        st.metric("Note Maximale", f"{class_max:.1f}/20")
        st.metric("Écart-Type", f"{class_std:.2f}")
        
        if class_std < 2:
            st.success("✅ Classe homogène")
        elif class_std < 4:
            st.info("ℹ️ Dispersion modérée")
        else:
            st.warning("⚠️ Forte hétérogénéité")


if __name__ == "__main__":
    main()
