"""
Vue Parent - EduTrack IA
Application Streamlit simplifiée pour les parents
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from frontend.shared.data.mock_data import (
    get_students,
    get_evaluations_for_student,
    get_student_stats
)
from frontend.shared.styles.theme import apply_custom_theme, get_color_scheme

# Configuration de la page
st.set_page_config(
    page_title="Vue Parent - EduTrack IA",
    page_icon="👨‍👩‍👧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le thème
apply_custom_theme()
colors = get_color_scheme()

# Initialiser session state
if 'selected_student_id' not in st.session_state:
    st.session_state.selected_student_id = None

# Sidebar - Sélection d'étudiant
with st.sidebar:
    st.title("👨‍👩‍👧 Vue Parent")
    st.markdown("---")
    
    st.info("👋 Interface simplifiée pour suivre la progression de votre enfant")
    
    # Simuler une connexion parent (plusieurs enfants possibles)
    students = get_students()
    
    st.subheader("Sélectionner votre enfant")
    
    student_options = {f"{s['nom']} {s['prenom']} ({s['classe']})": s['id'] 
                      for s in students}
    
    selected_option = st.selectbox(
        "Enfant",
        options=list(student_options.keys()),
        index=0 if student_options else None,
        label_visibility="collapsed"
    )
    
    if selected_option:
        st.session_state.selected_student_id = student_options[selected_option]
    
    st.markdown("---")
    
    # Navigation rapide
    st.markdown("### 🧭 Navigation")
    st.page_link("app.py", label="🏠 Accueil", icon="🏠")
    st.page_link("pages/1_📊_Vue_d_ensemble.py", label="📊 Vue d'ensemble", icon="📊")
    st.page_link("pages/2_🎯_Compétences.py", label="🎯 Compétences", icon="🎯")
    st.page_link("pages/3_📈_Historique.py", label="📈 Historique", icon="📈")
    st.page_link("pages/4_📋_Rapports.py", label="📋 Rapports", icon="📋")
    
    st.markdown("---")
    st.caption("🔒 Interface en lecture seule")
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y')}")

# Contenu principal
if not st.session_state.selected_student_id:
    st.warning("⚠️ Veuillez sélectionner un étudiant dans la barre latérale")
    st.stop()

# Récupérer les données de l'étudiant
student = next((s for s in students if s['id'] == st.session_state.selected_student_id), None)

if not student:
    st.error("❌ Étudiant non trouvé")
    st.stop()

# En-tête
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.title(f"👋 Bienvenue, parent de {student['prenom']} !")
    st.markdown(f"**Classe :** {student['classe']} | **Année scolaire :** 2024-2025")

with col2:
    st.metric("Dernière mise à jour", datetime.now().strftime("%d/%m/%Y"))

with col3:
    st.button("🔄 Actualiser", use_container_width=True)

st.markdown("---")

# Section 1: Aperçu de l'étudiant
st.subheader("👤 Profil de l'étudiant")

col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    # Photo placeholder
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
                    border-radius: 15px; padding: 60px 20px; text-align: center; color: white;
                    font-size: 48px; font-weight: bold;'>
            {student['prenom'][0]}{student['nom'][0]}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(f"**Nom complet :** {student['nom']} {student['prenom']}")
    st.markdown(f"**Classe :** {student['classe']}")
    st.markdown(f"**Âge :** {student.get('age', 'N/A')} ans")
    
with col3:
    stats = get_student_stats(st.session_state.selected_student_id)
    avg = stats.get('moyenne_generale', 0)
    
    # Afficher la moyenne avec couleur
    if avg >= 16:
        color = "green"
        emoji = "🌟"
    elif avg >= 14:
        color = "lightgreen"
        emoji = "✅"
    elif avg >= 12:
        color = "orange"
        emoji = "📊"
    else:
        color = color
        emoji = "📉"
    
    st.markdown(
        f"""
        <div style='background-color: {color}20; border-left: 5px solid {color};
                    padding: 20px; border-radius: 10px;'>
            <h3 style='margin: 0; color: {color};'>{emoji} Moyenne générale</h3>
            <h1 style='margin: 10px 0; color: {color};'>{avg:.2f}/20</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Statistiques rapides
st.subheader("📊 Statistiques rapides")

evaluations = get_evaluations_for_student(st.session_state.selected_student_id)
eval_df = pd.DataFrame(evaluations)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Moyenne générale",
        f"{avg:.2f}/20",
        delta=f"+{stats.get('evolution', 0):.2f}" if stats.get('evolution', 0) > 0 else f"{stats.get('evolution', 0):.2f}"
    )

with col2:
    trend = stats.get('tendance', 'stable')
    trend_emoji = "📈" if trend == "hausse" else "📉" if trend == "baisse" else "➡️"
    st.metric(
        "Tendance",
        trend.capitalize(),
        delta=trend_emoji
    )

with col3:
    total_evals = len(evaluations)
    st.metric(
        "Évaluations",
        total_evals,
        delta="Total"
    )

with col4:
    # Prochaine évaluation simulée
    next_eval_date = (datetime.now() + timedelta(days=5)).strftime("%d/%m")
    st.metric(
        "Prochaine éval.",
        next_eval_date,
        delta="Mathématiques"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Section 3: Performance récente
st.subheader("📈 Performance récente")

if not evaluations:
    st.info("📭 Aucune évaluation disponible pour le moment")
else:
    # Prendre les 5 dernières évaluations
    recent_evals = sorted(evaluations, key=lambda x: x['date'], reverse=True)[:5]
    recent_df = pd.DataFrame(recent_evals)
    
    # Graphique en barres
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=recent_df['matiere'],
        y=recent_df['note'],
        text=recent_df['note'].apply(lambda x: f"{x:.1f}"),
        textposition='auto',
        marker=dict(
            color=recent_df['note'],
            colorscale=[[0, 'red'], [0.5, 'orange'], [0.75, 'lightgreen'], [1, 'green']],
            cmin=0,
            cmax=20,
            showscale=False
        ),
        hovertemplate='<b>%{x}</b><br>Note: %{y:.2f}/20<extra></extra>'
    ))
    
    fig.update_layout(
        title="5 dernières évaluations",
        xaxis_title="Matière",
        yaxis_title="Note (/20)",
        yaxis=dict(range=[0, 20]),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 4: Navigation vers les pages détaillées
st.subheader("🧭 Explorer plus en détail")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📊 Vue d'ensemble", use_container_width=True):
        st.switch_page("pages/1_📊_Vue_d_ensemble.py")
    st.caption("Statistiques générales et moyennes par matière")

with col2:
    if st.button("🎯 Compétences", use_container_width=True):
        st.switch_page("pages/2_🎯_Compétences.py")
    st.caption("Radar des compétences acquises")

with col3:
    if st.button("📈 Historique", use_container_width=True):
        st.switch_page("pages/3_📈_Historique.py")
    st.caption("Évolution des notes au fil du temps")

with col4:
    if st.button("📋 Rapports", use_container_width=True):
        st.switch_page("pages/4_📋_Rapports.py")
    st.caption("Bulletins et observations des enseignants")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>💡 <b>Astuce :</b> Cette interface est mise à jour automatiquement après chaque évaluation.</p>
        <p>📧 Pour toute question, contactez l'enseignant via l'établissement.</p>
        <p style='font-size: 12px; margin-top: 20px;'>
            EduTrack IA - Plateforme de suivi scolaire avec intelligence artificielle<br>
            © 2024 - Interface Parents
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
