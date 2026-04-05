# frontend/streamlit/pages/7_✍️_Observations.py
"""
EduTrack IA - Teacher Observations Page
"""

import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from frontend.shared.styles.theme import apply_custom_css, COLORS
from frontend.streamlit.utils.helpers import format_date

st.set_page_config(page_title="Observations - EduTrack IA", page_icon="✍️", layout="wide")
apply_custom_css()

if 'data_loaded' not in st.session_state:
    st.error("⚠️ Données non chargées. Veuillez retourner à la page principale.")
    st.stop()

# Header
st.markdown(f"""
<div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['info']} 100%);
            padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1 style="margin: 0;">✍️ Observations Enseignant</h1>
    <p style="margin: 0.5rem 0 0 0;">Notes et commentaires sur la progression des élèves</p>
</div>
""", unsafe_allow_html=True)

# Statistics
col1, col2, col3 = st.columns(3)

with col1:
    total_obs = len(st.session_state.observations)
    st.metric("📝 Total observations", total_obs)

with col2:
    recent_obs = len(st.session_state.observations[
        pd.to_datetime(st.session_state.observations['observation_date']) > 
        pd.Timestamp.now() - pd.Timedelta(days=7)
    ])
    st.metric("📅 Cette semaine", recent_obs)

with col3:
    category_counts = st.session_state.observations['category'].value_counts()
    most_common = category_counts.index[0] if len(category_counts) > 0 else "N/A"
    st.metric("🏷️ Catégorie principale", most_common.capitalize())

st.markdown("<br>", unsafe_allow_html=True)

# Two column layout
col1, col2 = st.columns([1, 1])

with col1:
    # Add new observation
    st.markdown("### ➕ Nouvelle Observation")
    
    with st.form("new_observation_form", clear_on_submit=True):
        # Student selection
        students_list = st.session_state.students[st.session_state.students['is_active']].copy()
        students_list['full_name'] = students_list['first_name'] + ' ' + students_list['last_name'] + ' (' + students_list['class_name'] + ')'
        
        selected_student = st.selectbox(
            "Élève *",
            options=students_list['id'].tolist(),
            format_func=lambda x: students_list[students_list['id'] == x]['full_name'].iloc[0]
        )
        
        # Category selection
        category_icons = {
            "comportement": "👤 Comportement",
            "progrès": "📈 Progrès",
            "difficulté": "⚠️ Difficulté"
        }
        
        selected_category = st.selectbox(
            "Catégorie *",
            options=list(category_icons.keys()),
            format_func=lambda x: category_icons[x]
        )
        
        # Date
        obs_date = st.date_input(
            "Date de l'observation *",
            value=datetime.now()
        )
        
        # Content
        obs_content = st.text_area(
            "Observation *",
            placeholder="Décrivez votre observation...",
            height=150,
            max_chars=500
        )
        
        # Teacher name
        teacher_name = st.text_input(
            "Enseignant",
            value="M. Alaoui",
            disabled=True
        )
        
        # Submit button
        submitted = st.form_submit_button("💾 Enregistrer l'observation", type="primary", use_container_width=True)
        
        if submitted:
            if obs_content:
                # In real implementation, would save to database
                st.success(f"✅ Observation enregistrée pour {students_list[students_list['id'] == selected_student]['full_name'].iloc[0]}")
                st.info("Note: En mode démonstration, l'observation ne sera pas persistante.")
            else:
                st.error("❌ Veuillez saisir une observation.")

with col2:
    st.markdown("### 📋 Conseils de Rédaction")
    
    st.markdown(f"""
    <div style="background: {COLORS['light']}; padding: 1.5rem; border-radius: 8px; border-left: 4px solid {COLORS['info']};">
        <h4 style="margin-top: 0; color: {COLORS['primary']};">💡 Bonnes Pratiques</h4>
        
        <p><strong>👤 Comportement :</strong></p>
        <ul>
            <li>Niveau de participation en classe</li>
            <li>Attitude et motivation</li>
            <li>Respect des consignes</li>
        </ul>
        
        <p><strong>📈 Progrès :</strong></p>
        <ul>
            <li>Évolution depuis la dernière évaluation</li>
            <li>Compétences acquises</li>
            <li>Points forts constatés</li>
        </ul>
        
        <p><strong>⚠️ Difficulté :</strong></p>
        <ul>
            <li>Obstacles rencontrés</li>
            <li>Besoins de soutien identifiés</li>
            <li>Recommandations d'amélioration</li>
        </ul>
        
        <p style="margin-bottom: 0;"><em>💬 Restez factuel, constructif et bienveillant.</em></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Filters
st.markdown("### 🔍 Historique des Observations")

col1, col2, col3 = st.columns(3)

with col1:
    filter_student = st.selectbox(
        "Filtrer par élève",
        ["Tous les élèves"] + students_list['full_name'].tolist()
    )

with col2:
    filter_category = st.selectbox(
        "Filtrer par catégorie",
        ["Toutes"] + list(category_icons.values())
    )

with col3:
    filter_teacher = st.selectbox(
        "Filtrer par enseignant",
        ["Tous"] + st.session_state.observations['teacher_name'].unique().tolist()
    )

# Apply filters
filtered_obs = st.session_state.observations.copy()

if filter_student != "Tous les élèves":
    student_id = students_list[students_list['full_name'] == filter_student]['id'].iloc[0]
    filtered_obs = filtered_obs[filtered_obs['student_id'] == student_id]

if filter_category != "Toutes":
    category_key = [k for k, v in category_icons.items() if v == filter_category][0]
    filtered_obs = filtered_obs[filtered_obs['category'] == category_key]

if filter_teacher != "Tous":
    filtered_obs = filtered_obs[filtered_obs['teacher_name'] == filter_teacher]

# Sort by date (most recent first)
filtered_obs = filtered_obs.sort_values('observation_date', ascending=False)

st.markdown(f"**{len(filtered_obs)} observation(s) trouvée(s)**")

# Display observations
for _, obs in filtered_obs.iterrows():
    student = st.session_state.students[st.session_state.students['id'] == obs['student_id']].iloc[0]
    
    # Category styling
    category_colors = {
        "comportement": COLORS['info'],
        "progrès": COLORS['success'],
        "difficulté": COLORS['warning']
    }
    
    category_bg = {
        "comportement": "#DBEAFE",
        "progrès": "#D1FAE5",
        "difficulté": "#FEF3C7"
    }
    
    cat_color = category_colors.get(obs['category'], COLORS['info'])
    cat_bg = category_bg.get(obs['category'], COLORS['light'])
    
    st.markdown(f"""
    <div style="background: white; padding: 1.5rem; border-radius: 10px; 
                box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;
                border-left: 4px solid {cat_color};">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <h4 style="margin: 0; color: {COLORS['dark']};">
                    {student['first_name']} {student['last_name']}
                </h4>
                <p style="color: #6B7280; margin: 0.25rem 0; font-size: 0.9rem;">
                    📚 {student['class_name']}
                </p>
            </div>
            <div style="text-align: right;">
                <span style="background: {cat_bg}; color: {cat_color}; padding: 0.35rem 0.75rem; 
                           border-radius: 12px; font-size: 0.85rem; font-weight: 600;">
                    {category_icons[obs['category']]}
                </span>
            </div>
        </div>
        
        <p style="color: {COLORS['dark']}; line-height: 1.6; margin: 1rem 0;">
            {obs['content']}
        </p>
        
        <div style="display: flex; justify-content: space-between; align-items: center; 
                    padding-top: 0.75rem; border-top: 1px solid #E5E7EB;">
            <span style="color: #6B7280; font-size: 0.85rem;">
                👨‍🏫 {obs['teacher_name']}
            </span>
            <span style="color: #9CA3AF; font-size: 0.85rem;">
                📅 {format_date(obs['observation_date'], 'long')}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if len(filtered_obs) == 0:
    st.info("Aucune observation trouvée avec ces critères de filtrage.")

# Statistics by category
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📊 Statistiques par Catégorie")

col1, col2, col3 = st.columns(3)

category_counts = st.session_state.observations['category'].value_counts()

with col1:
    comportement_count = category_counts.get('comportement', 0)
    st.markdown(f"""
    <div style="background: #DBEAFE; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">👤</div>
        <div style="font-size: 2rem; font-weight: bold; color: {COLORS['info']};">{comportement_count}</div>
        <div style="color: {COLORS['info']}; font-weight: 600;">Comportement</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    progres_count = category_counts.get('progrès', 0)
    st.markdown(f"""
    <div style="background: #D1FAE5; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">📈</div>
        <div style="font-size: 2rem; font-weight: bold; color: {COLORS['success']};">{progres_count}</div>
        <div style="color: {COLORS['success']}; font-weight: 600;">Progrès</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    difficulte_count = category_counts.get('difficulté', 0)
    st.markdown(f"""
    <div style="background: #FEF3C7; padding: 1.5rem; border-radius: 10px; text-align: center;">
        <div style="font-size: 2rem;">⚠️</div>
        <div style="font-size: 2rem; font-weight: bold; color: {COLORS['warning']};">{difficulte_count}</div>
        <div style="color: {COLORS['warning']}; font-weight: 600;">Difficulté</div>
    </div>
    """, unsafe_allow_html=True)
