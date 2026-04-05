# frontend/streamlit/pages/4_🎯_Compétences.py
"""
EduTrack IA - Competencies Management Page
"""

import streamlit as st
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from frontend.shared.styles.theme import apply_custom_css, COLORS, create_badge
from frontend.streamlit.utils.helpers import calculate_competency_stats

st.set_page_config(page_title="Compétences - EduTrack IA", page_icon="🎯", layout="wide")
apply_custom_css()

if 'data_loaded' not in st.session_state:
    st.error("⚠️ Données non chargées. Veuillez retourner à la page principale.")
    st.stop()

# Header
st.markdown(f"""
<div style="background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['info']} 100%);
            padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1 style="margin: 0;">🎯 Référentiel de Compétences</h1>
    <p style="margin: 0.5rem 0 0 0;">Gestion et organisation des compétences pédagogiques</p>
</div>
""", unsafe_allow_html=True)

# Statistics
col1, col2, col3 = st.columns(3)

with col1:
    total_comps = len(st.session_state.competencies)
    st.metric("📚 Total compétences", total_comps)

with col2:
    subjects_count = st.session_state.competencies['subject'].nunique()
    st.metric("📖 Matières", subjects_count)

with col3:
    categories_count = st.session_state.competencies['category'].nunique()
    st.metric("🏷️ Catégories", categories_count)

st.markdown("<br>", unsafe_allow_html=True)

# Filter and search
col1, col2 = st.columns([2, 1])

with col1:
    search_term = st.text_input("🔍 Rechercher une compétence", placeholder="Entrez un mot-clé...")

with col2:
    category_filter = st.selectbox(
        "Catégorie",
        ["Toutes"] + sorted(st.session_state.competencies['category'].unique().tolist())
    )

# Subject filter tabs
subjects = sorted(st.session_state.competencies['subject'].unique().tolist())
selected_subject = st.selectbox("📚 Filtrer par matière", ["Toutes les matières"] + subjects)

# Apply filters
filtered_comps = st.session_state.competencies.copy()

if search_term:
    filtered_comps = filtered_comps[
        filtered_comps['name'].str.contains(search_term, case=False)
    ]

if category_filter != "Toutes":
    filtered_comps = filtered_comps[filtered_comps['category'] == category_filter]

if selected_subject != "Toutes les matières":
    filtered_comps = filtered_comps[filtered_comps['subject'] == selected_subject]

st.markdown(f"### 📋 Compétences ({len(filtered_comps)} résultats)")

# Calculate statistics for each competency
comp_stats = calculate_competency_stats(st.session_state.grades, filtered_comps)

# Group by subject
for subject in filtered_comps['subject'].unique():
    with st.expander(f"📖 {subject}", expanded=(selected_subject == subject)):
        subject_comps = filtered_comps[filtered_comps['subject'] == subject]
        
        for _, comp in subject_comps.iterrows():
            # Get stats for this competency
            comp_stat = comp_stats[comp_stats['competency_id'] == comp['id']]
            
            if len(comp_stat) > 0:
                stat = comp_stat.iloc[0]
                avg = stat['average']
                count = stat['count']
                emoji = stat['emoji']
                level = stat['level']
                
                avg_color = COLORS['success'] if avg >= 14 else COLORS['warning'] if avg >= 10 else COLORS['danger']
                
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; 
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 0.75rem;
                            border-left: 3px solid {avg_color};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: {COLORS['dark']};">{comp['name']}</h4>
                            <p style="color: #6B7280; margin: 0.25rem 0; font-size: 0.9rem;">
                                <span style="background: {COLORS['light']}; padding: 0.2rem 0.5rem; border-radius: 4px;">
                                    {comp['level']}
                                </span>
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.5rem;">{emoji}</div>
                            <div style="font-size: 1.2rem; font-weight: bold;">{avg:.1f}/20</div>
                            <div style="font-size: 0.8rem; color: #6B7280;">{count} évals</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # No grades for this competency
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; 
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 0.75rem;
                            border-left: 3px solid {COLORS['info']}; opacity: 0.7;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: {COLORS['dark']};">{comp['name']}</h4>
                            <p style="color: #6B7280; margin: 0.25rem 0; font-size: 0.9rem;">
                                <span style="background: {COLORS['light']}; padding: 0.2rem 0.5rem; border-radius: 4px;">
                                    {comp['level']}
                                </span>
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.9rem; color: #9CA3AF;">Non évaluée</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Add new competency section
with st.expander("➕ Ajouter une nouvelle compétence"):
    st.info("🔧 Fonctionnalité disponible en mode production avec backend API")
    
    with st.form("new_competency_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Nom de la compétence *", placeholder="ex: Résolution d'équations du second degré")
            new_category = st.selectbox("Catégorie *", ["Sciences", "Langues", "Humanités", "Techniques"])
        
        with col2:
            new_subject = st.text_input("Matière *", placeholder="ex: Mathématiques")
            new_level = st.selectbox("Niveau *", ["Fondamental", "Intermédiaire", "Avancé"])
        
        new_description = st.text_area("Description (optionnel)", placeholder="Description détaillée de la compétence...")
        
        submitted = st.form_submit_button("Ajouter la compétence", type="primary")
        
        if submitted:
            if new_name and new_subject:
                st.success(f"✅ Compétence '{new_name}' ajoutée avec succès!")
                st.info("Note: En mode démonstration, les changements ne sont pas persistants.")
            else:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")

# Summary statistics
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📊 Statistiques Globales")

if len(comp_stats) > 0:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        maitrisees = len(comp_stats[comp_stats['level'] == 'maîtrisée'])
        st.metric("🟢 Compétences maîtrisées", maitrisees, f"{maitrisees/len(comp_stats)*100:.0f}%")
    
    with col2:
        en_cours = len(comp_stats[comp_stats['level'] == 'en cours'])
        st.metric("🟡 Compétences en cours", en_cours, f"{en_cours/len(comp_stats)*100:.0f}%")
    
    with col3:
        a_renforcer = len(comp_stats[comp_stats['level'] == 'à renforcer'])
        st.metric("🔴 Compétences à renforcer", a_renforcer, f"{a_renforcer/len(comp_stats)*100:.0f}%")
else:
    st.info("Aucune statistique disponible. Commencez par évaluer des compétences.")
