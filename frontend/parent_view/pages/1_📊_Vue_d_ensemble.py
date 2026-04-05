"""
Page Vue d'ensemble - Vue Parent
Aperçu général des performances de l'étudiant
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from frontend.shared.data.mock_data import (
    get_students,
    get_evaluations_for_student,
    get_student_stats
)
from frontend.shared.styles.theme import apply_custom_theme, get_color_scheme

st.set_page_config(
    page_title="Vue d'ensemble - Vue Parent",
    page_icon="📊",
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
st.title(f"📊 Vue d'ensemble - {student['prenom']} {student['nom']}")
st.markdown(f"**Classe :** {student['classe']} | **Dernière mise à jour :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
st.markdown("---")

# Récupérer les données
evaluations = get_evaluations_for_student(st.session_state.selected_student_id)
stats = get_student_stats(st.session_state.selected_student_id)

# Section 1: Carte d'information de l'étudiant
col1, col2 = st.columns([1, 3])

with col1:
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
                    border-radius: 15px; padding: 80px 20px; text-align: center; color: white;
                    font-size: 64px; font-weight: bold;'>
            {student['prenom'][0]}{student['nom'][0]}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("### 👤 Informations de l'étudiant")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown(f"**Nom complet :** {student['nom']} {student['prenom']}")
        st.markdown(f"**Classe :** {student['classe']}")
        st.markdown(f"**Nombre d'évaluations :** {len(evaluations)}")
    
    with info_col2:
        avg = stats.get('moyenne_generale', 0)
        trend = stats.get('tendance', 'stable')
        evolution = stats.get('evolution', 0)
        
        st.markdown(f"**Moyenne générale :** {avg:.2f}/20")
        st.markdown(f"**Tendance :** {trend.capitalize()} ({evolution:+.2f})")
        st.markdown(f"**Période :** Année scolaire 2024-2025")

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Moyenne générale avec indicateur de tendance
st.subheader("📈 Moyenne générale")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    # Affichage grand format de la moyenne
    if avg >= 16:
        color = "green"
        appreciation = "Excellent"
        emoji = "🌟"
    elif avg >= 14:
        color = "lightgreen"
        appreciation = "Très bien"
        emoji = "✅"
    elif avg >= 12:
        color = "orange"
        appreciation = "Bien"
        emoji = "👍"
    elif avg >= 10:
        color = "orange"
        appreciation = "Assez bien"
        emoji = "📊"
    else:
        color = "red"
        appreciation = "À améliorer"
        emoji = "📉"
    
    st.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {color}30, {color}10);
                    border: 3px solid {color}; border-radius: 20px; padding: 40px; text-align: center;'>
            <h1 style='margin: 0; font-size: 72px; color: {color};'>{avg:.2f}/20</h1>
            <h2 style='margin: 10px 0; color: {color};'>{emoji} {appreciation}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.metric(
        "Évolution",
        f"{evolution:+.2f} pts",
        delta=trend.capitalize()
    )
    st.metric(
        "Évaluations",
        len(evaluations),
        delta="Total"
    )

with col3:
    # Répartition des notes
    if evaluations:
        eval_df = pd.DataFrame(evaluations)
        excellent = len(eval_df[eval_df['note'] >= 16])
        bien = len(eval_df[(eval_df['note'] >= 12) & (eval_df['note'] < 16)])
        moyen = len(eval_df[eval_df['note'] < 12])
        
        st.metric("Excellentes", excellent, delta="≥ 16/20")
        st.metric("Bonnes", bien, delta="12-16/20")
        st.metric("À améliorer", moyen, delta="< 12/20")

st.markdown("<br>", unsafe_allow_html=True)

# Section 3: Moyennes par matière
st.subheader("📚 Moyennes par matière")

if not evaluations:
    st.info("📭 Aucune évaluation disponible pour le moment")
else:
    eval_df = pd.DataFrame(evaluations)
    
    # Calculer les moyennes par matière
    moyennes_par_matiere = eval_df.groupby('matiere')['note'].agg(['mean', 'count']).reset_index()
    moyennes_par_matiere.columns = ['Matière', 'Moyenne', 'Nb. évaluations']
    moyennes_par_matiere = moyennes_par_matiere.sort_values('Moyenne', ascending=False)
    
    # Graphique en barres horizontales
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=moyennes_par_matiere['Matière'],
        x=moyennes_par_matiere['Moyenne'],
        orientation='h',
        text=moyennes_par_matiere['Moyenne'].apply(lambda x: f"{x:.2f}"),
        textposition='auto',
        marker=dict(
            color=moyennes_par_matiere['Moyenne'],
            colorscale=[[0, 'red'], [0.5, 'orange'], [0.75, 'lightgreen'], [1, 'green']],
            cmin=0,
            cmax=20,
            showscale=True,
            colorbar=dict(title="Note")
        ),
        hovertemplate='<b>%{y}</b><br>Moyenne: %{x:.2f}/20<extra></extra>'
    ))
    
    fig.update_layout(
        title="Moyennes par matière",
        xaxis_title="Moyenne (/20)",
        yaxis_title="",
        xaxis=dict(range=[0, 20]),
        height=max(400, len(moyennes_par_matiere) * 40)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau détaillé
    st.markdown("#### 📋 Détail par matière")
    
    moyennes_par_matiere['Moyenne'] = moyennes_par_matiere['Moyenne'].apply(lambda x: f"{x:.2f}")
    moyennes_par_matiere['Appréciation'] = moyennes_par_matiere['Moyenne'].apply(
        lambda x: "🌟 Excellent" if float(x) >= 16 else 
                  "✅ Très bien" if float(x) >= 14 else
                  "👍 Bien" if float(x) >= 12 else
                  "📊 Assez bien" if float(x) >= 10 else
                  "📉 À améliorer"
    )
    
    st.dataframe(
        moyennes_par_matiere,
        hide_index=True,
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Section 4: Évaluations récentes
st.subheader("📝 Dernières évaluations")

if evaluations:
    # Prendre les 10 dernières
    recent_evals = sorted(evaluations, key=lambda x: x['date'], reverse=True)[:10]
    recent_df = pd.DataFrame(recent_evals)
    
    recent_df['Date'] = pd.to_datetime(recent_df['date']).dt.strftime('%d/%m/%Y')
    recent_df['Note'] = recent_df['note'].apply(lambda x: f"{x:.2f}/20")
    recent_df['Matière'] = recent_df['matiere']
    recent_df['Coefficient'] = recent_df.get('coefficient', 1)
    
    display_df = recent_df[['Date', 'Matière', 'Note', 'Coefficient']]
    
    st.dataframe(
        display_df,
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("📭 Aucune évaluation récente")

st.markdown("<br>", unsafe_allow_html=True)

# Section 5: Prochaines évaluations (simulées)
st.subheader("📅 Prochaines évaluations")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style='background-color: {colors['primary']}20; border-left: 5px solid {colors['primary']};
                    padding: 20px; border-radius: 10px; margin-bottom: 10px;'>
            <h4 style='margin: 0;'>📐 Mathématiques</h4>
            <p style='margin: 5px 0;'>Date: {(datetime.now() + timedelta(days=5)).strftime('%d/%m/%Y')}</p>
            <p style='margin: 5px 0; color: gray;'>Type: Contrôle - Coefficient 2</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style='background-color: {colors['secondary']}20; border-left: 5px solid {colors['secondary']};
                    padding: 20px; border-radius: 10px;'>
            <h4 style='margin: 0;'>🧪 Sciences Physiques</h4>
            <p style='margin: 5px 0;'>Date: {(datetime.now() + timedelta(days=8)).strftime('%d/%m/%Y')}</p>
            <p style='margin: 5px 0; color: gray;'>Type: TP - Coefficient 1</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style='background-color: {colors['accent']}20; border-left: 5px solid {colors['accent']};
                    padding: 20px; border-radius: 10px; margin-bottom: 10px;'>
            <h4 style='margin: 0;'>🇫🇷 Français</h4>
            <p style='margin: 5px 0;'>Date: {(datetime.now() + timedelta(days=12)).strftime('%d/%m/%Y')}</p>
            <p style='margin: 5px 0; color: gray;'>Type: Rédaction - Coefficient 3</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.info("💡 Les dates sont indicatives et peuvent être modifiées par l'enseignant.")

st.markdown("<br>", unsafe_allow_html=True)

# Section 6: Résumé de la progression
st.subheader("📊 Résumé de la progression")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Points forts 💪**")
    if evaluations:
        # Identifier les meilleures matières
        top_subjects = moyennes_par_matiere.head(3)
        for _, row in top_subjects.iterrows():
            st.success(f"✅ {row['Matière']}: {row['Moyenne']}/20")
    else:
        st.info("Pas encore de données")

with col2:
    st.markdown("**À améliorer 📈**")
    if evaluations:
        # Identifier les matières à améliorer
        weak_subjects = moyennes_par_matiere.tail(3)
        for _, row in weak_subjects.iterrows():
            if float(row['Moyenne']) < 12:
                st.warning(f"⚠️ {row['Matière']}: {row['Moyenne']}/20")
        if all(float(row['Moyenne']) >= 12 for _, row in moyennes_par_matiere.iterrows()):
            st.success("✅ Toutes les matières sont satisfaisantes!")
    else:
        st.info("Pas encore de données")

with col3:
    st.markdown("**Tendance générale 📊**")
    if trend == "hausse":
        st.success(f"📈 En progression (+{evolution:.2f} pts)")
        st.markdown("Continue comme ça ! 🌟")
    elif trend == "baisse":
        st.warning(f"📉 En baisse ({evolution:.2f} pts)")
        st.markdown("Un petit coup de pouce ? 💪")
    else:
        st.info(f"➡️ Stable ({evolution:+.2f} pts)")
        st.markdown("Régularité maintenue ✅")

# Footer
st.markdown("---")
st.info("💡 **Astuce pour les parents :** Cette vue d'ensemble vous permet de suivre les performances globales. Consultez les autres sections pour plus de détails sur les compétences et l'historique.")
