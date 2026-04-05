"""
Page Compétences - Vue Parent
Visualisation radar des compétences par matière
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from frontend.shared.data.mock_data import (
    get_students,
    get_evaluations_for_student,
    get_student_competencies
)
from frontend.shared.styles.theme import apply_custom_theme, get_color_scheme

# Importer le composant radar (avec gestion d'erreur)
try:
    from frontend.streamlit.components.competency_radar import create_competency_radar
except ImportError:
    create_competency_radar = None

st.set_page_config(
    page_title="Compétences - Vue Parent",
    page_icon="🎯",
    layout="wide"
)

apply_custom_theme()
colors = get_color_scheme()

# Vérifier que l'étudiant est sélectionné
if 'selected_student_id' not in st.session_state or not st.session_state.selected_student_id:
    st.error("❌ Veuillez sélectionner un étudiant depuis la page d'accueil")
    if st.button("🏠 Retour à l'accueil"):
        st.switch_page("app.py")
    st.stop()

# Récupérer les données
students = get_students()
student = next((s for s in students if s['id'] == st.session_state.selected_student_id), None)

if not student:
    st.error("❌ Étudiant non trouvé")
    st.stop()

# En-tête
st.title(f"🎯 Compétences - {student['prenom']} {student['nom']}")
st.markdown(f"**Classe :** {student['classe']} | **Dernière mise à jour :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
st.markdown("---")

# Info box pour les parents
st.info("""
🎯 **Comprendre le radar de compétences**

Cette visualisation montre le niveau de maîtrise de votre enfant dans différentes compétences.
Plus le point est éloigné du centre, meilleure est la maîtrise.

**Niveaux de maîtrise :**
- 🔴 **Rouge (0-10)** : Compétence à acquérir
- 🟠 **Orange (10-14)** : Compétence en cours d'acquisition
- 🟢 **Vert (14-18)** : Compétence maîtrisée
- 🌟 **Vert foncé (18-20)** : Compétence excellente
""")

st.markdown("<br>", unsafe_allow_html=True)

# Récupérer les compétences
competencies = get_student_competencies(st.session_state.selected_student_id)

if not competencies:
    st.warning("📭 Aucune donnée de compétence disponible pour le moment")
    st.stop()

# Organiser les compétences par matière
comp_df = pd.DataFrame(competencies)
subjects = comp_df['matiere'].unique()

# Section 1: Radar global toutes matières
st.subheader("🌐 Vue globale des compétences")

# Créer un radar avec toutes les compétences
if create_competency_radar:
    try:
        all_comp_data = [
            {
                'competence': f"{row['matiere'][:3]}. {row['competence'][:20]}",
                'niveau': row['niveau']
            }
            for _, row in comp_df.iterrows()
        ]
        
        fig = create_competency_radar(all_comp_data[:15])  # Limiter à 15 pour la lisibilité
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Impossible d'afficher le radar global: {str(e)}")
        # Fallback: afficher un graphique simple
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=comp_df['niveau'][:15],
            theta=[f"{row['matiere'][:10]}" for _, row in comp_df.head(15).iterrows()],
            fill='toself',
            name='Niveau'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 20])),
            showlegend=False,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
else:
    # Fallback si le composant n'est pas disponible
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=comp_df['niveau'][:15],
        theta=[f"{row['matiere'][:10]} - {row['competence'][:15]}" for _, row in comp_df.head(15).iterrows()],
        fill='toself',
        marker=dict(color=colors['primary'])
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 20]
            )
        ),
        showlegend=False,
        height=500,
        title="Niveau de maîtrise des compétences"
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Détail par matière
st.subheader("📚 Compétences par matière")

# Sélecteur de matière
selected_subject = st.selectbox(
    "Sélectionnez une matière pour voir le détail :",
    subjects,
    index=0
)

subject_comp = comp_df[comp_df['matiere'] == selected_subject]

col1, col2 = st.columns([2, 1])

with col1:
    # Radar pour cette matière
    if create_competency_radar:
        try:
            subject_data = [
                {'competence': row['competence'], 'niveau': row['niveau']}
                for _, row in subject_comp.iterrows()
            ]
            fig = create_competency_radar(subject_data)
            st.plotly_chart(fig, use_container_width=True)
        except:
            # Fallback
            import plotly.graph_objects as go
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=subject_comp['niveau'],
                theta=subject_comp['competence'],
                fill='toself',
                marker=dict(color=colors['secondary'])
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 20])),
                showlegend=False,
                title=f"Compétences en {selected_subject}"
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        # Fallback
        import plotly.graph_objects as go
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=subject_comp['niveau'],
            theta=subject_comp['competence'],
            fill='toself',
            marker=dict(color=colors['secondary'])
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 20])),
            showlegend=False,
            title=f"Compétences en {selected_subject}"
        )
        
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"### 📊 Statistiques - {selected_subject}")
    
    avg_niveau = subject_comp['niveau'].mean()
    max_niveau = subject_comp['niveau'].max()
    min_niveau = subject_comp['niveau'].min()
    
    st.metric("Niveau moyen", f"{avg_niveau:.1f}/20")
    st.metric("Meilleure compétence", f"{max_niveau:.1f}/20")
    st.metric("Compétence à travailler", f"{min_niveau:.1f}/20")
    
    # Répartition par niveau de maîtrise
    excellent = len(subject_comp[subject_comp['niveau'] >= 16])
    bon = len(subject_comp[(subject_comp['niveau'] >= 12) & (subject_comp['niveau'] < 16)])
    moyen = len(subject_comp[subject_comp['niveau'] < 12])
    
    st.markdown("---")
    st.markdown("**Répartition :**")
    st.markdown(f"🌟 Excellentes : {excellent}")
    st.markdown(f"✅ Bonnes : {bon}")
    st.markdown(f"📈 À améliorer : {moyen}")

st.markdown("<br>", unsafe_allow_html=True)

# Section 3: Tableau détaillé des compétences pour la matière sélectionnée
st.markdown(f"#### 📋 Détail des compétences - {selected_subject}")

# Préparer le dataframe pour l'affichage
display_comp = subject_comp.copy()
display_comp['Niveau'] = display_comp['niveau'].apply(lambda x: f"{x:.1f}/20")
display_comp['Maîtrise'] = display_comp['niveau'].apply(
    lambda x: "🌟 Excellente" if x >= 18 else
              "🟢 Maîtrisée" if x >= 14 else
              "🟠 En cours" if x >= 10 else
              "🔴 À acquérir"
)
display_comp['Compétence'] = display_comp['competence']

# Colorer les lignes selon le niveau
def color_mastery(row):
    niveau = float(row['Niveau'].split('/')[0])
    if niveau >= 18:
        return ['background-color: #d4edda'] * len(row)
    elif niveau >= 14:
        return ['background-color: #d1f0d1'] * len(row)
    elif niveau >= 10:
        return ['background-color: #fff3cd'] * len(row)
    else:
        return ['background-color: #f8d7da'] * len(row)

styled_df = display_comp[['Compétence', 'Niveau', 'Maîtrise']].style.apply(color_mastery, axis=1)

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Section 4: Comparaison entre matières
st.subheader("📊 Comparaison entre matières")

# Calculer les moyennes par matière
moyennes_comp = comp_df.groupby('matiere')['niveau'].mean().reset_index()
moyennes_comp.columns = ['Matière', 'Niveau moyen']
moyennes_comp = moyennes_comp.sort_values('Niveau moyen', ascending=False)

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=moyennes_comp['Matière'],
    y=moyennes_comp['Niveau moyen'],
    text=moyennes_comp['Niveau moyen'].apply(lambda x: f"{x:.1f}"),
    textposition='auto',
    marker=dict(
        color=moyennes_comp['Niveau moyen'],
        colorscale=[[0, 'red'], [0.5, 'orange'], [0.75, 'lightgreen'], [1, 'green']],
        cmin=0,
        cmax=20,
        showscale=False
    ),
    hovertemplate='<b>%{x}</b><br>Niveau: %{y:.2f}/20<extra></extra>'
))

fig.update_layout(
    title="Niveau moyen de maîtrise par matière",
    xaxis_title="Matière",
    yaxis_title="Niveau moyen (/20)",
    yaxis=dict(range=[0, 20]),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 5: Recommandations pour les parents
st.subheader("💡 Recommandations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**✅ Points forts à encourager**")
    
    # Trouver les 3 meilleures compétences
    top_comp = comp_df.nlargest(3, 'niveau')
    
    for _, comp in top_comp.iterrows():
        st.success(f"🌟 **{comp['matiere']}** - {comp['competence']}: {comp['niveau']:.1f}/20")
    
    st.info("💪 Continuez à encourager votre enfant dans ces domaines où il/elle excelle!")

with col2:
    st.markdown("**📈 Axes d'amélioration**")
    
    # Trouver les 3 compétences à améliorer
    weak_comp = comp_df.nsmallest(3, 'niveau')
    
    for _, comp in weak_comp.iterrows():
        if comp['niveau'] < 12:
            st.warning(f"📚 **{comp['matiere']}** - {comp['competence']}: {comp['niveau']:.1f}/20")
        else:
            st.info(f"📊 **{comp['matiere']}** - {comp['competence']}: {comp['niveau']:.1f}/20")
    
    st.info("💡 Un accompagnement ciblé sur ces compétences peut aider à progresser!")

# Footer
st.markdown("---")
st.markdown("""
<div style='background-color: #e7f3ff; border-left: 5px solid #2196F3; padding: 15px; border-radius: 5px;'>
    <h4 style='margin-top: 0;'>📘 Pour les parents : Comment aider votre enfant ?</h4>
    <ul>
        <li>✅ <b>Valorisez les progrès</b> : Célébrez chaque amélioration, même petite</li>
        <li>📚 <b>Routine d'étude</b> : Établissez un moment régulier pour les devoirs</li>
        <li>🤝 <b>Dialogue avec l'enseignant</b> : N'hésitez pas à demander des conseils spécifiques</li>
        <li>🎯 <b>Objectifs réalistes</b> : Fixez des objectifs atteignables avec votre enfant</li>
        <li>💪 <b>Encouragements</b> : L'effort est aussi important que le résultat</li>
    </ul>
</div>
""", unsafe_allow_html=True)
