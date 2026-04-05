# frontend/streamlit/pages/1_🏠_Accueil.py
"""
EduTrack IA - Home/Dashboard Page
"""

import streamlit as st
import sys
import os
import pandas as pd
import calendar
from datetime import datetime

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
)

from frontend.shared.styles.theme import apply_custom_css  # noqa: E402
from frontend.streamlit.components.alert_banner import (  # noqa: E402
    display_student_alerts,
)
from frontend.streamlit.components.grade_chart import (  # noqa: E402
    display_grade_distribution,
)

st.set_page_config(
    page_title="Accueil - EduTrack IA", page_icon="🏠", layout="wide"
)
apply_custom_css()

# Check if data is loaded
if 'data_loaded' not in st.session_state:
    st.error(
        "⚠️ Données non chargées. Veuillez retourner à la page principale."
    )
    st.stop()

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
display_student_alerts(st.session_state.students, st.session_state.grades)
display_grade_distribution(st.session_state.grades)
