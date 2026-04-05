"""
Page Rapports - Vue Parent
Accès aux bulletins et rapports scolaires
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

# Importer le composant de prévisualisation (avec gestion d'erreur)
try:
    from frontend.streamlit.components.report_preview import create_report_preview
except ImportError:
    create_report_preview = None

st.set_page_config(
    page_title="Rapports - Vue Parent",
    page_icon="📋",
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
st.title(f"📋 Rapports et bulletins - {student['prenom']} {student['nom']}")
st.markdown(f"**Classe :** {student['classe']} | **Année scolaire :** 2024-2025")
st.markdown("---")

# Info pour les parents
st.info("""
📋 **Accès aux rapports scolaires**

Cette section vous permet de consulter tous les bulletins et rapports de votre enfant.
Vous pouvez prévisualiser et télécharger les documents en format PDF.
""")

st.markdown("<br>", unsafe_allow_html=True)

# Récupérer les données pour les statistiques
evaluations = get_evaluations_for_student(st.session_state.selected_student_id)
stats = get_student_stats(st.session_state.selected_student_id)

# Section 1: Bulletins trimestriels
st.subheader("📊 Bulletins trimestriels")

# Simuler des bulletins
bulletins = [
    {
        'periode': 'Trimestre 3',
        'date_debut': '01/04/2025',
        'date_fin': '30/06/2025',
        'date_edition': '05/07/2025',
        'moyenne': stats.get('moyenne_generale', 14.5),
        'rang': '12/30',
        'appreciation_generale': "Bon trimestre avec une progression notable en mathématiques. Continuez vos efforts en français.",
        'disponible': True
    },
    {
        'periode': 'Trimestre 2',
        'date_debut': '01/01/2025',
        'date_fin': '31/03/2025',
        'date_edition': '05/04/2025',
        'moyenne': stats.get('moyenne_generale', 14.5) - 0.5,
        'rang': '15/30',
        'appreciation_generale': "Trimestre satisfaisant. L'élève doit poursuivre ses efforts réguliers.",
        'disponible': True
    },
    {
        'periode': 'Trimestre 1',
        'date_debut': '01/09/2024',
        'date_fin': '31/12/2024',
        'date_edition': '05/01/2025',
        'moyenne': stats.get('moyenne_generale', 14.5) - 1.0,
        'rang': '18/30',
        'appreciation_generale': "Premier trimestre d'adaptation. L'élève montre du potentiel.",
        'disponible': True
    }
]

for bulletin in bulletins:
    with st.expander(f"📋 {bulletin['periode']} - Moyenne: {bulletin['moyenne']:.2f}/20", expanded=False):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**Période :** {bulletin['date_debut']} au {bulletin['date_fin']}")
            st.markdown(f"**Date d'édition :** {bulletin['date_edition']}")
            st.markdown(f"**Moyenne générale :** {bulletin['moyenne']:.2f}/20")
            st.markdown(f"**Rang :** {bulletin['rang']}")
        
        with col2:
            st.markdown("**Appréciation générale :**")
            st.markdown(f"_{bulletin['appreciation_generale']}_")
        
        with col3:
            if bulletin['disponible']:
                if st.button(f"👁️ Prévisualiser", key=f"preview_{bulletin['periode']}", use_container_width=True):
                    st.session_state[f'preview_{bulletin["periode"]}'] = True
                
                if st.button(f"📥 Télécharger PDF", key=f"download_{bulletin['periode']}", use_container_width=True):
                    # Simuler un téléchargement
                    st.success(f"✅ Téléchargement de {bulletin['periode']}.pdf")
                    st.info("📁 Le fichier sera sauvegardé dans votre dossier Téléchargements")
            else:
                st.warning("Pas encore disponible")
        
        # Prévisualisation si demandée
        if st.session_state.get(f'preview_{bulletin["periode"]}', False):
            st.markdown("---")
            st.markdown("### 📄 Prévisualisation du bulletin")
            
            if create_report_preview:
                try:
                    # Préparer les données pour la prévisualisation
                    preview_data = {
                        'student': student,
                        'periode': bulletin['periode'],
                        'moyenne': bulletin['moyenne'],
                        'rang': bulletin['rang'],
                        'appreciation': bulletin['appreciation_generale']
                    }
                    preview_html = create_report_preview(preview_data)
                    st.markdown(preview_html, unsafe_allow_html=True)
                except Exception as e:
                    st.warning(f"⚠️ Prévisualisation non disponible: {str(e)}")
                    create_report_preview = None
            
            if not create_report_preview:
                # Fallback: affichage simple
                st.markdown(
                    f"""
                    <div style='border: 2px solid {colors['primary']}; padding: 30px; 
                                border-radius: 10px; background-color: white;'>
                        <h2 style='text-align: center; color: {colors['primary']};'>
                            BULLETIN SCOLAIRE
                        </h2>
                        <h3 style='text-align: center;'>{bulletin['periode']} - Année 2024-2025</h3>
                        <hr>
                        <p><strong>Élève :</strong> {student['nom']} {student['prenom']}</p>
                        <p><strong>Classe :</strong> {student['classe']}</p>
                        <p><strong>Période :</strong> {bulletin['date_debut']} au {bulletin['date_fin']}</p>
                        <hr>
                        <h3>Résultats</h3>
                        <p><strong>Moyenne générale :</strong> {bulletin['moyenne']:.2f}/20</p>
                        <p><strong>Rang :</strong> {bulletin['rang']}</p>
                        <hr>
                        <h3>Appréciation générale</h3>
                        <p style='font-style: italic;'>{bulletin['appreciation_generale']}</p>
                        <hr>
                        <p style='text-align: center; color: gray; font-size: 12px;'>
                            Document officiel - EduTrack IA
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            if st.button("✖️ Fermer la prévisualisation", key=f"close_{bulletin['periode']}"):
                st.session_state[f'preview_{bulletin["periode"]}'] = False
                st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# Section 2: Observations des enseignants
st.subheader("📝 Dernières observations des enseignants")

# Simuler des observations
observations = [
    {
        'date': (datetime.now() - timedelta(days=5)).strftime('%d/%m/%Y'),
        'enseignant': 'M. Dupont',
        'matiere': 'Mathématiques',
        'observation': "Excellent travail sur les équations du second degré. L'élève participe activement en classe.",
        'type': 'positive'
    },
    {
        'date': (datetime.now() - timedelta(days=12)).strftime('%d/%m/%Y'),
        'enseignant': 'Mme Martin',
        'matiere': 'Français',
        'observation': "Bonne rédaction mais attention à l'orthographe. Pensez à relire vos productions.",
        'type': 'conseil'
    },
    {
        'date': (datetime.now() - timedelta(days=20)).strftime('%d/%m/%Y'),
        'enseignant': 'M. Bernard',
        'matiere': 'Histoire-Géographie',
        'observation': "Très bonne participation. Les exposés sont bien préparés et présentés.",
        'type': 'positive'
    },
    {
        'date': (datetime.now() - timedelta(days=28)).strftime('%d/%m/%Y'),
        'enseignant': 'Mme Dubois',
        'matiere': 'Sciences Physiques',
        'observation': "Besoin de plus de rigueur dans la rédaction des comptes-rendus de TP.",
        'type': 'conseil'
    }
]

for obs in observations:
    # Couleur selon le type
    if obs['type'] == 'positive':
        border_color = 'green'
        emoji = '✅'
    else:
        border_color = 'orange'
        emoji = '💡'
    
    st.markdown(
        f"""
        <div style='border-left: 5px solid {border_color}; padding: 15px; 
                    margin-bottom: 15px; background-color: {border_color}10; border-radius: 5px;'>
            <p style='margin: 0; color: gray; font-size: 12px;'>
                {obs['date']} - {obs['enseignant']} ({obs['matiere']})
            </p>
            <p style='margin: 10px 0; font-size: 16px;'>
                {emoji} {obs['observation']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# Section 3: Relevés de notes
st.subheader("📊 Relevés de notes mensuels")

col1, col2, col3 = st.columns(3)

mois = ['Janvier 2025', 'Février 2025', 'Mars 2025', 'Avril 2025', 'Mai 2025', 'Juin 2025']

for i, mois_nom in enumerate(mois[-3:]):  # 3 derniers mois
    col = [col1, col2, col3][i]
    
    with col:
        st.markdown(
            f"""
            <div style='border: 2px solid {colors['secondary']}; padding: 20px; 
                        border-radius: 10px; text-align: center; background-color: white;'>
                <h4 style='margin: 0; color: {colors['secondary']};'>📄 {mois_nom}</h4>
                <p style='margin: 10px 0; font-size: 14px; color: gray;'>Relevé mensuel de notes</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button(f"📥 Télécharger", key=f"releve_{mois_nom}", use_container_width=True):
            st.success(f"✅ Téléchargement du relevé {mois_nom}")

st.markdown("<br>", unsafe_allow_html=True)

# Section 4: Documents complémentaires
st.subheader("📎 Documents complémentaires")

documents = [
    {
        'nom': 'Certificat de scolarité 2024-2025',
        'type': 'Administratif',
        'date': '15/09/2024',
        'icone': '📜'
    },
    {
        'nom': 'Calendrier scolaire',
        'type': 'Information',
        'date': '01/09/2024',
        'icone': '📅'
    },
    {
        'nom': "Règlement intérieur de l'établissement",
        'type': 'Règlement',
        'date': '01/09/2024',
        'icone': '📋'
    }
]

col1, col2, col3 = st.columns(3)

for i, doc in enumerate(documents):
    col = [col1, col2, col3][i]
    
    with col:
        st.markdown(
            f"""
            <div style='border: 1px solid #ddd; padding: 20px; border-radius: 10px; 
                        text-align: center; background-color: #f9f9f9;'>
                <div style='font-size: 48px;'>{doc['icone']}</div>
                <h4 style='margin: 10px 0;'>{doc['nom']}</h4>
                <p style='margin: 5px 0; font-size: 12px; color: gray;'>
                    {doc['type']} - {doc['date']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button(f"📥 Télécharger", key=f"doc_{i}", use_container_width=True):
            st.success(f"✅ Téléchargement de {doc['nom']}")

st.markdown("<br>", unsafe_allow_html=True)

# Section 5: Historique des téléchargements
with st.expander("📥 Historique des téléchargements", expanded=False):
    st.markdown("Aucun téléchargement récent")
    st.caption("Les documents que vous téléchargez apparaîtront ici")

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='background-color: {colors['primary']}10; border-radius: 10px; 
                padding: 20px; text-align: center;'>
        <h4>💡 Besoin d'aide ?</h4>
        <p>Si vous rencontrez des difficultés pour accéder aux documents ou si vous avez des questions :</p>
        <ul style='text-align: left; max-width: 600px; margin: 20px auto;'>
            <li>📧 Contactez le secrétariat de l'établissement</li>
            <li>📞 Appelez le service scolarité</li>
            <li>🏫 Rendez-vous directement à l'établissement</li>
        </ul>
        <p style='font-size: 12px; color: gray; margin-top: 20px;'>
            Tous les documents sont authentiques et certifiés par l'établissement.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Section informative
st.info("""
🔒 **Protection des données**

Tous les documents sont sécurisés et accessibles uniquement aux parents autorisés.
Les téléchargements sont enregistrés pour des raisons de sécurité.
""")
