# frontend/streamlit/app.py
"""
EduTrack IA - Main Streamlit Application
Teacher Dashboard for Student Progress Tracking
"""

import streamlit as st
import sys
import os
import calendar
from datetime import datetime
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
)

from frontend.shared.data.mock_data import get_all_mock_data  # noqa: E402
from frontend.shared.styles.theme import apply_custom_css, COLORS  # noqa: E402

# Page configuration
st.set_page_config(
    page_title="EduTrack IA - Dashboard Enseignant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Initialize session state with mock data
if 'data_loaded' not in st.session_state:
    with st.spinner("Chargement des données..."):
        mock_data = get_all_mock_data()
        st.session_state.students = mock_data['students']
        st.session_state.competencies = mock_data['competencies']
        st.session_state.grades = mock_data['grades']
        st.session_state.observations = mock_data['observations']
        st.session_state.reports = mock_data['reports']
        st.session_state.data_loaded = True

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 1rem;
        background: linear-gradient(
            135deg,
            {COLORS['primary']} 0%,
            {COLORS['info']} 100%
        );
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    ">
        <h1 style="margin: 0;">📚</h1>
        <h2 style="margin: 0.5rem 0;">EduTrack IA</h2>
        <p style="margin: 0; font-size: 0.9rem;">Dashboard Enseignant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 👤 Utilisateur")
    st.markdown("**M. Alaoui**  \nEnseignant de Mathématiques")

    st.markdown("---")

    st.markdown("### 📊 Statistiques Rapides")
    active_students = len(
        st.session_state.students[st.session_state.students['is_active']]
    )
    st.metric("Élèves actifs", active_students)
    st.metric("Total notes", len(st.session_state.grades))
    avg_grade = round(st.session_state.grades['value'].mean(), 2)
    st.metric("Moyenne générale", f"{avg_grade}/20")

    st.markdown("---")

    st.markdown("### ℹ️ Navigation")
    st.info(
        "Utilisez le menu ci-dessus pour accéder "
        "aux différentes pages de l'application."
    )

    st.markdown("---")

    st.markdown("### 🔧 Mode Demo")
    st.warning("Application en mode démonstration avec données fictives.")

# Main content
students_df = st.session_state.students
grades_df = st.session_state.grades
observations_df = st.session_state.observations

total_students = len(students_df[students_df['is_active']])
total_parents = students_df['parent_phone'].nunique()
total_teachers = observations_df['teacher_name'].nunique()
total_centres = 1

st.markdown(
    """
    <div class="dashboard-top-strip"></div>
    <div class="dashboard-welcome">
        <div class="welcome-title">Bienvenue sur EduTrack IA</div>
        <div class="welcome-year">Année scolaire 2025 - 2026</div>
    </div>
    """,
    unsafe_allow_html=True,
)

kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

with kpi_col1:
    st.markdown(
        f"""
        <div class="kpi-tile accent-red">
            <div class="kpi-icon">🏫</div>
            <div>
                <div class="kpi-label">Centres</div>
                <div class="kpi-value">{total_centres}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col2:
    st.markdown(
        f"""
        <div class="kpi-tile accent-violet">
            <div class="kpi-icon">👩‍🏫</div>
            <div>
                <div class="kpi-label">Enseignants</div>
                <div class="kpi-value">{total_teachers}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col3:
    st.markdown(
        f"""
        <div class="kpi-tile accent-yellow">
            <div class="kpi-icon">🎓</div>
            <div>
                <div class="kpi-label">Élèves</div>
                <div class="kpi-value">{total_students}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with kpi_col4:
    st.markdown(
        f"""
        <div class="kpi-tile accent-green">
            <div class="kpi-icon">👨‍👩‍👧‍👦</div>
            <div>
                <div class="kpi-label">Parents</div>
                <div class="kpi-value">{total_parents}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:0.7rem'></div>", unsafe_allow_html=True)

row1_col1, row1_col2 = st.columns([1.15, 1])

now = datetime.now()
month_labels = [
    "JAN", "FEV", "MAR", "AVR", "MAI", "JUN",
    "JUL", "AOU", "SEP", "OCT", "NOV", "DEC"
]

eval_dates = pd.to_datetime(grades_df['evaluation_date'], errors='coerce')
highlight_days = set(
    eval_dates[
        (eval_dates.dt.month == now.month) &
        (eval_dates.dt.year == now.year)
    ].dt.day.dropna().astype(int).tolist()
)

month_matrix = calendar.monthcalendar(now.year, now.month)
days_html = ""
for week in month_matrix:
    days_html += '<div class="calendar-row">'
    for day in week:
        if day == 0:
            days_html += '<span class="calendar-day empty"></span>'
        elif day in highlight_days:
            days_html += f'<span class="calendar-day marked">{day}</span>'
        else:
            days_html += f'<span class="calendar-day">{day}</span>'
    days_html += '</div>'

month_pills = []
for idx, name in enumerate(month_labels):
    active_class = "active" if idx + 1 == now.month else ""
    month_pills.append(
        f'<span class="month-pill {active_class}">{name}</span>'
    )
month_pills_html = ''.join(month_pills)

with row1_col1:
    st.markdown(
        (
            '<div class="dashboard-panel section-fixed">'
            '<h3>Calendrier des évaluations</h3>'
            '<div class="month-strip">'
            + month_pills_html
            + '</div>'
            f'<div class="calendar-grid">{days_html}</div>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

levels = students_df['class_name'].str.lower()
college_count = int(levels.str.contains('collège').sum())
tronc_count = int(levels.str.contains('tronc').sum())
lycee_count = int((levels.str.contains('bac')).sum())

max_level = max(college_count, tronc_count, lycee_count, 1)
college_width = (college_count / max_level) * 100
tronc_width = (tronc_count / max_level) * 100
lycee_width = (lycee_count / max_level) * 100

with row1_col2:
    st.markdown(
        f"""
        <div class="dashboard-panel section-fixed">
            <h3>Niveaux éducatifs</h3>
            <div class="stage-row">
                <div class="stage-label">
                    <span class="dot violet"></span> Collège
                </div>
                <div class="stage-value">{college_count}</div>
                <div class="stage-bar">
                    <span style="width:{college_width:.0f}%"></span>
                </div>
            </div>
            <div class="stage-row">
                <div class="stage-label">
                    <span class="dot yellow"></span> Tronc Commun
                </div>
                <div class="stage-value">{tronc_count}</div>
                <div class="stage-bar">
                    <span style="width:{tronc_width:.0f}%"></span>
                </div>
            </div>
            <div class="stage-row">
                <div class="stage-label">
                    <span class="dot green"></span> Lycée
                </div>
                <div class="stage-value">{lycee_count}</div>
                <div class="stage-bar">
                    <span style="width:{lycee_width:.0f}%"></span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

row2_col1, row2_col2 = st.columns([1.15, 1])

recent_obs = observations_df.sort_values(
    'observation_date', ascending=False
).head(4)
activity_items = ""
for _, obs in recent_obs.iterrows():
    activity_items += (
        '<li>'
        f"{obs['content']}"
        f"<span>{obs['observation_date']}</span>"
        '</li>'
    )

with row2_col1:
    st.markdown(
        (
            '<div class="dashboard-panel section-fixed">'
            '<div class="panel-head">'
            '<h3>Activités & Événements</h3>'
            '<span class="view-all">Voir tout</span>'
            '</div>'
            f'<ul class="events-list">{activity_items}</ul>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

student_avg = grades_df.groupby('student_id', as_index=False)['value'].mean()
top3 = student_avg.sort_values('value', ascending=False).head(3)
top3 = top3.merge(
    students_df[['id', 'first_name', 'last_name']],
    left_on='student_id',
    right_on='id',
    how='left',
)

rank_classes = ['rank-green', 'rank-violet', 'rank-yellow']
rank_labels = ['1er', '2e', '3e']

cards_html = '<div class="top-cards-wrap">'
for idx, (_, row) in enumerate(top3.iterrows()):
    full_name = f"{row['first_name']} {row['last_name']}"
    score_text = f"{row['value']:.2f}/20"
    cards_html += (
        f'<div class="top-card {rank_classes[idx]}">'
        f'<div class="top-name">{full_name}</div>'
        f'<div class="top-score">{score_text}</div>'
        f'<div class="top-rank">{rank_labels[idx]}</div>'
        '</div>'
    )
cards_html += '</div>'

with row2_col2:
    st.markdown(
        f"""
        <div class="dashboard-panel section-fixed">
            <h3>Top élèves</h3>
            {cards_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# Help section
with st.expander("📖 Guide d'utilisation"):
    st.markdown("""
    ### Comment utiliser EduTrack IA

    **Navigation :**
    - Utilisez le menu latéral pour accéder aux différentes pages
    - **🏠 Accueil** : Vue d'ensemble et statistiques rapides
    - **👥 Élèves** : Gestion des profils élèves
    - **📊 Notes** : Saisie et consultation des notes
    - **🎯 Compétences** : Gestion du référentiel de compétences
    - **📈 Analyses** : Graphiques et analyses de progression
    - **📋 Rapports** : Génération de rapports pour les parents
    - **✍️ Observations** : Notes et commentaires sur les élèves

    **Mode démonstration :**
    - Les données affichées sont fictives et générées automatiquement
    - Toute modification sera perdue au rafraîchissement de la page
    - Cette version ne nécessite pas de backend API

    **Classification des notes :**
    - 🟢 **Maîtrisée** : ≥ 14/20
    - 🟡 **En cours** : 10-14/20
    - 🔴 **À renforcer** : < 10/20
    """)

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; font-size: 0.9rem;">
    <p>EduTrack IA v1.0 • Mode Démonstration • Données fictives</p>
</div>
""", unsafe_allow_html=True)
