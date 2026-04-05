"""
Page Historique - Vue Parent
Évolution des notes au fil du temps
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from frontend.shared.data.mock_data import (
    get_students,
    get_evaluations_for_student
)
from frontend.shared.styles.theme import apply_custom_theme, get_color_scheme

# Importer le composant de graphique (avec gestion d'erreur)
try:
    from frontend.streamlit.components.grade_chart import create_grade_evolution_chart
except ImportError:
    create_grade_evolution_chart = None

st.set_page_config(
    page_title="Historique - Vue Parent",
    page_icon="📈",
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
st.title(f"📈 Historique des notes - {student['prenom']} {student['nom']}")
st.markdown(f"**Classe :** {student['classe']} | **Dernière mise à jour :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}")
st.markdown("---")

# Récupérer les évaluations
evaluations = get_evaluations_for_student(st.session_state.selected_student_id)

if not evaluations:
    st.warning("📭 Aucune évaluation disponible pour le moment")
    st.stop()

# Préparer le DataFrame
eval_df = pd.DataFrame(evaluations)
eval_df['date'] = pd.to_datetime(eval_df['date'])
eval_df = eval_df.sort_values('date')

# Section de filtres
st.subheader("🔍 Filtres")

col1, col2, col3 = st.columns(3)

with col1:
    # Filtre par matière
    all_subjects = ["Toutes les matières"] + sorted(eval_df['matiere'].unique().tolist())
    selected_subject = st.selectbox("Matière", all_subjects)

with col2:
    # Filtre par période
    min_date = eval_df['date'].min().date()
    max_date = eval_df['date'].max().date()
    
    date_start = st.date_input(
        "Date de début",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

with col3:
    date_end = st.date_input(
        "Date de fin",
        value=max_date,
        min_value=min_date,
        max_value=max_date
    )

# Appliquer les filtres
filtered_df = eval_df.copy()

if selected_subject != "Toutes les matières":
    filtered_df = filtered_df[filtered_df['matiere'] == selected_subject]

filtered_df = filtered_df[
    (filtered_df['date'].dt.date >= date_start) & 
    (filtered_df['date'].dt.date <= date_end)
]

if filtered_df.empty:
    st.warning("⚠️ Aucune évaluation ne correspond aux filtres sélectionnés")
    st.stop()

st.markdown("---")

# Section 1: Graphique d'évolution
st.subheader("📈 Évolution des notes")

# Créer le graphique
if create_grade_evolution_chart:
    try:
        # Préparer les données pour le composant
        chart_data = filtered_df[['date', 'note', 'matiere']].copy()
        chart_data['date'] = chart_data['date'].dt.strftime('%Y-%m-%d')
        
        fig = create_grade_evolution_chart(
            chart_data.to_dict('records'),
            show_average=True
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"⚠️ Impossible d'utiliser le composant grade_chart: {str(e)}")
        create_grade_evolution_chart = None

if not create_grade_evolution_chart:
    # Fallback: créer un graphique simple
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    if selected_subject == "Toutes les matières":
        # Afficher toutes les matières
        for matiere in filtered_df['matiere'].unique():
            subject_data = filtered_df[filtered_df['matiere'] == matiere]
            
            fig.add_trace(go.Scatter(
                x=subject_data['date'],
                y=subject_data['note'],
                mode='lines+markers',
                name=matiere,
                hovertemplate='<b>%{fullData.name}</b><br>Date: %{x|%d/%m/%Y}<br>Note: %{y:.2f}/20<extra></extra>'
            ))
    else:
        # Afficher une seule matière
        fig.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['note'],
            mode='lines+markers',
            name=selected_subject,
            marker=dict(size=10, color=colors['primary']),
            line=dict(width=3, color=colors['primary']),
            hovertemplate='Date: %{x|%d/%m/%Y}<br>Note: %{y:.2f}/20<extra></extra>'
        ))
    
    # Ajouter une ligne de moyenne
    avg = filtered_df['note'].mean()
    fig.add_hline(
        y=avg,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Moyenne: {avg:.2f}",
        annotation_position="right"
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Note (/20)",
        yaxis=dict(range=[0, 20]),
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Statistiques
st.subheader("📊 Statistiques de la période")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    avg = filtered_df['note'].mean()
    st.metric("Moyenne", f"{avg:.2f}/20")

with col2:
    max_note = filtered_df['note'].max()
    st.metric("Note maximale", f"{max_note:.2f}/20")

with col3:
    min_note = filtered_df['note'].min()
    st.metric("Note minimale", f"{min_note:.2f}/20")

with col4:
    std = filtered_df['note'].std()
    st.metric("Écart-type", f"{std:.2f}")

with col5:
    nb_evals = len(filtered_df)
    st.metric("Nb. évaluations", nb_evals)

st.markdown("<br>", unsafe_allow_html=True)

# Section 3: Analyse de tendance
st.subheader("📉 Analyse de tendance")

col1, col2 = st.columns(2)

with col1:
    # Calculer la tendance
    if len(filtered_df) >= 2:
        # Régression linéaire simple
        x = range(len(filtered_df))
        y = filtered_df['note'].values
        
        # Calcul de la pente
        x_mean = sum(x) / len(x)
        y_mean = sum(y) / len(y)
        
        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(len(x)))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(len(x)))
        
        if denominator != 0:
            slope = numerator / denominator
            
            if slope > 0.1:
                trend = "📈 En progression"
                trend_color = "green"
                advice = "Excellent ! Votre enfant progresse régulièrement."
            elif slope < -0.1:
                trend = "📉 En baisse"
                trend_color = "red"
                advice = "Attention, les résultats baissent. Un accompagnement peut être nécessaire."
            else:
                trend = "➡️ Stable"
                trend_color = "orange"
                advice = "Les résultats sont stables. Continuez ainsi !"
            
            st.markdown(
                f"""
                <div style='background-color: {trend_color}20; border-left: 5px solid {trend_color};
                            padding: 20px; border-radius: 10px;'>
                    <h3 style='margin: 0; color: {trend_color};'>{trend}</h3>
                    <p style='margin: 10px 0;'>Pente: {slope:+.3f} points par évaluation</p>
                    <p style='margin: 5px 0; font-style: italic;'>{advice}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.info("Pas assez de données pour calculer la tendance")
    else:
        st.info("Au moins 2 évaluations sont nécessaires pour l'analyse de tendance")

with col2:
    # Distribution des notes
    st.markdown("**📊 Répartition des notes**")
    
    excellent = len(filtered_df[filtered_df['note'] >= 16])
    tres_bien = len(filtered_df[(filtered_df['note'] >= 14) & (filtered_df['note'] < 16)])
    bien = len(filtered_df[(filtered_df['note'] >= 12) & (filtered_df['note'] < 14)])
    assez_bien = len(filtered_df[(filtered_df['note'] >= 10) & (filtered_df['note'] < 12)])
    insuffisant = len(filtered_df[filtered_df['note'] < 10])
    
    import plotly.graph_objects as go
    
    fig = go.Figure(data=[go.Pie(
        labels=['Excellent (≥16)', 'Très bien (14-16)', 'Bien (12-14)', 
                'Assez bien (10-12)', 'Insuffisant (<10)'],
        values=[excellent, tres_bien, bien, assez_bien, insuffisant],
        marker=dict(colors=['green', 'lightgreen', 'yellow', 'orange', 'red']),
        hole=0.4
    )])
    
    fig.update_layout(
        height=300,
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 4: Évolution par matière (si toutes les matières)
if selected_subject == "Toutes les matières":
    st.subheader("📚 Évolution par matière")
    
    # Calculer les moyennes par matière et période
    matiere_stats = []
    
    for matiere in filtered_df['matiere'].unique():
        matiere_data = filtered_df[filtered_df['matiere'] == matiere]
        
        # Diviser en deux périodes
        mid_date = matiere_data['date'].min() + (matiere_data['date'].max() - matiere_data['date'].min()) / 2
        
        periode1 = matiere_data[matiere_data['date'] <= mid_date]
        periode2 = matiere_data[matiere_data['date'] > mid_date]
        
        avg1 = periode1['note'].mean() if len(periode1) > 0 else 0
        avg2 = periode2['note'].mean() if len(periode2) > 0 else avg1
        
        evolution = avg2 - avg1
        
        matiere_stats.append({
            'Matière': matiere,
            'Moyenne début': avg1,
            'Moyenne fin': avg2,
            'Évolution': evolution
        })
    
    stats_df = pd.DataFrame(matiere_stats)
    stats_df = stats_df.sort_values('Évolution', ascending=False)
    
    # Graphique d'évolution par matière
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Moyenne début',
        x=stats_df['Matière'],
        y=stats_df['Moyenne début'],
        marker_color='lightblue'
    ))
    
    fig.add_trace(go.Bar(
        name='Moyenne fin',
        x=stats_df['Matière'],
        y=stats_df['Moyenne fin'],
        marker_color='darkblue'
    ))
    
    fig.update_layout(
        barmode='group',
        xaxis_title="Matière",
        yaxis_title="Moyenne (/20)",
        yaxis=dict(range=[0, 20]),
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau avec les évolutions
    display_stats = stats_df.copy()
    display_stats['Moyenne début'] = display_stats['Moyenne début'].apply(lambda x: f"{x:.2f}")
    display_stats['Moyenne fin'] = display_stats['Moyenne fin'].apply(lambda x: f"{x:.2f}")
    display_stats['Évolution'] = display_stats['Évolution'].apply(
        lambda x: f"{x:+.2f} {'📈' if x > 0 else '📉' if x < 0 else '➡️'}"
    )
    
    st.dataframe(display_stats, hide_index=True, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Section 5: Tableau détaillé
st.subheader("📋 Détail des évaluations")

# Préparer le dataframe pour l'affichage
display_df = filtered_df.copy()
display_df['Date'] = display_df['date'].dt.strftime('%d/%m/%Y')
display_df['Matière'] = display_df['matiere']
display_df['Note'] = display_df['note'].apply(lambda x: f"{x:.2f}/20")
display_df['Appréciation'] = display_df['note'].apply(
    lambda x: "🌟 Excellent" if x >= 16 else
              "✅ Très bien" if x >= 14 else
              "👍 Bien" if x >= 12 else
              "📊 Assez bien" if x >= 10 else
              "📉 Insuffisant"
)

# Afficher le tableau (les plus récentes en premier)
display_df = display_df.sort_values('date', ascending=False)
display_df = display_df[['Date', 'Matière', 'Note', 'Appréciation']]

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    height=400
)

# Bouton d'export (simulé)
if st.button("📥 Exporter l'historique (CSV)", use_container_width=False):
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Télécharger le fichier CSV",
        data=csv,
        file_name=f"historique_{student['nom']}_{student['prenom']}_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv'
    )

# Footer
st.markdown("---")
st.info("""
💡 **Conseils pour interpréter l'historique :**
- 📈 Une tendance à la hausse montre que votre enfant progresse
- 📉 Une baisse peut indiquer un besoin d'accompagnement
- ➡️ Une stabilité est positive si la moyenne est satisfaisante
- 🎯 Regardez l'évolution sur le long terme plutôt que les notes isolées
""")
